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
        5: "Test Manada (Herding)",
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
        get_kibo_hero_banner(
            title="¡Hola! Soy Kibo 🚀",
            subtitle="Empecemos por lo básico: ¿cuánto dinero simulado quieres poner a prueba hoy?",
        ),
        unsafe_allow_html=True,
    )

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

    # Botones rápidos estilo Nequi / Nu
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

    # Parámetros técnicos del taller en acordeón discreto
    with st.expander("⚙️ Parámetros técnicos del taller (Avanzado)"):
        st.caption("Valores estándar del curso: proyección VaR al 99% de confianza y horizonte de 10 días hábiles.")
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

    # Medidor de Diversificación visual (estilo eToro Luxury)
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

    with st.spinner(f"Simulando 3.000 trayectorias Monte Carlo para {active_ticker}..."):
        comp_results = compare_models_for_asset(
            active_ticker,
            prices_df[active_ticker],
            returns_df[active_ticker],
            horizon_days=st.session_state.horizon,
            n_paths=3000,
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
        st.caption("🔄 **Evaluación Rolling del GBM (Paso 13 del PDF)**: Ventana móvil de 252 sesiones de calibración diaria. Compara el pronóstico condicional del GBM contra el pronóstico ingenuo.")
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
        st.button("Continuar al Test de Manada (Herding) ➔", type="primary", use_container_width=True, on_click=set_step, args=(5,))


# -------------------------------------------------------------
# PASO 5: Test de Manada (Herding) & Eficiencia de Mercado (CCK 2000)
# -------------------------------------------------------------
def step_5_herding_analysis():
    st.markdown(
        """
        <div class="step-eyebrow">PASO 5 · PSICOLOGÍA COLECTIVA & EFICIENCIA</div>
        <h1 class="step-title">¿Hay comportamiento de manada?</h1>
        <p class="step-lead">Test econométrico riguroso de Chang, Cheng & Khorana (CCK 2000). Evaluamos si el mercado cae en histeria colectiva o si los inversores analizan de forma racional y eficiente.</p>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.market_data or st.session_state.market_data["returns"].empty:
        with st.spinner("Cargando cotizaciones para el test de manada..."):
            prices, rets, stats_dict = download_market_data(st.session_state.tickers)
            st.session_state.market_data = {"prices": prices, "returns": rets, "stats": stats_dict}

    returns_df = st.session_state.market_data["returns"]
    valid_cols = [c for c in st.session_state.tickers if c in returns_df.columns]
    clean_rets = returns_df[valid_cols].dropna()

    if clean_rets.shape[1] < 3:
        st.warning("⚠️ Se necesitan al menos 3 acciones para realizar el test transversal de manada (CSAD). Vuelve al Paso 3 y agrega más acciones.")
        if st.button("⬅️ Volver a Elegir Acciones", on_click=set_step, args=(3,)):
            pass
        return

    with st.spinner("Ejecutando regresión econométrica no lineal CCK y errores White/HAC..."):
        herding_res = run_herding_analysis(clean_rets)

    if not herding_res.get("success", False):
        st.error(herding_res.get("error", "Error calculando el test de manada."))
        return

    # Tarjeta de Veredicto de Manada
    badge_color = "#f59e0b" if herding_res["is_herding"] else "#10b981"
    st.markdown(
        f"""
        <div class="herding-verdict-card">
            <div class="verdict-badge" style="background: rgba({ '245, 158, 11' if herding_res['is_herding'] else '16, 185, 129' }, 0.15); color: {badge_color}; border: 1px solid rgba({ '245, 158, 11' if herding_res['is_herding'] else '16, 185, 129' }, 0.35);">
                {herding_res['verdict_badge']}
            </div>
            <div class="verdict-title" style="margin-top: 0.5rem; font-size: 1.25rem;">{herding_res['verdict']}</div>
            <p class="verdict-desc" style="margin-top: 0.5rem; line-height: 1.55;">{herding_res['explanation']}</p>
            <div style="margin-top: 0.75rem; font-size: 0.84rem; font-weight: 650; color: #cbd5e1; background: rgba(255,255,255,0.03); padding: 0.5rem 0.75rem; border-radius: 8px;">
                {herding_res['asym_insight']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Rejilla de Métricas Econométricas
    st.markdown(
        f"""
        <div class="herding-stat-grid">
            <div class="herding-stat-box">
                <div class="herding-stat-label">Coef. No Lineal (γ₂)</div>
                <div class="herding-stat-val" style="color: {'#f59e0b' if herding_res['gamma2'] < 0 else '#10b981'};">{herding_res['gamma2']:.4f}</div>
                <div class="herding-stat-sub">{'Negativo (Compresión)' if herding_res['gamma2'] < 0 else 'Positivo (Dispersión)'}</div>
            </div>
            <div class="herding-stat-box">
                <div class="herding-stat-label">Estadístico t (White)</div>
                <div class="herding-stat-val">{herding_res['gamma2_t']:.2f}</div>
                <div class="herding-stat-sub">Crítico: |t| > 1.96</div>
            </div>
            <div class="herding-stat-box">
                <div class="herding-stat-label">P-Valor (Signif.)</div>
                <div class="herding-stat-val">{herding_res['gamma2_p']:.4f}</div>
                <div class="herding-stat-sub">{'Significativo (p < 0.05)' if herding_res['gamma2_p'] < 0.05 else 'No Significativo'}</div>
            </div>
            <div class="herding-stat-box">
                <div class="herding-stat-label">Ajuste del Modelo R²</div>
                <div class="herding-stat-val">{herding_res['r_squared']:.1%}</div>
                <div class="herding-stat-sub">{herding_res['observations']} ruedas analizadas</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Gráficos interactivos
    t_h1, t_h2 = st.tabs([
        "1. Dispersión Cuadrática CCK",
        "2. Serie Histórica de Dispersión (CSAD)",
    ])

    with t_h1:
        st.caption("📉 **Curva de CCK**: Compara cómo se dispersan los precios a medida que el mercado se mueve con fuerza. Si la curva se dobla hacia abajo, hay histeria colectiva.")
        st.plotly_chart(plot_herding_scatter(herding_res), use_container_width=True)

    with t_h2:
        st.caption("⏱️ **Evolución Temporal de CSAD**: Observa los momentos de la historia donde la dispersión se contrajo o se expandió bruscamente.")
        st.plotly_chart(plot_csad_timeline(herding_res), use_container_width=True)

    with st.expander("📚 ¿Cómo entender este test si no sé de finanzas?"):
        st.markdown(
            """
            - **¿Qué es 'Comportamiento en Manada' (Herding)?**: Es cuando los inversionistas dejan de pensar por su cuenta y copian lo que hace la masa. Si hay una noticia fuerte, todos compran o venden en pánico al mismo tiempo sin mirar los balances de cada empresa.
            - **¿Cómo lo descubre la matemática?**: En un mercado racional (normal), cuando el mercado se mueve mucho, cada acción reacciona a su propio ritmo según su salud financiera (la diferencia entre ellas o **dispersión** aumenta).
            - **La trampa del pánico**: Cuando hay *herding*, esa dispersión se desploma de forma no lineal (coeficiente $\\gamma_2$ negativo y estadísticamente significativo), porque todas las acciones caen o suben exactamente igual como ovejas siguiendo al rebaño.
            - **¿Para qué te sirve?**: Saber si el mercado es eficiente te protege de comprar en euforias irracionales (burbujas) o vender en pánico cuando todos los demás están asustados.
            """
        )

    st.markdown("<br>", unsafe_allow_html=True)
    b_prev, b_next = st.columns([1, 1.4])
    with b_prev:
        st.button("⬅️ Volver a Modelos", use_container_width=True, on_click=set_step, args=(4,))
    with b_next:
        st.button("Continuar a Mi Portafolio ➔", type="primary", use_container_width=True, on_click=set_step, args=(6,))


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

    # KPI Grid tipo Wallet Nu / Binance Luxury
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
        st.caption("🛡️ **Comparativa Oficial de los 3 Estimadores de VaR al 99% (Paso 10 del PDF)** a un horizonte de 10 días.")
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
        st.caption("⚡ **Pruebas de Estrés Oficiales (Paso 10 del PDF)**: Simulación de crisis extremas de mercado y pérdida de diversificación.")
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
        step_5_herding_analysis()
    elif st.session_state.step == 6:
        step_6_final_portfolio()

    # Inyección del tour interactivo con foco spotlight, difuminado y mascota 3D
    render_kibo_tour(st.session_state.step)
    render_floating_kibo_button()


if __name__ == "__main__":
    main()
