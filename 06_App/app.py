"""
Kibo · Plataforma Móvil Inteligente de Inversión y Gestión de Riesgo (Mobile-First)
Universidad Externado de Colombia · DEFI 2
Diseño Step-by-Step Mobile-First: Paleta Obsidiana, Esmeralda Financiero y Oro Champaña.
"""

import os
import sys
import io
from pathlib import Path
from datetime import date, timedelta
from typing import Dict, List, Optional, Any

# Blindaje de rutas absolutas para Streamlit Cloud, Docker y ejecución local
_APP_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _APP_DIR.parent
_SRC_DIR = _APP_DIR / "src"
_UI_DIR = _APP_DIR / "ui"

for p in [str(_SRC_DIR), str(_UI_DIR), str(_APP_DIR), str(_REPO_ROOT)]:
    while p in sys.path:
        sys.path.remove(p)
    sys.path.insert(0, p)

# Prevenir colisión de espacio de nombres con /mount/src en contenedores de Streamlit Cloud
if "src" in sys.modules:
    try:
        mod = sys.modules["src"]
        if not hasattr(mod, "__file__") or "06_App" not in getattr(mod, "__file__", ""):
            del sys.modules["src"]
    except Exception:
        pass

import numpy as np
import pandas as pd
import streamlit as st

# Importaciones con fallback tolerante a fallos de ruta en la nube
try:
    from src.data_engine import (
        DEFAULT_TICKERS,
        SECTOR_MAP,
        ALL_SECTORS,
        get_default_portfolio,
        detect_sector,
        download_market_data,
        load_market_data_from_csv,
        get_library_versions,
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
        run_out_of_sample_portfolio_audit,
        plot_var_distribution_hist,
        plot_out_of_sample_audit,
    )
    from src.options_engine import (
        get_option_candidates,
        crr_price,
        contract_probabilities,
        generate_crr_3step_tree,
        verify_crr_control_benchmark,
        crr_convergence_chart,
        black_scholes_price,
    )
    from src.rolling_engine import (
        run_gbm_rolling_evaluation,
        run_multi_asset_rolling_table,
        plot_rolling_forecast_chart,
    )
except (ImportError, ModuleNotFoundError):
    from data_engine import (
        DEFAULT_TICKERS,
        SECTOR_MAP,
        ALL_SECTORS,
        get_default_portfolio,
        detect_sector,
        download_market_data,
        load_market_data_from_csv,
        get_library_versions,
    )
    from stochastic_engine import (
        calibrate_gbm,
        simulate_gbm,
        calibrate_merton_jump,
        simulate_merton_jump,
        calibrate_ornstein_uhlenbeck,
        simulate_ornstein_uhlenbeck,
    )
    from model_comparison import compare_models_for_asset
    from portfolio_engine import compute_portfolio_allocation
    from herding_engine import (
        run_herding_analysis,
        plot_herding_scatter,
        plot_csad_timeline,
    )
    from risk_engine import (
        compute_var_comparison_and_stress,
        run_out_of_sample_portfolio_audit,
        plot_var_distribution_hist,
        plot_out_of_sample_audit,
    )
    from options_engine import (
        get_option_candidates,
        crr_price,
        contract_probabilities,
        generate_crr_3step_tree,
        verify_crr_control_benchmark,
        crr_convergence_chart,
        black_scholes_price,
    )
    from rolling_engine import (
        run_gbm_rolling_evaluation,
        run_multi_asset_rolling_table,
        plot_rolling_forecast_chart,
    )

try:
    from ui.styles import APP_CSS
    from ui.kibo_avatar import get_kibo_hero_banner, get_kibo_image_base64
    from ui.charts import (
        plot_stochastic_fan,
        plot_model_comparison_bars,
        plot_portfolio_allocation_chart,
        plot_option_payoff_and_profit,
        plot_sector_allocation_donut,
        plot_normalized_prices_chart,
        plot_correlation_heatmap,
    )
except (ImportError, ModuleNotFoundError):
    from styles import APP_CSS
    from kibo_avatar import get_kibo_hero_banner, get_kibo_image_base64
    from charts import (
        plot_stochastic_fan,
        plot_model_comparison_bars,
        plot_portfolio_allocation_chart,
        plot_option_payoff_and_profit,
        plot_sector_allocation_donut,
        plot_normalized_prices_chart,
        plot_correlation_heatmap,
    )

# Importación ultra segura de ui.tour con recarga forzada
try:
    import importlib
    try:
        import ui.tour as tour_module
    except (ImportError, ModuleNotFoundError):
        import tour as tour_module
    importlib.reload(tour_module)
    render_kibo_tour = getattr(tour_module, "render_kibo_tour")
    render_intro_splash_animation = getattr(tour_module, "render_intro_splash_animation")
except Exception:
    def render_kibo_tour(*args, **kwargs): pass
    def render_intro_splash_animation(*args, **kwargs): pass

# Importación del Diccionario Financiero de Kibo
try:
    try:
        from ui.kibo_dictionary import show_kibo_dictionary_dialog, render_kibo_dictionary_content
    except (ImportError, ModuleNotFoundError):
        from kibo_dictionary import show_kibo_dictionary_dialog, render_kibo_dictionary_content
except Exception:
    def show_kibo_dictionary_dialog(): pass
    def render_kibo_dictionary_content(): pass


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
    if "_last_profile_applied" not in st.session_state:
        st.session_state._last_profile_applied = None
    if "horizon" not in st.session_state:
        st.session_state.horizon = 10
    if "confidence" not in st.session_state:
        st.session_state.confidence = 99.0
    if "risk_budget" not in st.session_state:
        st.session_state.risk_budget = 7500.0
    if "tickers" not in st.session_state:
        st.session_state.tickers = list(DEFAULT_TICKERS)
    if "portfolio" not in st.session_state:
        st.session_state.portfolio = get_default_portfolio()
    if "market_data" not in st.session_state:
        st.session_state.market_data = None
    if "active_asset_tab" not in st.session_state:
        st.session_state.active_asset_tab = "AAPL"
    if "broker_cost_bps" not in st.session_state:
        st.session_state.broker_cost_bps = 10.0


def set_step(new_step: int):
    st.session_state.step = new_step
    st.rerun()


def render_mobile_header(current_step: int):
    step_titles = {
        1: "Tu Capital",
        2: "Tu Perfil",
        3: "Tus Acciones",
        4: "Cerebros Matemáticos",
        5: "Tu Seguro (Opciones)",
        6: "Tu Portafolio",
    }
    label = step_titles.get(current_step, "Paso")
    kibo_b64 = get_kibo_image_base64()
    logo_inner = f'<img src="{kibo_b64}" class="mobile-logo-img" alt="Kibo" />' if kibo_b64 else '🤖'

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

    # Stepper móvil minimalista de 6 pasos con puntos
    stepper_html = '<div class="mobile-stepper">'
    for i in range(1, 7):
        state = "active" if i == current_step else ("done" if i < current_step else "")
        stepper_html += f'<div class="mobile-step-dot {state}"></div>'
    stepper_html += '</div>'
    st.markdown(stepper_html, unsafe_allow_html=True)

    # Botones superiores de acceso rápido a Diccionario y Guía
    c_dict, c_tour = st.columns([1, 1])
    with c_dict:
        if st.button("📖 Diccionario Kibo", key=f"hdr_dict_{current_step}", use_container_width=True, help="Abre el traductor de jerga financiera a cristiano"):
            show_kibo_dictionary_dialog()
    with c_tour:
        if st.button("🚀 Guía de este paso", key=f"hdr_tour_{current_step}", use_container_width=True, help="Inicia el tutorial guiado interactivo de esta pantalla"):
            st.session_state["trigger_tour_now"] = True
            st.rerun()


def render_floating_kibo_button():
    kibo_b64 = get_kibo_image_base64()
    avatar_html = f'<img src="{kibo_b64}" class="kibo-face-img" alt="Kibo" />' if kibo_b64 else '🤖'

    st.markdown(
        f"""
        <div class="kibo-bubble" id="kibo-help-trigger" title="Tócame para abrir el Centro de Ayuda Kibo" style="cursor: pointer; pointer-events: auto;">
            <div class="kibo-face-wrapper">
                {avatar_html}
            </div>
            <div>
                <strong>Kibo</strong>
                <small>Guía y ayuda</small>
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

    # Botones rápidos de selección de monto estilo Nequi
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

    # Opciones avanzadas discretas
    with st.expander("⚙️ Opciones avanzadas (Presupuesto de Riesgo)", expanded=False):
        st.caption("Si deseas fijar un techo máximo de dinero en riesgo para la estrategia:")
        st.session_state.risk_budget = st.number_input(
            "Presupuesto de Riesgo Máximo (V_bar en USD):",
            min_value=500.0,
            value=float(st.session_state.risk_budget),
            step=500.0,
            help="Cota máxima de pérdida tolerada para el portafolio según el presupuesto de riesgo asignado."
        )

    st.markdown("<br>", unsafe_allow_html=True)
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
        index=list(profile_options.keys()).index(st.session_state.profile) if st.session_state.profile in profile_options else 1,
        format_func=lambda k: profile_options[k],
        label_visibility="collapsed",
    )

    # Aplicar valores sugeridos solo al cambiar el perfil; así se conservan los ajustes manuales.
    if st.session_state.profile != st.session_state._last_profile_applied:
        if st.session_state.profile == "Conservador":
            st.session_state.confidence = 99.0
            st.session_state.risk_budget = min(st.session_state.risk_budget, st.session_state.capital * 0.05)
        elif st.session_state.profile == "Moderado":
            st.session_state.confidence = 99.0
            st.session_state.risk_budget = min(st.session_state.risk_budget, st.session_state.capital * 0.075)
        elif st.session_state.profile == "Agresivo":
            st.session_state.confidence = 95.0
            st.session_state.risk_budget = min(st.session_state.risk_budget, st.session_state.capital * 0.12)
        st.session_state._last_profile_applied = st.session_state.profile

    # Opciones avanzadas discretas
    with st.expander("⚙️ Opciones avanzadas (Horizonte y Confianza Estadística)", expanded=False):
        st.caption("Configura el horizonte temporal y la confianza del Value at Risk (VaR):")
        col_h, col_c = st.columns(2)
        with col_h:
            st.session_state.horizon = st.selectbox(
                "Horizonte de riesgo (días):",
                options=[5, 10, 20, 40],
                index=[5, 10, 20, 40].index(st.session_state.horizon) if st.session_state.horizon in [5, 10, 20, 40] else 1,
            )
        with col_c:
            st.session_state.confidence = st.selectbox(
                "Nivel de Confianza VaR:",
                options=[95.0, 99.0],
                index=0 if float(st.session_state.confidence) == 95.0 else 1,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    b_prev, b_next = st.columns([1, 1.4])
    with b_prev:
        st.button("⬅️ Volver a Capital", use_container_width=True, on_click=set_step, args=(1,))
    with b_next:
        st.button("Continuar a Elegir Empresas ➔", type="primary", use_container_width=True, on_click=set_step, args=(3,))


# -------------------------------------------------------------
# PASO 3: Armemos tu canasta de empresas (Universo & Diversificación)
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
        "Acciones disponibles en Wall Street (USD):",
        options=available_tickers,
        default=st.session_state.tickers,
        help="Escribe para buscar cualquier acción líder del mercado estadounidense.",
    )
    if selected != st.session_state.tickers and len(selected) >= 2:
        st.session_state.tickers = selected
        st.session_state.portfolio = pd.DataFrame({
            "Ticker": selected,
            "Sector": [SECTOR_MAP.get(t, detect_sector(t)) for t in selected]
        })
        st.session_state.market_data = None

    n_activos = len(st.session_state.tickers)
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
                {'✅ ¡Diversificación blindada! Cubres al menos 4 sectores diferentes de la economía.' if n_sectores >= 4 else '⚠️ Te recomendamos cubrir al menos 4 sectores diferentes (salud, tecnología, energía, etc.).'}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Descarga o sincronización transparente de cotizaciones
    if st.session_state.market_data is None:
        with st.spinner("Sincronizando cotizaciones oficiales de Wall Street..."):
            prices, rets, stats_dict = download_market_data(st.session_state.tickers)
            st.session_state.market_data = {
                "prices": prices,
                "returns": rets,
                "stats": stats_dict,
            }

    # Opciones avanzadas discretas
    with st.expander("⚙️ Opciones avanzadas (Personalizar sectores de tus acciones)", expanded=False):
        st.caption("Si deseas cambiar el sector económico asignado a alguna de tus acciones:")
        portfolio_df = st.session_state.portfolio.copy()

        c_tick, c_sec = st.columns([1, 1.2])
        with c_tick:
            reclass_ticker = st.selectbox(
                "Acción a modificar:",
                options=st.session_state.tickers,
                key="reclass_ticker_select",
            )

        current_sector = "Tecnología"
        if not portfolio_df.empty and reclass_ticker in portfolio_df["Ticker"].values:
            current_sector = str(portfolio_df.loc[portfolio_df["Ticker"] == reclass_ticker, "Sector"].values[0])

        all_possible_sectors = [
            "Tecnología",
            "Consumo Discrecional",
            "Consumo Básico",
            "Salud",
            "Servicios Financieros",
            "Energía",
            "Industrial",
            "Comunicaciones",
            "Materiales",
            "Inmobiliario",
            "Servicios Públicos",
        ]
        if current_sector not in all_possible_sectors:
            all_possible_sectors.insert(0, current_sector)

        with c_sec:
            new_sector = st.selectbox(
                "Nuevo sector asignado:",
                options=all_possible_sectors,
                index=all_possible_sectors.index(current_sector) if current_sector in all_possible_sectors else 0,
                key="reclass_sector_select",
            )

        if st.button("💾 Guardar y Aplicar Cambio de Sector", use_container_width=True, key="apply_reclass_btn"):
            if new_sector != current_sector:
                portfolio_df.loc[portfolio_df["Ticker"] == reclass_ticker, "Sector"] = new_sector
                st.session_state.portfolio = portfolio_df
                st.success(f"✅ {reclass_ticker} reclasificado al sector '{new_sector}'.")
                st.rerun()
            else:
                st.info(f"{reclass_ticker} ya está asignado al sector '{current_sector}'.")

    st.markdown("<br>", unsafe_allow_html=True)
    b_prev, b_next = st.columns([1, 1.4])
    with b_prev:
        st.button("⬅️ Volver a Perfil", use_container_width=True, on_click=set_step, args=(2,))
    with b_next:
        st.button("Analizar con los Cerebros de Kibo ➔", type="primary", use_container_width=True, on_click=set_step, args=(4,))


# -------------------------------------------------------------
# PASO 4: Kibo analiza tus acciones (4 Modelos Estocásticos & Manada)
# -------------------------------------------------------------
def step_4_stochastic_models():
    st.markdown(
        """
        <div class="step-eyebrow">PASO 4 · LOS CEREBROS MATEMÁTICOS</div>
        <h1 class="step-title">Kibo analiza tus acciones</h1>
        <p class="step-lead">Pusimos a competir 4 teorías matemáticas avanzadas para predecir el comportamiento real de tus empresas sin engañarte.</p>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.market_data or st.session_state.market_data["returns"].empty:
        with st.spinner("Cargando historial de cotizaciones..."):
            prices, rets, stats_dict = download_market_data(st.session_state.tickers)
            st.session_state.market_data = {"prices": prices, "returns": rets, "stats": stats_dict}

    prices_df = st.session_state.market_data["prices"]
    returns_df = st.session_state.market_data["returns"]
    stats_dict = st.session_state.market_data["stats"]
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

    with st.spinner(f"Simulando 5.000 trayectorias para {active_ticker}..."):
        comp_results = compare_models_for_asset(
            active_ticker,
            prices_df[active_ticker],
            returns_df[active_ticker],
            horizon_days=st.session_state.horizon,
            n_paths=5000,
        )

    # Tarjeta amigable del Veredicto Ganador
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

    # Pestañas pedagógicas amigables
    t1, t2, t3, t4, t5, t6 = st.tabs([
        "1. Difusión (GBM)",
        "2. Saltos (Merton)",
        "3. Reversión (O-U)",
        "4. Memoria (fBm)",
        "5. Manada (CCK)",
        "6. Examen Histórico",
    ])

    with t1:
        st.caption("📈 **Movimiento Browniano (GBM)**: Simula miles de futuros posibles asumiendo que el precio flota con tendencia y volatilidad continua.")
        st.plotly_chart(plot_stochastic_fan(comp_results["sim_gbm"], f"· {active_ticker}"), use_container_width=True)
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Rendimiento Anual (μ)", f"{comp_results['sim_gbm'].parameters['mu_annual']:.2%}")
        with c2:
            st.metric("Volatilidad Anual (σ)", f"{comp_results['sim_gbm'].parameters['sigma_annual']:.2%}")

    with t2:
        st.caption("⚡ **Salto de Merton (MJD)**: Contempla noticias sorpresa, anuncios de balances o caídas repentinas provocadas por eventos inesperados.")
        st.plotly_chart(plot_stochastic_fan(comp_results["sim_mjd"], f"· {active_ticker}"), use_container_width=True)
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Saltos por año (λ)", f"{comp_results['sim_mjd'].parameters['lambda']:.1f}")
        with c2:
            st.metric("Caída media del salto", f"{comp_results['sim_mjd'].parameters['mu_j']:.2%}")

    with t3:
        st.caption("🧲 **Ornstein-Uhlenbeck (O-U)**: Modela si el precio tiende a regresar a su costo histórico promedio de largo plazo.")
        # Guardrail inteligente amigable
        if active_ticker in ["NVDA", "AAPL", "MSFT", "AMZN", "GOOGL"]:
            st.warning(
                f"💡 **Consejo de Kibo**: Para empresas de innovación tecnológica como **{active_ticker}**, "
                "este modelo no es el ideal porque asume que la acción no crecerá y volverá al pasado. "
                "Para este activo es mucho mejor usar Difusión (GBM) o Saltos (Merton)."
            )
        st.plotly_chart(plot_stochastic_fan(comp_results["sim_ou"], f"· {active_ticker}"), use_container_width=True)
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Precio de Equilibrio", f"USD ${comp_results['sim_ou'].parameters['mu_ou_price']:.2f}")
        with c2:
            st.metric("Tiempo de Retorno", f"{comp_results['sim_ou'].parameters['half_life_days']:.0f} días")

    with t4:
        st.caption("🌀 **Browniano Fraccionario (fBm)**: Evalúa si la acción tiene memoria de largo plazo o inercia de tendencia.")
        st.plotly_chart(plot_stochastic_fan(comp_results["sim_fbm"], f"· {active_ticker}"), use_container_width=True)
        h_info = comp_results["hurst_info"]
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Exponente Hurst (H)", f"{h_info['H']:.2f}")
        with c2:
            st.metric("Ajuste R²", f"{h_info['r_squared']:.1%}")
        with c3:
            st.metric("Régimen", h_info['regime'])
        st.info(f"💡 **Explicación sencilla**: {h_info['interpretation']}")

    with t5:
        st.caption("🐑 **Diagnóstico de Efecto Manada (CCK 2000)**: Evalúa si en momentos de estrés los inversores se asustan y corren todos en estampida.")
        h_res = run_herding_analysis(returns_df)
        if h_res.get("success"):
            v_badge = h_res["verdict_badge"]
            v_text = h_res["verdict"]
            v_color = h_res["verdict_color"]
            st.markdown(
                f"""
                <div style="background:#0f1420; border-left:4px solid {v_color}; border-radius:10px; padding:0.9rem 1.1rem; margin-bottom:0.8rem;">
                    <div style="font-size:0.75rem; font-weight:700; color:{v_color}; text-transform:uppercase;">{v_badge}</div>
                    <div style="font-size:1.15rem; font-weight:800; color:#f8fafc; margin:0.2rem 0 0.4rem;">{v_text}</div>
                    <div style="font-size:0.85rem; color:#cbd5e1; line-height:1.4;">{h_res['explanation']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.plotly_chart(plot_herding_scatter(h_res), use_container_width=True)
        else:
            st.warning("No se pudo calcular el diagnóstico de manada.")

    with t6:
        st.caption("🔄 **Examen Histórico (Rolling Backtest de 252 días)**: Ponemos a prueba el modelo día por día en el pasado real.")
        roll_res = run_gbm_rolling_evaluation(prices_df[active_ticker], active_ticker, window_train=252, horizon_H=1)
        if roll_res.get("success", False):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Error Típico RMSE", f"${roll_res['rmse_gbm']:.2f}")
            with c2:
                st.metric("Margen de Error MAPE", f"{roll_res['mape_gbm']:.2f}%")
            with c3:
                st.metric("Veredicto Kibo", "✅ Precisión Aprobada" if roll_res["gbm_beats_naive"] else "⚖️ Paridad")
            st.plotly_chart(plot_rolling_forecast_chart(roll_res), use_container_width=True)
        else:
            st.warning("No se pudo calcular el examen histórico.")

    # Opciones avanzadas discretas
    with st.expander("⚙️ Opciones avanzadas (Parámetros cuantitativos y criterios AIC/BIC)", expanded=False):
        st.caption("Parámetros cuantitativos calibrados y criterios de selección AIC / BIC:")
        if "parameters_table" in stats_dict:
            st.dataframe(stats_dict["parameters_table"], use_container_width=True, hide_index=True)
        df_bars = comp_results.get("models_table", comp_results.get("comparison_df"))
        if df_bars is not None:
            st.plotly_chart(plot_model_comparison_bars(df_bars), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    b_prev, b_next = st.columns([1, 1.4])
    with b_prev:
        st.button("⬅️ Volver a Acciones", use_container_width=True, on_click=set_step, args=(3,))
    with b_next:
        st.button("Continuar a Tu Seguro (Opciones) ➔", type="primary", use_container_width=True, on_click=set_step, args=(5,))


# -------------------------------------------------------------
# PASO 5: Tu Seguro de Inversión (Opciones Reales & CRR)
# -------------------------------------------------------------
def step_5_options():
    st.markdown(
        """
        <div class="step-eyebrow">PASO 5 · TU SEGURO DE INVERSIÓN</div>
        <h1 class="step-title">Protégete con una opción</h1>
        <p class="step-lead">Una opción es como el seguro de un carro: pagas una prima pequeña para protegerte de una pérdida gigante en la bolsa.</p>
        """,
        unsafe_allow_html=True,
    )

    prices_df = st.session_state.market_data["prices"]
    returns_df = st.session_state.market_data["returns"]
    stats_dict = st.session_state.market_data["stats"]
    tickers = [t for t in st.session_state.tickers if t in returns_df.columns]

    if not tickers:
        st.error("Selecciona acciones válidas primero.")
        return

    ticker = st.selectbox("Activo a proteger:", tickers, key="option_ticker")
    t_stat = stats_dict.get(ticker, {})
    spot = float(t_stat.get("raw_spot", prices_df[ticker].iloc[-1]))
    sigma = float(t_stat.get("sigma_annual", 0.25))
    mu_spot = float(t_stat.get("a_spot_drift", 0.10))

    if st.button("🔎 Buscar Seguros (Opciones) Disponibles en Wall Street", type="primary", use_container_width=True):
        with st.spinner("Consultando contratos reales de Wall Street..."):
            st.session_state.option_result = get_option_candidates(ticker, spot, mu_spot, sigma)

    result = st.session_state.get("option_result")
    if result and result.get("success") and st.session_state.get("option_ticker") == ticker:
        candidates = result["candidates"]
        st.caption("Contratos reales más cercanos a los escenarios del modelo:")
        st.dataframe(candidates, use_container_width=True, hide_index=True)

        labels = [f"{r['Tipo']} · Strike ${r['Strike (K)']:.2f} · {r['Vencimiento']} · {r['Cuantil GBM']}" for _, r in candidates.iterrows()]
        sel_idx = st.selectbox("Elige un seguro para analizar:", range(len(labels)), format_func=lambda i: labels[i])
        contract = candidates.iloc[int(sel_idx)]

        t_years = float(contract["T (años)"])
        k_val = float(contract["Strike (K)"])
        opt_type = str(contract["Tipo"])
        ask_val = float(contract["Ask"]) if pd.notna(contract["Ask"]) and float(contract["Ask"]) > 0 else np.nan
        mid_val = float(contract["Mid"]) if pd.notna(contract["Mid"]) else np.nan

        # Valoración con árbol CRR
        val_crr = crr_price(spot, k_val, t_years, rate=0.04, dividend_yield=0.0, sigma=sigma, steps=200, option_type=opt_type, style="Europea")

        if val_crr["valid"]:
            # Probabilidades en lenguaje sencillo
            premium_per_share = ask_val if np.isfinite(ask_val) and ask_val > 0 else val_crr["price"]
            sim_opt = simulate_gbm(spot, {"mu_annual": mu_spot, "sigma_annual": sigma, "log_likelihood": 0, "aic": 0, "bic": 0}, horizon_days=max(1, round(t_years * 252)), n_paths=5000, seed=42)
            prob_res = contract_probabilities(sim_opt.paths[:, -1], k_val, premium_per_share, 0.04, t_years, opt_type, 0.0)

            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Costo del Seguro (Prima)", f"${val_crr['price']:.2f}")
            with c2:
                st.metric("Prob. de Ganar Dinero", f"{prob_res['profit_probability']:.1%}")
            with c3:
                st.metric("Ganancia Media Esperada", f"${prob_res['expected_profit']:+.2f}")

            # Gráfico de Payoff y Beneficio Neto
            st.plotly_chart(plot_option_payoff_and_profit(spot, k_val, premium_per_share, 0.04, t_years, opt_type, 0.0), use_container_width=True)

            # Simulador interactivo de escenarios: actualiza el resultado al mover el control.
            st.markdown("##### 🛡️ Simulador de escenarios (100 acciones + 1 contrato):")
            sim_drop = st.slider(
                f"Variación simulada del precio de {ticker} (%):",
                min_value=-40,
                max_value=40,
                value=-15,
                step=5,
                key="protection_price_change",
            )
            s_future = spot * (1.0 + sim_drop / 100.0)
            shares = 100
            stock_pnl = shares * (s_future - spot)
            option_payoff_per_share = (
                max(k_val - s_future, 0.0) if opt_type == "Put"
                else max(s_future - k_val, 0.0)
            )
            option_pnl = shares * (option_payoff_per_share - premium_per_share)
            combined_pnl = stock_pnl + option_pnl

            st.caption(
                f"Precio simulado: **${s_future:,.2f}** por acción "
                f"({sim_drop:+d}%); prima usada: **${premium_per_share:.2f}** por acción."
            )
            metric_stock, metric_option, metric_combined = st.columns(3)
            metric_stock.metric("Resultado de las acciones", f"${stock_pnl:+,.2f}")
            metric_option.metric("Resultado neto de la opción", f"${option_pnl:+,.2f}")
            metric_combined.metric("Resultado combinado", f"${combined_pnl:+,.2f}")

            if opt_type == "Put":
                st.info("El Put compensa parte de la caída cuando el precio termina por debajo del strike; la prima se descuenta del resultado.")
            else:
                st.info("El Call aporta valor cuando el precio termina por encima del strike; la prima se descuenta del resultado.")

            # Opciones avanzadas discretas
            with st.expander("⚙️ Opciones avanzadas (Árbol binomial de 3 pasos y test de control)", expanded=False):
                st.caption("Diagrama interactivo del árbol binomial CRR de 3 pasos:")
                fig_tree, df_nodes = generate_crr_3step_tree(spot, k_val, t_years, 0.04, 0.0, sigma, opt_type, "Europea")
                st.plotly_chart(fig_tree, use_container_width=True)
                st.dataframe(df_nodes, use_container_width=True, hide_index=True)

                st.caption("Referencia de calibración teórica ($10.4506):")
                bench = verify_crr_control_benchmark()
                st.write(f"- Teórico exigido: USD ${bench['target']:.4f}")
                st.write(f"- CRR 200 pasos: USD ${bench['crr_200']:.4f}")
                st.write(f"- Estado: {'✅ Aprobado' if bench['passed'] else 'X Error'}")

    st.markdown("<br>", unsafe_allow_html=True)
    b_prev, b_next = st.columns([1, 1.4])
    with b_prev:
        st.button("⬅️ Volver a Modelos", use_container_width=True, on_click=set_step, args=(4,))
    with b_next:
        st.button("Ver Mi Portafolio Final ➔", type="primary", use_container_width=True, on_click=set_step, args=(6,))


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
        risk_budget_v=st.session_state.risk_budget,
    )

    if not alloc_res:
        st.error("No se pudo calcular la asignación del portafolio.")
        return

    df_alloc = alloc_res["allocation_df"]
    risk_capital = float(alloc_res["total_invertido_acciones"])
    if risk_capital > 0:
        risk_weights = df_alloc["Inversión Real (USD)"].astype(float).to_numpy() / risk_capital
    else:
        # Si el capital no alcanza para comprar acciones enteras, mostramos el escenario planeado.
        risk_capital = float(alloc_res["capital_riesgoso"])
        risk_weights = np.asarray(alloc_res["w_min_var"], dtype=float)

    # KPI Grid de billetera estilo Fintech (Nu / Nequi)
    st.markdown(
        f"""
        <div class="kpi-wallet-grid">
            <div class="wallet-card">
                <div class="wallet-label">Capital Total Asignado</div>
                <div class="wallet-value">USD ${st.session_state.capital:,.0f}</div>
                <div class="wallet-sub">Perfil {st.session_state.profile}</div>
            </div>
            <div class="wallet-card">
                <div class="wallet-label">VaR Estimado de la Posición ({int(round(float(st.session_state.confidence)))}%)</div>
                <div class="wallet-value">{alloc_res['var_efectivo_pct']:.2%}</div>
                <div class="wallet-sub">USD ${alloc_res['var_efectivo_usd']:,.2f} a {st.session_state.horizon}d</div>
            </div>
            <div class="wallet-card">
                <div class="wallet-label">Efectivo de Reserva</div>
                <div class="wallet-value">USD ${alloc_res['efectivo_residual_redondeo']:,.2f}</div>
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

    # Pestañas amigables del Portafolio
    tab_plan, tab_var, tab_stress, tab_oos, tab_export = st.tabs([
        "🛒 Plan de Compra",
        "🛡️ Riesgo & VaR",
        "⚡ Pruebas de Estrés",
        "📈 Examen Histórico",
        "📦 Descargas",
    ])

    with tab_plan:
        st.markdown("#### 🛒 Acciones a Comprar en Wall Street:")
        stock_rows_html = '<div class="stocks-plan-container">'
        for _, row in df_alloc.iterrows():
            t = row["Ticker"]
            sec = row["Sector"]
            shares = int(row["Acciones Enteras"])
            inv = float(row["Inversión Real (USD)"])
            pct = float(row["Peso Real (%)"].replace("%", "")) if isinstance(row["Peso Real (%)"], str) else float(row["Peso Real (%)"]) * 100

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

        # Gráficos de apoyo
        st.plotly_chart(plot_portfolio_allocation_chart(df_alloc), use_container_width=True)
        st.plotly_chart(plot_sector_allocation_donut(alloc_res["sector_summary"]), use_container_width=True)

    with tab_var:
        st.caption("🛡️ **Medición de Riesgo (Value at Risk)**: Estimación para el horizonte y nivel de confianza elegidos.")
        risk_res = compute_var_comparison_and_stress(
            capital=risk_capital,
            weights=risk_weights,
            returns_df=returns_df,
            sectors=df_alloc["Sector"].tolist(),
            tickers=df_alloc["Ticker"].tolist(),
            confidence=st.session_state.confidence / 100.0,
            horizon_days=st.session_state.horizon,
            n_mc_sims=20000,
        )

        st.info(
            f"💡 **En cristiano**: Para un horizonte de {st.session_state.horizon} días y un nivel de confianza de "
            f"{int(round(float(st.session_state.confidence)))}%, el VaR estimado es **USD ${risk_res['var_mc_usd']:,.2f}** "
            f"({risk_res['var_mc_pct']:.2%}). No es una pérdida máxima garantizada. "
            f"El CVaR estima la pérdida media en los escenarios que superan ese VaR: **USD ${risk_res['cvar_mc_usd']:,.2f}**."
        )
        st.dataframe(risk_res["var_comparison_df"], use_container_width=True, hide_index=True)
        st.plotly_chart(plot_var_distribution_hist(risk_res), use_container_width=True)

    with tab_stress:
        st.caption("⚡ **Pruebas de Estrés**: ¿Tu dinero sobreviviría a una catástrofe financiera?")
        if "risk_res" not in locals():
            risk_res = compute_var_comparison_and_stress(
                capital=risk_capital,
                weights=risk_weights,
                returns_df=returns_df,
                sectors=df_alloc["Sector"].tolist(),
                tickers=df_alloc["Ticker"].tolist(),
                confidence=st.session_state.confidence / 100.0,
                horizon_days=st.session_state.horizon,
                n_mc_sims=20000,
            )

        st.warning(
            f"🛡️ **Resistencia probada**: Si tu sector principal (**{risk_res['top_sector']}**) sufriera una crisis de -20%, "
            f"tu pérdida se mantendría contenida en **USD ${risk_res['stress2_loss_usd']:,.2f}** ({risk_res['stress2_loss_pct']:.2%}) "
            "gracias al límite de concentración del 35% que protege tu patrimonio."
        )
        st.dataframe(risk_res["stress_df"], use_container_width=True, hide_index=True)

    with tab_oos:
        st.caption(f"📈 **Evaluación Histórica (252 días)**: Estimamos cómo se habría comportado la posición invertida de USD ${risk_capital:,.2f} durante el último año de mercado.")
        oos_res = run_out_of_sample_portfolio_audit(
            prices_df=prices_df,
            returns_df=returns_df,
            weights=risk_weights,
            tickers=df_alloc["Ticker"].tolist(),
            capital=risk_capital,
            test_sessions=252,
            confidence=st.session_state.confidence / 100.0,
            cost_bps=st.session_state.broker_cost_bps,
        )
        st.dataframe(oos_res["summary_table"], use_container_width=True, hide_index=True)
        st.plotly_chart(plot_out_of_sample_audit(oos_res), use_container_width=True)

    with tab_export:
        st.caption("📦 **Descarga tus reportes**: Guarda tu plan de compra o el informe cuantitativo completo.")
        csv_plan = df_alloc.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Descargar Solo Plan de Compras (CSV)",
            data=csv_plan,
            file_name="kibo_plan_compras.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary",
        )

        # Buffer consolidado oficial
        out_buf = io.StringIO()
        out_buf.write(f"# REPORTE CUANTITATIVO KIBO\n# Capital: USD {st.session_state.capital:,.2f} | Fecha: {date.today().isoformat()}\n\n")
        out_buf.write("## 1. ASIGNACION DE CAPITAL Y ACCIONES ENTERAS\n")
        df_alloc.to_csv(out_buf, index=False)
        out_buf.write("\n## 2. METODOS DE VAR Y CVAR\n")
        risk_res["var_comparison_df"].to_csv(out_buf, index=False)
        out_buf.write("\n## 3. PRUEBAS DE ESTRES\n")
        risk_res["stress_df"].to_csv(out_buf, index=False)
        out_buf.write("\n## 4. AUDITORIA FUERA DE MUESTRA Y KUPIEC\n")
        oos_res["summary_table"].to_csv(out_buf, index=False)

        st.download_button(
            "📥 Descargar Informe Cuantitativo Completo (CSV)",
            data=out_buf.getvalue().encode("utf-8"),
            file_name=f"kibo_informe_cuantitativo_{date.today().isoformat()}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    b_prev, b_restart = st.columns([1, 1.4])
    with b_prev:
        st.button("⬅️ Volver a Opciones", use_container_width=True, on_click=set_step, args=(5,))
    with b_restart:
        st.button("🔄 Iniciar Nueva Simulación", use_container_width=True, on_click=set_step, args=(1,))


# -------------------------------------------------------------
# APP MAIN
# -------------------------------------------------------------
def main():
    initialize_session_state()
    st.markdown(APP_CSS, unsafe_allow_html=True)

    # Pantalla de bienvenida con intro cinematográfica Kibo
    render_intro_splash_animation()

    # Cabecera minimalista móvil
    render_mobile_header(st.session_state.step)

    # Navegación del asistente paso a paso
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

    # Tutorial spotlight guiado interactivo de Kibo y botón flotante
    force_tour = st.session_state.pop("trigger_tour_now", False)
    render_kibo_tour(st.session_state.step, force_trigger=force_tour)
    render_floating_kibo_button()


if __name__ == "__main__":
    main()
