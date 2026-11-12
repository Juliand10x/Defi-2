"""
Generación de Gráficos Financieros Interactivos con Plotly (Paleta Obsidiana & Esmeralda).
Universidad Externado de Colombia · DEFI 2
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats


def plot_stochastic_fan(sim_result, title_suffix=""):
    """
    Gráfico de abanico estocástico:
    - 30-50 trayectorias individuales discretas (40 mostradas).
    - Mediana P50, bandas 10%-90% y 25%-75%.
    - Comparación de media simulada vs media teórica S0*exp(a*T).
    - Subplot derecho: Distribución terminal S_T (histograma).
    """
    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.75, 0.25],
        shared_yaxes=True,
        horizontal_spacing=0.03,
        subplot_titles=(
            f"<b>{sim_result.model_name}</b> {title_suffix}",
            "<b>Distribución Terminal (S_T)</b>"
        )
    )

    x_axis = sim_result.time_grid
    paths = sim_result.paths
    n_sample = min(40, paths.shape[0])

    # 1. 40 trayectorias individuales discretas (Paso 4)
    for i in range(n_sample):
        fig.add_trace(go.Scatter(
            x=x_axis,
            y=paths[i, :],
            mode="lines",
            line=dict(color="rgba(148, 163, 184, 0.12)", width=1),
            showlegend=False,
            hoverinfo="skip"
        ), row=1, col=1)

    # 2. Banda 10% - 90%
    fig.add_trace(go.Scatter(
        x=x_axis, y=sim_result.percentiles[90],
        mode="lines", line=dict(width=0), showlegend=False, hoverinfo="skip"
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=x_axis, y=sim_result.percentiles[10],
        mode="lines", line=dict(width=0), fill="tonexty",
        fillcolor="rgba(16, 185, 129, 0.10)", name="Banda 10% - 90%"
    ), row=1, col=1)

    # 3. Banda 25% - 75%
    fig.add_trace(go.Scatter(
        x=x_axis, y=sim_result.percentiles[75],
        mode="lines", line=dict(width=0), showlegend=False, hoverinfo="skip"
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=x_axis, y=sim_result.percentiles[25],
        mode="lines", line=dict(width=0), fill="tonexty",
        fillcolor="rgba(16, 185, 129, 0.22)", name="Banda 25% - 75%"
    ), row=1, col=1)

    # 4. Mediana P50
    fig.add_trace(go.Scatter(
        x=x_axis, y=sim_result.percentiles[50],
        mode="lines", line=dict(color="#10b981", width=2.8), name="Mediana P50",
        hovertemplate="<b>Mediana P50</b><br>Día: %{x}<br>Precio: $%{y:.2f}<extra></extra>"
    ), row=1, col=1)

    # 5. Media Simulada y Teórica
    fig.add_trace(go.Scatter(
        x=[0, x_axis[-1]], y=[sim_result.spot, sim_result.simulated_mean],
        mode="lines+markers", line=dict(color="#f59e0b", width=2, dash="dash"),
        name=f"Media Sim (${sim_result.simulated_mean:.2f})",
        hovertemplate="<b>Media Monte Carlo</b><br>Precio: $%{y:.2f}<extra></extra>"
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=[0, x_axis[-1]], y=[sim_result.spot, sim_result.theoretical_mean],
        mode="lines+markers", line=dict(color="#38bdf8", width=1.8, dash="dot"),
        name=f"Teórica S0*e^aT (${sim_result.theoretical_mean:.2f})",
        hovertemplate="<b>Media Teórica S0·e^(aT)</b><br>Precio: $%{y:.2f}<extra></extra>"
    ), row=1, col=1)

    # 6. Histograma Terminal en Subplot 2
    terminal_prices = paths[:, -1]
    fig.add_trace(go.Histogram(
        y=terminal_prices,
        nbinsy=40,
        orientation="h",
        marker_color="rgba(16, 185, 129, 0.35)",
        marker_line=dict(color="#10b981", width=1),
        showlegend=False,
    ), row=1, col=2)

    # Línea horizontal del spot actual y media
    fig.add_hline(y=sim_result.spot, line_dash="dash", line_color="#94a3b8", line_width=1.2, row=1, col=2)
    fig.add_hline(y=sim_result.simulated_mean, line_dash="dash", line_color="#f59e0b", line_width=1.5, row=1, col=2)

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0d131f",
        plot_bgcolor="#111726",
        margin=dict(l=45, r=25, t=55, b=65),
        height=400,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="center",
            x=0.5,
            font=dict(size=10, color="#94a3b8"),
        ),
    )
    fig.update_xaxes(title_text="Días proyectados", row=1, col=1, gridcolor="rgba(255,255,255,0.06)", color="#94a3b8")
    fig.update_xaxes(title_text="Frecuencia", row=1, col=2, gridcolor="rgba(255,255,255,0.06)", color="#94a3b8")
    fig.update_yaxes(title_text="Precio (USD)", tickprefix="$", row=1, col=1, gridcolor="rgba(255,255,255,0.06)", color="#94a3b8")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.06)", color="#94a3b8", row=1, col=2)

    return fig


def plot_normalized_prices_chart(normalized_df: pd.DataFrame) -> go.Figure:
    """Gráfico de evolución temporal de precios normalizados base 100 (Paso 3)."""
    fig = go.Figure()
    palette = [
        "#10b981", "#3b82f6", "#f59e0b", "#ec4899", "#8b5cf6",
        "#06b6d4", "#14b8a6", "#f97316", "#a855f7", "#6366f1"
    ]
    for i, col in enumerate(normalized_df.columns):
        fig.add_trace(go.Scatter(
            x=normalized_df.index,
            y=normalized_df[col],
            mode="lines",
            name=col,
            line=dict(color=palette[i % len(palette)], width=1.6),
        ))
    fig.update_layout(
        title=dict(
            text="<b>Evolución de Precios Normalizados (Base 100)</b>",
            font=dict(size=13, color="#f8fafc", family="Inter"),
            x=0.02, y=0.98,
        ),
        template="plotly_dark",
        paper_bgcolor="#080b12",
        plot_bgcolor="#0c101b",
        xaxis=dict(title=dict(text="Fecha", font=dict(size=11, color="#94a3b8")), gridcolor="rgba(255, 255, 255, 0.06)", color="#94a3b8"),
        yaxis=dict(title=dict(text="Rendimiento Relativo (Base 100)", font=dict(size=11, color="#94a3b8")), gridcolor="rgba(255, 255, 255, 0.06)", color="#94a3b8"),
        margin=dict(l=45, r=25, t=55, b=65),
        height=360,
        legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5, font=dict(size=10, color="#94a3b8")),
    )
    return fig


def plot_correlation_heatmap(corr_df: pd.DataFrame) -> go.Figure:
    """Mapa de calor interactivo de la matriz de correlación muestral (Paso 3)."""
    z_vals = np.round(corr_df.values, 2)
    fig = go.Figure(data=go.Heatmap(
        z=z_vals,
        x=corr_df.columns,
        y=corr_df.index,
        colorscale=[
            [0.0, "#ef4444"],
            [0.5, "#0c101b"],
            [1.0, "#10b981"]
        ],
        zmin=-1.0, zmax=1.0,
        text=z_vals,
        texttemplate="%{text}",
        textfont=dict(size=10, color="#f8fafc", family="Inter"),
        colorbar=dict(title=dict(text="Correlación", font=dict(color="#94a3b8", size=10)), tickcolor="#94a3b8"),
    ))
    fig.update_layout(
        title=dict(
            text="<b>Matriz de Correlación Muestral entre Activos (Divisor n - 1)</b>",
            font=dict(size=13, color="#f8fafc", family="Inter"),
            x=0.02, y=0.98,
        ),
        template="plotly_dark",
        paper_bgcolor="#080b12",
        plot_bgcolor="#0c101b",
        xaxis=dict(color="#94a3b8", tickangle=-45),
        yaxis=dict(color="#94a3b8", autorange="reversed"),
        margin=dict(l=55, r=35, t=55, b=55),
        height=380,
    )
    return fig


def plot_returns_histogram(returns_series: pd.Series, ticker: str) -> go.Figure:
    """Histograma de log-retornos con ajuste de campana normal teórica y métricas de cola (Paso 3)."""
    clean_r = returns_series.dropna()
    mu = float(clean_r.mean())
    sigma = float(clean_r.std(ddof=1))
    jb_stat, jb_pval = stats.jarque_bera(clean_r)

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=clean_r,
        nbinsx=60,
        histnorm="probability density",
        name="Retornos Empíricos",
        marker_color="rgba(16, 185, 129, 0.4)",
        marker_line=dict(color="#10b981", width=1),
    ))

    # Campana Gaussiana Teórica
    x_grid = np.linspace(clean_r.min(), clean_r.max(), 200)
    y_normal = stats.norm.pdf(x_grid, loc=mu, scale=sigma)
    fig.add_trace(go.Scatter(
        x=x_grid, y=y_normal,
        mode="lines",
        name=f"Normal Teórica (JB p={jb_pval:.4f})",
        line=dict(color="#f59e0b", width=2, dash="dash"),
    ))

    fig.update_layout(
        title=dict(
            text=f"<b>Distribución de Retornos Diarios · {ticker}</b>",
            font=dict(size=13, color="#f8fafc", family="Inter"),
            x=0.02, y=0.98,
        ),
        template="plotly_dark",
        paper_bgcolor="#080b12",
        plot_bgcolor="#0c101b",
        xaxis=dict(title=dict(text="Log-retorno Diario", font=dict(size=11, color="#94a3b8")), gridcolor="rgba(255, 255, 255, 0.06)", color="#94a3b8"),
        yaxis=dict(title=dict(text="Densidad", font=dict(size=11, color="#94a3b8")), gridcolor="rgba(255, 255, 255, 0.06)", color="#94a3b8"),
        margin=dict(l=45, r=25, t=55, b=55),
        height=320,
        legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5, font=dict(size=10, color="#94a3b8")),
    )
    return fig


def plot_model_comparison_bars(models_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=models_df["Modelo"],
        y=models_df["AIC"],
        name="AIC (Menor = mejor)",
        marker_color="rgba(148, 163, 184, 0.65)"
    ))
    fig.add_trace(go.Bar(
        x=models_df["Modelo"],
        y=models_df["BIC"],
        name="BIC (Penaliza sobreajuste)",
        marker_color="#f59e0b"
    ))
    fig.update_layout(
        title=dict(
            text="<b>Criterios Estadísticos de Selección (AIC vs BIC)</b>",
            font=dict(size=13, color="#f8fafc", family="Inter"),
            x=0.02, y=0.98,
        ),
        barmode="group",
        template="plotly_dark",
        paper_bgcolor="#0d131f",
        plot_bgcolor="#111726",
        xaxis=dict(gridcolor="rgba(255, 255, 255, 0.06)", color="#94a3b8"),
        yaxis=dict(title=dict(text="Puntaje del Criterio", font=dict(size=11, color="#94a3b8")), gridcolor="rgba(255, 255, 255, 0.06)", color="#94a3b8"),
        margin=dict(l=45, r=25, t=55, b=65),
        height=330,
        legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5, font=dict(size=10, color="#94a3b8")),
    )
    return fig


def plot_portfolio_allocation_chart(alloc_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=alloc_df["Ticker"],
        y=[float(str(p).replace('%', '')) for p in alloc_df["Peso Equiponderado (1/N)"]],
        name="Pesos Iguales (1/N)",
        marker_color="rgba(148, 163, 184, 0.35)",
    ))
    
    fig.add_trace(go.Bar(
        x=alloc_df["Ticker"],
        y=[float(str(p).replace('%', '')) for p in alloc_df["Peso Inverso VaR"]],
        name="Inverso al VaR",
        marker_color="#f59e0b",
    ))
    
    fig.add_trace(go.Bar(
        x=alloc_df["Ticker"],
        y=[float(w) * 100.0 for w in alloc_df["Peso Teórico Óptimo"]],
        name="Mínimo VaR Restringido (SLSQP)",
        marker_color="#10b981",
    ))
    
    fig.update_layout(
        title=dict(
            text="<b>Ponderaciones por Modelo de Asignación (%)</b>",
            font=dict(size=13, color="#f8fafc", family="Inter"),
            x=0.02, y=0.98,
        ),
        barmode="group",
        template="plotly_dark",
        paper_bgcolor="#0d131f",
        plot_bgcolor="#111726",
        xaxis=dict(title=dict(text="Activo", font=dict(size=11, color="#94a3b8")), gridcolor="rgba(255, 255, 255, 0.06)", color="#94a3b8"),
        yaxis=dict(title=dict(text="Peso en Cartera (%)", font=dict(size=11, color="#94a3b8")), gridcolor="rgba(255, 255, 255, 0.06)", color="#94a3b8", ticksuffix="%"),
        margin=dict(l=45, r=25, t=55, b=65),
        height=360,
        legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5, font=dict(size=10, color="#94a3b8")),
    )
    return fig


def plot_option_payoff_and_profit(
    spot: float,
    strike: float,
    ask: float,
    rate: float,
    maturity: float,
    option_type: str = "Call",
    terminal_cost: float = 0.0,
) -> go.Figure:
    """
    Gráfico pedagógico interactivo de Payoff vs Beneficio Neto.
    Explica visualmente por qué ejercer una opción no equivale a ganar dinero:
    - Payoff Bruto: H(S_T) = max(S_T - K, 0)
    - Beneficio Neto: Pi_T = H(S_T) - A * exp(r * T) - c_T
    - Punto de Equilibrio (Break-even): Strike + Prima Capitalizada
    """
    cost_fv = ask * np.exp(rate * maturity) if (np.isfinite(ask) and ask > 0) else 0.0
    total_cost = cost_fv + terminal_cost

    s_min = max(1.0, spot * 0.6)
    s_max = spot * 1.4
    s_grid = np.linspace(s_min, s_max, 250)

    if option_type == "Call":
        payoff = np.maximum(s_grid - strike, 0.0)
        profit = payoff - total_cost
        breakeven = strike + total_cost
    else:
        payoff = np.maximum(strike - s_grid, 0.0)
        profit = payoff - total_cost
        breakeven = max(0.0, strike - total_cost)

    fig = go.Figure()

    # Zona de Pérdida / Ganancia Neta
    fig.add_trace(go.Scatter(
        x=s_grid, y=profit,
        mode="lines",
        name="Beneficio Neto (Π_T en USD)",
        line=dict(color="#10b981", width=2.8),
        hovertemplate="<b>Beneficio Neto (Π_T)</b><br>Precio S_T: $%{x:.2f}<br>Resultado: $%{y:+.2f} USD<extra></extra>",
    ))

    # Payoff Bruto
    fig.add_trace(go.Scatter(
        x=s_grid, y=payoff,
        mode="lines",
        name="Payoff Bruto H(S_T)",
        line=dict(color="rgba(148, 163, 184, 0.45)", width=1.5, dash="dash"),
        hovertemplate="<b>Payoff Bruto H(S_T)</b><br>Precio S_T: $%{x:.2f}<br>Valor al Vencer: $%{y:.2f} USD<extra></extra>",
    ))

    # Línea horizontal de cero beneficio
    fig.add_hline(y=0.0, line_color="rgba(255,255,255,0.2)", line_width=1)

    # Línea vertical del Strike K
    fig.add_vline(
        x=strike, line_dash="dot", line_color="#f59e0b", line_width=1.5,
        annotation_text=f"Strike K: ${strike:.2f}",
        annotation_position="top left",
        annotation_font=dict(color="#f59e0b", size=10)
    )

    # Línea vertical del Spot Actual S0
    fig.add_vline(
        x=spot, line_dash="dash", line_color="#38bdf8", line_width=1.5,
        annotation_text=f"Spot S0: ${spot:.2f}",
        annotation_position="bottom right",
        annotation_font=dict(color="#38bdf8", size=10)
    )

    # Línea vertical del Break-Even
    if total_cost > 0:
        fig.add_vline(
            x=breakeven, line_dash="dashdot", line_color="#a855f7", line_width=1.8,
            annotation_text=f"Equilibrio: ${breakeven:.2f}",
            annotation_position="top right",
            annotation_font=dict(color="#a855f7", size=10)
        )

    fig.update_layout(
        title=dict(
            text=f"<b>Curva de Payoff y Utilidad Neta al Vencimiento ({option_type})</b>",
            font=dict(size=13, color="#f8fafc", family="Inter"),
            x=0.02, y=0.98
        ),
        template="plotly_dark",
        paper_bgcolor="#080b12",
        plot_bgcolor="#0c101b",
        xaxis=dict(title=dict(text="Precio de la Acción al Vencimiento S_T (USD)", font=dict(size=11, color="#94a3b8")), gridcolor="rgba(255,255,255,0.06)", color="#94a3b8", tickprefix="$"),
        yaxis=dict(title=dict(text="Utilidad / Pérdida por Acción (USD)", font=dict(size=11, color="#94a3b8")), gridcolor="rgba(255,255,255,0.06)", color="#94a3b8", tickprefix="$"),
        margin=dict(l=45, r=25, t=55, b=55),
        height=340,
        legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5, font=dict(size=10, color="#94a3b8")),
    )
    return fig


def plot_sector_allocation_donut(sec_summary: pd.DataFrame) -> go.Figure:
    """
    Gráfico interactivo de Dona con la diversificación sectorial del portafolio (Paso 11).
    Destaca el límite regulatorio del 35% de concentración máxima.
    """
    labels = sec_summary["Sector"].tolist()
    values = sec_summary["Inversión Real (USD)"].tolist()
    percentages = sec_summary["Peso Sectorial Real (%)"].tolist()

    palette = [
        "#10b981", "#3b82f6", "#f59e0b", "#ec4899", "#8b5cf6",
        "#06b6d4", "#14b8a6", "#f97316", "#a855f7", "#6366f1"
    ]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(colors=palette[:len(labels)], line=dict(color="#080b12", width=2)),
        textinfo="label+percent",
        textfont=dict(family="Inter", size=11, color="#f8fafc"),
        hovertemplate="<b>Sector: %{label}</b><br>Inversión: $%{value:,.2f} USD<br>Peso en Cartera: %{percent}<extra></extra>",
    )])

    fig.update_layout(
        title=dict(
            text="<b>Distribución Sectorial Real del Portafolio (Límite ≤ 35%)</b>",
            font=dict(size=13, color="#f8fafc", family="Inter"),
            x=0.02, y=0.98
        ),
        template="plotly_dark",
        paper_bgcolor="#080b12",
        plot_bgcolor="#0c101b",
        margin=dict(l=25, r=25, t=55, b=25),
        height=330,
        showlegend=False,
        annotations=[dict(text="Límite<br><b>≤ 35%</b>", x=0.5, y=0.5, font_size=13, font_color="#10b981", showarrow=False)]
    )
    return fig
