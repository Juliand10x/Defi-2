"""Herramientas reproducibles para explorar y valorar opciones listadas."""

from datetime import date
from typing import Dict, Iterable, List

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy import stats
import yfinance as yf


def _nearest_expirations(expirations: Iterable[str], as_of: date) -> List[str]:
    targets = np.array([30, 91, 182])
    available = [(value, (pd.Timestamp(value).date() - as_of).days) for value in expirations]
    available = [(value, days) for value, days in available if days > 0]
    chosen = []
    for target in targets:
        candidates = [x for x in available if x[0] not in chosen]
        if candidates:
            chosen.append(min(candidates, key=lambda x: abs(x[1] - target))[0])
    return chosen


def _market_mid(row: pd.Series) -> float:
    bid, ask = float(row.get("bid", 0) or 0), float(row.get("ask", 0) or 0)
    return (bid + ask) / 2 if bid > 0 and ask >= bid else np.nan


def get_option_candidates(ticker: str, spot: float, mu_spot: float, sigma: float, as_of: date | None = None) -> Dict[str, object]:
    """Obtiene contratos reales y selecciona strikes cercanos a Q25, Q50 y Q75."""
    as_of = as_of or date.today()
    try:
        instrument = yf.Ticker(ticker)
        expirations = list(instrument.options)
    except Exception as exc:
        return {"success": False, "error": f"No fue posible consultar opciones de {ticker}: {exc}"}
    if not expirations:
        return {"success": False, "error": f"{ticker} no tiene vencimientos disponibles en la consulta actual."}
    rows = []
    selected_expirations = _nearest_expirations(expirations, as_of)
    for expiry in selected_expirations:
        try:
            chain = instrument.option_chain(expiry)
        except Exception:
            continue
        maturity_days = (pd.Timestamp(expiry).date() - as_of).days
        maturity = maturity_days / 365.0
        quantiles = {q: spot * np.exp((mu_spot - 0.5 * sigma**2) * maturity + sigma * np.sqrt(maturity) * stats.norm.ppf(q)) for q in (0.25, 0.50, 0.75)}
        for option_type, contracts in (("Call", chain.calls), ("Put", chain.puts)):
            if contracts is None or contracts.empty:
                continue
            contracts = contracts.copy()
            contracts["mid"] = contracts.apply(_market_mid, axis=1)
            for q, projected in quantiles.items():
                nearest = contracts.iloc[(contracts["strike"] - projected).abs().argsort().iloc[:1]]
                if nearest.empty:
                    continue
                row = nearest.iloc[0]
                rows.append({"Vencimiento": expiry, "Días calendario": maturity_days, "T (años)": maturity,
                    "Tipo": option_type, "Cuantil GBM": f"Q{int(q * 100)}", "Precio proyectado": projected,
                    "Contrato": row.get("contractSymbol", ""), "Strike": float(row["strike"]),
                    "Bid": float(row.get("bid", np.nan)), "Ask": float(row.get("ask", np.nan)), "Mid": float(row["mid"]),
                    "Volumen": int(row.get("volume", 0) or 0), "Interés abierto": int(row.get("openInterest", 0) or 0),
                    "Última cotización": row.get("lastTradeDate", pd.NaT)})
    candidates = pd.DataFrame(rows)
    if candidates.empty:
        return {"success": False, "error": "La cadena no ofreció contratos utilizables para los vencimientos seleccionados."}
    return {"success": True, "candidates": candidates, "selected_expirations": selected_expirations, "queried_at": pd.Timestamp.now(tz="UTC")}


def crr_price(spot: float, strike: float, maturity: float, rate: float, dividend_yield: float, sigma: float, steps: int = 200, option_type: str = "Call", style: str = "Europea") -> Dict[str, float]:
    """Valora una opción con CRR europeo o americano."""
    if maturity <= 0:
        payoff = max(spot - strike, 0.0) if option_type == "Call" else max(strike - spot, 0.0)
        return {"price": payoff, "u": np.nan, "d": np.nan, "p_q": np.nan, "valid": True}
    if min(spot, strike, sigma) <= 0 or steps < 1:
        return {"price": np.nan, "u": np.nan, "d": np.nan, "p_q": np.nan, "valid": False}
    dt = maturity / steps
    u, d = np.exp(sigma * np.sqrt(dt)), np.exp(-sigma * np.sqrt(dt))
    p_q = (np.exp((rate - dividend_yield) * dt) - d) / (u - d)
    if not 0 < p_q < 1:
        return {"price": np.nan, "u": u, "d": d, "p_q": p_q, "valid": False}
    j = np.arange(steps + 1)
    terminal = spot * (u ** j) * (d ** (steps - j))
    values = np.maximum(terminal - strike, 0) if option_type == "Call" else np.maximum(strike - terminal, 0)
    for level in range(steps - 1, -1, -1):
        values = np.exp(-rate * dt) * (p_q * values[1:] + (1 - p_q) * values[:-1])
        if style == "Americana":
            nodes = spot * (u ** np.arange(level + 1)) * (d ** (level - np.arange(level + 1)))
            exercise = np.maximum(nodes - strike, 0) if option_type == "Call" else np.maximum(strike - nodes, 0)
            values = np.maximum(values, exercise)
    return {"price": float(values[0]), "u": float(u), "d": float(d), "p_q": float(p_q), "valid": True}


def contract_probabilities(terminal_prices: np.ndarray, strike: float, ask: float, rate: float, maturity: float, option_type: str, terminal_cost: float = 0.0) -> Dict[str, float]:
    payoff = np.maximum(terminal_prices - strike, 0) if option_type == "Call" else np.maximum(strike - terminal_prices, 0)
    exercise = terminal_prices > strike if option_type == "Call" else terminal_prices < strike
    profit = payoff - ask * np.exp(rate * maturity) - terminal_cost
    return {"exercise_probability": float(np.mean(exercise)), "profit_probability": float(np.mean(profit > 0)), "expected_profit": float(np.mean(profit))}


def crr_convergence_chart(spot: float, strike: float, maturity: float, rate: float, dividend_yield: float, sigma: float, option_type: str, style: str) -> go.Figure:
    steps = [25, 50, 100, 200, 400]
    prices = [crr_price(spot, strike, maturity, rate, dividend_yield, sigma, n, option_type, style)["price"] for n in steps]
    fig = go.Figure(go.Scatter(x=steps, y=prices, mode="lines+markers", line=dict(color="#10b981", width=3)))
    fig.update_layout(template="plotly_dark", paper_bgcolor="#080b12", plot_bgcolor="#0c101b", height=300, title="Convergencia del árbol CRR", xaxis_title="Pasos del árbol", yaxis_title="Prima teórica (USD)")
    return fig
