"""
Nexa · Plataforma Cuantitativa de Valoración y Gestión de Riesgo
Implementación de GBM, Salto de Merton, Ornstein-Uhlenbeck y Asignación de Portafolios
"""

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
from ui.styles import APP_CSS
from ui.kibo_copilot import render_step_insight, render_copilot_badge, open_copilot_modal
from ui.kibo_avatar import get_kibo_hero_banner
from ui.charts import plot_stochastic_fan, plot_model_comparison_bars, plot_portfolio_allocation_chart


st.set_page_config(
    page_title="Kibo · Tu Copiloto de Inversión",
    page_icon="🤖",
    layout="wide",
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


def render_header(current_step: int):
    st.markdown(
        f"""
        <div class="nexa-header">
            <div class="nexa-brand">
                <div class="brand-logo">K</div>
                <div>
                    <div class="brand-title">Kibo Quantitative</div>
                    <div class="brand-subtitle">Tu Copiloto Inteligente de Finanzas & Riesgo</div>
                </div>
            </div>
            <div class="header-badge">
                <span>🤖 Copiloto Kibo Activo</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Stepper
    steps = [
        (1, "1. Parámetros"),
        (2, "2. Universo & Auditoría"),
        (3, "3. Modelos Estocásticos"),
        (4, "4. Decisión & Portafolio"),
    ]
    stepper_html = '<div class="stepper">'
    for num, label in steps:
        state_class = "active" if num == current_step else ("done" if num < current_step else "")
        stepper_html += f"""
        <div class="stepper-item {state_class}">
            <div class="stepper-num">{num if num >= current_step else '✓'}</div>
            <div class="stepper-label">{label}</div>
        </div>
        """
    stepper_html += '</div>'
    st.markdown(stepper_html, unsafe_allow_html=True)
    
    # Barra de acción del Copiloto Kibo
    render_copilot_badge(current_step)


def step_1_parameters():
    # Hero Banner animado de Kibo
    st.markdown(get_kibo_hero_banner(), unsafe_allow_html=True)

    render_step_insight(
        1,
        st.session_state.profile,
        "Tu elección condicionará si protegemos colas de salto o maximizamos retornos de deriva."
    )
    
    st.markdown("### Configuración de Parámetros de Inversión")
    st.caption("Ajusta el capital a analizar, el perfil de riesgo del inversionista y el horizonte regulatorio.")
    
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        with st.container(border=True):
            st.markdown("#### 💰 Capital Inicial para Simulación")
            st.session_state.capital = st.number_input(
                "Capital (USD)",
                min_value=1000.0,
                max_value=10000000.0,
                value=float(st.session_state.capital),
                step=5000.0,
                help="Base del taller: USD 100.000 para evaluación de asignación."
            )
            st.caption("Nota: No se ejecutan órdenes de compra reales ni se compromete capital financiero.")
            
        with st.container(border=True):
            st.markdown("#### ⏱️ Parámetros de Riesgo Regulatorio (Taller)")
            c_h, c_conf = st.columns(2)
            with c_h:
                st.session_state.horizon = st.selectbox(
                    "Horizonte temporal (días)",
                    options=[5, 10, 20, 40, 60],
                    index=[5, 10, 20, 40, 60].index(st.session_state.horizon) if st.session_state.horizon in [5, 10, 20, 40, 60] else 1,
                    help="Días hábiles de proyección para la métrica de VaR (Taller: 10 días)."
                )
            with c_conf:
                st.session_state.confidence = st.selectbox(
                    "Nivel de Confianza VaR",
                    options=[90.0, 95.0, 99.0],
                    index=2,
                    help="Nivel de significancia estadística (Taller: 99%)."
                )

    with col2:
        with st.container(border=True):
            st.markdown("#### 🎯 Perfil de Riesgo del Inversionista")
            profiles = {
                "Conservador": "Prioridad estricta en preservar capital. Exige cobertura ante saltos catastróficos (Merton) y activos mean-reverting (Ornstein-Uhlenbeck).",
                "Moderado": "Equilibrio entre crecimiento y control de volatilidad. Se guía por el criterio estadístico óptimo (BIC/AIC).",
                "Agresivo": "Acepta variaciones significativas y riesgo de cola buscando capturar la mayor rentabilidad esperada acumulada.",
            }
            selected_p = st.radio(
                "Selecciona tu perfil:",
                options=list(profiles.keys()),
                index=list(profiles.keys()).index(st.session_state.profile),
                format_func=lambda x: f"**{x}** — {profiles[x]}",
            )
            st.session_state.profile = selected_p
            
        st.markdown(
            f"""
            <div class="metric-box" style="margin-top:1.2rem;">
                <div class="metric-lbl">Resumen Estratégico</div>
                <div class="metric-val">USD {st.session_state.capital:,.0f}</div>
                <div class="metric-sub">Perfil {st.session_state.profile} · VaR {st.session_state.confidence:.0f}% a {st.session_state.horizon} días</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Continuar a Selección de Activos ➔", type="primary", use_container_width=True):
        set_step(2)


def step_2_assets():
    render_step_insight(
        2,
        st.session_state.profile,
        "Verifica que el portafolio cuente con al menos 4 sectores para garantizar diversificación robusta."
    )
    
    st.markdown("### Universo de Inversión y Auditoría de Datos")
    st.caption("Gestiona las acciones del portafolio, audita su sector y valida el historial descargado de Yahoo Finance.")
    
    col_input, col_audit = st.columns([1, 1], gap="large")
    
    with col_input:
        st.markdown("#### 📋 Acciones del Portafolio")
        available_tickers = sorted(list(set(list(SECTOR_MAP.keys()) + st.session_state.tickers)))
        selected_tickers = st.multiselect(
            "Seleccionar o añadir Tickers:",
            options=available_tickers,
            default=st.session_state.tickers,
            help="Escribe para buscar cualquier ticker de Yahoo Finance."
        )
        st.session_state.tickers = selected_tickers
        
        # Actualización de tabla de portafolio
        port_rows = []
        for t in selected_tickers:
            current_sec = st.session_state.portfolio.loc[st.session_state.portfolio["Ticker"] == t, "Sector"].values
            sec = current_sec[0] if len(current_sec) > 0 else detect_sector(t)
            port_rows.append({"Ticker": t, "Sector": sec})
            
        st.session_state.portfolio = pd.DataFrame(port_rows)
        
        st.markdown("##### ✏️ Clasificación Sectorial (Editable)")
        edited_portfolio = st.data_editor(
            st.session_state.portfolio,
            column_config={
                "Ticker": st.column_config.TextColumn("Ticker", disabled=True),
                "Sector": st.column_config.SelectboxColumn("Sector", options=ALL_SECTORS, required=True),
            },
            hide_index=True,
            use_container_width=True,
        )
        st.session_state.portfolio = edited_portfolio
        
        # Botón para descargar / actualizar datos de Yahoo Finance
        if st.button("🔄 Descargar y Auditar Precios Reales", type="secondary", use_container_width=True) or st.session_state.market_data is None:
            with st.spinner("Descargando historial de 3 años desde Yahoo Finance..."):
                prices, rets, stats_dict = download_market_data(st.session_state.tickers)
                st.session_state.market_data = {
                    "prices": prices,
                    "returns": rets,
                    "stats": stats_dict,
                }
            st.success("¡Datos históricos de 3 años sincronizados exitosamente!")

    with col_audit:
        st.markdown("#### 📊 Auditoría de Calidad y Diversificación")
        n_activos = len(st.session_state.tickers)
        n_sectores = st.session_state.portfolio["Sector"].nunique() if n_activos > 0 else 0
        
        m1, m2 = st.columns(2)
        with m1:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-lbl">Total Activos</div>
                    <div class="metric-val">{n_activos}</div>
                    <div class="metric-sub">{"✅ Rúbrica 10 acciones" if n_activos >= 10 else "⚠️ Recomendado: 10 acciones"}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m2:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-lbl">Sectores Únicos</div>
                    <div class="metric-val">{n_sectores}</div>
                    <div class="metric-sub">{"✅ Cumple ≥ 4 sectores" if n_sectores >= 4 else "⚠️ Faltan sectores (Mín 4)"}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
        st.markdown("<br>", unsafe_allow_html=True)
        # Mostrar tabla de auditoría estadística si ya hay datos
        if st.session_state.market_data:
            stats_dict = st.session_state.market_data["stats"]
            audit_list = []
            for t in st.session_state.tickers:
                if t in stats_dict:
                    s = stats_dict[t]
                    audit_list.append({
                        "Ticker": t,
                        "Spot (USD)": f"${s['spot']:.2f}",
                        "Vol Anual": f"{s['ann_vol']:.1%}",
                        "Asimetría": f"{s['skewness']:.2f}",
                        "Curtosis": f"{s['kurtosis']:.2f}",
                        "¿Normal?": "Sí (p>5%)" if s['is_normal'] else "No (Colas Pesadas)",
                    })
            if audit_list:
                st.markdown("##### 🔍 Test de Normalidad & Colas (Jarque-Bera)")
                st.dataframe(pd.DataFrame(audit_list), hide_index=True, use_container_width=True)
                st.caption("Nota: Acciones con Curtosis > 3 o p-value < 0.05 violan la normalidad del Browniano puro, justificando el Modelo de Salto de Merton.")

    st.markdown("<br>", unsafe_allow_html=True)
    c_prev, c_next = st.columns(2)
    with c_prev:
        st.button("⬅️ Volver a Parámetros", use_container_width=True, on_click=set_step, args=(1,))
    with c_next:
        st.button("Calcular y Comparar Modelos Estocásticos ➔", type="primary", use_container_width=True, on_click=set_step, args=(3,))


def step_3_stochastic_models():
    render_step_insight(
        3,
        st.session_state.profile,
        "Comparamos la bondad de ajuste estadística (AIC, BIC, Log-Likelihood) de cada modelo para elegir el óptimo."
    )
    
    st.markdown("### Motores Estocásticos y Comparación Cuantitativa")
    st.caption("Simulación exacta Monte Carlo bajo Movimiento Browniano, Salto de Merton y Ornstein-Uhlenbeck.")
    
    if not st.session_state.market_data or st.session_state.market_data["returns"].empty:
        st.warning("Descargando datos necesarios...")
        prices, rets, stats_dict = download_market_data(st.session_state.tickers)
        st.session_state.market_data = {"prices": prices, "returns": rets, "stats": stats_dict}
        
    prices_df = st.session_state.market_data["prices"]
    returns_df = st.session_state.market_data["returns"]
    
    # Selector de activo para análisis individual detallado
    valid_tickers = [t for t in st.session_state.tickers if t in returns_df.columns]
    if not valid_tickers:
        st.error("No hay datos disponibles para los tickers seleccionados.")
        return
        
    active_ticker = st.selectbox(
        "🔎 Selecciona la acción a inspeccionar en detalle:",
        options=valid_tickers,
        index=0 if st.session_state.active_asset_tab not in valid_tickers else valid_tickers.index(st.session_state.active_asset_tab)
    )
    st.session_state.active_asset_tab = active_ticker
    
    # Ejecución de la comparación cuantitativa
    with st.spinner(f"Calibrando y simulando 3.000 trayectorias para {active_ticker}..."):
        comp_results = compare_models_for_asset(
            active_ticker,
            prices_df[active_ticker],
            returns_df[active_ticker],
            horizon_days=st.session_state.horizon,
            n_paths=3000,
        )
        
    # Veredicto del Mejor Modelo
    winner_name = comp_results["winner"]
    st.markdown(
        f"""
        <div class="glass-card" style="border-left: 4px solid var(--accent-cyan);">
            <div class="card-title">🏆 Veredicto Cuantitativo para {active_ticker}: <span style="color:#38bdf8;">{winner_name}</span></div>
            <p style="margin: 0; color:#e2e8f0; font-size:0.92rem;">{comp_results['winner_reason']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Tabla comparativa de los 3 modelos
    st.markdown("#### 📋 Matriz de Bondad de Ajuste y Métricas de Riesgo")
    st.dataframe(comp_results["models_table"], hide_index=True, use_container_width=True)
    
    # Gráficos de los 3 modelos
    st.markdown("#### 📈 Abanicos de Proyección Estocástica (Percentiles 10-90% y Mediana)")
    t1, t2, t3 = st.tabs([
        "1. Mov. Browniano Geométrico (GBM)",
        "2. Salto de Merton (Jump-Diffusion)",
        "3. Ornstein-Uhlenbeck (Mean Reversion)",
    ])
    
    with t1:
        st.plotly_chart(plot_stochastic_fan(comp_results["sim_gbm"], f"· {active_ticker}"), use_container_width=True)
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Drift Anualizado (μ)", f"{comp_results['sim_gbm'].parameters['mu_annual']:.2%}")
        with col_m2:
            st.metric("Volatilidad Anual (σ)", f"{comp_results['sim_gbm'].parameters['sigma_annual']:.2%}")
        with col_m3:
            st.metric(f"VaR 99% ({st.session_state.horizon}d)", f"{comp_results['sim_gbm'].var_99:.2%}")
            
    with t2:
        st.plotly_chart(plot_stochastic_fan(comp_results["sim_mjd"], f"· {active_ticker}"), use_container_width=True)
        col_j1, col_j2, col_j3, col_j4 = st.columns(4)
        with col_j1:
            st.metric("Frecuencia Saltos (λ)", f"{comp_results['sim_mjd'].parameters['lambda']:.1f} / año")
        with col_j2:
            st.metric("Media del Salto (μ_j)", f"{comp_results['sim_mjd'].parameters['mu_j']:.2%}")
        with col_j3:
            st.metric("Desv. del Salto (σ_j)", f"{comp_results['sim_mjd'].parameters['sigma_j']:.2%}")
        with col_j4:
            st.metric(f"CVaR 99% ({st.session_state.horizon}d)", f"{comp_results['sim_mjd'].cvar_99:.2%}")
            
    with t3:
        st.plotly_chart(plot_stochastic_fan(comp_results["sim_ou"], f"· {active_ticker}"), use_container_width=True)
        col_o1, col_o2, col_o3 = st.columns(3)
        with col_o1:
            st.metric("Velocidad Reversión (θ)", f"{comp_results['sim_ou'].parameters['theta']:.2f}")
        with col_o2:
            st.metric("Media de Equilibrio", f"USD {comp_results['sim_ou'].parameters['mu_ou_price']:.2f}")
        with col_o3:
            st.metric("Vida Media (Half-Life)", f"{comp_results['sim_ou'].parameters['half_life_days']:.0f} días")

    # Comparativa Gráfica de AIC / BIC
    st.plotly_chart(plot_model_comparison_bars(comp_results["models_table"]), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c_prev, c_next = st.columns(2)
    with c_prev:
        st.button("⬅️ Modificar Activos", use_container_width=True, on_click=set_step, args=(2,))
    with c_next:
        st.button("Avanzar a Decisión de Portafolio ➔", type="primary", use_container_width=True, on_click=set_step, args=(4,))


def step_4_decision_and_portfolio():
    render_step_insight(
        4,
        st.session_state.profile,
        "Asignación con Mínimo VaR bajo restricciones sectoriales (máx 35% sector, 2%-20% acción)."
    )
    
    st.markdown("### Decisión de Inversión y Asignación de Portafolio")
    st.caption("Integración del modelo estocástico óptimo con los perfiles de riesgo y optimización de cartera.")
    
    returns_df = st.session_state.market_data["returns"]
    portfolio_df = st.session_state.portfolio
    
    # 1. Recomendación Estratégica según Perfil
    prof = st.session_state.profile
    profile_cards = {
        "Conservador": {
            "badge": "🛡️ Escenario Defensivo de Cola (Merton & O-U)",
            "text": "Se adoptan las pérdidas de cola del Modelo de Salto de Merton para blindar el capital. Los activos de utilities o con reversión rápida reducen la volatilidad. Se minimiza el VaR conjunto.",
            "rule": "Asignación Mínimo VaR Restringido · Sin sobreexposición a tecnología.",
        },
        "Moderado": {
            "badge": "⚖️ Ensamble Óptimo BIC / AIC",
            "text": "Se adopta el modelo con menor BIC para cada activo, balanceando colas pesadas y eficiencia de parámetros. Se aplica diversificación sectorial estricta.",
            "rule": "Asignación Mínimo VaR · Máximo 35% por sector y cotas 2%-20% por acción.",
        },
        "Agresivo": {
            "badge": "🚀 Maximizador de Deriva & Convexidad (GBM Alcista)",
            "text": "Se asume la varianza temporal para aprovechar el drift anualizado superior. Se permite mayor ponderación en activos de alto crecimiento tecnológico.",
            "rule": "Asignación Inverso al VaR / Pesos Iguales con sesgo en activos de alto drift.",
        },
    }
    
    p_info = profile_cards[prof]
    st.markdown(
        f"""
        <div class="glass-card" style="border: 1px solid rgba(121, 82, 245, 0.4);">
            <div class="card-title">{p_info['badge']}</div>
            <p style="margin: 0.3rem 0; color:#e2e8f0; font-size:0.92rem;">{p_info['text']}</p>
            <div style="font-size:0.82rem; color:var(--accent-cyan); font-weight:700; margin-top:0.4rem;">{p_info['rule']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # 2. Cálculo de la asignación del portafolio
    alloc_res = compute_portfolio_allocation(
        st.session_state.capital,
        portfolio_df,
        returns_df,
        confidence=st.session_state.confidence,
        horizon_days=st.session_state.horizon,
    )
    
    if not alloc_res:
        st.error("No se pudo calcular la asignación de portafolio.")
        return
        
    df_alloc = alloc_res["allocation_df"]
    
    # Tarjetas KPI de Portafolio
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-lbl">Capital Analizado</div>
                <div class="metric-val">USD {st.session_state.capital:,.0f}</div>
                <div class="metric-sub">Perfil {prof}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-lbl">VaR 99% Cartera ({st.session_state.horizon}d)</div>
                <div class="metric-val">{alloc_res['var_portfolio_pct']:.2%}</div>
                <div class="metric-sub">USD {alloc_res['var_portfolio_usd']:,.2f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-lbl">Efectivo Residual</div>
                <div class="metric-val">USD {alloc_res['efectivo_residual']:,.2f}</div>
                <div class="metric-sub">Por redondeo de acciones</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k4:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-lbl">Optimización SLSQP</div>
                <div class="metric-val">{'Óptimo' if alloc_res['solver_success'] else 'Aproximado'}</div>
                <div class="metric-sub">Límites sectoriales OK</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 💼 Plan de Inversión Detallado (Cantidades de Acciones Enteras)")
    st.dataframe(
        df_alloc[[
            "Ticker", "Sector", "Precio Spot (USD)", "VaR Indiv 99%",
            "Peso Óptimo", "Monto Objetivo (USD)", "Acciones Enteras", "Inversión Real (USD)", "Peso Real"
        ]],
        hide_index=True,
        use_container_width=True,
    )
    
    # Gráfico de asignación de pesos
    st.plotly_chart(plot_portfolio_allocation_chart(df_alloc), use_container_width=True)

    # Descarga CSV
    csv_bytes = df_alloc.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Descargar Plan de Portafolio en CSV",
        data=csv_bytes,
        file_name="kibo_portfolio_allocation.csv",
        mime="text/csv",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    c_prev, c_restart = st.columns(2)
    with c_prev:
        st.button("⬅️ Volver a Modelos Estocásticos", use_container_width=True, on_click=set_step, args=(3,))
    with c_restart:
        st.button("🔄 Reiniciar Simulación desde el Inicio", use_container_width=True, on_click=set_step, args=(1,))


def main():
    initialize_session_state()
    st.markdown(APP_CSS, unsafe_allow_html=True)
    render_header(st.session_state.step)
    
    if st.session_state.step == 1:
        step_1_parameters()
    elif st.session_state.step == 2:
        step_2_assets()
    elif st.session_state.step == 3:
        step_3_stochastic_models()
    elif st.session_state.step == 4:
        step_4_decision_and_portfolio()


if __name__ == "__main__":
    main()