"""
Motor de Cálculo Estocástico Fraccionario:
Movimiento Browniano Fraccionario (fBm) & Estimación del Exponente de Hurst (H).
"""

from typing import Dict, Tuple, List, Optional
import numpy as np
import pandas as pd
from src.stochastic_engine import SimulationResult


def estimate_hurst_rs(returns_series: pd.Series) -> Dict[str, any]:
    """
    Estima el Exponente de Hurst (H) mediante el Análisis de Rango Reescalado (R/S Analysis)
    desarrollado por H.E. Hurst y formalizado por Benoit Mandelbrot.
    
    Interpretación cuantitativa:
    - H ~ 0.50 (0.45 - 0.55): Paseo Aleatorio Puro (Movimiento Browniano Estándar, sin memoria, mercado eficiente).
    - H > 0.55: Proceso Persistente (Memoria Larga / Long Memory, tendencia, momentum alcista/bajista).
    - H < 0.45: Proceso Antipersistente (Reversión a la Media / Mean-Reverting, alternancia frecuente de signos).
    """
    series = returns_series.dropna().values
    N = len(series)
    if N < 100:
        return {
            "H": 0.50,
            "r_squared": 0.0,
            "regime": "Paseo Aleatorio Estándar (Sin Memoria)",
            "interpretation": "Muestra insuficiente para estimar persistencia.",
            "tau_values": [],
            "rs_values": [],
        }

    # Definir tamaños de ventana tau (escalas de tiempo logarítmicas)
    min_tau = 10
    max_tau = N // 2
    tau_list = []
    rs_list = []

    # Probar diferentes subdivisiones
    num_windows = 18
    tau_candidates = np.unique(np.logspace(np.log10(min_tau), np.log10(max_tau), num=num_windows).astype(int))

    for tau in tau_candidates:
        if tau >= N:
            continue
        num_chunks = N // tau
        if num_chunks < 1:
            continue

        chunk_rs = []
        for i in range(num_chunks):
            chunk = series[i * tau : (i + 1) * tau]
            mean_chunk = np.mean(chunk)
            cum_dev = np.cumsum(chunk - mean_chunk)
            R = np.max(cum_dev) - np.min(cum_dev)
            S = np.std(chunk, ddof=1)
            if S > 1e-8:
                chunk_rs.append(R / S)

        if chunk_rs:
            tau_list.append(tau)
            rs_list.append(np.mean(chunk_rs))

    if len(tau_list) < 4:
        return {
            "H": 0.50,
            "r_squared": 0.0,
            "regime": "Paseo Aleatorio Estándar",
            "interpretation": "Datos insuficientes.",
            "tau_values": [],
            "rs_values": [],
        }

    # Regresión log-log: ln(R/S) = alpha + H * ln(tau)
    log_tau = np.log(tau_list)
    log_rs = np.log(rs_list)

    # Ajuste lineal por mínimos cuadrados
    slope, intercept = np.polyfit(log_tau, log_rs, 1)
    H_estimated = float(slope)

    # Coeficiente de determinación R^2
    y_pred = slope * log_tau + intercept
    ss_tot = np.sum((log_rs - np.mean(log_rs)) ** 2)
    ss_res = np.sum((log_rs - y_pred) ** 2)
    r_squared = float(1.0 - (ss_res / ss_tot)) if ss_tot > 0 else 0.0

    # Acotar en rango teórico viable de Hurst
    H_bounded = max(0.05, min(0.95, H_estimated))

    if H_bounded >= 0.55:
        regime = "Persistente (Memoria Larga / Tendencial)"
        interpretation = (
            f"Hurst H = {H_bounded:.2f} > 0.50 indica que el activo tiene memoria de largo plazo. "
            "Los retornos positivos tienden a generar rachas de retornos positivos (efecto de inercia o momentum)."
        )
    elif H_bounded <= 0.45:
        regime = "Antipersistente (Reversión a la Media)"
        interpretation = (
            f"Hurst H = {H_bounded:.2f} < 0.50 indica que el activo exhibe micro-reversión a la media. "
            "El precio tiende a alternar oscilaciones y volver hacia su equilibrio de corto plazo."
        )
    else:
        regime = "Paseo Aleatorio Puro (Sin Memoria / Eficiente)"
        interpretation = (
            f"Hurst H = {H_bounded:.2f} ≈ 0.50 valida la hipótesis de mercado eficiente y el Movimiento Browniano clásico. "
            "Las variaciones de hoy no tienen correlación con las variaciones pasadas."
        )

    return {
        "H": H_bounded,
        "H_raw": H_estimated,
        "r_squared": r_squared,
        "regime": regime,
        "interpretation": interpretation,
        "tau_values": tau_list,
        "rs_values": rs_list,
    }


def simulate_fractional_brownian_motion(
    spot: float,
    ann_mu: float,
    ann_vol: float,
    H: float = 0.60,
    horizon_days: int = 10,
    n_paths: int = 3000,
    seed: int = 42,
    ticker: str = "ASSET",
) -> SimulationResult:
    """
    Simula trayectorias Monte Carlo de un Movimiento Browniano Fraccionario (fBm)
    bajo la medida física:
    S(t) = S0 * exp( (mu - 0.5 * sigma^2) * t + sigma * B_H(t) )
    donde B_H(t) es el proceso fraccionario con parámetro de Hurst H in (0, 1).
    """
    np.random.seed(seed)
    dt = 1.0 / 252.0
    time_grid = np.arange(horizon_days + 1)
    T = horizon_days * dt

    # Si H es muy cercano a 0.5, es el Browniano tradicional
    if abs(H - 0.5) < 0.02:
        H = 0.5

    # Construcción de la matriz de covarianza de incrementos fraccionarios (fGn)
    # gamma(k) = 0.5 * (|k+1|^{2H} - 2|k|^{2H} + |k-1|^{2H})
    m = horizon_days
    k_vals = np.arange(m)
    autocov = 0.5 * (np.abs(k_vals + 1) ** (2 * H) - 2 * (k_vals ** (2 * H)) + np.abs(k_vals - 1) ** (2 * H))

    # Matriz Toeplitz de covarianza
    from scipy.linalg import toeplitz, cholesky
    gamma_matrix = toeplitz(autocov)

    # Descomposición de Cholesky regularizada
    try:
        L = cholesky(gamma_matrix + np.eye(m) * 1e-9, lower=True)
    except Exception:
        L = np.eye(m)

    # Generación de trayectorias de fGn (fracciones de ruido gaussiano)
    # Z ~ N(0, 1) de tamaño (n_paths, m)
    Z = np.random.normal(0, 1, size=(n_paths, m))
    fgn = np.dot(Z, L.T) * (dt ** H)

    # Trayectorias del proceso fBm B_H(t) acumulando incrementos
    fbm_paths = np.zeros((n_paths, m + 1))
    fbm_paths[:, 1:] = np.cumsum(fgn, axis=1)

    # Construcción de precios
    drift = (ann_mu - 0.5 * (ann_vol ** 2)) * (time_grid * dt)
    paths = spot * np.exp(drift + ann_vol * fbm_paths)

    # Percentiles
    percentiles = {
        p: np.percentile(paths, p, axis=0) for p in [10, 25, 50, 75, 90]
    }
    terminal_prices = paths[:, -1]
    pct_changes = (terminal_prices - spot) / spot
    simulated_mean = float(np.mean(terminal_prices))
    theoretical_mean = float(spot * np.exp(ann_mu * T))
    std_error = float(np.std(terminal_prices, ddof=1) / np.sqrt(n_paths))

    # Pérdidas positivas
    losses = -pct_changes
    var_95 = float(np.percentile(losses, 95))
    var_99 = float(np.percentile(losses, 99))
    cvar_95 = float(np.mean(losses[losses >= var_95]))
    cvar_99 = float(np.mean(losses[losses >= var_99]))

    return SimulationResult(
        model_name=f"Browniano Fraccionario (fBm, H={H:.2f})",
        ticker=ticker,
        spot=spot,
        horizon_days=horizon_days,
        n_paths=n_paths,
        time_grid=time_grid,
        paths=paths,
        percentiles=percentiles,
        simulated_mean=simulated_mean,
        theoretical_mean=theoretical_mean,
        std_error=std_error,
        var_95=var_95,
        var_99=var_99,
        cvar_95=cvar_95,
        cvar_99=cvar_99,
        parameters={
            "H": H,
            "ann_mu": ann_mu,
            "ann_vol": ann_vol,
            "horizon_days": horizon_days,
            "dt": dt,
        },
        log_likelihood=0.0,
        aic=0.0,
        bic=0.0,
    )
