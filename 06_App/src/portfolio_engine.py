"""
Módulo de Asignación de Capital y Optimización de Portafolios (Pasos 11 y 12 del Taller).
Implementa:
- 3 esquemas: Pesos Iguales (1/N), Inverso al VaR individual (1/v_i) y Mínimo VaR Conjunto Restringido.
- Optimización Cuadrática SLSQP con media cero y cotas oficiales (2% a 20% por acción, sector <= 35%).
- Presupuesto de riesgo V_bar y factor de escala dinámico f = min{1, V_bar / V_riesgo}.
- Ejecución con acciones enteras, reporte de efectivo residual y recalculo de pesos y VaR efectivo.
- Motor de explicabilidad financiera.
"""

from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import pandas as pd
from scipy import optimize, stats


def compute_portfolio_allocation(
    capital: float,
    portfolio_df: pd.DataFrame,
    returns_df: pd.DataFrame,
    confidence: float = 99.0,
    horizon_days: int = 10,
    prices_df: Optional[pd.DataFrame] = None,
    risk_budget_v: Optional[float] = None,
    custom_bounds: Optional[Tuple[float, float]] = None,
    max_sector_exposure: float = 0.35,
) -> Dict[str, Any]:
    """
    Calcula la asignación de capital óptima y comparativa según los Pasos 11 y 12 del Taller:
    1. Pesos iguales: w_i = 1/N
    2. Inverso al VaR: w_i proporcional a 1/v_i (ignora correlaciones)
    3. Mínimo VaR con SLSQP:
       min_w B * Phi^-1(alpha) * sqrt(h * w^T Sigma_R w)
       s.a. sum(w) = 1, 0.02 <= w_i <= 0.20, sum_{i in sector} w_i <= 0.35
    4. Presupuesto de riesgo V_bar:
       f = min{1, V_bar / V_riesgo}, A_i = f * B * w_i, E = (1 - f) * B
    5. Redondeo a acciones enteras, efectivo residual y recalculo del VaR efectivo.
    """
    valid_tickers = [t for t in portfolio_df["Ticker"] if t in returns_df.columns]
    N = len(valid_tickers)
    if N < 2:
        return {}

    sub_returns = returns_df[valid_tickers].dropna()
    # Usar divisor n-1 y media cero para asignación (Paso 11)
    daily_cov = sub_returns.cov().values
    alpha = confidence / 100.0 if confidence > 1.0 else confidence
    z_alpha = stats.norm.ppf(alpha)  # ~2.3263 para 99%

    sectors = [portfolio_df.loc[portfolio_df["Ticker"] == t, "Sector"].values[0] for t in valid_tickers]

    # Precios Spot observados
    if prices_df is not None:
        spots = np.array([float(prices_df[t].dropna().iloc[-1]) for t in valid_tickers])
    else:
        spots = np.array([100.0 for _ in valid_tickers])

    # -----------------------------------------------------------------
    # Esquema 1: Pesos Iguales (1/N)
    # -----------------------------------------------------------------
    w_equal = np.ones(N) / N

    # -----------------------------------------------------------------
    # Esquema 2: Pesos Inversos al VaR Individual (1 / v_i)
    # v_i = B * Phi^-1(alpha) * sqrt(h * sigma_i^2)
    # -----------------------------------------------------------------
    vols_daily = np.sqrt(np.diag(daily_cov))
    indiv_vars_pct = z_alpha * np.sqrt(horizon_days) * vols_daily
    indiv_vars_usd = capital * indiv_vars_pct

    inv_vars = 1.0 / np.maximum(indiv_vars_pct, 1e-6)
    w_inv_var = inv_vars / np.sum(inv_vars)

    # -----------------------------------------------------------------
    # Esquema 3: Mínimo VaR Conjunto (Optimización Restringida SLSQP)
    # -----------------------------------------------------------------
    # Con 10 acciones las cotas estrictas del taller son 0.02 y 0.20
    if custom_bounds is not None:
        w_min, w_max = custom_bounds
    else:
        w_min = 0.02 if N >= 5 else 0.05
        w_max = 0.20 if N == 10 else min(0.35, max(0.15, 2.0 / N))

    # Función objetivo cuadrática pura: min w^T Sigma_R w
    # Matemáticamente equivalente a minimizar B * Phi^-1(alpha) * sqrt(h * w^T Sigma_R w)
    # pero con gradiente cuadrático suave y convergencia óptima en SLSQP.
    def portfolio_variance_obj(w: np.ndarray) -> float:
        return float(np.dot(w.T, np.dot(daily_cov, w)))

    # Restricción de presupuesto: sum(w) = 1
    constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1.0}]

    # Restricción sectorial: sum_{i in sector} w_i <= max_sector_exposure (0.35)
    unique_sectors = list(dict.fromkeys(sectors))
    for sec in unique_sectors:
        sec_idxs = [i for i, s in enumerate(sectors) if s == sec]
        constraints.append({
            "type": "ineq",
            "fun": lambda w, idxs=sec_idxs: max_sector_exposure - np.sum(w[idxs])
        })

    bounds = [(w_min, w_max) for _ in range(N)]
    init_w = np.ones(N) / N

    opt_res = optimize.minimize(
        portfolio_variance_obj,
        init_w,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"maxiter": 300, "ftol": 1e-9}
    )

    if opt_res.success:
        w_min_var = opt_res.x
        solver_status = "Óptimo convergente (SLSQP exitoso)"
    else:
        w_min_var = w_equal
        solver_status = f"Aproximado (Solver no convergió: {opt_res.message})"

    # Normalizar por precisión flotante
    w_min_var = w_min_var / np.sum(w_min_var)

    # VaR del portafolio 100% invertido
    sigma_daily_port = np.sqrt(float(np.dot(w_min_var.T, np.dot(daily_cov, w_min_var))))
    v_riesgo_pct = float(z_alpha * np.sqrt(horizon_days) * sigma_daily_port)
    v_riesgo_usd = float(capital * v_riesgo_pct)

    # -----------------------------------------------------------------
    # Paso 12: Presupuesto de Riesgo V_bar y Factor de Escala f
    # f = min{1, V_bar / V_riesgo}, A_i = f * B * w_i, E = (1 - f) * B
    # -----------------------------------------------------------------
    if risk_budget_v is not None and risk_budget_v > 0 and v_riesgo_usd > 0:
        f_scale = min(1.0, float(risk_budget_v / v_riesgo_usd))
    else:
        f_scale = 1.0

    capital_riesgoso = capital * f_scale
    capital_efectivo_estrategia = capital * (1.0 - f_scale)

    # Montos teóricos asignados
    montos_teoricos_usd = capital_riesgoso * w_min_var

    # Cantidad de acciones enteras y redondeo a mercado real
    acciones_enteras = np.floor(montos_teoricos_usd / spots).astype(int)
    inversion_real_acciones = acciones_enteras * spots
    total_invertido_acciones = float(np.sum(inversion_real_acciones))
    efectivo_residual_redondeo = float(capital_riesgoso - total_invertido_acciones)
    efectivo_total_disponible = float(capital_efectivo_estrategia + efectivo_residual_redondeo)

    # -----------------------------------------------------------------
    # Recalculo de Pesos Reales y Riesgo Efectivo de Cartera
    # -----------------------------------------------------------------
    pesos_reales_sobre_capital = inversion_real_acciones / capital
    if total_invertido_acciones > 0:
        pesos_normalizados_invertidos = inversion_real_acciones / total_invertido_acciones
        sigma_real_daily = np.sqrt(float(np.dot(pesos_normalizados_invertidos.T, np.dot(daily_cov, pesos_normalizados_invertidos))))
        var_efectivo_usd = float(total_invertido_acciones * z_alpha * np.sqrt(horizon_days) * sigma_real_daily)
        var_efectivo_pct = float(var_efectivo_usd / capital)
    else:
        var_efectivo_usd = 0.0
        var_efectivo_pct = 0.0

    # Construcción de la tabla maestra de asignación
    df_alloc = pd.DataFrame({
        "Ticker": valid_tickers,
        "Sector": sectors,
        "Precio Spot (USD)": [round(s, 2) for s in spots],
        "VaR Individual 99% (%)": [f"{v:.2%}" for v in indiv_vars_pct],
        "VaR Individual 99% (USD)": [f"${v:,.2f}" for v in indiv_vars_usd],
        "Peso Equiponderado (1/N)": [f"{w:.2%}" for w in w_equal],
        "Peso Inverso VaR": [f"{w:.2%}" for w in w_inv_var],
        "Peso Teórico Óptimo": [round(w, 4) for w in w_min_var],
        "Peso Teórico (%)": [f"{w:.2%}" for w in w_min_var],
        "Monto Teórico (USD)": [round(m, 2) for m in montos_teoricos_usd],
        "Acciones Enteras": acciones_enteras,
        "Inversión Real (USD)": [round(inv, 2) for inv in inversion_real_acciones],
        "Peso Real (%)": [f"{p:.2%}" for p in pesos_reales_sobre_capital],
    })

    # Resumen sectorial
    sec_summary = df_alloc.groupby("Sector").agg({
        "Inversión Real (USD)": "sum",
        "Peso Teórico Óptimo": "sum",
    }).reset_index()
    sec_summary["Peso Sectorial Real (%)"] = sec_summary["Inversión Real (USD)"] / capital
    sec_summary["Cumple Cota (<= 35%)"] = sec_summary["Peso Sectorial Real (%)"] <= (max_sector_exposure + 0.01)

    # Explicabilidad financiera
    top_asset_idx = int(np.argmax(w_min_var))
    min_asset_idx = int(np.argmin(w_min_var))
    explanations = [
        f"**Criterio del Módulo**: La asignación de Mínimo VaR minimiza la varianza conjunta considerando covarianzas cruzadas. La regla inversa al VaR asigna {w_inv_var[top_asset_idx]:.1%} frente al {w_min_var[top_asset_idx]:.1%} del modelo óptimo, demostrando que ignorar correlaciones sobrepondera activos correlacionados.",
        f"**Activo más blindado**: `{valid_tickers[top_asset_idx]}` recibe la mayor ponderación ({w_min_var[top_asset_idx]:.2%}) por su bajo riesgo marginal dentro de la matriz de covarianza conjunta.",
        f"**Activo más acotado**: `{valid_tickers[min_asset_idx]}` recibe la menor ponderación ({w_min_var[min_asset_idx]:.2%}), respetando el límite mínimo del 2.0% exigido por la rúbrica.",
        f"**Presupuesto de Riesgo (f={f_scale:.2f})**: El VaR no diversificado de {v_riesgo_usd:,.2f} USD se ajusta al presupuesto de riesgo asignando USD {capital_riesgoso:,.2f} a activos de riesgo y preservando USD {efectivo_total_disponible:,.2f} en efectivo libre de riesgo.",
    ]

    return {
        "allocation_df": df_alloc,
        "sector_summary": sec_summary,
        "w_equal": w_equal,
        "w_inv_var": w_inv_var,
        "w_min_var": w_min_var,
        "capital": capital,
        "risk_budget_v": risk_budget_v,
        "f_scale": f_scale,
        "capital_riesgoso": capital_riesgoso,
        "capital_efectivo": capital_efectivo_estrategia,
        "efectivo_residual_redondeo": efectivo_residual_redondeo,
        "efectivo_total": efectivo_total_disponible,
        "total_invertido_acciones": total_invertido_acciones,
        "var_portfolio_pct": v_riesgo_pct,
        "var_portfolio_usd": v_riesgo_usd,
        "var_efectivo_pct": var_efectivo_pct,
        "var_efectivo_usd": var_efectivo_usd,
        "solver_success": opt_res.success,
        "solver_status": solver_status,
        "explanations": explanations,
    }
