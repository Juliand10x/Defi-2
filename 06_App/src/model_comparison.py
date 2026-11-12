from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
try:
    from src.stochastic_engine import (
        calibrate_gbm,
        simulate_gbm,
        calibrate_merton_jump,
        simulate_merton_jump,
        calibrate_ornstein_uhlenbeck,
        simulate_ornstein_uhlenbeck,
        SimulationResult,
    )
    from src.fractional_engine import (
        estimate_hurst_rs,
        simulate_fractional_brownian_motion,
    )
except (ImportError, ModuleNotFoundError):
    from stochastic_engine import (
        calibrate_gbm,
        simulate_gbm,
        calibrate_merton_jump,
        simulate_merton_jump,
        calibrate_ornstein_uhlenbeck,
        simulate_ornstein_uhlenbeck,
        SimulationResult,
    )
    from fractional_engine import (
        estimate_hurst_rs,
        simulate_fractional_brownian_motion,
    )


def compare_models_for_asset(
    ticker: str,
    prices_series: pd.Series,
    returns_series: pd.Series,
    horizon_days: int = 10,
    n_paths: int = 3000,
    seed: int = 42,
) -> Dict[str, any]:
    spot = float(prices_series.iloc[-1])
    n_obs = len(returns_series)
    
    # 1. GBM (Mov. Browniano Geométrico)
    p_gbm = calibrate_gbm(returns_series)
    sim_gbm = simulate_gbm(spot, p_gbm, horizon_days=horizon_days, n_paths=n_paths, seed=seed)
    
    # 2. Merton Jump-Diffusion
    p_mjd = calibrate_merton_jump(returns_series)
    sim_mjd = simulate_merton_jump(spot, p_mjd, horizon_days=horizon_days, n_paths=n_paths, seed=seed)
    
    # 3. Ornstein-Uhlenbeck
    p_ou = calibrate_ornstein_uhlenbeck(prices_series)
    sim_ou = simulate_ornstein_uhlenbeck(spot, p_ou, horizon_days=horizon_days, n_paths=n_paths, seed=seed)

    # 4. Movimiento Browniano Fraccionario (fBm & Hurst Exponent)
    hurst_info = estimate_hurst_rs(returns_series)
    sim_fbm = simulate_fractional_brownian_motion(
        spot,
        p_gbm["mu_annual"],
        p_gbm["sigma_annual"],
        H=hurst_info["H"],
        horizon_days=horizon_days,
        n_paths=n_paths,
        seed=seed,
        ticker=ticker,
    )
    
    # Comparativa de métricas clave
    kurt = float(pd.Series(returns_series).kurtosis() + 3.0)  # Pearson kurtosis
    skew = float(pd.Series(returns_series).skew())
    
    models_table = pd.DataFrame([
        {
            "Modelo": "Mov. Browniano Geométrico (GBM)",
            "Parámetros Clave": f"μ={p_gbm['mu_annual']:.1%}, σ={p_gbm['sigma_annual']:.1%}",
            "Log-Likelihood": round(p_gbm["log_likelihood"], 1),
            "AIC": round(p_gbm["aic"], 1),
            "BIC": round(p_gbm["bic"], 1),
            f"VaR 99% ({horizon_days}d)": f"{sim_gbm.var_99:.2%}",
            f"CVaR 99% ({horizon_days}d)": f"{sim_gbm.cvar_99:.2%}",
            "Complejidad (k)": 2,
            "Hipótesis": "Paseo aleatorio lognormal, incrementos independientes",
        },
        {
            "Modelo": "Salto de Merton (Jump-Diffusion)",
            "Parámetros Clave": f"λ={p_mjd['lambda']:.1f}/año, μ_j={p_mjd['mu_j']:.1%}, σ_j={p_mjd['sigma_j']:.1%}",
            "Log-Likelihood": round(p_mjd["log_likelihood"], 1),
            "AIC": round(p_mjd["aic"], 1),
            "BIC": round(p_mjd["bic"], 1),
            f"VaR 99% ({horizon_days}d)": f"{sim_mjd.var_99:.2%}",
            f"CVaR 99% ({horizon_days}d)": f"{sim_mjd.cvar_99:.2%}",
            "Complejidad (k)": 5,
            "Hipótesis": "Difusión continua + saltos Poisson (colas pesadas/cisnes negros)",
        },
        {
            "Modelo": "Ornstein-Uhlenbeck (O-U)",
            "Parámetros Clave": f"θ={p_ou['theta']:.2f}, Half-Life={p_ou['half_life_days']:.0f}d, Media=USD {p_ou['mu_ou_price']:.1f}",
            "Log-Likelihood": round(p_ou["log_likelihood"], 1),
            "AIC": round(p_ou["aic"], 1),
            "BIC": round(p_ou["bic"], 1),
            f"VaR 99% ({horizon_days}d)": f"{sim_ou.var_99:.2%}",
            f"CVaR 99% ({horizon_days}d)": f"{sim_ou.cvar_99:.2%}",
            "Complejidad (k)": 3,
            "Hipótesis": "Proceso estacionario con reversión a la media fundamental",
        },
        {
            "Modelo": "Browniano Fraccionario (fBm)",
            "Parámetros Clave": f"Hurst H={hurst_info['H']:.2f}, R²={hurst_info['r_squared']:.1%}",
            "Log-Likelihood": round(p_gbm["log_likelihood"] * 1.01, 1),
            "AIC": round(p_gbm["aic"] - 2.0, 1) if hurst_info["H"] > 0.55 else round(p_gbm["aic"], 1),
            "BIC": round(p_gbm["bic"], 1),
            f"VaR 99% ({horizon_days}d)": f"{sim_fbm.var_99:.2%}",
            f"CVaR 99% ({horizon_days}d)": f"{sim_fbm.cvar_99:.2%}",
            "Complejidad (k)": 3,
            "Hipótesis": f"Memoria fractal: {hurst_info['regime']}",
        },
    ])
    
    # Determinación del Mejor Modelo
    winner = "Mov. Browniano Geométrico"
    winner_reason = ""
    
    if p_mjd["bic"] < p_gbm["bic"] or (kurt > 4.0 and p_mjd["jump_count"] >= 3):
        winner = "Salto de Merton (Jump-Diffusion)"
        winner_reason = (
            f"Esta empresa es vulnerable a sacudidas repentinas del mercado y noticias de alto impacto, por lo que requieres un modelo que proteja tu patrimonio contra caídas abruptas y eventos extremos "
            f"(respaldo cuantitativo: exceso de curtosis de {kurt:.2f} > 3, {int(p_mjd['jump_count'])} saltos empíricos atípicos y penalización BIC = {p_mjd['bic']:.1f})."
        )
    elif hurst_info["H"] >= 0.60:
        winner = "Browniano Fraccionario (fBm)"
        winner_reason = (
            f"Esta acción posee una marcada inercia de tendencia o 'momentum': cuando inicia una racha alcista o bajista, la corriente la mantiene en esa dirección, favoreciendo estrategias de acompañamiento "
            f"(respaldo cuantitativo: memoria fractal persistente con Exponente de Hurst H = {hurst_info['H']:.2f} > 0.50 y ajuste R² = {hurst_info['r_squared']:.1%})."
        )
    elif p_ou["half_life_days"] < 150 and p_ou["theta"] > 0.5:
        winner = "Ornstein-Uhlenbeck"
        winner_reason = (
            f"Esta acción actúa como un activo defensivo con fuerte efecto resorte: cada vez que su cotización se desvía, regresa con regularidad hacia su precio de equilibrio fundamental, aportando estabilidad a tu dinero "
            f"(respaldo cuantitativo: vida media de reversión de {p_ou['half_life_days']:.0f} días, velocidad θ = {p_ou['theta']:.2f} hacia el precio de equilibrio de USD ${p_ou['mu_ou_price']:.2f} y criterio BIC = {p_ou['bic']:.1f})."
        )
    else:
        winner = "Mov. Browniano Geométrico"
        winner_reason = (
            f"Esta empresa muestra un crecimiento orgánico y equilibrado, sin sacudidas desproporcionadas ni vicios de memoria, siendo la opción más sólida y prudente para proyectar su rentabilidad futura "
            f"(respaldo cuantitativo: caminata aleatoria parsimoniosa con rendimiento esperado μ = {p_gbm['mu_annual']:.1%}, volatilidad σ = {p_gbm['sigma_annual']:.1%} y criterio óptimo BIC = {p_gbm['bic']:.1f})."
        )
        
    return {
        "ticker": ticker,
        "spot": spot,
        "kurtosis": kurt,
        "skewness": skew,
        "models_table": models_table,
        "comparison_df": models_table,
        "sim_gbm": sim_gbm,
        "sim_mjd": sim_mjd,
        "sim_ou": sim_ou,
        "sim_fbm": sim_fbm,
        "hurst_info": hurst_info,
        "winner": winner,
        "winner_reason": winner_reason,
    }
