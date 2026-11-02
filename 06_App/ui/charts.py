"""Generación de Gráficos Financieros Interactivos con Plotly."""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_stochastic_fan(sim_result, title_suffix=""):
    fig = go.Figure()
    x_axis = sim_result.time_grid
    
    # Muestra de 25 trayectorias individuales
    n_sample = min(25, sim_result.paths.shape[0])
    for i in range(n_sample):
        fig.add_trace(go.Scatter(
            x=x_axis,
            y=sim_result.paths[i, :],
            mode="lines",
            line=dict(color="rgba(148, 163, 184, 0.12)", width=1),
            showlegend=False,
            hoverinfo="skip"
        ))
        
    # Bandas percentiles
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
        fillcolor="rgba(121, 82, 245, 0.14)",
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
        fillcolor="rgba(6, 182, 212, 0.22)",
        name="Banda 25% - 75%",
    ))
    
    # Mediana (Percentil 50)
    fig.add_trace(go.Scatter(
        x=x_axis,
        y=sim_result.percentiles[50],
        mode="lines",
        line=dict(color="#06b6d4", width=2.5),
        name="Mediana P50",
    ))
    
    # Media simulada y spot
    fig.add_trace(go.Scatter(
        x=[0, x_axis[-1]],
        y=[sim_result.spot, sim_result.simulated_mean],
        mode="lines+markers",
        line=dict(color="#f59e0b", width=2, dash="dash"),
        name=f"Media Sim (USD {sim_result.simulated_mean:.2f})",
    ))

    fig.update_layout(
        title=f"<b>{sim_result.model_name}</b> {title_suffix}",
        template="plotly_dark",
        paper_bgcolor="rgba(15, 23, 42, 0.4)",
        plot_bgcolor="rgba(15, 23, 42, 0.6)",
        xaxis=dict(title="Días hábiles de proyección", gridcolor="rgba(148, 163, 184, 0.1)"),
        yaxis=dict(title="Precio Proyectado (USD)", gridcolor="rgba(148, 163, 184, 0.1)"),
        margin=dict(l=40, r=40, t=50, b=40),
        height=380,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def plot_model_comparison_bars(models_df):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=models_df["Modelo"],
        y=models_df["AIC"],
        name="AIC (Menor es mejor)",
        marker_color="#7952f5"
    ))
    fig.add_trace(go.Bar(
        x=models_df["Modelo"],
        y=models_df["BIC"],
        name="BIC (Penaliza sobreajuste)",
        marker_color="#06b6d4"
    ))
    fig.update_layout(
        title="<b>Criterios de Información Estadística (AIC vs BIC)</b>",
        barmode="group",
        template="plotly_dark",
        paper_bgcolor="rgba(15, 23, 42, 0.4)",
        plot_bgcolor="rgba(15, 23, 42, 0.6)",
        xaxis=dict(gridcolor="rgba(148, 163, 184, 0.1)"),
        yaxis=dict(title="Valor del Criterio", gridcolor="rgba(148, 163, 184, 0.1)"),
        margin=dict(l=40, r=40, t=50, b=40),
        height=320,
    )
    return fig


def plot_portfolio_allocation_chart(alloc_df):
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=alloc_df["Ticker"],
        y=[float(p.replace('%', '')) for p in alloc_df["Peso Igual"]],
        name="Pesos Iguales (1/N)",
        marker_color="rgba(148, 163, 184, 0.4)",
    ))
    
    fig.add_trace(go.Bar(
        x=alloc_df["Ticker"],
        y=[float(p.replace('%', '')) for p in alloc_df["Peso Inv VaR"]],
        name="Inverso al VaR",
        marker_color="#06b6d4",
    ))
    
    fig.add_trace(go.Bar(
        x=alloc_df["Ticker"],
        y=[w * 100.0 for w in alloc_df["Peso Óptimo"]],
        name="Mínimo VaR Restringido",
        marker_color="#7952f5",
    ))
    
    fig.update_layout(
        title="<b>Ponderaciones por Modelo de Asignación (%)</b>",
        barmode="group",
        template="plotly_dark",
        paper_bgcolor="rgba(15, 23, 42, 0.4)",
        plot_bgcolor="rgba(15, 23, 42, 0.6)",
        xaxis=dict(title="Activo", gridcolor="rgba(148, 163, 184, 0.1)"),
        yaxis=dict(title="Peso en Portafolio (%)", gridcolor="rgba(148, 163, 184, 0.1)"),
        margin=dict(l=40, r=40, t=50, b=40),
        height=360,
    )
    return fig