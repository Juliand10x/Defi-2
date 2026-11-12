"""
Motor de Medición de Riesgo Integral y Pruebas de Estrés Financiero.
Implementación de los 3 Estimadores de VaR al 99% (Horizonte h=10 días) + Expected Shortfall (CVaR):
1. VaR Histórico (Ventanas no solapadas / solapadas con cuantiles de pérdida empírica)
2. VaR Paramétrico Normal (B * Phi^-1(alpha) * sqrt(h * w^T Sigma w))
3. VaR Monte Carlo Multivariado (20.000 trayectorias conjuntas con correlación Cholesky)
+ 3 Escenarios Oficiales de Stress Testing:
- Estrés 1: Caída Uniforme de Mercado (-10%)
- Estrés 2: Desplome Sectorial Asimétrico (-20% sector principal, -5% resto)
- Estrés 3: Choque de Volatilidad (Volatilidad x 1.5 y Correlación rho = 0.80)
"""

from typing import Dict, List, Tuple, Any, Optional
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
    junto con los 3 escenarios oficiales de estrés financiero.
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
    var_param_daily_sigma = np.sqrt(float(np.asarray(w.T @ cov_daily @ w).item()))
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
        comp_r = np.exp(np.sum(block)) - 1.0
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
    Z = np.random.normal(0, 1, size=(n_mc_sims, horizon_days, N))
    daily_log_paths = mu_daily.reshape(1, 1, N) + Z @ L_chol.T
    sim_asset_h_rets = np.exp(daily_log_paths.sum(axis=1)) - 1.0
    sim_asset_h_rets = sim_asset_h_rets.T

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
    conf_pct_str = f"{int(round(confidence * 100))}%"
    df_var_comparison = pd.DataFrame([
        {
            "Método": "1. Normal (Paramétrico)",
            f"VaR {conf_pct_str} (%)": f"{var_param_pct:.2%}",
            f"VaR {conf_pct_str} (USD)": f"${var_param_usd:,.2f}",
            f"CVaR {conf_pct_str} (%)": f"{cvar_param_pct:.2%}",
            f"CVaR {conf_pct_str} (USD)": f"${cvar_param_usd:,.2f}",
            "Supuesto Clave": "Distribución Normal multivariada elíptica.",
        },
        {
            "Método": "2. Histórico Empírico",
            f"VaR {conf_pct_str} (%)": f"{var_hist_pct:.2%}",
            f"VaR {conf_pct_str} (USD)": f"${var_hist_usd:,.2f}",
            f"CVaR {conf_pct_str} (%)": f"{cvar_hist_pct:.2%}",
            f"CVaR {conf_pct_str} (USD)": f"${cvar_hist_usd:,.2f}",
            "Supuesto Clave": "No asume distribución; captura colas empíricas reales.",
        },
        {
            "Método": f"3. Monte Carlo ({n_mc_sims:,} sims)",
            f"VaR {conf_pct_str} (%)": f"{var_mc_pct:.2%}",
            f"VaR {conf_pct_str} (USD)": f"${var_mc_usd:,.2f}",
            f"CVaR {conf_pct_str} (%)": f"{cvar_mc_pct:.2%}",
            f"CVaR {conf_pct_str} (USD)": f"${cvar_mc_usd:,.2f}",
            "Supuesto Clave": "Proyección conjunta multivariada con correlaciones cruzadas.",
        },
    ])

    # -------------------------------------------------------------
    # 4. Pruebas de Estrés Financiero (Stress Testing)
    # -------------------------------------------------------------
    # Identificar el sector con mayor asignación
    sec_weights = {}
    for t_i, s_i, w_i in zip(tickers, sectors, weights):
        sec_weights[s_i] = sec_weights.get(s_i, 0.0) + float(w_i)
    top_sector = max(sec_weights, key=sec_weights.get)
    top_sector_weight = sec_weights[top_sector]

    w_flat = np.asarray(weights).flatten()

    # Estrés 1: Caída Uniforme de Mercado (-10%)
    stress1_asset_shocks = np.full(N, -0.10)
    stress1_loss_pct = float(np.sum(w_flat * (-stress1_asset_shocks)))
    stress1_loss_usd = capital * stress1_loss_pct

    # Estrés 2: Sector de Mayor Peso (-20%) y Resto (-5%)
    stress2_asset_shocks = np.array([-0.20 if s == top_sector else -0.05 for s in sectors])
    stress2_loss_pct = float(np.sum(w_flat * (-stress2_asset_shocks)))
    stress2_loss_usd = capital * stress2_loss_pct

    # Estrés 3: Volatilidad x 1.5 y Correlación rho = 0.80
    vols_daily = np.sqrt(np.diag(cov_daily))
    stressed_vols = vols_daily * 1.5
    # Construcción de matriz con rho = 0.80 fuera de la diagonal
    corr_stressed = np.full((N, N), 0.80)
    np.fill_diagonal(corr_stressed, 1.0)
    stressed_cov = np.outer(stressed_vols, stressed_vols) * corr_stressed

    stressed_port_sigma = np.sqrt(float(np.asarray(w.T @ stressed_cov @ w).item())) * np.sqrt(horizon_days)
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
        "cvar_mc_usd": cvar_mc_usd,
        "stress1_loss_pct": stress1_loss_pct,
        "stress1_loss_usd": stress1_loss_usd,
        "stress2_loss_pct": stress2_loss_pct,
        "stress2_loss_usd": stress2_loss_usd,
        "stress3_var_pct": stress3_var_pct,
        "stress3_var_usd": stress3_var_usd,
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
            x=0.02,
            y=0.98,
            xanchor="left",
            yanchor="top",
        ),
        paper_bgcolor="#080b12",
        plot_bgcolor="#0c101b",
        xaxis=dict(
            title=dict(text="Pérdida Potencial (%)", font=dict(size=11, color="#94a3b8")),
            gridcolor="rgba(255,255,255,0.06)",
            color="#94a3b8",
            ticksuffix="%",
        ),
        yaxis=dict(
            title=dict(text="Frecuencia de Escenarios", font=dict(size=11, color="#94a3b8")),
            gridcolor="rgba(255,255,255,0.06)",
            color="#94a3b8",
        ),
        margin=dict(l=45, r=25, t=55, b=45),
        showlegend=False,
        height=320,
    )
    return fig



def run_out_of_sample_portfolio_audit(
    prices_df: pd.DataFrame,
    returns_df: pd.DataFrame,
    weights: np.ndarray,
    tickers: List[str],
    capital: float = 100000.0,
    test_sessions: int = 252,
    window_calib: int = 252,
    cost_bps: float = 10.0,
    confidence: float = 0.99,
) -> Dict[str, Any]:
    """
    Auditoría fuera de muestra de la cartera (Paso 10 del Taller):
    - Curva patrimonial en las 252 sesiones de evaluación.
    - Máximo Drawdown (MDD) y costos de transacción.
    - Excepciones del VaR diario al 99% mediante ventana móvil de 252 sesiones anteriores.
    - Test de Cobertura Incondicional de Kupiec (POF).
    """
    sub_prices = prices_df[tickers].dropna()
    sub_rets = returns_df[tickers].dropna()
    total_len = len(sub_rets)

    if total_len < (window_calib + test_sessions):
        test_sessions = max(50, total_len - window_calib)

    w = np.array(weights).reshape(-1, 1)
    w_flat = w.flatten()

    eval_start_idx = total_len - test_sessions
    eval_dates = sub_rets.index[eval_start_idx:]

    # Costo inicial de transacción
    trans_cost_init = capital * (cost_bps / 10000.0)
    current_wealth = capital - trans_cost_init

    wealth_series = []
    drawdown_series = []
    daily_losses = []
    daily_vars_usd = []
    exception_flags = []
    peak_wealth = current_wealth

    z_alpha = stats.norm.ppf(confidence)

    for i, idx in enumerate(range(eval_start_idx, total_len)):
        t_date = sub_rets.index[idx]
        
        # 1. Ventana móvil de calibración previa de 252 sesiones para el VaR diario
        train_slice = sub_rets.iloc[idx - window_calib : idx]
        cov_daily_train = train_slice.cov().values
        port_sigma_daily = np.sqrt(float(np.dot(w_flat.T, np.dot(cov_daily_train, w_flat))))
        var_1d_usd = current_wealth * z_alpha * port_sigma_daily
        daily_vars_usd.append(var_1d_usd)

        # 2. Rendimiento discreto observado del portafolio en t
        day_rets = sub_rets.iloc[idx].values
        # Retorno discreto aproximado o exacto exp(r) - 1
        day_disc_rets = np.exp(day_rets) - 1.0
        port_day_return = float(np.sum(w_flat * day_disc_rets))

        # 3. Evolución del patrimonio
        prev_wealth = current_wealth
        current_wealth = prev_wealth * (1.0 + port_day_return)
        wealth_series.append(current_wealth)

        # 4. Pérdida en USD y chequeo de excepción
        loss_usd = prev_wealth - current_wealth
        daily_losses.append(loss_usd)
        is_exception = loss_usd > var_1d_usd
        exception_flags.append(is_exception)

        # 5. Drawdown acumulado
        if current_wealth > peak_wealth:
            peak_wealth = current_wealth
        dd = (peak_wealth - current_wealth) / peak_wealth
        drawdown_series.append(dd)

    # Métricas consolidadas
    wealth_arr = np.array(wealth_series)
    dd_arr = np.array(drawdown_series)
    exc_arr = np.array(exception_flags)

    final_wealth = float(wealth_arr[-1])
    total_net_return = float((final_wealth - capital) / capital)
    max_drawdown = float(np.max(dd_arr))
    num_exceptions = int(np.sum(exc_arr))
    total_eval_days = len(wealth_arr)
    exception_rate = float(num_exceptions / total_eval_days)

    expected_exceptions = total_eval_days * (1.0 - confidence)

    # Test de Kupiec (Proportion of Failures - POF)
    p_0 = 1.0 - confidence
    k = num_exceptions
    n = total_eval_days

    if k == 0:
        lr_pof = -2.0 * np.log((1.0 - p_0) ** n)
    elif k == n:
        lr_pof = -2.0 * np.log(p_0 ** n)
    else:
        num = ((1.0 - p_0) ** (n - k)) * (p_0 ** k)
        den = ((1.0 - k / n) ** (n - k)) * ((k / n) ** k)
        lr_pof = -2.0 * np.log(max(num / den, 1e-12))

    p_value_kupiec = float(1.0 - stats.chi2.cdf(lr_pof, df=1))
    kupiec_passed = bool(p_value_kupiec > 0.05)

    df_oos_summary = pd.DataFrame([
        {"Métrica": "Capital Inicial", "Valor": f"${capital:,.2f}"},
        {"Métrica": "Costos de Transacción (10 bps)", "Valor": f"${trans_cost_init:,.2f}"},
        {"Métrica": "Patrimonio Final Fuera de Muestra", "Valor": f"${final_wealth:,.2f}"},
        {"Métrica": "Rentabilidad Neta Acumulada", "Valor": f"{total_net_return:.2%}"},
        {"Métrica": "Máximo Drawdown (MDD)", "Valor": f"{max_drawdown:.2%}"},
        {"Métrica": "Sesiones Evaluadas", "Valor": str(total_eval_days)},
        {"Métrica": "Excepciones de VaR Diario Observadas", "Valor": f"{num_exceptions} (Esperadas: ~{expected_exceptions:.1f})"},
        {"Métrica": "Tasa de Falla Empírica", "Valor": f"{exception_rate:.2%} (Teórica: {(1-confidence):.2%})"},
        {"Métrica": "Kupiec LR Estadístico", "Valor": f"{lr_pof:.3f} (p-val: {p_value_kupiec:.4f})"},
        {"Métrica": "Veredicto Modelo VaR", "Valor": "✅ Válido (No se rechaza al 95%)" if kupiec_passed else "⚠️ Alerta de Calibración"},
    ])

    return {
        "dates": eval_dates,
        "wealth_series": wealth_series,
        "drawdown_series": drawdown_series,
        "daily_losses": daily_losses,
        "daily_vars_usd": daily_vars_usd,
        "exception_flags": exception_flags,
        "final_wealth": final_wealth,
        "total_net_return": total_net_return,
        "max_drawdown": max_drawdown,
        "num_exceptions": num_exceptions,
        "expected_exceptions": expected_exceptions,
        "exception_rate": exception_rate,
        "lr_pof": lr_pof,
        "p_value_kupiec": p_value_kupiec,
        "kupiec_passed": kupiec_passed,
        "summary_table": df_oos_summary,
    }


def plot_out_of_sample_audit(oos_res: Dict[str, Any]) -> go.Figure:
    """Genera el gráfico interactivo de la auditoría fuera de muestra (curva de patrimonio y drawdown)."""
    dates = oos_res["dates"]
    wealth = oos_res["wealth_series"]
    dd_pct = np.array(oos_res["drawdown_series"]) * 100.0

    from plotly.subplots import make_subplots
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        row_heights=[0.65, 0.35],
        subplot_titles=("<b>Curva Patrimonial Fuera de Muestra (252 Sesiones)</b>", "<b>Evolución del Drawdown (%)</b>")
    )

    # 1. Patrimonio
    fig.add_trace(go.Scatter(
        x=dates, y=wealth, mode="lines",
        name="Patrimonio de Cartera", line=dict(color="#10b981", width=2.2),
        hovertemplate="<b>Patrimonio</b><br>Fecha: %{x|%Y-%m-%d}<br>Valor: $%{y:,.2f} USD<extra></extra>"
    ), row=1, col=1)

    # 2. Drawdown
    fig.add_trace(go.Scatter(
        x=dates, y=-dd_pct, mode="lines",
        fill="tozeroy", fillcolor="rgba(239, 68, 68, 0.25)",
        name="Drawdown (%)", line=dict(color="#ef4444", width=1.5),
        hovertemplate="<b>Drawdown</b><br>Fecha: %{x|%Y-%m-%d}<br>Caída: %{y:.2f}%<extra></extra>"
    ), row=2, col=1)

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#080b12", plot_bgcolor="#0c101b",
        margin=dict(l=45, r=25, t=55, b=45), height=380,
        showlegend=False
    )
    fig.update_yaxes(title_text="Patrimonio (USD)", tickprefix="$", row=1, col=1, gridcolor="rgba(255,255,255,0.06)", color="#94a3b8")
    fig.update_yaxes(title_text="Caída (%)", ticksuffix="%", row=2, col=1, gridcolor="rgba(255,255,255,0.06)", color="#94a3b8")
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.06)", color="#94a3b8")
    return fig
