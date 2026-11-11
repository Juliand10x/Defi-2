"""
Kibo · Plataforma Móvil Inteligente de Inversión y Gestión de Riesgo
Diseño Step-by-Step Mobile-First: Paleta Obsidiana, Esmeralda Financiero y Oro Champaña.
"""

import os
import sys

# Asegurar rutas absolutas para Streamlit Cloud
_APP_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_APP_DIR)
for _p in [_APP_DIR, _REPO_ROOT]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from datetime import date, timedelta
import numpy as np
import pandas as pd
import streamlit as st

from src.data_engine import (
    DEFAULT_TICKERS,
    SECTOR_MAP,
    ALL_SECTORS,
    get_default_portfolio,
    detect_sector,
    download_market_data,
)
from src.stochastic_engine import (
    calibrate_gbm,
    simulate_gbm,
    calibrate_merton_jump,
    simulate_merton_jump,
    calibrate_ornstein_uhlenbeck,
    simulate_ornstein_uhlenbeck,
)
from src.model_comparison import compare_models_for_asset
from src.portfolio_engine import compute_portfolio_allocation
from src.herding_engine import (
    run_herding_analysis,
    plot_herding_scatter,
    plot_csad_timeline,
)
from src.risk_engine import (
    compute_var_comparison_and_stress,
    plot_var_distribution_hist,
)
from src.options_engine import get_option_candidates, crr_price, contract_probabilities, crr_convergence_chart
from src.rolling_engine import (
    run_gbm_rolling_evaluation,
    run_multi_asset_rolling_table,
    plot_rolling_forecast_chart,
)
from ui.styles import APP_CSS
from ui.kibo_avatar import get_kibo_hero_banner, get_kibo_image_base64
from ui.charts import plot_stochastic_fan, plot_model_comparison_bars, plot_portfolio_allocation_chart

# Importación ultra segura de ui.tour con recarga forzada para Streamlit Cloud
try:
    import importlib
    import ui.tour as tour_module
    importlib.reload(tour_module)
    render_kibo_tour = getattr(tour_module, "render_kibo_tour")
    render_intro_splash_animation = getattr(tour_module, "render_intro_splash_animation")
except Exception:
    try:
        from ui.tour import render_kibo_tour, render_intro_splash_animation
    except Exception:
        def render_kibo_tour(*args, **kwargs):
            pass
        def render_intro_splash_animation(*args, **kwargs):
            pass


st.set_page_config(
    page_title="Kibo · Copiloto de Inversión",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)


def initialize_session_state():
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "capital" not in st.session_state:
        st.session_state.capital = 100000.0
    if "profile" not in st.session_state:
        st.session_state.profile = "Moderado"
    if "horizon" not in st.session_state:
        st.session_state.horizon = 10
    if "confidence" not in st.session_state:
        st.session_state.confidence = 99.0
    if "tickers" not in st.session_state:
        st.session_state.tickers = list(DEFAULT_TICKERS)
    if "portfolio" not in st.session_state:
        st.session_state.portfolio = get_default_portfolio()
    if "market_data" not in st.session_state:
        st.session_state.market_data = None
    if "active_asset_tab" not in st.session_state:
        st.session_state.active_asset_tab = "AAPL"


def set_step(new_step: int):
    st.session_state.step = new_step
    st.rerun()


def render_mobile_header(current_step: int):
    step_titles = {
        1: "Tu Capital",
        2: "Tu Perfil",
        3: "Tus Acciones",
        4: "4 Modelos Estocásticos",
        5: "Opciones",
        6: "Tu Portafolio",
    }
    label = step_titles.get(current_step, "Paso")
    kibo_b64 = get_kibo_image_base64()
    
    logo_inner = f'<img src="{kibo_b64}" class="mobile-logo-img" alt="Kibo" />' if kibo_b64 else 'K'

    st.markdown(
        f"""
        <div class="mobile-app-header">
            <div class="mobile-brand">
                <div class="mobile-logo-circle" title="Tócame para ver la bienvenida">
                    {logo_inner}
                </div>
                <div>
                    <div class="mobile-brand-title">Kibo</div>
                    <div class="mobile-brand-sub">Copiloto Inteligente de Finanzas</div>
                </div>
            </div>
            <div class="mobile-step-pill">
                Paso {current_step} de 6 · {label}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Stepper móvil minimalista de 6 pasos
    stepper_html = '<div class="mobile-stepper">'
    for i in range(1, 7):
        state = "active" if i == current_step else ("done" if i < current_step else "")
        stepper_html += f'<div class="mobile-step-dot {state}"></div>'
    stepper_html += '</div>'
    st.markdown(stepper_html, unsafe_allow_html=True)


def render_floating_kibo_button():
    kibo_b64 = get_kibo_image_base64()
    avatar_html = f'<img src="{kibo_b64}" class="kibo-face-img" alt="Kibo" />' if kibo_b64 else '🤖'

    st.markdown(
        f"""
        <div class="kibo-bubble" id="kibo-help-trigger" title="Toca aquí para activar la guía interactiva con foco">
            <div class="kibo-face-wrapper">
                {avatar_html}
            </div>
            <div>
                <strong>Kibo Guía</strong>
                <small>Tutorial interactivo</small>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -------------------------------------------------------------
# PASO 1: ¿Con cuánto dinero empezamos? (Capital)
# -------------------------------------------------------------
def step_1_capital():
    st.markdown(
        """
        <div class="step-eyebrow">PASO 1 · TU CAPITAL INICIAL</div>
        <h1 class="step-title">¿Con cuánto dinero empezamos?</h1>
        <p class="step-lead">Tú tienes el control. Elige el monto simulado para armar tu estrategia con cotizaciones reales.</p>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown("#### 💰 Capital a Simular (USD)")
        capital_input = st.number_input(
            "Capital a simular (USD)",
            min_value=1000.0,
            max_value=10000000.0,
            value=float(st.session_state.capital),
            step=5000.0,
            label_visibility="collapsed",
        )
        st.session_state.capital = capital_input

    # Botones rápidos de selección de monto
    st.markdown("<div style='font-size:0.78rem; font-weight:750; color:#8e9bb0; letter-spacing:0.06em; margin: 0.8rem 0 0.35rem;'>⚡ MONTOS RÁPIDOS:</div>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        if st.button("$10K", use_container_width=True):
            st.session_state.capital = 10000.0
            st.rerun()
    with c2:
        if st.button("$25K", use_container_width=True):
            st.session_state.capital = 25000.0
            st.rerun()
    with c3:
        if st.button("$50K", use_container_width=True):
            st.session_state.capital = 50000.0
            st.rerun()
    with c4:
        if st.button("$100K", use_container_width=True):
            st.session_state.capital = 100000.0
            st.rerun()
    with c5:
        if st.button("$250K", use_container_width=True):
            st.session_state.capital = 250000.0
            st.rerun()

    st.markdown(
        f"""
        <div class="safe-simulation-pill">
            <span style="font-size:1.4rem;">🛡️</span>
            <div>
                <strong>Laboratorio 100% Seguro</strong><br>
                Simularemos <strong>USD ${st.session_state.capital:,.0f}</strong> con precios reales de Wall Street. Cero dinero real en juego ni conexiones bancarias.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Continuar a Mi Perfil de Riesgo ➔", type="primary", use_container_width=True):
        set_step(2)


# -------------------------------------------------------------
# PASO 2: ¿Cuál es tu estilo frente al mercado? (Perfil)
# -------------------------------------------------------------
def step_2_risk_profile():
    st.markdown(
        """
        <div class="step-eyebrow">PASO 2 · TU PERFIL DE INVERSIONISTA</div>
        <h1 class="step-title">¿Cuál es tu estilo frente al mercado?</h1>
        <p class="step-lead">Dime cómo duermes mejor por las noches para que Kibo adapte las fórmulas matemáticas a tu medida.</p>
        """,
        unsafe_allow_html=True,
    )

    profile_options = {
        "Conservador": "🛡️ Modo Blindaje: Lo primero es no perder capital. Prefieres estabilidad y evitar sustos, aunque la ganancia sea moderada.",
        "Moderado": "⚖️ Modo Equilibrio: Crecimiento constante a buen ritmo, tolerando pequeños vaivenes normales del mercado.",
        "Agresivo": "🚀 Modo Alto Impacto: Buscas la máxima rentabilidad a largo plazo y no te asustan las caídas temporales de corto plazo.",
    }

    st.session_state.profile = st.radio(
        "Perfil de riesgo:",
        options=list(profile_options.keys()),
        index=list(profile_options.keys()).index(st.session_state.profile),
        format_func=lambda k: profile_options[k],
        label_visibility="collapsed",
    )

    # Parámetros del análisis
    with st.expander("⚙️ Parámetros del análisis"):
        st.caption("Configura el horizonte y el nivel de confianza para medir el riesgo.")
        col_h, col_c = st.columns(2)
        with col_h:
            st.session_state.horizon = st.selectbox(
                "Horizonte de proyección (días)",
                options=[5, 10, 20, 40],
                index=[5, 10, 20, 40].index(st.session_state.horizon) if st.session_state.horizon in [5, 10, 20, 40] else 1,
            )
        with col_c:
            st.session_state.confidence = st.selectbox(
                "Nivel de Confianza VaR",
                options=[95.0, 99.0],
                index=1,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    b_prev, b_next = st.columns([1, 1.4])
    with b_prev:
        st.button("⬅️ Volver a Capital", use_container_width=True, on_click=set_step, args=(1,))
    with b_next:
        st.button("Continuar a Elegir Empresas ➔", type="primary", use_container_width=True, on_click=set_step, args=(3,))


# -------------------------------------------------------------
# PASO 3: Armemos tu canasta de empresas (Universo y Diversificación)
# -------------------------------------------------------------
def step_3_assets_universe():
    st.markdown(
        """
        <div class="step-eyebrow">PASO 3 · UNIVERSO & DIVERSIFICACIÓN</div>
        <h1 class="step-title">Armemos tu canasta de empresas</h1>
        <p class="step-lead">Regla de oro de la inversión: <strong>"No pongas todos los huevos en la misma canasta"</strong>. Combinar sectores protege tu dinero ante crisis.</p>
        """,
        unsafe_allow_html=True,
    )

    available_tickers = sorted(list(set(list(SECTOR_MAP.keys()) + st.session_state.tickers)))
    selected = st.multiselect(
        "Acciones disponibles:",
        options=available_tickers,
        default=st.session_state.tickers,
        help="Escribe para buscar cualquier ticker de Wall Street.",
    )
    st.session_state.tickers = selected

    # Actualizar portafolio
    rows = []
    for t in selected:
        cur_sec = st.session_state.portfolio.loc[st.session_state.portfolio["Ticker"] == t, "Sector"].values
        sec = cur_sec[0] if len(cur_sec) > 0 else detect_sector(t)
        rows.append({"Ticker": t, "Sector": sec})
    st.session_state.portfolio = pd.DataFrame(rows)

    n_activos = len(selected)
    n_sectores = st.session_state.portfolio["Sector"].nunique() if n_activos > 0 else 0

    # Medidor de Diversificación visual sectorial
    target_sectors = 4
    gauge_pct = min(100, int((n_sectores / target_sectors) * 100))
    st.markdown(
        f"""
        <div class="diversification-gauge-card">
            <div class="gauge-header">
                <span class="gauge-title">🛡️ Medidor de Diversificación Kibo</span>
                <span class="gauge-score">{n_activos} acciones · {n_sectores} sectores</span>
            </div>
            <div class="gauge-bar-track">
                <div class="gauge-bar-fill" style="width: {gauge_pct}%;"></div>
            </div>
            <div style="font-size: 0.82rem; color: {'#34d399' if n_sectores >= 4 else '#f59e0b'}; font-weight: 600;">
                {'✅ ¡Diversificación blindada! Cubres suficientes sectores para proteger tu dinero.' if n_sectores >= 4 else '⚠️ Te recomendamos cubrir al menos 4 sectores diferentes (salud, tecnología, energía, etc.).'}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Descarga o sincronización transparente de cotizaciones
    if st.session_state.market_data is None:
        with st.spinner("Sincronizando 3 años de cotizaciones reales de Wall Street..."):
            prices, rets, stats_dict = download_market_data(st.session_state.tickers)
            st.session_state.market_data = {
                "prices": prices,
                "returns": rets,
                "stats": stats_dict,
            }

    st.markdown("<br>", unsafe_allow_html=True)
    b_prev, b_next = st.columns([1, 1.4])
    with b_prev:
        st.button("⬅️ Volver a Perfil", use_container_width=True, on_click=set_step, args=(2,))
    with b_next:
        st.button("Analizar con los Cerebros de Kibo ➔", type="primary", use_container_width=True, on_click=set_step, args=(4,))


# -------------------------------------------------------------
# PASO 4: Kibo analiza tus acciones (4 Modelos Estocásticos)
# -------------------------------------------------------------
def step_4_stochastic_models():
    st.markdown(
        """
        <div class="step-eyebrow">PASO 4 · LOS 4 CEREBROS MATEMÁTICOS</div>
        <h1 class="step-title">Kibo analiza tus acciones</h1>
        <p class="step-lead">Pusimos a competir 4 teorías matemáticas avanzadas (incluyendo Browniano Fraccionario y Exponente de Hurst) para predecir el comportamiento real de tus empresas sin engañarte.</p>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.market_data or st.session_state.market_data["returns"].empty:
        with st.spinner("Cargando historial de cotizaciones..."):
            prices, rets, stats_dict = download_market_data(st.session_state.tickers)
            st.session_state.market_data = {"prices": prices, "returns": rets, "stats": stats_dict}

    prices_df = st.session_state.market_data["prices"]
    returns_df = st.session_state.market_data["returns"]
    valid_tickers = [t for t in st.session_state.tickers if t in returns_df.columns]

    if not valid_tickers:
        st.error("No hay cotizaciones disponibles para los tickers seleccionados.")
        return

    active_ticker = st.selectbox(
        "🔎 Selecciona la acción a inspeccionar:",
        options=valid_tickers,
        index=0 if st.session_state.active_asset_tab not in valid_tickers else valid_tickers.index(st.session_state.active_asset_tab),
    )
    st.session_state.active_asset_tab = active_ticker

    with st.spinner(f"Simulando 5.000 trayectorias Monte Carlo para {active_ticker}..."):
        comp_results = compare_models_for_asset(
            active_ticker,
            prices_df[active_ticker],
            returns_df[active_ticker],
            horizon_days=st.session_state.horizon,
            n_paths=5000,
        )

    # Tarjeta del Veredicto Ganador
    winner_name = comp_results["winner"]
    st.markdown(
        f"""
        <div class="verdict-glass-card">
            <div class="verdict-badge">🏆 CEREBRO GANADOR PARA {active_ticker}</div>
            <div class="verdict-title">{winner_name}</div>
            <p class="verdict-desc">{comp_results['winner_reason']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Pestañas explicativas con gráficos
    t1, t2, t3, t4, t5 = st.tabs([
        "1. Mov. Browniano (GBM)",
        "2. Salto de Merton (MJD)",
        "3. Ornstein-Uhlenbeck (O-U)",
        "4. Browniano Fraccionario (fBm)",
        "5. Backtest Rolling (RMSE/MAPE)",
    ])

    with t1:
        st.caption("📈 **Movimiento Browniano**: Asume que el precio flota con tendencia continua y fluctuaciones normales.")
        st.plotly_chart(plot_stochastic_fan(comp_results["sim_gbm"], f"· {active_ticker}"), use_container_width=True)
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Retorno Anual (μ)", f"{comp_results['sim_gbm'].parameters['mu_annual']:.2%}")
        with c2:
            st.metric("Volatilidad Anual (σ)", f"{comp_results['sim_gbm'].parameters['sigma_annual']:.2%}")

    with t2:
        st.caption("⚡ **Salto de Merton**: Contempla noticias sorpresa, caídas repentinas y colas pesadas (cisnes negros).")
        st.plotly_chart(plot_stochastic_fan(comp_results["sim_mjd"], f"· {active_ticker}"), use_container_width=True)
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Saltos por año (λ)", f"{comp_results['sim_mjd'].parameters['lambda']:.1f}")
        with c2:
            st.metric("Caída media del salto", f"{comp_results['sim_mjd'].parameters['mu_j']:.2%}")

    with t3:
        st.caption("🧲 **Ornstein-Uhlenbeck**: Para empresas maduras o de energía que siempre tienden a volver a su precio medio histórico.")
        st.plotly_chart(plot_stochastic_fan(comp_results["sim_ou"], f"· {active_ticker}"), use_container_width=True)
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Precio Equilibrio", f"USD ${comp_results['sim_ou'].parameters['mu_ou_price']:.2f}")
        with c2:
            st.metric("Tiempo de retorno", f"{comp_results['sim_ou'].parameters['half_life_days']:.0f} días")

    with t4:
        st.caption("🌀 **Browniano Fraccionario (fBm)**: Detecta si la acción tiene memoria fractal de largo plazo (H > 0.5) o si revierte a la media.")
        st.plotly_chart(plot_stochastic_fan(comp_results["sim_fbm"], f"· {active_ticker}"), use_container_width=True)
        h_info = comp_results["hurst_info"]
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Exponente de Hurst (H)", f"{h_info['H']:.2f}")
        with c2:
            st.metric("Ajuste Fractal (R²)", f"{h_info['r_squared']:.1%}")
        with c3:
            st.metric("Régimen de Memoria", h_info['regime'])
        st.info(f"💡 **Diagnóstico Fractal de Kibo**: {h_info['interpretation']}")

    with t5:
        st.caption("🔄 **Evaluación Predictiva Rolling (GBM)**: Ventana móvil de 252 sesiones de calibración diaria. Compara el pronóstico condicional del modelo frente al pronóstico ingenuo de caminata aleatoria.")
        with st.spinner(f"Calculando evaluación rolling de 252 días para {active_ticker}..."):
            roll_res = run_gbm_rolling_evaluation(prices_df[active_ticker], active_ticker, window_train=252, horizon_H=1)
        
        if roll_res.get("success", False):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("RMSE GBM", f"${roll_res['rmse_gbm']:.2f}", delta=f"-${roll_res['rmse_naive'] - roll_res['rmse_gbm']:.2f} vs Ingenuo" if roll_res['rmse_gbm'] <= roll_res['rmse_naive'] else f"+${roll_res['rmse_gbm'] - roll_res['rmse_naive']:.2f}")
            with c2:
                st.metric("MAPE GBM", f"{roll_res['mape_gbm']:.2f}%")
            with c3:
                st.metric("Veredicto", "✅ Supera al Ingenuo" if roll_res["gbm_beats_naive"] else "⚖️ Paridad")
            
            if roll_res["gbm_beats_naive"]:
                st.info(
                    "💡 **Lectura Financiera**: El modelo matemático predice con mayor precisión el precio que simplemente suponer que el precio de mañana será igual al de hoy. "
                    f"Esto le permite a tu estrategia anticipar giros y calibrar mejor el riesgo de pérdida (respaldo cuantitativo: margen de error medio MAPE = {roll_res['mape_gbm']:.2f}%, superando al pronóstico ingenuo con una reducción del error RMSE de USD ${roll_res['rmse_naive'] - roll_res['rmse_gbm']:.2f})."
                )
            else:
                st.info(
                    "💡 **Lectura Financiera**: La acción exhibe un comportamiento altamente eficiente de corto plazo, donde el mejor pronóstico inmediato es el precio más reciente. "
                    f"Conviene apoyarse en diversificación y modelos de salto antes que en tendencias puras (respaldo cuantitativo: paridad estadística frente a caminata aleatoria ingenua con MAPE = {roll_res['mape_gbm']:.2f}% y RMSE = USD ${roll_res['rmse_gbm']:.2f})."
                )

            st.plotly_chart(plot_rolling_forecast_chart(roll_res), use_container_width=True)

            with st.expander("📊 Ver tabla comparativa rolling de todas tus acciones"):
                df_roll_table = run_multi_asset_rolling_table(prices_df, valid_tickers)
                st.dataframe(df_roll_table, use_container_width=True, hide_index=True)
        else:
            st.warning(roll_res.get("error", "No se pudo calcular la evaluación rolling."))

    st.markdown("<br>", unsafe_allow_html=True)
    b_prev, b_next = st.columns([1, 1.4])
    with b_prev:
        st.button("⬅️ Volver a Acciones", use_container_width=True, on_click=set_step, args=(3,))
    with b_next:
        st.button("Continuar a Opciones ➔", type="primary", use_container_width=True, on_click=set_step, args=(5,))


# -------------------------------------------------------------
# PASO 5: Test de Manada (Herding) & Eficiencia de Mercado (CCK 2000)
# -------------------------------------------------------------

def step_5_options():
    st.markdown("""<div class="step-eyebrow">PASO 5 · OPCIONES Y VALORACIÓN</div><h1 class="step-title">Explora y valora una opción</h1><p class="step-lead">Compara contratos listados con proyecciones y una prima calculada bajo medida neutral al riesgo.</p>""", unsafe_allow_html=True)
    prices_df = st.session_state.market_data["prices"]
    returns_df = st.session_state.market_data["returns"]
    tickers = [t for t in st.session_state.tickers if t in returns_df.columns]
    if not tickers:
        st.error("Primero selecciona acciones con historial válido.")
        return
    ticker = st.selectbox("Activo subyacente", tickers, key="option_ticker")
    parameters = calibrate_gbm(returns_df[ticker])
    spot = float(st.session_state.market_data["stats"].get(ticker, {}).get("raw_spot", prices_df[ticker].iloc[-1]))
    left, right = st.columns(2)
    with left:
        rate = st.number_input("Tasa libre de riesgo anual (%)", 0.0, 25.0, 4.0, 0.1) / 100
    with right:
        dividend = st.number_input("Dividendo continuo anual (%)", 0.0, 25.0, 0.0, 0.1) / 100
    st.caption(f"Spot sin ajustar: USD {spot:,.2f}. La proyección usa P; la prima CRR usa Q con drift r - q.")
    if st.button("Consultar contratos listados", type="primary", use_container_width=True):
        with st.spinner("Consultando cadena de opciones..."):
            st.session_state.option_result = get_option_candidates(ticker, spot, parameters["mu_annual"] - dividend, parameters["sigma_annual"])
    result = st.session_state.get("option_result")
    if result and result.get("success") and st.session_state.get("option_ticker") == ticker:
        candidates = result["candidates"]
        st.caption(f"Consulta registrada en UTC: {result['queried_at'].strftime('%Y-%m-%d %H:%M')}. Se muestran contratos cercanos a los cuantiles Q25, Q50 y Q75 para tres vencimientos.")
        st.dataframe(candidates, use_container_width=True, hide_index=True)
        labels = [f"{r['Tipo']} · K={r['Strike']:.2f} · {r['Vencimiento']} · {r['Cuantil GBM']}" for _, r in candidates.iterrows()]
        selected_index = st.selectbox("Contrato para valorar", range(len(labels)), format_func=lambda i: labels[i])
        contract = candidates.iloc[int(selected_index)]
        c1, c2, c3 = st.columns(3)
        with c1:
            style = st.selectbox("Estilo", ["Europea", "Americana"])
        with c2:
            steps = st.select_slider("Pasos CRR", options=[50, 100, 200, 400], value=200)
        with c3:
            terminal_cost = st.number_input("Costos al vencimiento (USD)", min_value=0.0, value=0.0, step=0.01)
        valuation = crr_price(spot, float(contract["Strike"]), float(contract["T (años)"]), rate, dividend, parameters["sigma_annual"], int(steps), contract["Tipo"], style)
        if not valuation["valid"]:
            st.error("Los parámetros no producen una probabilidad neutral al riesgo válida. Revisa tasa, dividendo, volatilidad y pasos.")
        else:
            sim_days = max(1, round(float(contract["T (años)"]) * 252))
            simulation = simulate_gbm(spot, parameters, horizon_days=sim_days, n_paths=5000, seed=42)
            ask = float(contract["Ask"]) if pd.notna(contract["Ask"]) and float(contract["Ask"]) > 0 else np.nan
            probabilities = contract_probabilities(simulation.paths[:, -1], float(contract["Strike"]), ask, rate, float(contract["T (años)"]), contract["Tipo"], terminal_cost) if np.isfinite(ask) else None
            mid = contract["Mid"]
            metrics = st.columns(4)
            metrics[0].metric("Prima CRR", f"USD {valuation['price']:,.2f}")
            metrics[1].metric("Mercado", f"USD {mid:,.2f}" if pd.notna(mid) else "Bid/ask no utilizable")
            metrics[2].metric("pQ", f"{valuation['p_q']:.4f}")
            metrics[3].metric("Prob. de ejercicio", f"{probabilities['exercise_probability']:.1%}" if probabilities else "Requiere ask")
            if probabilities:
                st.info(f"La probabilidad de beneficio al vencimiento es {probabilities['profit_probability']:.1%}; no equivale a la probabilidad de ejercicio. Utilidad media simulada: USD {probabilities['expected_profit']:,.2f} por acción.")
            if pd.notna(mid):
                delta = valuation["price"] - float(mid)
                st.caption(f"Diferencia frente al punto medio bid/ask: USD {delta:,.2f} ({delta / float(mid):.1%}). Una diferencia puede reflejar volatilidad histórica frente a implícita, liquidez, dividendos o estilo; no demuestra arbitraje.")
            st.plotly_chart(crr_convergence_chart(spot, float(contract["Strike"]), float(contract["T (años)"]), rate, dividend, parameters["sigma_annual"], contract["Tipo"], style), use_container_width=True)
            st.session_state.selected_option_export = pd.DataFrame([{"Ticker": ticker, "Spot sin ajustar": spot, "Contrato": contract["Contrato"], "Tipo": contract["Tipo"], "Vencimiento": contract["Vencimiento"], "Strike": contract["Strike"], "Bid": contract["Bid"], "Ask": contract["Ask"], "Prima CRR": valuation["price"], "pQ": valuation["p_q"], "Estilo": style, "Pasos": steps}])
    elif result and not result.get("success"):
        st.warning(result["error"])
    st.markdown("<br>", unsafe_allow_html=True)
    b_prev, b_next = st.columns([1, 1.4])
    with b_prev:
        st.button("⬅️ Volver a Proyecciones", use_container_width=True, on_click=set_step, args=(4,))
    with b_next:
        st.button("Ver mi portafolio ➔", type="primary", use_container_width=True, on_click=set_step, args=(6,))
# -------------------------------------------------------------
# PASO 6: Tu Portafolio y Plan de Compra Final (Wallet Luxury)
# -------------------------------------------------------------
def step_6_final_portfolio():
    st.markdown(
        """
        <div class="step-eyebrow">PASO 6 · TU RECETA DE INVERSIÓN FINAL</div>
        <h1 class="step-title">Tu plan de inversión inteligente</h1>
        <p class="step-lead">Aquí tienes la receta matemática exacta para comprar tus acciones minimizando el riesgo total.</p>
        """,
        unsafe_allow_html=True,
    )

    prices_df = st.session_state.market_data["prices"]
    returns_df = st.session_state.market_data["returns"]
    portfolio_df = st.session_state.portfolio

    alloc_res = compute_portfolio_allocation(
        st.session_state.capital,
        portfolio_df,
        returns_df,
        confidence=st.session_state.confidence,
        horizon_days=st.session_state.horizon,
        prices_df=prices_df,
    )

    if not alloc_res:
        st.error("No se pudo calcular la asignación del portafolio.")
        return

    df_alloc = alloc_res["allocation_df"]

    # KPI Grid de resumen ejecutivo de portafolio
    st.markdown(
        f"""
        <div class="kpi-wallet-grid">
            <div class="wallet-card">
                <div class="wallet-label">Capital Total Asignado</div>
                <div class="wallet-value">USD ${st.session_state.capital:,.0f}</div>
                <div class="wallet-sub">Perfil {st.session_state.profile}</div>
            </div>
            <div class="wallet-card">
                <div class="wallet-label">Riesgo Máx. Estimado (VaR 99%)</div>
                <div class="wallet-value">{alloc_res['var_portfolio_pct']:.2%}</div>
                <div class="wallet-sub">USD ${alloc_res['var_portfolio_usd']:,.2f} a {st.session_state.horizon}d</div>
            </div>
            <div class="wallet-card">
                <div class="wallet-label">Efectivo de Reserva</div>
                <div class="wallet-value">USD ${alloc_res['efectivo_residual']:,.2f}</div>
                <div class="wallet-sub">Por redondeo de acciones</div>
            </div>
            <div class="wallet-card">
                <div class="wallet-label">Optimización Cuadrática</div>
                <div class="wallet-value">{'Óptimo' if alloc_res['solver_success'] else 'Aproximado'}</div>
                <div class="wallet-sub">SLSQP Restringido</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Pestañas del Portafolio: Plan, 3 Métodos de VaR y Pruebas de Estrés
    tab_plan, tab_var_methods, tab_stress = st.tabs([
        "🛒 Plan de Compra",
        "🛡️ 3 Métodos de VaR & CVaR",
        "⚡ Pruebas de Estrés",
    ])

    with tab_plan:
        st.markdown("#### 🛒 Acciones a Comprar en Wall Street:")
        stock_rows_html = '<div class="stocks-plan-container">'
        for _, row in df_alloc.iterrows():
            t = row["Ticker"]
            sec = row["Sector"]
            shares = int(row["Acciones Enteras"])
            inv = float(row["Inversión Real (USD)"])
            pct = float(row["Peso Real"].replace("%", "")) if isinstance(row["Peso Real"], str) else float(row["Peso Real"]) * 100
            
            icon = "🍏" if t == "AAPL" else "💻" if t in ["MSFT", "NVDA"] else "🔍" if t == "GOOGL" else "🏦" if t == "JPM" else "⚡" if t == "XOM" else "💊" if t == "JNJ" else "💡"
            
            stock_rows_html += (
                f'<div class="stock-item-row">'
                f'<div class="stock-left">'
                f'<div class="stock-avatar">{icon}</div>'
                f'<div><div class="stock-name">{t}</div><div class="stock-sector">{sec}</div></div>'
                f'</div>'
                f'<div class="stock-right">'
                f'<div class="stock-shares">Compra {shares:,} accs</div>'
                f'<div class="stock-amount">USD ${inv:,.2f} ({pct:.1f}%)</div>'
                f'</div>'
                f'</div>'
            )
        stock_rows_html += '</div>'
        st.markdown(stock_rows_html, unsafe_allow_html=True)

        # Gráfico de asignación
        st.plotly_chart(plot_portfolio_allocation_chart(df_alloc), use_container_width=True)

        # Descarga CSV
        csv_bytes = df_alloc.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Descargar Plan de Inversión en CSV",
            data=csv_bytes,
            file_name="kibo_plan_inversion.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with tab_var_methods:
        st.caption("🛡️ **Comparativa de Estimadores de VaR y CVaR al 99%**: Medición multimetodológica a un horizonte de 10 días para evaluar la robustez frente a colas pesadas.")
        with st.spinner("Calculando VaR Histórico, Paramétrico y Monte Carlo (25.000 escenarios)..."):
            risk_res = compute_var_comparison_and_stress(
                capital=st.session_state.capital,
                weights=alloc_res["w_min_var"],
                returns_df=returns_df,
                sectors=df_alloc["Sector"].tolist(),
                tickers=df_alloc["Ticker"].tolist(),
                confidence=0.99,
                horizon_days=st.session_state.horizon,
                n_mc_sims=20000,
            )

        st.info(
            f"💡 **Diagnóstico de Pérdida Máxima**: Con un 99% de confianza, tu cartera no perderá más de "
            f"**USD ${risk_res['var_mc_usd']:,.2f}** ({risk_res['var_mc_pct']:.2%}) en las próximas 2 semanas de mercado normal. "
            f"Y en caso de un evento extremo dentro del 1% peor de la historia, la pérdida promedio esperada sería de **USD ${risk_res['cvar_mc_usd']:,.2f}** ({risk_res['cvar_mc_pct']:.2%}) "
            f"(respaldo cuantitativo: simulación Monte Carlo multivariada de 20.000 trayectorias con correlaciones de Cholesky y VaR paramétrico de USD ${risk_res['var_param_usd']:,.2f})."
        )
        st.dataframe(risk_res["var_comparison_df"], use_container_width=True, hide_index=True)
        st.plotly_chart(plot_var_distribution_hist(risk_res), use_container_width=True)

        with st.expander("📚 ¿Cuál es la diferencia entre los 3 métodos de VaR?"):
            st.markdown(
                """
                - **Normal (Paramétrico)**: Asume que las pérdidas siguen una campana de Gauss multivariada. Es muy rápido y elegante, pero suele subestimar las colas pesadas.
                - **Histórico**: Busca directamente en la historia empírica los peores bloques de 10 días que vivieron tus acciones. No hace supuestos teóricos.
                - **Monte Carlo Multivariado**: Simula 20.000 futuros simultáneos preservando la correlación real de Wall Street para encontrar el percentil de riesgo más conservador.
                """
            )

    with tab_stress:
        st.caption("⚡ **Pruebas de Estrés Financiero (Stress Testing)**: Simulación de crisis extremas de mercado, caídas sectoriales asimétricas y pérdida de diversificación.")
        if "risk_res" not in locals():
            risk_res = compute_var_comparison_and_stress(
                capital=st.session_state.capital,
                weights=alloc_res["w_min_var"],
                returns_df=returns_df,
                sectors=df_alloc["Sector"].tolist(),
                tickers=df_alloc["Ticker"].tolist(),
                confidence=0.99,
                horizon_days=st.session_state.horizon,
                n_mc_sims=20000,
            )

        st.warning(
            f"🛡️ **Resistencia ante Escenarios Extremos**: Si ocurriese un colapso en tu industria principal (**{risk_res['top_sector']}**), tu portafolio soportaría una pérdida estimada de "
            f"**USD ${risk_res['stress2_loss_usd']:,.2f}** ({risk_res['stress2_loss_pct']:.2%}). Gracias al límite de diversificación del 35%, el impacto queda acotado y preserva la mayor parte de tu capital "
            f"(respaldo cuantitativo: estrés sectorial del -20% en {risk_res['top_sector']} y -5% en las demás industrias; shock uniforme de mercado del -10% representaría USD ${risk_res['stress1_loss_usd']:,.2f})."
        )
        st.dataframe(risk_res["stress_df"], use_container_width=True, hide_index=True)

        with st.expander("💡 ¿Por qué es vital el Stress Testing?"):
            st.markdown(
                f"""
                El Value at Risk calcula lo que puede pasar en días normales. En cambio, las **Pruebas de Estrés** evalúan si tu patrimonio sobreviviría a una catástrofe financiera:
                1. **Caída uniforme**: Si el mercado entero cae un -10% de golpe.
                2. **Crisis en tu sector principal ({risk_res['top_sector']})**: Se desploma un -20% y el resto cae -5%.
                3. **Pánico de correlación**: La volatilidad sube un 50% y todas las acciones se mueven juntas ($\\\\rho = 0.80$), anulando la diversificación.
                """
            )

    st.markdown("<br>", unsafe_allow_html=True)
    b_prev, b_restart = st.columns([1, 1.4])
    with b_prev:
        st.button("⬅️ Volver a Test Manada", use_container_width=True, on_click=set_step, args=(5,))
    with b_restart:
        st.button("🔄 Iniciar Nueva Simulación", use_container_width=True, on_click=set_step, args=(1,))


# -------------------------------------------------------------
# APP MAIN
# -------------------------------------------------------------
def main():
    initialize_session_state()
    st.markdown(APP_CSS, unsafe_allow_html=True)

    # Animación Intro Splash de bienvenida (solo una vez por sesión o al tocar el logo)
    render_intro_splash_animation()

    # Cabecera de la app móvil
    render_mobile_header(st.session_state.step)

    if st.session_state.step == 1:
        step_1_capital()
    elif st.session_state.step == 2:
        step_2_risk_profile()
    elif st.session_state.step == 3:
        step_3_assets_universe()
    elif st.session_state.step == 4:
        step_4_stochastic_models()
    elif st.session_state.step == 5:
        step_5_options()
    elif st.session_state.step == 6:
        step_6_final_portfolio()

    # Inyección del tour interactivo con foco spotlight, difuminado y mascota 3D
    render_kibo_tour(st.session_state.step)
    render_floating_kibo_button()


if __name__ == "__main__":
    main()
