"""
Módulo de Exploración y Valoración de Opciones (Pasos 5, 6, 8 y 9 del Taller).
Implementa árbol binomial CRR (Europeo/Americano), Black-Scholes, cuantiles proyectados,
comparativa frente a mercado y diagrama del árbol de 3 pasos.
"""

from datetime import date
from typing import Dict, Iterable, List, Optional, Tuple, Any

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy import stats
import yfinance as yf


def black_scholes_price(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    dividend_yield: float,
    sigma: float,
    option_type: str = "Call",
) -> float:
    """Calcula el precio analítico de Black-Scholes-Merton como benchmark continuo."""
    if maturity <= 0 or sigma <= 0 or spot <= 0 or strike <= 0:
        return max(spot - strike, 0.0) if option_type == "Call" else max(strike - spot, 0.0)
    
    d1 = (np.log(spot / strike) + (rate - dividend_yield + 0.5 * sigma**2) * maturity) / (sigma * np.sqrt(maturity))
    d2 = d1 - sigma * np.sqrt(maturity)
    
    if option_type == "Call":
        price = spot * np.exp(-dividend_yield * maturity) * stats.norm.cdf(d1) - strike * np.exp(-rate * maturity) * stats.norm.cdf(d2)
    else:
        price = strike * np.exp(-rate * maturity) * stats.norm.cdf(-d2) - spot * np.exp(-dividend_yield * maturity) * stats.norm.cdf(-d1)
    return float(max(price, 0.0))


def verify_crr_control_benchmark() -> Dict[str, Any]:
    """
    Verifica el control obligatorio del taller (Paso 8):
    Call europea con S0 = K = 100, T = 1, r = 0.05, q = 0, sigma = 0.20
    debe aproximar USD 10.4506.
    """
    s0 = 100.0
    k = 100.0
    t = 1.0
    r = 0.05
    q = 0.0
    sigma = 0.20
    
    bs_exact = black_scholes_price(s0, k, t, r, q, sigma, "Call")
    crr_50 = crr_price(s0, k, t, r, q, sigma, steps=50, option_type="Call", style="Europea")["price"]
    crr_200 = crr_price(s0, k, t, r, q, sigma, steps=200, option_type="Call", style="Europea")["price"]
    crr_500 = crr_price(s0, k, t, r, q, sigma, steps=500, option_type="Call", style="Europea")["price"]
    
    benchmark_target = 10.4506
    diff_crr = abs(crr_200 - benchmark_target)
    passed = diff_crr < 0.05
    
    return {
        "target": benchmark_target,
        "black_scholes_exact": bs_exact,
        "crr_50": crr_50,
        "crr_200": crr_200,
        "crr_500": crr_500,
        "difference": diff_crr,
        "passed": passed,
    }


def _nearest_expirations(expirations: Iterable[str], as_of: date) -> List[str]:
    """Selecciona 3 vencimientos reales cercanos a 1, 3 y 6 meses (30, 91, 182 días)."""
    targets = [30, 91, 182]
    available = []
    for exp_str in expirations:
        try:
            d = (pd.Timestamp(exp_str).date() - as_of).days
            if d > 5:
                available.append((exp_str, d))
        except Exception:
            continue
    available.sort(key=lambda x: x[1])
    
    chosen = []
    for target in targets:
        candidates = [x for x in available if x[0] not in [c[0] for c in chosen]]
        if candidates:
            best = min(candidates, key=lambda x: abs(x[1] - target))
            chosen.append(best)
    return [c[0] for c in chosen]


def _market_mid(row: pd.Series) -> float:
    bid = float(row.get("bid", 0) or 0)
    ask = float(row.get("ask", 0) or 0)
    return (bid + ask) / 2.0 if bid > 0 and ask >= bid else np.nan


def get_option_candidates(
    ticker: str,
    spot: float,
    mu_spot: float,
    sigma: float,
    as_of: Optional[date] = None,
) -> Dict[str, Any]:
    """
    Obtiene contratos reales de mercado (Paso 5) y construye la tabla de al menos
    9 candidatos evaluando los cuantiles Q25, Q50 y Q75 en 3 vencimientos.
    Si los cuantiles caen en el mismo strike, se expande a strikes vecinos para garantizar 9 distintos.
    """
    as_of = as_of or date.today()
    try:
        instrument = yf.Ticker(ticker)
        expirations = list(instrument.options)
    except Exception as exc:
        return {"success": False, "error": f"No fue posible consultar opciones de {ticker}: {exc}"}

    if not expirations:
        return {"success": False, "error": f"{ticker} no tiene contratos de opciones disponibles actualmente en Yahoo Finance."}

    selected_expirations = _nearest_expirations(expirations, as_of)
    if len(selected_expirations) < 3 and len(expirations) >= 3:
        selected_expirations = expirations[:3]

    rows = []
    quantiles_probs = [0.25, 0.50, 0.75]

    for expiry in selected_expirations:
        try:
            chain = instrument.option_chain(expiry)
        except Exception:
            continue

        maturity_days = (pd.Timestamp(expiry).date() - as_of).days
        maturity = maturity_days / 365.0
        gbm_sessions = round(maturity * 252.0)

        # Proyección de cuantiles analíticos según ec. (4) del Taller:
        # Q_beta(S_T) = S0 * exp((a - 0.5 * sigma^2)*T + sigma * sqrt(T) * Phi^-1(beta))
        quantiles = {}
        for q in quantiles_probs:
            z_q = stats.norm.ppf(q)
            q_val = spot * np.exp((mu_spot - 0.5 * (sigma**2)) * maturity + sigma * np.sqrt(maturity) * z_q)
            quantiles[q] = q_val

        for option_type, contracts in [("Call", chain.calls), ("Put", chain.puts)]:
            if contracts is None or contracts.empty:
                continue

            contracts = contracts.copy().sort_values("strike")
            contracts["mid"] = contracts.apply(_market_mid, axis=1)

            used_strikes = set()
            for q in quantiles_probs:
                proj_q = quantiles[q]
                # Encontrar el strike más cercano no repetido si es posible
                diffs = (contracts["strike"] - proj_q).abs()
                sorted_idx = diffs.argsort()
                
                selected_row = None
                for idx in sorted_idx:
                    cand_strike = float(contracts.iloc[idx]["strike"])
                    if cand_strike not in used_strikes:
                        selected_row = contracts.iloc[idx]
                        used_strikes.add(cand_strike)
                        break
                
                if selected_row is None and not contracts.empty:
                    selected_row = contracts.iloc[sorted_idx.iloc[0]]

                if selected_row is not None:
                    strike_val = float(selected_row["strike"])
                    bid_val = float(selected_row.get("bid", np.nan))
                    ask_val = float(selected_row.get("ask", np.nan))
                    mid_val = float(selected_row["mid"])
                    
                    rows.append({
                        "Vencimiento": expiry,
                        "Días Calendario (dc)": maturity_days,
                        "T (años)": round(maturity, 4),
                        "Sesiones GBM": gbm_sessions,
                        "Tipo": option_type,
                        "Cuantil GBM": f"Q{int(q * 100)}",
                        "Precio Proyectado (USD)": round(proj_q, 2),
                        "Contrato": selected_row.get("contractSymbol", f"{ticker}_{expiry}_{strike_val}"),
                        "Strike (K)": round(strike_val, 2),
                        "Bid": round(bid_val, 2) if np.isfinite(bid_val) and bid_val > 0 else np.nan,
                        "Ask": round(ask_val, 2) if np.isfinite(ask_val) and ask_val > 0 else np.nan,
                        "Mid": round(mid_val, 2) if np.isfinite(mid_val) else np.nan,
                        "Volumen": int(selected_row.get("volume", 0) or 0),
                        "Interés Abierto": int(selected_row.get("openInterest", 0) or 0),
                        "Última Consulta": selected_row.get("lastTradeDate", pd.NaT),
                    })

    candidates_df = pd.DataFrame(rows)
    if candidates_df.empty:
        return {"success": False, "error": "No se encontraron contratos utilizables para los vencimientos seleccionados."}

    return {
        "success": True,
        "candidates": candidates_df,
        "selected_expirations": selected_expirations,
        "queried_at": pd.Timestamp.now(tz="UTC"),
    }


def crr_price(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    dividend_yield: float,
    sigma: float,
    steps: int = 200,
    option_type: str = "Call",
    style: str = "Europea",
) -> Dict[str, Any]:
    """
    Valora una opción con árbol binomial Cox-Ross-Rubinstein (CRR) (Paso 8):
    - dt = T / N, u = exp(sigma * sqrt(dt)), d = 1 / u
    - p_Q = (exp((r - q) * dt) - d) / (u - d)
    - Verificación estricta de no arbitraje: 0 < p_Q < 1
    - Soporte para estilo Europeo (continuación) y Americano (max{Payoff, Continuación})
    - Tratamiento robusto de T = 0 con payoff inmediato.
    """
    if maturity <= 0:
        payoff = max(spot - strike, 0.0) if option_type == "Call" else max(strike - spot, 0.0)
        return {
            "price": float(payoff),
            "u": 1.0,
            "d": 1.0,
            "p_q": 0.5,
            "valid": True,
            "black_scholes": float(payoff),
        }

    if min(spot, strike, sigma) <= 0 or steps < 1:
        return {"price": np.nan, "u": np.nan, "d": np.nan, "p_q": np.nan, "valid": False}

    dt = maturity / steps
    u = float(np.exp(sigma * np.sqrt(dt)))
    d = float(1.0 / u)
    p_q = float((np.exp((rate - dividend_yield) * dt) - d) / (u - d))

    if not (0.0 < p_q < 1.0):
        return {
            "price": np.nan,
            "u": u,
            "d": d,
            "p_q": p_q,
            "valid": False,
            "error": f"Probabilidad neutral al riesgo pQ = {p_q:.4f} fuera de (0, 1). Aumente pasos N o revise tasa/dividendo.",
        }

    # Precios terminales del subyacente en el paso terminal N
    j = np.arange(steps + 1)
    s_terminal = spot * (u ** j) * (d ** (steps - j))

    # Payoff en vencimiento
    if option_type == "Call":
        values = np.maximum(s_terminal - strike, 0.0)
    else:
        values = np.maximum(strike - s_terminal, 0.0)

    # Inducción hacia atrás
    discount = np.exp(-rate * dt)
    for level in range(steps - 1, -1, -1):
        continuation = discount * (p_q * values[1:] + (1.0 - p_q) * values[:-1])
        if style == "Americana":
            j_curr = np.arange(level + 1)
            s_current = spot * (u ** j_curr) * (d ** (level - j_curr))
            exercise = np.maximum(s_current - strike, 0.0) if option_type == "Call" else np.maximum(strike - s_current, 0.0)
            values = np.maximum(continuation, exercise)
        else:
            values = continuation

    bs_val = black_scholes_price(spot, strike, maturity, rate, dividend_yield, sigma, option_type)

    return {
        "price": float(values[0]),
        "u": u,
        "d": d,
        "p_q": p_q,
        "dt": dt,
        "steps": steps,
        "valid": True,
        "black_scholes": bs_val,
        "diff_bs": float(values[0] - bs_val),
    }


def contract_probabilities(
    terminal_prices: np.ndarray,
    strike: float,
    ask: float,
    rate: float,
    maturity: float,
    option_type: str,
    terminal_cost: float = 0.0,
) -> Dict[str, float]:
    """
    Calcula probabilidades bajo la medida física P (Paso 6):
    - Probabilidad de ejercicio: P(ST > K) para Call, P(ST < K) para Put.
    - Probabilidad de beneficio neto: P(Pi_T > 0), con Pi_T = H(ST) - A * exp(r*T) - c_T.
    - Utilidad neta esperada E[Pi_T].
    """
    if option_type == "Call":
        payoff = np.maximum(terminal_prices - strike, 0.0)
        exercise = terminal_prices > strike
    else:
        payoff = np.maximum(strike - terminal_prices, 0.0)
        exercise = terminal_prices < strike

    cost_fv = ask * np.exp(rate * maturity) if (np.isfinite(ask) and ask > 0) else 0.0
    profit = payoff - cost_fv - terminal_cost

    return {
        "exercise_probability": float(np.mean(exercise)),
        "profit_probability": float(np.mean(profit > 0.0)),
        "expected_profit": float(np.mean(profit)),
        "ask_compounded": float(cost_fv),
        "terminal_cost": terminal_cost,
    }


def generate_crr_3step_tree(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    dividend_yield: float,
    sigma: float,
    option_type: str = "Call",
    style: str = "Europea",
) -> Tuple[go.Figure, pd.DataFrame]:
    """
    Dibuja un árbol binomial de 3 pasos (Paso 8 del Taller) mostrando en cada nodo:
    - Precio del subyacente S_{k,j}
    - Valor de la opción V_{k,j}
    """
    N = 3
    dt = maturity / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1.0 / u
    p_q = (np.exp((rate - dividend_yield) * dt) - d) / (u - d)
    discount = np.exp(-rate * dt)

    # Construir matrices del árbol (4 niveles: k=0,1,2,3)
    stock_tree = {}
    option_tree = {}

    for k in range(N + 1):
        stock_tree[k] = []
        for j in range(k + 1):
            s_val = spot * (u ** j) * (d ** (k - j))
            stock_tree[k].append(s_val)

    # Nivel terminal k=3
    option_tree[N] = []
    for s_val in stock_tree[N]:
        payoff = max(s_val - strike, 0.0) if option_type == "Call" else max(strike - s_val, 0.0)
        option_tree[N].append(payoff)

    # Retroceder niveles 2, 1, 0
    for k in range(N - 1, -1, -1):
        option_tree[k] = []
        for j in range(k + 1):
            cont = discount * (p_q * option_tree[k + 1][j + 1] + (1.0 - p_q) * option_tree[k + 1][j])
            if style == "Americana":
                s_val = stock_tree[k][j]
                payoff = max(s_val - strike, 0.0) if option_type == "Call" else max(strike - s_val, 0.0)
                opt_val = max(cont, payoff)
            else:
                opt_val = cont
            option_tree[k].append(opt_val)

    # Gráfico interactivo con Plotly
    fig = go.Figure()
    table_rows = []

    # Trazar ramas
    for k in range(N):
        for j in range(k + 1):
            x_start, y_start = k, j - k / 2.0
            # Rama up
            x_up, y_up = k + 1, (j + 1) - (k + 1) / 2.0
            fig.add_trace(go.Scatter(
                x=[x_start, x_up], y=[y_start, y_up],
                mode="lines", line=dict(color="rgba(16, 185, 129, 0.4)", width=1.5),
                hoverinfo="skip", showlegend=False
            ))
            # Rama down
            x_down, y_down = k + 1, j - (k + 1) / 2.0
            fig.add_trace(go.Scatter(
                x=[x_start, x_down], y=[y_start, y_down],
                mode="lines", line=dict(color="rgba(239, 68, 68, 0.4)", width=1.5),
                hoverinfo="skip", showlegend=False
            ))

    # Trazar nodos y recolectar tabla
    node_x, node_y, node_text, node_hover = [], [], [], []
    for k in range(N + 1):
        for j in range(k + 1):
            s_val = stock_tree[k][j]
            v_val = option_tree[k][j]
            x_pos = k
            y_pos = j - k / 2.0
            
            node_x.append(x_pos)
            node_y.append(y_pos)
            node_text.append(f"<b>S: ${s_val:.1f}</b><br>V: ${v_val:.2f}")
            node_hover.append(f"Paso k={k}, Subidas j={j}<br>Spot: ${s_val:,.2f}<br>Opción ({style}): ${v_val:,.2f}")
            
            table_rows.append({
                "Paso (k)": k,
                "Subidas (j)": j,
                "Precio Acción (S)": round(s_val, 2),
                "Valor Opción (V)": round(v_val, 2),
                "Etapa": "Inicial" if k == 0 else ("Vencimiento" if k == N else f"Paso {k}")
            })

    fig.add_trace(go.Scatter(
        x=node_x, y=node_y, mode="markers+text",
        marker=dict(size=34, color="#0c101b", line=dict(color="#10b981", width=2)),
        text=node_text, textposition="middle center",
        textfont=dict(color="#f8fafc", size=9, family="Inter"),
        hovertext=node_hover, hoverinfo="text", showlegend=False
    ))

    fig.update_layout(
        title=dict(
            text=f"<b>Árbol Binomial CRR de 3 Pasos</b> (u={u:.3f}, d={d:.3f}, pQ={p_q:.3f})",
            font=dict(size=12, color="#f8fafc"),
            x=0.02, y=0.98,
        ),
        paper_bgcolor="#080b12", plot_bgcolor="#0c101b",
        xaxis=dict(
            title=dict(text="Paso Temporal (k)", font=dict(color="#94a3b8", size=11)),
            tickmode="array", tickvals=[0, 1, 2, 3], ticktext=["t=0", "t=1", "t=2", "Vencimiento (t=3)"],
            gridcolor="rgba(255,255,255,0.05)", color="#94a3b8"
        ),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        margin=dict(l=25, r=25, t=45, b=35),
        height=320,
    )

    return fig, pd.DataFrame(table_rows)


def crr_convergence_chart(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    dividend_yield: float,
    sigma: float,
    option_type: str = "Call",
    style: str = "Europea",
) -> go.Figure:
    """Gráfico de convergencia del árbol CRR al aumentar N vs el benchmark analítico Black-Scholes."""
    steps_list = [5, 10, 25, 50, 100, 150, 200, 300, 400]
    prices = [crr_price(spot, strike, maturity, rate, dividend_yield, sigma, n, option_type, style)["price"] for n in steps_list]
    bs_val = black_scholes_price(spot, strike, maturity, rate, dividend_yield, sigma, option_type)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=steps_list, y=prices, mode="lines+markers",
        name=f"Árbol CRR ({style})", line=dict(color="#10b981", width=2.5),
        marker=dict(size=6, color="#34d399")
    ))
    fig.add_hline(
        y=bs_val, line_dash="dash", line_color="#f59e0b", line_width=1.8,
        annotation_text=f"Black-Scholes continuo: USD ${bs_val:.2f}",
        annotation_position="bottom right",
        annotation_font=dict(color="#f59e0b", size=10)
    )

    fig.update_layout(
        title=dict(
            text=f"<b>Convergencia del Árbol CRR vs Black-Scholes</b> ({option_type} {style})",
            font=dict(size=12, color="#f8fafc"), x=0.02, y=0.98
        ),
        paper_bgcolor="#080b12", plot_bgcolor="#0c101b",
        xaxis=dict(title=dict(text="Número de Pasos (N)", font=dict(color="#94a3b8", size=11)), gridcolor="rgba(255,255,255,0.06)", color="#94a3b8"),
        yaxis=dict(title=dict(text="Prima Teórica (USD)", font=dict(color="#94a3b8", size=11)), gridcolor="rgba(255,255,255,0.06)", color="#94a3b8", tickprefix="$"),
        margin=dict(l=45, r=25, t=45, b=45), height=300,
        legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5, font=dict(size=10, color="#94a3b8"))
    )
    return fig
