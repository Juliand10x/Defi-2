"""
Motor de Detección de Comportamiento en Manada (Herding Behavior) y Test de Eficiencia de Mercado.
Implementación econométrica de Chang, Cheng & Khorana (CCK, 2000) y Christie & Huang (CH, 1995).
"""

from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from scipy import stats
import plotly.graph_objects as go


def run_herding_analysis(returns_df: pd.DataFrame) -> Dict[str, any]:
    """
    Ejecuta el test econométrico riguroso de Comportamiento en Manada (Herding Behavior)
    mediante la metodología de Chang, Cheng y Khorana (CCK, 2000).
    
    Ecuación de Chang, Cheng & Khorana (2000):
        CSAD_t = alpha + gamma_1 * |R_{m,t}| + gamma_2 * (R_{m,t})^2 + e_t
        
    Criterio de Eficiencia vs Comportamiento en Manada:
    - gamma_2 >= 0 (o no significativo): Comportamiento Racional / Eficiente (CAPM).
      A mayor volatilidad del mercado, las acciones divergen más por sus sensibilidades (betas) individuales.
    - gamma_2 < 0 y estadísticamente significativo (t < -1.96, p < 0.05):
      EVIDENCIA DE HERDING (COMPORTAMIENTO EN MANADA).
      Ante movimientos extremos, los inversionistas dejan de analizar los fundamentos y siguen a la masa,
      comprimiendo la dispersión transversal de los precios de forma no lineal.
    """
    clean_rets = returns_df.dropna()
    N = clean_rets.shape[1]
    T = clean_rets.shape[0]

    if N < 3 or T < 50:
        return {"success": False, "error": "Se requieren al menos 3 activos y 50 observaciones."}

    # 1. Retorno del mercado (equiponderado de la canasta)
    r_market = clean_rets.mean(axis=1)
    abs_rm = np.abs(r_market)
    rm_squared = r_market ** 2

    # 2. Desviación Absoluta Transversal (CSAD_t)
    # CSAD_t = (1 / N) * sum |R_{i,t} - R_{m,t}|
    csad = clean_rets.sub(r_market, axis=0).abs().mean(axis=1)

    # 3. Desviación Estándar Transversal (CSSD_t) - Christie & Huang (1995)
    cssd = clean_rets.sub(r_market, axis=0).std(axis=1, ddof=1)

    # -------------------------------------------------------------
    # REGRESIÓN 1: Modelo Cuadrático Clásico de CCK (2000)
    # CSAD_t = alpha + gamma_1 * |R_m| + gamma_2 * R_m^2 + e_t
    # -------------------------------------------------------------
    X_cck = np.column_stack([np.ones(T), abs_rm.values, rm_squared.values])
    y_cck = csad.values

    # MCO con matriz de covarianza robusta a heterocedasticidad (White 1980)
    beta_cck = np.linalg.lstsq(X_cck, y_cck, rcond=None)[0]
    residuals = y_cck - X_cck @ beta_cck

    # Matriz White Heteroskedasticity-Consistent (HAC básica)
    XtX_inv = np.linalg.inv(X_cck.T @ X_cck)
    omega = np.diag(residuals ** 2)
    var_white = XtX_inv @ (X_cck.T @ omega @ X_cck) @ XtX_inv
    se_white = np.sqrt(np.diag(var_white))

    dof = T - 3
    t_stats = beta_cck / se_white
    p_values = 2.0 * (1.0 - stats.t.cdf(np.abs(t_stats), df=dof))

    # Métricas de bondad de ajuste
    ss_tot = np.sum((y_cck - np.mean(y_cck)) ** 2)
    ss_res = np.sum(residuals ** 2)
    r_squared = float(1.0 - (ss_res / ss_tot)) if ss_tot > 0 else 0.0
    adj_r_squared = float(1.0 - (1.0 - r_squared) * (T - 1) / dof)

    alpha_val, gamma1_val, gamma2_val = beta_cck[0], beta_cck[1], beta_cck[2]
    gamma2_t = float(t_stats[2])
    gamma2_p = float(p_values[2])

    # -------------------------------------------------------------
    # REGRESIÓN 2: Asimetría Alcista vs Bajista (Bull vs Bear)
    # CSAD_t = alpha + gamma_1^D (1-D)|R_m| + gamma_1^U D |R_m| + gamma_2^D (1-D) R_m^2 + gamma_2^U D R_m^2 + e_t
    # -------------------------------------------------------------
    d_up = (r_market >= 0).astype(float).values
    d_down = (r_market < 0).astype(float).values

    X_asym = np.column_stack([
        np.ones(T),
        d_down * abs_rm.values,
        d_up * abs_rm.values,
        d_down * rm_squared.values,
        d_up * rm_squared.values,
    ])
    beta_asym = np.linalg.lstsq(X_asym, y_cck, rcond=None)[0]
    res_asym = y_cck - X_asym @ beta_asym
    XtX_inv_asym = np.linalg.inv(X_asym.T @ X_asym)
    omega_asym = np.diag(res_asym ** 2)
    var_asym = XtX_inv_asym @ (X_asym.T @ omega_asym @ X_asym) @ XtX_inv_asym
    se_asym = np.sqrt(np.diag(var_asym))
    t_asym = beta_asym / se_asym
    p_asym = 2.0 * (1.0 - stats.t.cdf(np.abs(t_asym), df=T - 5))

    gamma2_down = float(beta_asym[3])
    gamma2_down_p = float(p_asym[3])
    gamma2_up = float(beta_asym[4])
    gamma2_up_p = float(p_asym[4])

    # -------------------------------------------------------------
    # VEREDICTO CUALITATIVO DE EFICIENCIA Y HERDING
    # -------------------------------------------------------------
    is_herding = bool(gamma2_val < 0 and gamma2_p < 0.05)
    is_down_herding = bool(gamma2_down < 0 and gamma2_down_p < 0.05)
    is_up_herding = bool(gamma2_up < 0 and gamma2_up_p < 0.05)

    if is_herding:
        verdict = "🐑 Comportamiento en Manada (Herding) Detectado"
        verdict_badge = "Ineficiencia Conductual Confirmada"
        verdict_color = "#f59e0b"
        explanation = (
            "Los inversionistas están operando bajo contagio emocional e imitación en masa: ante movimientos bruscos de Wall Street, la gente deja de examinar los números de cada negocio y se abalanza a comprar o vender en estampida. Esto debilita la protección de la diversificación y amplifica el riesgo de caídas sincronizadas "
            f"(respaldo cuantitativo: dispersión transversal de retornos comprimida de forma no lineal con coeficiente γ₂ = {gamma2_val:.4f}, t = {gamma2_t:.2f}, significancia p = {gamma2_p:.4f} < 0.05)."
        )
    else:
        verdict = "🛡️ Mercado Racional y Eficiente (Sin Manada)"
        verdict_badge = "Racionalidad según Modelo CAPM"
        verdict_color = "#10b981"
        explanation = (
            "El mercado opera con calma y criterio financiero individual: los inversionistas premian a las empresas con sólidos balances y castigan a las débiles, permitiendo que la diversificación proteja eficazmente tu capital en cualquier escenario "
            f"(respaldo cuantitativo: comportamiento racional acorde al modelo CAPM con coeficiente de manada no significativo γ₂ = {gamma2_val:.4f}, p = {gamma2_p:.4f} >= 0.05)."
        )

    # Detalle de asimetría
    if is_down_herding and not is_up_herding:
        asym_insight = (
            "⚠️ Efecto Manada por Pánico: La estampida se desata cuando el mercado cae; los inversionistas liquidan posiciones por miedo sin mirar el valor real de los negocios "
            f"(respaldo cuantitativo: coeficiente bajista γ₂_down = {gamma2_down:.4f}, significancia p = {gamma2_down_p:.4f} < 0.05)."
        )
    elif is_up_herding and not is_down_herding:
        asym_insight = (
            "🚀 Efecto Manada por Euforia (FOMO): El contagio ocurre en las subidas; los participantes compran por miedo a quedarse fuera de la racha alcista "
            f"(respaldo cuantitativo: coeficiente alcista γ₂_up = {gamma2_up:.4f}, significancia p = {gamma2_up_p:.4f} < 0.05)."
        )
    elif is_down_herding and is_up_herding:
        asym_insight = (
            "⚡ Manada en Ambos Sentidos: El mercado sufre contagio colectivo tanto en euforias de compra como en pánicos de venta "
            f"(respaldo cuantitativo: coeficientes bajista γ₂_down = {gamma2_down:.4f} y alcista γ₂_up = {gamma2_up:.4f}, ambos con p < 0.05)."
        )
    else:
        asym_insight = (
            "✅ Conducta Equilibrada: No se observan sesgos emocionales desproporcionados ni en alzas ni en bajas "
            "(respaldo cuantitativo: p-valores en ambos regímenes superiores a 0.05)."
        )

    # Datos para graficar la curva teórica cuadrática
    rm_grid = np.linspace(0, float(abs_rm.max()) * 1.05, 120)
    csad_curve = alpha_val + gamma1_val * rm_grid + gamma2_val * (rm_grid ** 2)

    return {
        "success": True,
        "N_assets": N,
        "observations": T,
        "is_herding": is_herding,
        "verdict": verdict,
        "verdict_badge": verdict_badge,
        "verdict_color": verdict_color,
        "explanation": explanation,
        "asym_insight": asym_insight,
        "alpha": float(alpha_val),
        "gamma1": float(gamma1_val),
        "gamma2": float(gamma2_val),
        "gamma2_t": gamma2_t,
        "gamma2_p": gamma2_p,
        "r_squared": r_squared,
        "adj_r_squared": adj_r_squared,
        "gamma2_down": gamma2_down,
        "gamma2_down_p": gamma2_down_p,
        "gamma2_up": gamma2_up,
        "gamma2_up_p": gamma2_up_p,
        # Series de tiempo
        "dates": clean_rets.index,
        "csad": csad,
        "abs_rm": abs_rm,
        "r_market": r_market,
        "rm_grid": rm_grid,
        "csad_curve": csad_curve,
    }


def plot_herding_scatter(herding_res: Dict[str, any]) -> go.Figure:
    """
    Genera el gráfico interactivo de dispersión CSAD vs |R_m| con la parábola de CCK (2000).
    """
    abs_rm = herding_res["abs_rm"].values * 100.0  # en %
    csad = herding_res["csad"].values * 100.0      # en %
    r_m = herding_res["r_market"].values
    dates = herding_res["dates"]

    is_up = r_m >= 0

    fig = go.Figure()

    # Puntos en días alcistas (Verde Esmeralda)
    fig.add_trace(go.Scatter(
        x=abs_rm[is_up],
        y=csad[is_up],
        mode="markers",
        marker=dict(size=5, color="rgba(16, 185, 129, 0.45)", line=dict(width=0.5, color="#10b981")),
        name="Días Alcistas (Rm ≥ 0)",
        text=[f"Fecha: {d.strftime('%Y-%m-%d')}<br>|Rm|: {x:.2f}%<br>CSAD: {y:.2f}%" for d, x, y in zip(dates[is_up], abs_rm[is_up], csad[is_up])],
        hoverinfo="text",
    ))

    # Puntos en días bajistas (Oro / Ámbar)
    fig.add_trace(go.Scatter(
        x=abs_rm[~is_up],
        y=csad[~is_up],
        mode="markers",
        marker=dict(size=5, color="rgba(245, 158, 11, 0.45)", line=dict(width=0.5, color="#f59e0b")),
        name="Días Bajistas (Rm < 0)",
        text=[f"Fecha: {d.strftime('%Y-%m-%d')}<br>|Rm|: {x:.2f}%<br>CSAD: {y:.2f}%" for d, x, y in zip(dates[~is_up], abs_rm[~is_up], csad[~is_up])],
        hoverinfo="text",
    ))

    # Curva cuadrática teórica CCK
    curve_x = herding_res["rm_grid"] * 100.0
    curve_y = herding_res["csad_curve"] * 100.0
    curve_color = "#f59e0b" if herding_res["is_herding"] else "#10b981"
    curve_name = "Curva CCK (Compresión Manada)" if herding_res["is_herding"] else "Curva CCK (Dispersión Racional)"

    fig.add_trace(go.Scatter(
        x=curve_x,
        y=curve_y,
        mode="lines",
        line=dict(color=curve_color, width=3.2),
        name=curve_name,
    ))

    fig.update_layout(
        title=dict(
            text="<b>Dispersión Transversal (Test CCK 2000)</b>",
            font=dict(size=12, color="#f8fafc", family="Inter"),
            x=0.02,
            y=0.98,
            xanchor="left",
            yanchor="top",
        ),
        template="plotly_dark",
        paper_bgcolor="#0d131f",
        plot_bgcolor="#111726",
        xaxis=dict(
            title=dict(text="Magnitud del Retorno del Mercado |R_m| (%)", font=dict(size=11, color="#94a3b8")),
            gridcolor="rgba(255, 255, 255, 0.06)",
            color="#94a3b8",
            ticksuffix="%",
        ),
        yaxis=dict(
            title=dict(text="Dispersión Absoluta CSAD (%)", font=dict(size=11, color="#94a3b8")),
            gridcolor="rgba(255, 255, 255, 0.06)",
            color="#94a3b8",
            ticksuffix="%",
        ),
        margin=dict(l=35, r=15, t=40, b=65),
        height=380,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="center",
            x=0.5,
            font=dict(size=10, color="#94a3b8"),
        ),
    )
    return fig


def plot_csad_timeline(herding_res: Dict[str, any]) -> go.Figure:
    """
    Genera la serie temporal de CSAD a lo largo de los 3 años.
    """
    dates = herding_res["dates"]
    csad = herding_res["csad"] * 100.0
    abs_rm = herding_res["abs_rm"] * 100.0

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=csad,
        mode="lines",
        line=dict(color="#10b981", width=1.5),
        name="Dispersión CSAD (%)",
    ))

    fig.add_trace(go.Scatter(
        x=dates,
        y=abs_rm,
        mode="lines",
        line=dict(color="rgba(245, 158, 11, 0.5)", width=1),
        name="Volatilidad Mercado |Rm| (%)",
    ))

    fig.update_layout(
        title=dict(
            text="<b>Evolución Temporal de la Dispersión Transversal (3 Años)</b>",
            font=dict(size=13, color="#f8fafc", family="Inter"),
            x=0.02,
            y=0.98,
            xanchor="left",
            yanchor="top",
        ),
        template="plotly_dark",
        paper_bgcolor="#0d131f",
        plot_bgcolor="#111726",
        xaxis=dict(
            title=dict(text="Fecha", font=dict(size=11, color="#94a3b8")),
            gridcolor="rgba(255, 255, 255, 0.06)",
            color="#94a3b8",
        ),
        yaxis=dict(
            title=dict(text="Porcentaje (%)", font=dict(size=11, color="#94a3b8")),
            gridcolor="rgba(255, 255, 255, 0.06)",
            color="#94a3b8",
            ticksuffix="%",
        ),
        margin=dict(l=45, r=25, t=55, b=65),
        height=320,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="center",
            x=0.5,
            font=dict(size=10, color="#94a3b8"),
        ),
    )
    return fig

