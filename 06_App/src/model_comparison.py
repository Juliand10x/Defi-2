from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from src.stochastic_engine import (
    calibrate_gbm,
    simulate_gbm,
    calibrate_merton_jump,
    simulate_merton_jump,
    calibrate_ornstein_uhlenbeck,
    simulate_ornstein_uhlenbeck,
    SimulationResult,
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
    
    # 1. GBM
    p_gbm = calibrate_gbm(returns_series)
    sim_gbm = simulate_gbm(spot, p_gbm, horizon_days=horizon_days, n_paths=n_paths, seed=seed)
    
    # 2. Merton Jump-Diffusion
    p_mjd = calibrate_merton_jump(returns_series)
    sim_mjd = simulate_merton_jump(spot, p_mjd, horizon_days=horizon_days, n_paths=n_paths, seed=seed)
    
    # 3. Ornstein-Uhlenbeck
    p_ou = calibrate_ornstein_uhlenbeck(prices_series)
    sim_ou = simulate_ornstein_uhlenbeck(spot, p_ou, horizon_days=horizon_days, n_paths=n_paths, seed=seed)
    
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
            "VaR 99% (10d)": f"{sim_gbm.var_99:.2%}",
            "CVaR 99% (10d)": f"{sim_gbm.cvar_99:.2%}",
            "Complejidad (k)": 2,
            "Hipótesis": "Caminata aleatoria lognormal, volatilidad constante",
        },
        {
            "Modelo": "Salto de Merton (Jump-Diffusion)",
            "Parámetros Clave": f"λ={p_mjd['lambda']:.1f}/año, μ_j={p_mjd['mu_j']:.1%}, σ_j={p_mjd['sigma_j']:.1%}",
            "Log-Likelihood": round(p_mjd["log_likelihood"], 1),
            "AIC": round(p_mjd["aic"], 1),
            "BIC": round(p_mjd["bic"], 1),
            "VaR 99% (10d)": f"{sim_mjd.var_99:.2%}",
            "CVaR 99% (10d)": f"{sim_mjd.cvar_99:.2%}",
            "Complejidad (k)": 5,
            "Hipótesis": "Difusión continua + saltos discretos Poisson (colas pesadas)",
        },
        {
            "Modelo": "Ornstein-Uhlenbeck (O-U)",
            "Parámetros Clave": f"θ={p_ou['theta']:.2f}, Half-Life={p_ou['half_life_days']:.0f}d, Media=USD {p_ou['mu_ou_price']:.1f}",
            "Log-Likelihood": round(p_ou["log_likelihood"], 1),
            "AIC": round(p_ou["aic"], 1),
            "BIC": round(p_ou["bic"], 1),
            "VaR 99% (10d)": f"{sim_ou.var_99:.2%}",
            "CVaR 99% (10d)": f"{sim_ou.cvar_99:.2%}",
            "Complejidad (k)": 3,
            "Hipótesis": "Proceso estacionario con reversión a la media fundamental",
        },
    ])
    
    # Determinación del Mejor Modelo
    # Regla cuantitativa:
    # 1. Si Kurtosis > 3.8 y BIC Merton es significativamente competitivo o menor que GBM -> Merton captura colas de riesgo reales.
    # 2. Si Half-life < 180 días y theta > 0.4 -> O-U es ideal para activos defensivos / mean-reverting.
    # 3. Si no, GBM por principio de parsimonia.
    
    winner = "GBM"
    winner_reason = ""
    
    if p_mjd["bic"] < p_gbm["bic"] or (kurt > 4.0 and p_mjd["jump_count"] >= 3):
        winner = "Merton Jump-Diffusion"
        winner_reason = f"Kurtosis elevada ({kurt:.2f} > 3) y presencia de {int(p_mjd['jump_count'])} saltos empíricos. El modelo de Merton captura las colas pesadas y cisnes negros que el Browniano ignora."
    elif p_ou["half_life_days"] < 150 and p_ou["theta"] > 0.5:
        winner = "Ornstein-Uhlenbeck"
        winner_reason = f"Fuerte evidencia de reversión a la media con vida media de {p_ou['half_life_days']:.0f} días y velocidad θ={p_ou['theta']:.2f}. Ideal para activos defensivos."
    else:
        winner = "Mov. Browniano Geométrico"
        winner_reason = f"Distribución de retornos parsimoniosa (BIC óptimo {p_gbm['bic']:.1f}). La estructura estándar de caminata aleatoria modela adecuadamente la serie sin sobreparametrización."
        
    # Recomendación por Perfil de Riesgo
    risk_decisions = {
        "Conservador": {
            "modelo_recomendado": "Salto de Merton (para estrés) o Ornstein-Uhlenbeck (para activos defensivos)",
            "var_adopcion": sim_mjd.var_99 if sim_mjd.var_99 > sim_gbm.var_99 else sim_gbm.var_99,
            "cvar_adopcion": sim_mjd.cvar_99,
            "justificacion": "El perfil conservador debe blindarse contra caídas abruptas. El modelo de Merton revela el verdadero riesgo de cola que el Browniano subestima (CVaR 99%). Se sugiere limitar la exposición a este activo si exhibe alta frecuencia de salto (λ).",
            "accion": "Asignar ponderación defensiva (mínimo VaR conjunto) y exigir cobertura si CVaR supera el 8% a 10 días."
        },
        "Moderado": {
            "modelo_recomendado": winner,
            "var_adopcion": sim_mjd.var_99 if winner == "Merton Jump-Diffusion" else sim_gbm.var_99,
            "cvar_adopcion": sim_mjd.cvar_99 if winner == "Merton Jump-Diffusion" else sim_gbm.cvar_99,
            "justificacion": f"Equilibrio entre precisión econométrica y parsimonia. Se adopta el modelo ganador ({winner}) respaldado por criterios de información BIC/AIC.",
            "accion": "Ponderación balanceada por inverso de VaR o mínimo VaR con tope sectorial del 35%."
        },
        "Agresivo": {
            "modelo_recomendado": "Mov. Browniano con deriva (GBM) o Salto Alcista de Merton",
            "var_adopcion": sim_gbm.var_99,
            "cvar_adopcion": sim_gbm.cvar_99,
            "justificacion": f"El inversionista agresivo tolera la varianza y los saltos de corto plazo buscando capturar el drift anualizado (μ={p_gbm['mu_annual']:.1%}) y la convexidad en las colas superiores.",
            "accion": "Maximizar asignación hacia el tope individual (hasta 20%) en activos con drift positivo superior al 12% anual."
        }
    }
    
    return {
        "ticker": ticker,
        "spot": spot,
        "kurtosis": kurt,
        "skewness": skew,
        "models_table": models_table,
        "sim_gbm": sim_gbm,
        "sim_mjd": sim_mjd,
        "sim_ou": sim_ou,
        "winner": winner,
        "winner_reason": winner_reason,
        "risk_decisions": risk_decisions,
    }