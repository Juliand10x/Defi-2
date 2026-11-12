"""
Motor de Evaluación Predictiva Rolling del GBM y Caminata Aleatoria.
Implementación de ventana móvil de 252 sesiones de calibración diaria:
- Pronóstico fuera de muestra condicional del GBM: P_hat(t+H|t) = P_t * exp(mu_total * H / 252)
- Pronóstico ingenuo (Naive benchmark): P_hat(t+H|t) = P_t
- Métricas de desempeño: RMSE y MAPE (%)
- Gráficos comparativos de trayectoria observada vs pronóstico condicional.
"""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
import plotly.graph_objects as go


def run_gbm_rolling_evaluation(
    prices_series: pd.Series,
    ticker: str,
    window_train: int = 252,
    horizon_H: int = 1,
    test_sessions: int = 252,
) -> Dict[str, any]:
    """
    Ejecuta el backtesting rolling estricto de 252 sesiones para una acción.
    Calcula RMSE y MAPE del GBM frente al benchmark ingenuo (Random Walk sin drift).
    """
    p = prices_series.dropna()
    total_len = len(p)

    if total_len < (window_train + 50):
        return {"success": False, "error": f"Se requieren al menos {window_train + 50} precios para el rolling."}

    # Definir el rango de evaluación (últimas test_sessions sesiones)
    eval_len = min(test_sessions, total_len - window_train - horizon_H)
    start_idx = total_len - eval_len - horizon_H

    forecast_dates = []
    actual_prices = []
    gbm_forecasts = []
    naive_forecasts = []
    errors_gbm = []
    errors_naive = []

    for idx in range(start_idx, total_len - horizon_H):
        # Ventana móvil de calibración de 252 retornos
        train_slice = p.iloc[idx - window_train : idx + 1]
        log_rets = np.diff(np.log(train_slice.values))

        if len(log_rets) < window_train:
            continue

        mu_daily = np.mean(log_rets)
        sigma_daily = np.std(log_rets, ddof=1)
        mu_total = (mu_daily * 252.0) + 0.5 * (sigma_daily ** 2) * 252.0

        p_t = float(train_slice.iloc[-1])
        target_date = p.index[idx + horizon_H]
        actual_p = float(p.iloc[idx + horizon_H])

        # Pronóstico puntual condicional del GBM: E[S_{t+H} | S_t]
        pred_gbm = p_t * np.exp(mu_total * (horizon_H / 252.0))
        pred_naive = p_t

        forecast_dates.append(target_date)
        actual_prices.append(actual_p)
        gbm_forecasts.append(pred_gbm)
        naive_forecasts.append(pred_naive)

        errors_gbm.append(actual_p - pred_gbm)
        errors_naive.append(actual_p - pred_naive)

    m = len(actual_prices)
    if m == 0:
        return {"success": False, "error": "No se pudieron calcular pronósticos suficientes."}

    actual_arr = np.array(actual_prices)
    e_gbm = np.array(errors_gbm)
    e_naive = np.array(errors_naive)

    rmse_gbm = float(np.sqrt(np.mean(e_gbm ** 2)))
    rmse_naive = float(np.sqrt(np.mean(e_naive ** 2)))

    mape_gbm = float(np.mean(np.abs(e_gbm) / actual_arr) * 100.0)
    mape_naive = float(np.mean(np.abs(e_naive) / actual_arr) * 100.0)

    # Determinar ganador
    gbm_beats_naive = rmse_gbm <= rmse_naive
    pct_improvement = ((rmse_naive - rmse_gbm) / rmse_naive) * 100.0 if rmse_naive > 0 else 0.0

    return {
        "success": True,
        "ticker": ticker,
        "m_evaluations": m,
        "horizon_H": horizon_H,
        "window_train": window_train,
        "rmse_gbm": rmse_gbm,
        "rmse_naive": rmse_naive,
        "mape_gbm": mape_gbm,
        "mape_naive": mape_naive,
        "gbm_beats_naive": gbm_beats_naive,
        "pct_improvement": pct_improvement,
        "forecast_dates": forecast_dates,
        "actual_prices": actual_prices,
        "gbm_forecasts": gbm_forecasts,
        "naive_forecasts": naive_forecasts,
        "errors_gbm": errors_gbm,
        "errors_naive": errors_naive,
    }


def run_multi_asset_rolling_table(
    prices_df: pd.DataFrame,
    tickers: List[str],
    window_train: int = 252,
    horizon_H: int = 1,
) -> pd.DataFrame:
    """
    Genera la tabla resumen de desempeño rolling RMSE y MAPE para las 10 acciones del portafolio.
    """
    rows = []
    for t in tickers:
        if t in prices_df.columns:
            res = run_gbm_rolling_evaluation(prices_df[t], t, window_train, horizon_H)
            if res.get("success", False):
                rows.append({
                    "Acción": t,
                    "Horizonte (H)": f"{horizon_H} día(s)",
                    "Muestras (m)": res["m_evaluations"],
                    "RMSE GBM (USD)": f"${res['rmse_gbm']:.2f}",
                    "RMSE Ingenuo (USD)": f"${res['rmse_naive']:.2f}",
                    "MAPE GBM (%)": f"{res['mape_gbm']:.2f}%",
                    "MAPE Ingenuo (%)": f"{res['mape_naive']:.2f}%",
                    "Diferencia RMSE": f"${res['rmse_gbm'] - res['rmse_naive']:+.2f}",
                    "¿Supera al Ingenuo?": "✅ Sí" if res["gbm_beats_naive"] else "⚖️ Paridad",
                })
    return pd.DataFrame(rows)


def plot_rolling_forecast_chart(rolling_res: Dict[str, any]) -> go.Figure:
    """
    Genera el gráfico interactivo de la evaluación rolling: Real vs GBM vs Ingenuo y curva de errores.
    """
    from plotly.subplots import make_subplots

    dates = rolling_res["forecast_dates"]
    actual = rolling_res["actual_prices"]
    pred_gbm = rolling_res["gbm_forecasts"]
    pred_naive = rolling_res.get("naive_forecasts", actual)
    errors = rolling_res.get("errors_gbm", [a - p for a, p in zip(actual, pred_gbm)])

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        row_heights=[0.68, 0.32],
        subplot_titles=(
            f"<b>Evaluación Predictiva Rolling (H = {rolling_res['horizon_H']}d) · {rolling_res['ticker']}</b>",
            "<b>Error de Pronóstico (e_t = P_observado - P_pronosticado)</b>"
        )
    )

    # 1. Precio Real Observado
    fig.add_trace(go.Scatter(
        x=dates, y=actual, mode="lines",
        name="Precio Real de Mercado", line=dict(color="#f8fafc", width=1.8),
    ), row=1, col=1)

    # 2. Pronóstico GBM Rolling
    fig.add_trace(go.Scatter(
        x=dates, y=pred_gbm, mode="lines",
        name=f"Pronóstico GBM (H={rolling_res['horizon_H']}d)",
        line=dict(color="#10b981", width=1.5, dash="dash"),
    ), row=1, col=1)

    # 3. Pronóstico Ingenuo
    fig.add_trace(go.Scatter(
        x=dates, y=pred_naive, mode="lines",
        name="Pronóstico Ingenuo (P_t)",
        line=dict(color="#94a3b8", width=1.0, dash="dot"),
    ), row=1, col=1)

    # 4. Serie de Errores
    fig.add_trace(go.Scatter(
        x=dates, y=errors, mode="lines",
        name="Error GBM (USD)", line=dict(color="#f59e0b", width=1.2),
        fill="tozeroy", fillcolor="rgba(245, 158, 11, 0.15)"
    ), row=2, col=1)

    fig.add_hline(y=0.0, line_dash="solid", line_color="rgba(255,255,255,0.2)", line_width=1, row=2, col=1)

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#080b12",
        plot_bgcolor="#0c101b",
        margin=dict(l=45, r=25, t=55, b=65),
        height=420,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.18,
            xanchor="center",
            x=0.5,
            font=dict(color="#94a3b8", size=10),
        ),
    )
    fig.update_yaxes(title_text="Precio (USD)", tickprefix="$", row=1, col=1, gridcolor="rgba(255,255,255,0.06)", color="#94a3b8")
    fig.update_yaxes(title_text="Error (USD)", tickprefix="$", row=2, col=1, gridcolor="rgba(255,255,255,0.06)", color="#94a3b8")
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.06)", color="#94a3b8")
    return fig

