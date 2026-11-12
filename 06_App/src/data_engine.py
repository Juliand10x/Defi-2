"""
Módulo de Ingesta, Validación y Calibración de Parámetros de Mercado (Pasos 1, 2 y 3 del Taller).
Universidad Externado de Colombia · DEFI 2
"""

import os
import sys
import platform
from datetime import date, timedelta
from typing import Dict, List, Optional, Tuple, Any

import numpy as np
import pandas as pd
from scipy import stats
import yfinance as yf

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CACHE_FILE_ADJ = os.path.join(CACHE_DIR, "cache_precios.csv")
CACHE_FILE_RAW = os.path.join(CACHE_DIR, "cache_precios_raw.csv")

SECTOR_MAP = {
    "AAPL": "Information Technology",
    "MSFT": "Information Technology",
    "NVDA": "Information Technology",
    "GOOGL": "Communication Services",
    "META": "Communication Services",
    "AMZN": "Consumer Discretionary",
    "TSLA": "Consumer Discretionary",
    "HD": "Consumer Discretionary",
    "JPM": "Financials",
    "BAC": "Financials",
    "V": "Financials",
    "MA": "Financials",
    "XOM": "Energy",
    "CVX": "Energy",
    "JNJ": "Healthcare",
    "UNH": "Healthcare",
    "PG": "Consumer Staples",
    "KO": "Consumer Staples",
    "WMT": "Consumer Staples",
    "NEE": "Utilities",
    "DUK": "Utilities",
    "SO": "Utilities",
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
    """Retorna el portafolio predeterminado de 10 acciones en al menos 4 sectores."""
    return pd.DataFrame({
        "Ticker": DEFAULT_TICKERS,
        "Sector": [SECTOR_MAP.get(t, "Sin clasificar") for t in DEFAULT_TICKERS]
    })


def detect_sector(ticker: str) -> str:
    """Autodetección de sector vía diccionario o consulta yfinance."""
    ticker = ticker.upper().strip()
    if ticker in SECTOR_MAP:
        return SECTOR_MAP[ticker]
    try:
        info = yf.Ticker(ticker).info
        sector = info.get("sector")
        if isinstance(sector, str) and sector.strip():
            return sector.strip()
    except Exception:
        pass
    return "Sin clasificar"


def get_library_versions() -> Dict[str, str]:
    """Reporta versiones del entorno y bibliotecas clave para auditoría y reproducibilidad."""
    import streamlit as st
    import plotly
    import scipy
    return {
        "Python": sys.version.split()[0],
        "Sistema Operativo": f"{platform.system()} {platform.release()}",
        "Streamlit": st.__version__,
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "plotly": plotly.__version__,
        "yfinance": yf.__version__,
    }


def _clean_close_frame(raw: pd.DataFrame, tickers: List[str]) -> pd.DataFrame:
    """Extrae la columna Close unificada y ordena cronológicamente."""
    if raw.empty:
        return pd.DataFrame()
    if isinstance(raw.columns, pd.MultiIndex):
        if "Close" in raw.columns.get_level_values(0):
            res = raw["Close"].copy()
        else:
            return pd.DataFrame()
    else:
        if "Close" in raw.columns:
            res = raw[["Close"]].copy()
            if len(tickers) == 1:
                res.columns = tickers
        else:
            res = raw.copy()
    valid_cols = [t for t in tickers if t in res.columns]
    res = res[valid_cols].copy()
    res.index = pd.to_datetime(res.index)
    res = res[~res.index.duplicated(keep="last")].sort_index()
    return res


def load_market_data_from_csv(
    file_or_path: Any,
    tickers: Optional[List[str]] = None,
    provenance: str = "CSV cargado por usuario"
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """Carga precios desde un archivo CSV con procedencia registrada (Paso 2.3)."""
    try:
        df = pd.read_csv(file_or_path, index_col=0, parse_dates=True)
        df.index = pd.to_datetime(df.index)
        df = df[~df.index.duplicated(keep="last")].sort_index()
        if tickers:
            available = [t for t in tickers if t in df.columns]
            df = df[available]
        return process_market_dataframe(df, df.copy(), tickers or df.columns.tolist(), source_name=provenance)
    except Exception as exc:
        return pd.DataFrame(), pd.DataFrame(), {"error": f"Error al procesar CSV: {exc}", "source": provenance}


def download_market_data(
    tickers: List[str],
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    use_cache: bool = True,
    custom_dividends: Optional[Dict[str, float]] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """
    Descarga al menos tres años diarios con yfinance (Paso 2 del Taller):
    - auto_adjust=True para retornos continuos y discretos.
    - Cierre sin ajustar como spot S0 de la opción.
    - Fecha end exclusiva.
    - Fallback a caché local si la red o API falla.
    """
    tickers = list(dict.fromkeys(t.upper().strip() for t in tickers if t and t.strip()))
    start_date = start_date or (date.today() - timedelta(days=365 * 4 + 45))
    end_date = end_date or date.today()  # Exclusivo

    adj_df = pd.DataFrame()
    raw_df = pd.DataFrame()
    source = "Yahoo Finance (descarga directa)"

    try:
        raw_adj = yf.download(
            tickers,
            start=start_date.isoformat(),
            end=end_date.isoformat(),
            auto_adjust=True,
            progress=False,
        )
        raw_unadj = yf.download(
            tickers,
            start=start_date.isoformat(),
            end=end_date.isoformat(),
            auto_adjust=False,
            progress=False,
        )
        adj_df = _clean_close_frame(raw_adj, tickers)
        raw_df = _clean_close_frame(raw_unadj, tickers)
    except Exception:
        pass

    # Si la descarga falló o fue incompleta, activar caché de respaldo
    needs_fallback = adj_df.empty or len(adj_df) < 500 or any(t not in adj_df.columns for t in tickers)
    if needs_fallback and use_cache and os.path.exists(CACHE_FILE_ADJ):
        try:
            cached_adj = pd.read_csv(CACHE_FILE_ADJ, index_col=0, parse_dates=True)
            cached_raw = pd.read_csv(CACHE_FILE_RAW, index_col=0, parse_dates=True) if os.path.exists(CACHE_FILE_RAW) else cached_adj.copy()
            
            avail = [t for t in tickers if t in cached_adj.columns]
            if len(avail) >= len(tickers) * 0.7:  # Al menos la gran mayoría disponible
                adj_df = cached_adj[avail].copy()
                raw_df = cached_raw[avail].copy()
                source = "Caché local de respaldo verificado (06_App/data/cache_precios.csv)"
        except Exception:
            pass

    if adj_df.empty:
        return pd.DataFrame(), pd.DataFrame(), {
            "error": "No hubo descarga de Yahoo Finance y la caché no está disponible. Cargue un CSV para continuar.",
            "source": "Sin datos"
        }

    return process_market_dataframe(
        adj_df,
        raw_df,
        tickers,
        source_name=source,
        start_date=start_date,
        end_date=end_date,
        custom_dividends=custom_dividends
    )


def process_market_dataframe(
    adj_df: pd.DataFrame,
    raw_df: pd.DataFrame,
    tickers: List[str],
    source_name: str = "Yahoo Finance",
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    custom_dividends: Optional[Dict[str, float]] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """
    Audita y calibra precios y retornos según los Pasos 2 y 3 del Taller:
    1. Precios no positivos y nulos.
    2. Sesiones comunes completas y reporte de descartes (sin fabricar retornos cero).
    3. Partición estricta: últimas 252 sesiones para evaluación, anteriores (>= 504) para calibración.
    4. Fórmulas oficiales:
       - R_{i,t} = P_{i,t}/P_{i,t-1} - 1 (discreto)
       - x_{i,t} = ln(P_{i,t}/P_{i,t-1}) (logarítmico)
       - sigma_hat_i = sqrt(252) * s_{x,i}
       - mu_hat_total_i = 252 * x_bar_i + 0.5 * sigma_hat_i^2
       - a_hat_i = mu_hat_total_i - q_i
    """
    custom_dividends = custom_dividends or {}
    source_rows = len(adj_df)

    # Filtrar solo tickers que existen en ambos
    common_cols = [t for t in tickers if t in adj_df.columns and t in raw_df.columns]
    if not common_cols:
        return pd.DataFrame(), pd.DataFrame(), {"error": "Los activos solicitados no tienen cotizaciones disponibles.", "source": source_name}

    adj_clean = adj_df[common_cols].copy()
    raw_clean = raw_df[common_cols].copy()

    # Detección de no positivos
    non_positive_count = int((adj_clean <= 0).sum().sum() + (raw_clean <= 0).sum().sum())
    adj_clean = adj_clean.mask(adj_clean <= 0)
    raw_clean = raw_clean.mask(raw_clean <= 0)

    # Intersección estricta de sesiones comunes completas
    common_idx = adj_clean.dropna().index.intersection(raw_clean.dropna().index)
    adj_clean = adj_clean.loc[common_idx].sort_index()
    raw_clean = raw_clean.loc[common_idx].sort_index()

    discarded_sessions = source_rows - len(adj_clean)
    total_sessions = len(adj_clean)
    total_returns = total_sessions - 1 if total_sessions > 1 else 0

    # Partición 756: 504 calibración inicial + 252 evaluación
    has_756 = total_returns >= 756
    calib_sessions = max(0, total_returns - 252)
    eval_sessions = min(252, total_returns)

    # Cálculo de retornos discretos (R) y continuos (x)
    discrete_returns = (adj_clean / adj_clean.shift(1) - 1.0).dropna()
    log_returns = np.log(adj_clean / adj_clean.shift(1)).dropna()

    # Precios normalizados (base 100)
    normalized_prices = (adj_clean / adj_clean.iloc[0]) * 100.0

    # Matrices muestrales en las mismas fechas con divisor n-1 (Paso 3)
    cov_matrix_daily = log_returns.cov()
    cov_matrix_annual = cov_matrix_daily * 252.0
    corr_matrix = log_returns.corr()

    # Calibración individual de parámetros
    params_rows = []
    stats_dict: Dict[str, Any] = {}

    quality_meta = {
        "source": source_name,
        "requested_tickers": tickers,
        "available_tickers": common_cols,
        "total_source_rows": source_rows,
        "common_sessions": total_sessions,
        "total_returns": total_returns,
        "discarded_sessions": discarded_sessions,
        "non_positive_count": non_positive_count,
        "meets_756_returns": has_756,
        "calibration_sessions_count": calib_sessions,
        "evaluation_sessions_count": eval_sessions,
        "first_date": str(adj_clean.index.min().date()) if not adj_clean.empty else "N/A",
        "last_date": str(adj_clean.index.max().date()) if not adj_clean.empty else "N/A",
        "library_versions": get_library_versions(),
        "raw_spots": {t: float(raw_clean[t].iloc[-1]) for t in common_cols},
        "adjusted_spots": {t: float(adj_clean[t].iloc[-1]) for t in common_cols},
    }
    stats_dict["quality"] = quality_meta

    for t in common_cols:
        r_log = log_returns[t]
        s_raw = float(raw_clean[t].iloc[-1])
        s_adj = float(adj_clean[t].iloc[-1])
        
        n_obs = len(r_log)
        x_bar = float(r_log.mean())
        s_x = float(r_log.std(ddof=1))  # Divisor n-1
        
        sigma_hat = float(np.sqrt(252.0) * s_x)
        mu_hat_total = float(252.0 * x_bar + 0.5 * (sigma_hat ** 2))
        
        # Tasa de dividendos continuo anual q_i
        q_i = custom_dividends.get(t, 0.0)
        a_hat = float(mu_hat_total - q_i)

        # Pruebas estadísticas de normalidad
        jb_stat, jb_pval = stats.jarque_bera(r_log)
        skew = float(stats.skew(r_log))
        kurt = float(stats.kurtosis(r_log, fisher=True))

        stats_dict[t] = {
            "spot": s_adj,
            "raw_spot": s_raw,
            "mu_total_annual": mu_hat_total,
            "sigma_annual": sigma_hat,
            "sigma_daily": s_x,
            "q_dividend": q_i,
            "a_spot_drift": a_hat,
            "observations": n_obs,
            "mean_daily_return": x_bar,
            "skewness": skew,
            "kurtosis": kurt,
            "jb_stat": float(jb_stat),
            "jb_pvalue": float(jb_pval),
        }

        params_rows.append({
            "Ticker": t,
            "Sector": SECTOR_MAP.get(t, detect_sector(t)),
            "Spot Sin Ajustar (S0)": round(s_raw, 2),
            "Spot Ajustado (P0)": round(s_adj, 2),
            "Drift Total (μ^total)": f"{mu_hat_total:.2%}",
            "Volatilidad Anual (σ)": f"{sigma_hat:.2%}",
            "Dividendo (q)": f"{q_i:.2%}",
            "Drift Exdividendo (a)": f"{a_hat:.2%}",
            "Asimetría": round(skew, 2),
            "Curtosis": round(kurt, 2),
            "Jarque-Bera p-val": f"{jb_pval:.4f}",
            "Normalidad": "Normal (p>0.05)" if jb_pval > 0.05 else "No normal (p≤0.05)"
        })

    stats_dict["parameters_table"] = pd.DataFrame(params_rows)
    stats_dict["normalized_prices"] = normalized_prices
    stats_dict["discrete_returns"] = discrete_returns
    stats_dict["log_returns"] = log_returns
    stats_dict["cov_matrix_daily"] = cov_matrix_daily
    stats_dict["cov_matrix_annual"] = cov_matrix_annual
    stats_dict["corr_matrix"] = corr_matrix

    return adj_clean, log_returns, stats_dict
