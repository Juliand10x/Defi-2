"""
Motor de Medición de Riesgo Integral y Pruebas de Estrés (Paso 10 del PDF).
Implementación de los 3 Estimadores de VaR al 99% (Horizonte h=10 días) + Expected Shortfall (CVaR):
1. VaR Histórico (Ventanas no solapadas / solapadas con cuantiles de pérdida empírica)
2. VaR Paramétrico Normal (B * Phi^-1(alpha) * sqrt(h * w^T Sigma w))
3. VaR Monte Carlo Multivariado (20.000 trayectorias conjuntas con correlación Cholesky)
+ 3 Escenarios Oficiales de Stress Testing:
- Estrés 1: Caída Uniforme de Mercado (-10%)
- Estrés 2: Desplome Sectorial Asimétrico (-20% sector principal, -5% resto)
- Estrés 3: Choque de Volatilidad (Volatilidad x 1.5 y Correlación rho = 0.80)
"""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from scipy import stats
import plotly.graph_objects as go


def compute_var_comparison_and_stress(
    capital: float,
    weights: np.ndarray,
    returns_df: pd.DataFrame,
    sectors: List[str],
    tickers: List[str],
    confidence: float = 0.99,
    horizon_days: int = 10,
    n_mc_sims: int = 25000,
    seed: int = 42,
) -> Dict[str, any]:
    """
    Calcula los 3 estimadores de VaR y CVaR (Expected Shortfall) del portafolio
    junto con los 3 escenarios de estrés definidos en el taller de Valoración de Activos.
    """
    clean_rets = returns_df[tickers].dropna()
    N = len(tickers)
    w = np.array(weights).reshape(-1, 1)

    # Covarianza diaria y anual
    cov_daily = clean_rets.cov().values
    z_alpha = stats.norm.ppf(confidence)  # ~2.3263 al 99%

    # -------------------------------------------------------------
    # 1. VaR y CVaR Paramétrico Normal
    # VaR = B * Phi^-1(alpha) * sqrt(h * w^T Sigma w)
    # -------------------------------------------------------------
    var_param_daily_sigma = np.sqrt(float(w.T @ cov_daily @ w))
    var_param_h_sigma = var_param_daily_sigma * np.sqrt(horizon_days)
    var_param_pct = float(z_alpha * var_param_h_sigma)
    var_param_usd = capital * var_param_pct

    # Expected Shortfall Normal: E[L | L > VaR] = B * sigma * phi(z) / (1 - alpha)
    phi_z = stats.norm.pdf(z_alpha)
    cvar_param_pct = float(var_param_h_sigma * (phi_z / (1.0 - confidence)))
    cvar_param_usd = capital * cvar_param_pct

    # -------------------------------------------------------------
    # 2. VaR y CVaR Histórico
    # Construcción de retornos acumulados a h días
    # -------------------------------------------------------------
    # Retornos diarios del portafolio
    port_daily_rets = (clean_rets.values @ w).flatten()
    T_obs = len(port_daily_rets)

    # Retornos de bloques compuestos de h días
    cum_h_returns = []
    for i in range(T_obs - horizon_days + 1):
        block = port_daily_rets[i : i + horizon_days]
        comp_r = np.prod(1.0 + block) - 1.0
        cum_h_returns.append(comp_r)
    cum_h_returns = np.array(cum_h_returns)

    # Pérdidas L = -R_h
    losses_hist_pct = -cum_h_returns
    var_hist_pct = float(np.percentile(losses_hist_pct, confidence * 100))
    var_hist_usd = capital * var_hist_pct

    tail_losses = losses_hist_pct[losses_hist_pct >= var_hist_pct]
    cvar_hist_pct = float(np.mean(tail_losses)) if len(tail_losses) > 0 else var_hist_pct
    cvar_hist_usd = capital * cvar_hist_pct

    # -------------------------------------------------------------
    # 3. VaR y CVaR Monte Carlo Multivariado (20.000+ escenarios)
    # -------------------------------------------------------------
    np.random.seed(seed)
    mu_daily = clean_rets.mean().values.reshape(-1, 1)

    # Descomposición de Cholesky de la covarianza diaria
    try:
        L_chol = np.linalg.cholesky(cov_daily + np.eye(N) * 1e-9)
    except Exception:
        # Regularización si no es definida positiva
        eigvals, eigvecs = np.linalg.eigh(cov_daily)
        eigvals = np.maximum(eigvals, 1e-8)
        cov_reg = eigvecs @ np.diag(eigvals) @ eigvecs.T
        L_chol = np.linalg.cholesky(cov_reg)

    # Simulación de retornos a h días: R_h ~ N(mu * h, cov * h)
    Z = np.random.normal(0, 1, size=(N, n_mc_sims))
    sim_asset_h_rets = (mu_daily * horizon_days) + (L_chol * np.sqrt(horizon_days)) @ Z

    # Retorno simulado del portafolio: R_port = w^T R_asset
    sim_port_h_rets = (w.T @ sim_asset_h_rets).flatten()
    losses_mc_pct = -sim_port_h_rets

    var_mc_pct = float(np.percentile(losses_mc_pct, confidence * 100))
    var_mc_usd = capital * var_mc_pct

    tail_mc = losses_mc_pct[losses_mc_pct >= var_mc_pct]
    cvar_mc_pct = float(np.mean(tail_mc)) if len(tail_mc) > 0 else var_mc_pct
    cvar_mc_usd = capital * cvar_mc_pct

    # -------------------------------------------------------------
    # Tabla Comparativa de los 3 Estimadores
    # -------------------------------------------------------------
    df_var_comparison = pd.DataFrame([
        {
            "Método": "1. Normal (Paramétrico)",
            "VaR 99% (%)": f"{var_param_pct:.2%}",
            "VaR 99% (USD)": f"${var_param_usd:,.2f}",
            "CVaR 99% (%)": f"{cvar_param_pct:.2%}",
            "CVaR 99% (USD)": f"${cvar_param_usd:,.2f}",
            "Supuesto Clave": "Distribución Normal multivariada elíptica.",
        },
        {
            "Método": "2. Histórico Empírico",
            "VaR 99% (%)": f"{var_hist_pct:.2%}",
            "VaR 99% (USD)": f"${var_hist_usd:,.2f}",
            "CVaR 99% (%)": f"{cvar_hist_pct:.2%}",
            "CVaR 99% (USD)": f"${cvar_hist_usd:,.2f}",
            "Supuesto Clave": "No asume distribución; captura colas empíricas reales.",
        },
        {
            "Método": f"3. Monte Carlo ({n_mc_sims:,} sims)",
            "VaR 99% (%)": f"{var_mc_pct:.2%}",
            "VaR 99% (USD)": f"${var_mc_usd:,.2f}",
            "CVaR 99% (%)": f"{cvar_mc_pct:.2%}",
            "CVaR 99% (USD)": f"${cvar_mc_usd:,.2f}",
            "Supuesto Clave": "Proyección conjunta multivariada con correlaciones cruzadas.",
        },
    ])

    # -------------------------------------------------------------
    # 4. Pruebas de Estrés Oficiales del PDF (Stress Testing)
    # -------------------------------------------------------------
    # Identificar el sector con mayor asignación
    sec_weights = {}
    for t_i, s_i, w_i in zip(tickers, sectors, weights):
        sec_weights[s_i] = sec_weights.get(s_i, 0.0) + float(w_i)
    top_sector = max(sec_weights, key=sec_weights.get)
    top_sector_weight = sec_weights[top_sector]

    # Estrés 1: Caída Uniforme de Mercado (-10%)
    stress1_asset_shocks = np.full(N, -0.10)
    stress1_loss_pct = float(np.sum(weights * (-stress1_asset_shocks)))
    stress1_loss_usd = capital * stress1_loss_pct

    # Estrés 2: Sector de Mayor Peso (-20%) y Resto (-5%)
    stress2_asset_shocks = np.array([-0.20 if s == top_sector else -0.05 for s in sectors])
    stress2_loss_pct = float(np.sum(weights * (-stress2_asset_shocks)))
    stress2_loss_usd = capital * stress2_loss_pct

    # Estrés 3: Volatilidad x 1.5 y Correlación rho = 0.80
    vols_daily = np.sqrt(np.diag(cov_daily))
    stressed_vols = vols_daily * 1.5
    # Construcción de matriz con rho = 0.80 fuera de la diagonal
    corr_stressed = np.full((N, N), 0.80)
    np.fill_diagonal(corr_stressed, 1.0)
    stressed_cov = np.outer(stressed_vols, stressed_vols) * corr_stressed

    stressed_port_sigma = np.sqrt(float(w.T @ stressed_cov @ w)) * np.sqrt(horizon_days)
    stress3_var_pct = float(z_alpha * stressed_port_sigma)
    stress3_var_usd = capital * stress3_var_pct

    df_stress = pd.DataFrame([
        {
            "Escenario de Estrés": "1. Caída Uniforme (-10%)",
            "Impacto (%)": f"-{stress1_loss_pct:.2%}",
            "Pérdida en USD": f"-${stress1_loss_usd:,.2f}",
            "Descripción": "Shock sistémico generalizado en todas las acciones de Wall Street.",
        },
        {
            "Escenario de Estrés": f"2. Crisis en {top_sector} (-20% / -5%)",
            "Impacto (%)": f"-{stress2_loss_pct:.2%}",
            "Pérdida en USD": f"-${stress2_loss_usd:,.2f}",
            "Descripción": f"Colapso en tu mayor sector ({top_sector}: {top_sector_weight:.1%}) y contagio defensivo en el resto.",
        },
        {
            "Escenario de Estrés": "3. Pánico de Volatilidad (σ × 1.5, ρ = 0.8)",
            "Impacto (%)": f"-{stress3_var_pct:.2%}",
            "Pérdida en USD": f"-${stress3_var_usd:,.2f}",
            "Descripción": "Las acciones pierden diversificación y caen al unísono con alta volatilidad.",
        },
    ])

    return {
        "var_comparison_df": df_var_comparison,
        "stress_df": df_stress,
        "top_sector": top_sector,
        "top_sector_weight": top_sector_weight,
        "losses_hist_pct": losses_hist_pct,
        "losses_mc_pct": losses_mc_pct,
        "var_param_pct": var_param_pct,
        "var_hist_pct": var_hist_pct,
        "var_mc_pct": var_mc_pct,
        "cvar_mc_pct": cvar_mc_pct,
        "var_param_usd": var_param_usd,
        "var_hist_usd": var_hist_usd,
        "var_mc_usd": var_mc_usd,
    }


def plot_var_distribution_hist(risk_results: Dict[str, any]) -> go.Figure:
    """
    Gráfico de densidad de pérdidas Monte Carlo con las líneas de corte de VaR y CVaR al 99%.
    """
    losses = risk_results["losses_mc_pct"] * 100.0  # En porcentaje
    var_cut = risk_results["var_mc_pct"] * 100.0
    cvar_cut = risk_results["cvar_mc_pct"] * 100.0

    fig = go.Figure()

    # Histograma de pérdidas
    fig.add_trace(go.Histogram(
        x=losses,
        nbinsx=80,
        name="Distribución de Pérdidas",
        marker_color="rgba(16, 185, 129, 0.4)",
        marker_line=dict(color="#10b981", width=1),
        opacity=0.75,
    ))

    # Línea vertical de VaR 99%
    fig.add_vline(
        x=var_cut,
        line_width=2.5,
        line_dash="dash",
        line_color="#f59e0b",
        annotation_text=f"VaR 99%: {var_cut:.2f}%",
        annotation_position="top left",
        annotation_font=dict(color="#f59e0b", size=11, family="Inter"),
    )

    # Línea vertical de CVaR 99%
    fig.add_vline(
        x=cvar_cut,
        line_width=2.5,
        line_dash="dot",
        line_color="#ef4444",
        annotation_text=f"CVaR 99%: {cvar_cut:.2f}%",
        annotation_position="top right",
        annotation_font=dict(color="#ef4444", size=11, family="Inter"),
    )

    fig.update_layout(
        title=dict(
            text="<b>Distribución de Pérdidas Monte Carlo a 10 Días</b>",
            font=dict(color="#f8fafc", size=13, family="Inter"),
        ),
        paper_bgcolor="#080b12",
        plot_bgcolor="#0c101b",
        xaxis=dict(
            title="Pérdida Potencial (%)",
            gridcolor="rgba(255,255,255,0.06)",
            color="#94a3b8",
            ticksuffix="%",
        ),
        yaxis=dict(
            title="Frecuencia de Escenarios",
            gridcolor="rgba(255,255,255,0.06)",
            color="#94a3b8",
        ),
        margin=dict(l=35, r=25, t=45, b=35),
        showlegend=False,
        height=320,
    )
    return fig
