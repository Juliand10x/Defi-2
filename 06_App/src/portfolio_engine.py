from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from scipy import optimize


def compute_portfolio_allocation(
    capital: float,
    portfolio_df: pd.DataFrame,
    returns_df: pd.DataFrame,
    confidence: float = 99.0,
    horizon_days: int = 10,
    prices_df: Optional[pd.DataFrame] = None,
) -> Dict[str, any]:
    valid_tickers = [t for t in portfolio_df["Ticker"] if t in returns_df.columns]
    if len(valid_tickers) < 2:
        return {}
        
    sub_returns = returns_df[valid_tickers].dropna()
    cov_matrix = sub_returns.cov() * 252.0  # Anualizada
    daily_cov = sub_returns.cov()
    
    n = len(valid_tickers)
    sectors = [portfolio_df.loc[portfolio_df["Ticker"] == t, "Sector"].values[0] for t in valid_tickers]
    
    # Precios Spot reales (no retornos)
    if prices_df is not None:
        spots = [float(prices_df[t].dropna().iloc[-1]) for t in valid_tickers]
    else:
        spots = [100.0 for _ in valid_tickers]
    
    # VaR individual histórico al nivel de confianza y horizonte h
    z_score = float(np.percentile(np.random.normal(0, 1, 100000), confidence))
    # Desviación estándar a h días
    h_factor = np.sqrt(horizon_days / 252.0)
    vols = np.sqrt(np.diag(cov_matrix.values))
    individual_vars = vols * h_factor * z_score
    
    # 1. Pesos Iguales
    w_equal = np.ones(n) / n
    
    # 2. Pesos Inverso al VaR
    inv_vars = 1.0 / np.maximum(individual_vars, 1e-4)
    w_inv_var = inv_vars / np.sum(inv_vars)
    
    # 3. Mínimo VaR con restricciones
    # min w^T Sigma w
    # s.a. sum w = 1, w_min <= w_i <= w_max, sum_{sector} w <= 0.35
    w_min = 0.02 if n >= 5 else 0.05
    w_max = min(0.25, max(0.15, 2.0 / n))
    
    def portfolio_var_obj(w):
        return np.dot(w.T, np.dot(daily_cov.values, w))
        
    bounds = [(w_min, w_max) for _ in range(n)]
    constraints = [
        {"type": "eq", "fun": lambda w: np.sum(w) - 1.0}
    ]
    
    # Restricción sectorial <= 35%
    unique_sectors = list(set(sectors))
    for sec in unique_sectors:
        sec_indices = [i for i, s in enumerate(sectors) if s == sec]
        if len(sec_indices) > 1:
            constraints.append({
                "type": "ineq",
                "fun": lambda w, idxs=sec_indices: 0.35 - np.sum(w[idxs])
            })
            
    init_w = np.ones(n) / n
    res = optimize.minimize(
        portfolio_var_obj,
        init_w,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"maxiter": 200, "ftol": 1e-7}
    )
    
    if res.success:
        w_min_var = res.x
    else:
        w_min_var = w_equal
        
    # Construcción de tabla de asignación con Mínimo VaR
    df_alloc = pd.DataFrame({
        "Ticker": valid_tickers,
        "Sector": sectors,
        "Precio Spot (USD)": [round(s, 2) for s in spots],
        "VaR Indiv 99%": [f"{v:.2%}" for v in individual_vars],
        "Peso Igual": [f"{w:.2%}" for w in w_equal],
        "Peso Inv VaR": [f"{w:.2%}" for w in w_inv_var],
        "Peso Óptimo": [round(w, 4) for w in w_min_var],
    })
    
    # Cálculo en USD y acciones enteras para el modelo óptimo
    monto_usd = capital * w_min_var
    acciones = np.floor(monto_usd / np.array(spots)).astype(int)
    invertido_real = acciones * np.array(spots)
    efectivo_residual = capital - np.sum(invertido_real)
    peso_real = invertido_real / capital
    
    df_alloc["Monto Objetivo (USD)"] = monto_usd
    df_alloc["Acciones Enteras"] = acciones
    df_alloc["Inversión Real (USD)"] = invertido_real
    df_alloc["Peso Real"] = [f"{p:.2%}" for p in peso_real]
    
    # Riesgo del portafolio (VaR de cartera)
    sigma_port_daily = np.sqrt(np.dot(w_min_var.T, np.dot(daily_cov.values, w_min_var)))
    var_port_pct = sigma_port_daily * np.sqrt(horizon_days) * z_score
    var_port_usd = capital * var_port_pct
    
    return {
        "allocation_df": df_alloc,
        "w_equal": w_equal,
        "w_inv_var": w_inv_var,
        "w_min_var": w_min_var,
        "capital": capital,
        "efectivo_residual": efectivo_residual,
        "var_portfolio_pct": var_port_pct,
        "var_portfolio_usd": var_port_usd,
        "solver_success": res.success,
    }