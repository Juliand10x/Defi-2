"""Ingesta, validación y trazabilidad de datos de mercado."""
import os
from datetime import date, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from scipy import stats
import yfinance as yf

CACHE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "cache_precios.csv")

SECTOR_MAP = {
    "AAPL": "Information Technology", "MSFT": "Information Technology", "NVDA": "Information Technology",
    "GOOGL": "Communication Services", "AMZN": "Consumer Discretionary", "JPM": "Financials",
    "XOM": "Energy", "JNJ": "Healthcare", "PG": "Consumer Staples", "NEE": "Utilities",
    "TSLA": "Consumer Discretionary", "META": "Communication Services", "BAC": "Financials",
    "CVX": "Energy", "UNH": "Healthcare", "KO": "Consumer Staples", "DUK": "Utilities",
    "SO": "Utilities", "V": "Financials", "MA": "Financials", "WMT": "Consumer Staples", "HD": "Consumer Discretionary",
}
ALL_SECTORS = ["Information Technology", "Financials", "Healthcare", "Energy", "Consumer Discretionary",
               "Consumer Staples", "Utilities", "Communication Services", "Industrials", "Materials", "Real Estate"]
DEFAULT_TICKERS = ["AAPL", "MSFT", "GOOGL", "JPM", "XOM", "JNJ", "AMZN", "PG", "NEE", "NVDA"]


def get_default_portfolio() -> pd.DataFrame:
    return pd.DataFrame({"Ticker": DEFAULT_TICKERS, "Sector": [SECTOR_MAP[t] for t in DEFAULT_TICKERS]})


def detect_sector(ticker: str) -> str:
    ticker = ticker.upper().strip()
    if ticker in SECTOR_MAP:
        return SECTOR_MAP[ticker]
    try:
        sector = yf.Ticker(ticker).info.get("sector")
        if isinstance(sector, str) and sector:
            return sector
    except Exception:
        pass
    return "Sin clasificar"


def _close_frame(raw: pd.DataFrame, tickers: List[str]) -> pd.DataFrame:
    if raw.empty:
        return pd.DataFrame()
    if isinstance(raw.columns, pd.MultiIndex):
        if "Close" not in raw.columns.get_level_values(0):
            return pd.DataFrame()
        result = raw["Close"].copy()
    else:
        result = raw[["Close"]].copy() if "Close" in raw.columns else pd.DataFrame()
        if len(tickers) == 1 and not result.empty:
            result.columns = tickers
    return result.reindex(columns=[t for t in tickers if t in result.columns]).sort_index()


def _validate_common_sessions(prices: pd.DataFrame, requested: List[str]) -> Tuple[pd.DataFrame, Dict[str, object]]:
    source_rows = len(prices)
    prices = prices[~prices.index.duplicated(keep="last")].sort_index()
    invalid_values = int((prices <= 0).sum().sum())
    prices = prices.mask(prices <= 0)
    common = prices.dropna(how="any")
    discarded = source_rows - len(common)
    metadata = {
        "requested_tickers": requested, "available_tickers": common.columns.tolist(),
        "source_rows": source_rows, "common_sessions": len(common), "discarded_sessions": discarded,
        "non_positive_values": invalid_values, "minimum_required_returns": 756,
        "meets_minimum_history": len(common) - 1 >= 756,
    }
    return common, metadata


def download_market_data(tickers: List[str], start_date: Optional[date] = None, end_date: Optional[date] = None,
                         use_cache: bool = True) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, object]]:
    """Descarga precios ajustados para retornos y cierre sin ajustar para el spot.

    No rellena huecos ni fabrica datos: el análisis usa únicamente sesiones comunes observadas.
    """
    tickers = list(dict.fromkeys(t.upper().strip() for t in tickers if t and t.strip()))
    start_date = start_date or (date.today() - timedelta(days=365 * 4 + 45))
    end_date = end_date or date.today()  # La fecha final de Yahoo es exclusiva.
    adjusted, raw_close, source = pd.DataFrame(), pd.DataFrame(), "Yahoo Finance"
    try:
        raw_adjusted = yf.download(tickers, start=start_date.isoformat(), end=end_date.isoformat(), auto_adjust=True, progress=False)
        raw_unadjusted = yf.download(tickers, start=start_date.isoformat(), end=end_date.isoformat(), auto_adjust=False, progress=False)
        adjusted, raw_close = _close_frame(raw_adjusted, tickers), _close_frame(raw_unadjusted, tickers)
    except Exception:
        pass
    if adjusted.empty and use_cache and os.path.exists(CACHE_FILE):
        cached = pd.read_csv(CACHE_FILE, index_col=0, parse_dates=True)
        adjusted = cached.reindex(columns=[t for t in tickers if t in cached.columns])
        raw_close = adjusted.copy()
        source = "Caché local; el spot corresponde al último cierre disponible en caché"
    if adjusted.empty:
        return pd.DataFrame(), pd.DataFrame(), {"error": "No hubo descarga y no existe un respaldo CSV compatible. Cargue un CSV con precios observados.", "source": "Sin datos"}
    common_adjusted, quality = _validate_common_sessions(adjusted, tickers)
    common_raw = raw_close.reindex(index=common_adjusted.index, columns=common_adjusted.columns)
    common_raw = common_raw.dropna(how="any")
    common_adjusted = common_adjusted.reindex(common_raw.index)
    returns = np.log(common_adjusted / common_adjusted.shift(1)).dropna()
    quality.update({"source": source, "start_date": str(common_adjusted.index.min().date()), "end_date_exclusive": end_date.isoformat(),
                    "raw_spots": {t: float(common_raw[t].iloc[-1]) for t in common_raw.columns},
                    "adjusted_spots": {t: float(common_adjusted[t].iloc[-1]) for t in common_adjusted.columns}})
    stats_dict: Dict[str, object] = {"quality": quality}
    for ticker in common_adjusted.columns:
        series_r = returns[ticker].dropna()
        sigma_daily = float(series_r.std(ddof=1))
        sigma_annual = sigma_daily * np.sqrt(252.0)
        mu_total = float(series_r.mean() * 252.0 + 0.5 * sigma_annual**2)
        dividend_yield = 0.0  # Se configura explícitamente al valorar la opción.
        jb_stat, jb_pvalue = stats.jarque_bera(series_r)
        stats_dict[ticker] = {"spot": float(common_adjusted[ticker].iloc[-1]), "raw_spot": float(common_raw[ticker].iloc[-1]),
            "observations": len(series_r), "mu_total_annual": mu_total, "sigma_annual": sigma_annual,
            "sigma_daily": sigma_daily, "dividend_yield_proxy": dividend_yield,
            "jb_stat": float(jb_stat), "jb_pvalue": float(jb_pvalue)}
    return common_adjusted, returns, stats_dict
