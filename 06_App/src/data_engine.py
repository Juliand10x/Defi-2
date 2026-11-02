import os
from datetime import date, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from scipy import stats
import yfinance as yf

CACHE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "cache_precios.csv")

SECTOR_MAP = {
    "AAPL": "Information Technology",
    "MSFT": "Information Technology",
    "NVDA": "Information Technology",
    "GOOGL": "Communication Services",
    "AMZN": "Consumer Discretionary",
    "JPM": "Financials",
    "XOM": "Energy",
    "JNJ": "Healthcare",
    "PG": "Consumer Staples",
    "NEE": "Utilities",
    "TSLA": "Consumer Discretionary",
    "META": "Communication Services",
    "BAC": "Financials",
    "CVX": "Energy",
    "UNH": "Healthcare",
    "KO": "Consumer Staples",
    "DUK": "Utilities",
    "SO": "Utilities",
    "V": "Financials",
    "MA": "Financials",
    "WMT": "Consumer Staples",
    "HD": "Consumer Discretionary",
}

ALL_SECTORS = [
    "Information Technology",
    "Financials",
    "Healthcare",
    "Energy",
    "Consumer Discretionary",
    "Consumer Staples",
    "Utilities",
    "Communication Services",
    "Industrials",
    "Materials",
    "Real Estate",
]

DEFAULT_TICKERS = ["AAPL", "MSFT", "GOOGL", "JPM", "XOM", "JNJ", "AMZN", "PG", "NEE", "NVDA"]


def get_default_portfolio() -> pd.DataFrame:
    return pd.DataFrame({
        "Ticker": DEFAULT_TICKERS,
        "Sector": [SECTOR_MAP.get(t, "Information Technology") for t in DEFAULT_TICKERS]
    })


def detect_sector(ticker: str) -> str:
    ticker = ticker.upper().strip()
    if ticker in SECTOR_MAP:
        return SECTOR_MAP[ticker]
    try:
        t = yf.Ticker(ticker)
        sec = t.info.get("sector")
        if sec and isinstance(sec, str):
            return sec
    except Exception:
        pass
    return "Information Technology"


def download_market_data(
    tickers: List[str],
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    use_cache: bool = True,
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, dict]]:
    tickers = [t.upper().strip() for t in tickers if t]
    if not start_date:
        start_date = date.today() - timedelta(days=365 * 3 + 45)
    if not end_date:
        end_date = date.today()

    prices_df = pd.DataFrame()
    downloaded = False

    try:
        raw = yf.download(
            tickers,
            start=start_date.strftime("%Y-%m-%d"),
            end=end_date.strftime("%Y-%m-%d"),
            auto_adjust=True,
            progress=False,
        )
        if isinstance(raw.columns, pd.MultiIndex):
            if "Close" in raw.columns.levels[0]:
                prices_df = raw["Close"].copy()
            else:
                prices_df = raw.xs("Close", axis=1, level=0).copy()
        elif "Close" in raw.columns:
            prices_df = raw[["Close"]].copy()
            if len(tickers) == 1:
                prices_df.columns = [tickers[0]]
        else:
            prices_df = raw.copy()
            if len(tickers) == 1:
                prices_df.columns = [tickers[0]]

        if not prices_df.empty and prices_df.shape[0] > 100:
            downloaded = True
            os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
            prices_df.to_csv(CACHE_FILE)
    except Exception as exc:
        print(f"Warning yfinance download: {exc}")

    if (prices_df.empty or not downloaded) and use_cache and os.path.exists(CACHE_FILE):
        try:
            cached = pd.read_csv(CACHE_FILE, index_col=0, parse_dates=True)
            valid_cols = [c for c in tickers if c in cached.columns]
            if len(valid_cols) > 0:
                prices_df = cached[valid_cols].copy()
        except Exception:
            pass

    if prices_df.empty:
        # Generador de respaldo sintético realista
        np.random.seed(42)
        dates = pd.date_range(end=end_date, periods=756, freq="B")
        synth = {}
        for t in tickers:
            base_p = 100.0 + (hash(t) % 150)
            daily_rets = np.random.normal(0.0005, 0.015, len(dates))
            prices = base_p * np.exp(np.cumsum(daily_rets))
            synth[t] = prices
        prices_df = pd.DataFrame(synth, index=dates)

    prices_df = prices_df.ffill().bfill().dropna(how="all")
    returns_df = np.log(prices_df / prices_df.shift(1)).dropna()

    stats_dict = {}
    for col in prices_df.columns:
        series_r = returns_df[col].dropna()
        series_p = prices_df[col].dropna()
        if len(series_r) < 30:
            continue
        spot = float(series_p.iloc[-1])
        mu_daily = float(series_r.mean())
        sigma_daily = float(series_r.std(ddof=1))
        ann_mu = mu_daily * 252.0
        ann_vol = sigma_daily * np.sqrt(252.0)
        skew = float(stats.skew(series_r))
        kurt = float(stats.kurtosis(series_r, fisher=False))  # Pearson kurtosis (normal = 3)
        jb_stat, jb_pval = stats.jarque_bera(series_r)
        
        stats_dict[col] = {
            "spot": spot,
            "observations": len(series_r),
            "mu_daily": mu_daily,
            "sigma_daily": sigma_daily,
            "ann_mu": ann_mu,
            "ann_vol": ann_vol,
            "skewness": skew,
            "kurtosis": kurt,
            "jb_stat": float(jb_stat),
            "jb_pvalue": float(jb_pval),
            "is_normal": bool(jb_pval > 0.05),
        }

    return prices_df, returns_df, stats_dict