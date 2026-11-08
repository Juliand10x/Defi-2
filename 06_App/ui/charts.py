"""Generación de Gráficos Financieros Interactivos con Plotly (Paleta Obsidiana & Esmeralda)."""

import numpy as np
import pandas as pd
import plotly.graph_objects as go


def plot_stochastic_fan(sim_result, title_suffix=""):
    fig = go.Figure()
    x_axis = sim_result.time_grid
    
    # Muestra de 20 trayectorias individuales discretas
    n_sample = min(20, sim_result.paths.shape[0])
    for i in range(n_sample):
        fig.add_trace(go.Scatter(
            x=x_axis,
            y=sim_result.paths[i, :],
            mode="lines",
            line=dict(color="rgba(148, 163, 184, 0.12)", width=1),
            showlegend=False,
            hoverinfo="skip"
        ))
        
    # Bandas percentiles (Esmeralda Financiero)
    # 10% - 90%
    fig.add_trace(go.Scatter(
        x=x_axis,
        y=sim_result.percentiles[90],
        mode="lines",
        line=dict(width=0),
        showlegend=False,
        hoverinfo="skip"
    ))
    fig.add_trace(go.Scatter(
        x=x_axis,
        y=sim_result.percentiles[10],
        mode="lines",
        line=dict(width=0),
        fill="tonexty",
        fillcolor="rgba(16, 185, 129, 0.10)",
        name="Banda 10% - 90%",
    ))
    
    # 25% - 75%
    fig.add_trace(go.Scatter(
        x=x_axis,
        y=sim_result.percentiles[75],
        mode="lines",
        line=dict(width=0),
        showlegend=False,
        hoverinfo="skip"
    ))
    fig.add_trace(go.Scatter(
        x=x_axis,
        y=sim_result.percentiles[25],
        mode="lines",
        line=dict(width=0),
        fill="tonexty",
        fillcolor="rgba(16, 185, 129, 0.22)",
        name="Banda 25% - 75%",
    ))
    
    # Mediana (Percentil 50)
    fig.add_trace(go.Scatter(
        x=x_axis,
        y=sim_result.percentiles[50],
        mode="lines",
        line=dict(color="#10b981", width=2.8),
        name="Mediana P50",
    ))
    
    # Media simulada y spot
    fig.add_trace(go.Scatter(
        x=[0, x_axis[-1]],
        y=[sim_result.spot, sim_result.simulated_mean],
        mode="lines+markers",
        line=dict(color="#f59e0b", width=2, dash="dash"),
        name=f"Media Sim (USD ${sim_result.simulated_mean:.2f})",
    ))

    fig.update_layout(
        title=dict(
            text=f"<b>{sim_result.model_name}</b> {title_suffix}",
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
            title=dict(text="Días hábiles proyectados", font=dict(size=11, color="#94a3b8")),
            gridcolor="rgba(255, 255, 255, 0.06)",
            color="#94a3b8",
        ),
        yaxis=dict(
            title=dict(text="Precio Proyectado (USD)", font=dict(size=11, color="#94a3b8")),
            gridcolor="rgba(255, 255, 255, 0.06)",
            color="#94a3b8",
            tickprefix="$",
        ),
        margin=dict(l=45, r=25, t=55, b=65),
        height=390,
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


def plot_model_comparison_bars(models_df):
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
            x=0.02,
            y=0.98,
            xanchor="left",
            yanchor="top",
        ),
        barmode="group",
        template="plotly_dark",
        paper_bgcolor="#0d131f",
        plot_bgcolor="#111726",
        xaxis=dict(gridcolor="rgba(255, 255, 255, 0.06)", color="#94a3b8"),
        yaxis=dict(
            title=dict(text="Puntaje del Criterio", font=dict(size=11, color="#94a3b8")),
            gridcolor="rgba(255, 255, 255, 0.06)",
            color="#94a3b8",
        ),
        margin=dict(l=45, r=25, t=55, b=65),
        height=330,
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


def plot_portfolio_allocation_chart(alloc_df):
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=alloc_df["Ticker"],
        y=[float(p.replace('%', '')) for p in alloc_df["Peso Igual"]],
        name="Pesos Iguales (1/N)",
        marker_color="rgba(148, 163, 184, 0.35)",
    ))
    
    fig.add_trace(go.Bar(
        x=alloc_df["Ticker"],
        y=[float(p.replace('%', '')) for p in alloc_df["Peso Inv VaR"]],
        name="Inverso al VaR",
        marker_color="#f59e0b",
    ))
    
    fig.add_trace(go.Bar(
        x=alloc_df["Ticker"],
        y=[w * 100.0 for w in alloc_df["Peso Óptimo"]],
        name="Mínimo VaR Óptimo (SLSQP)",
        marker_color="#10b981",
    ))
    
    fig.update_layout(
        title=dict(
            text="<b>Ponderaciones por Modelo de Asignación (%)</b>",
            font=dict(size=13, color="#f8fafc", family="Inter"),
            x=0.02,
            y=0.98,
            xanchor="left",
            yanchor="top",
        ),
        barmode="group",
        template="plotly_dark",
        paper_bgcolor="#0d131f",
        plot_bgcolor="#111726",
        xaxis=dict(
            title=dict(text="Activo", font=dict(size=11, color="#94a3b8")),
            gridcolor="rgba(255, 255, 255, 0.06)",
            color="#94a3b8",
        ),
        yaxis=dict(
            title=dict(text="Peso en Cartera (%)", font=dict(size=11, color="#94a3b8")),
            gridcolor="rgba(255, 255, 255, 0.06)",
            color="#94a3b8",
            ticksuffix="%",
        ),
        margin=dict(l=45, r=25, t=55, b=65),
        height=360,
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
