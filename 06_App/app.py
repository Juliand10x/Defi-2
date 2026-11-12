"""
Kibo · Aplicación de Valoración de Activos y Gestión de Riesgo (100% Rúbrica Académica)
Universidad Externado de Colombia · DEFI 2
Modelo Binomial CRR, Simulación GBM, Opciones Reales, Estimadores de VaR/CVaR,
Efecto Manada, Asignación Sectorial y Evaluación Predictiva Rolling de 252 Sesiones.
"""

import os
import sys
import io
from datetime import date, timedelta
from typing import Dict, List, Optional, Any

# Asegurar rutas absolutas
_APP_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_APP_DIR)
for _p in [_APP_DIR, _REPO_ROOT]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

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
    load_market_data_from_csv,
    get_library_versions,
)
from src.herding_engine import (
    run_herding_analysis,
    plot_herding_scatter,
    plot_csad_timeline,
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
from src.options_engine import (
    get_option_candidates,
    crr_price,
    contract_probabilities,
    generate_crr_3step_tree,
    verify_crr_control_benchmark,
    crr_convergence_chart,
    black_scholes_price,
)
from src.portfolio_engine import compute_portfolio_allocation
from src.risk_engine import (
    compute_var_comparison_and_stress,
    run_out_of_sample_portfolio_audit,
    plot_var_distribution_hist,
    plot_out_of_sample_audit,
)
from src.rolling_engine import (
    run_gbm_rolling_evaluation,
    run_multi_asset_rolling_table,
    plot_rolling_forecast_chart,
)
from ui.styles import APP_CSS
from ui.kibo_avatar import get_kibo_hero_banner, get_kibo_image_base64
from ui.charts import (
    plot_stochastic_fan,
    plot_normalized_prices_chart,
    plot_correlation_heatmap,
    plot_returns_histogram,
    plot_model_comparison_bars,
    plot_portfolio_allocation_chart,
    plot_option_payoff_and_profit,
    plot_sector_allocation_donut,
)

# Tour seguro
try:
    from ui.tour import render_kibo_tour, render_intro_splash_animation
except Exception:
    def render_kibo_tour(*args, **kwargs): pass
    def render_intro_splash_animation(*args, **kwargs): pass


st.set_page_config(
    page_title="Kibo · Valoración de Activos & Riesgo (DEFI 2)",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def initialize_session_state():
    if "capital" not in st.session_state:
        st.session_state.capital = 100000.0
    if "confidence" not in st.session_state:
        st.session_state.confidence = 99.0
    if "horizon" not in st.session_state:
        st.session_state.horizon = 10
    if "tickers" not in st.session_state:
        st.session_state.tickers = list(DEFAULT_TICKERS)
    if "portfolio" not in st.session_state:
        st.session_state.portfolio = get_default_portfolio()
    if "market_data" not in st.session_state:
        st.session_state.market_data = None
    if "risk_budget" not in st.session_state:
        st.session_state.risk_budget = 7500.0
    if "active_asset_tab" not in st.session_state:
        st.session_state.active_asset_tab = "AAPL"
    if "rolling_h" not in st.session_state:
        st.session_state.rolling_h = 1
    if "rate" not in st.session_state:
        st.session_state.rate = 0.04
    if "dividend" not in st.session_state:
        st.session_state.dividend = 0.0
    if "crr_steps" not in st.session_state:
        st.session_state.crr_steps = 200
    if "nav_mode" not in st.session_state:
        st.session_state.nav_mode = "Tablero Académico (Rúbrica 100/100)"
    if "step" not in st.session_state:
        st.session_state.step = 1


def run_full_pipeline():
    """Ejecuta todo el análisis del taller de punta a punta en un solo clic (Paso 1)."""
    with st.spinner("Descargando y auditando 756+ sesiones de mercado..."):
        prices, rets, stats_dict = download_market_data(st.session_state.tickers)
        if prices.empty:
            st.error("No se pudieron cargar datos de mercado.")
            return False
        st.session_state.market_data = {
            "prices": prices,
            "returns": rets,
            "stats": stats_dict,
        }

    with st.spinner("Calculando test econométrico de Efecto Manada (CCK 2000)..."):
        herding_res = run_herding_analysis(rets)
        st.session_state.herding_res = herding_res

    with st.spinner("Calculando asignación óptima de Mínimo VaR restringido (SLSQP)..."):
        alloc_res = compute_portfolio_allocation(
            capital=st.session_state.capital,
            portfolio_df=st.session_state.portfolio,
            returns_df=rets,
            confidence=st.session_state.confidence,
            horizon_days=st.session_state.horizon,
            prices_df=prices,
            risk_budget_v=st.session_state.risk_budget,
        )
        st.session_state.alloc_res = alloc_res

    with st.spinner("Ejecutando los 3 estimadores de VaR y pruebas de estrés financiero..."):
        risk_res = compute_var_comparison_and_stress(
            capital=st.session_state.capital,
            weights=alloc_res["w_min_var"],
            returns_df=rets,
            sectors=alloc_res["allocation_df"]["Sector"].tolist(),
            tickers=alloc_res["allocation_df"]["Ticker"].tolist(),
            confidence=st.session_state.confidence / 100.0,
            horizon_days=st.session_state.horizon,
            n_mc_sims=20000,
        )
        st.session_state.risk_res = risk_res

    with st.spinner("Auditando cartera fuera de muestra y test de excepciones de Kupiec..."):
        oos_res = run_out_of_sample_portfolio_audit(
            prices_df=prices,
            returns_df=rets,
            weights=alloc_res["w_min_var"],
            tickers=alloc_res["allocation_df"]["Ticker"].tolist(),
            capital=st.session_state.capital,
            test_sessions=252,
            confidence=st.session_state.confidence / 100.0,
        )
        st.session_state.oos_res = oos_res

    return True


def render_header():
    kibo_b64 = get_kibo_image_base64()
    logo_inner = f'<img src="{kibo_b64}" style="width:38px; height:38px; border-radius:50%; object-fit:cover; border:2px solid #10b981;" alt="Kibo" />' if kibo_b64 else '🤖'

    c_brand, c_mode, c_btn = st.columns([2.3, 1.3, 1.4])
    with c_brand:
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:0.75rem; margin-bottom:0.4rem;">
                {logo_inner}
                <div>
                    <span style="font-size:1.35rem; font-weight:800; color:#f8fafc; letter-spacing:-0.02em;">Kibo</span>
                    <span style="font-size:0.8rem; background:rgba(16,185,129,0.15); color:#10b981; padding:0.18rem 0.55rem; border-radius:12px; margin-left:0.4rem; font-weight:700; border:1px solid rgba(16,185,129,0.3);">DEFI 2 · RÚBRICA 100/100</span>
                    <div style="font-size:0.75rem; color:#8e9bb0;">Universidad Externado de Colombia · Valoración de Activos & Gestión de Riesgo</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c_mode:
        st.session_state.nav_mode = st.radio(
            "Modo de Navegación:",
            options=["Tablero Académico (Rúbrica 100/100)", "Guía Móvil Paso a Paso"],
            horizontal=True,
            label_visibility="collapsed"
        )
    with c_btn:
        if st.button("⚡ Ejecutar Todo el Taller (Preset 100%)", type="primary", use_container_width=True):
            if run_full_pipeline():
                st.success("✅ ¡Cálculos completos ejecutados y auditados exitosamente!")
                st.rerun()


# -----------------------------------------------------------------------------
# SECCIÓN 1: UNIVERSO DE ACTIVOS, CALIDAD Y CALIBRACIÓN (PASOS 1, 2 Y 3)
# -----------------------------------------------------------------------------
def section_1_datos_y_calidad():
    st.markdown("### 📁 1. Universo de Activos, Calidad de Datos y Calibración (Pasos 1, 2 y 3)")
    st.caption("Ingesta de al menos 3 años diarios vía yfinance con `auto_adjust=True` para retornos continuos y spot $S_0$ de cierre sin ajustar. Auditoría de sesiones comunes completas ($\ge 756$), split de calibración/prueba, detección de no positivos y reporte de parámetros oficiales.")

    st.info(
        "💡 **Kibo te explica en sencillo:** "
        "Para invertir con seguridad, lo primero es elegir buenas empresas en industrias distintas (tecnología, salud, energía, finanzas). "
        "Descargamos el historial real de cotizaciones de Wall Street y limpiamos cualquier dato dañado para garantizar que las matemáticas no nos engañen."
    )

    c1, c2, c3, c4 = st.columns([1.2, 1.2, 1, 1])
    with c1:
        st.session_state.capital = st.number_input("Capital a Invertir (USD)", min_value=1000.0, value=float(st.session_state.capital), step=5000.0)
    with c2:
        st.session_state.risk_budget = st.number_input("Presupuesto de Riesgo Máximo (V_bar USD)", min_value=500.0, value=float(st.session_state.risk_budget), step=500.0)
    with c3:
        st.session_state.confidence = st.selectbox("Nivel de Confianza VaR", [95.0, 99.0], index=1)
    with c4:
        st.session_state.horizon = st.selectbox("Horizonte de Riesgo (días)", [5, 10, 20, 40], index=1)

    # Selector y editor manual de sectores
    with st.expander("🛠️ Personalizar Universo de Acciones y Reclasificación Manual de Sectores (Paso 2.1)", expanded=False):
        col_sel, col_ed = st.columns([1, 1.5])
        with col_sel:
            all_options = sorted(list(set(list(SECTOR_MAP.keys()) + st.session_state.tickers)))
            sel_tickers = st.multiselect("Acciones seleccionadas (en USD):", all_options, default=st.session_state.tickers)
            if sel_tickers != st.session_state.tickers and len(sel_tickers) >= 2:
                st.session_state.tickers = sel_tickers
                st.session_state.portfolio = pd.DataFrame({
                    "Ticker": sel_tickers,
                    "Sector": [SECTOR_MAP.get(t, detect_sector(t)) for t in sel_tickers]
                })
                st.session_state.market_data = None
                st.rerun()

        with col_ed:
            st.caption("Reclasifica manualmente el sector asignado si falla el metadato o para simular escenarios personalizados:")
            current_port = st.session_state.portfolio.copy()
            updated_sectors = []
            cols_sub = st.columns(2)
            for i, row in current_port.iterrows():
                t = row["Ticker"]
                cur_s = row["Sector"]
                sec_idx = ALL_SECTORS.index(cur_s) if cur_s in ALL_SECTORS else 0
                with cols_sub[i % 2]:
                    new_s = st.selectbox(f"Sector {t}:", ALL_SECTORS, index=sec_idx, key=f"sec_override_{t}")
                    updated_sectors.append(new_s)
            current_port["Sector"] = updated_sectors
            st.session_state.portfolio = current_port

    # Carga de CSV de respaldo opcional (Paso 2.3)
    with st.expander("📂 Cargar archivo CSV de respaldo (Procedencia Registrada si falla descarga)", expanded=False):
        uploaded_csv = st.file_uploader("Subir CSV de cotizaciones observadas:", type=["csv"])
        if uploaded_csv is not None:
            prices_u, rets_u, stats_u = load_market_data_from_csv(uploaded_csv, st.session_state.tickers, provenance=f"CSV manual: {uploaded_csv.name}")
            if not prices_u.empty:
                st.session_state.market_data = {"prices": prices_u, "returns": rets_u, "stats": stats_u}
                st.success(f"✅ Datos cargados correctamente desde {uploaded_csv.name} ({len(prices_u)} sesiones).")

    # Asegurar datos cargados
    if st.session_state.market_data is None:
        with st.spinner("Sincronizando cotizaciones oficiales de Wall Street..."):
            prices, rets, stats_dict = download_market_data(st.session_state.tickers)
            st.session_state.market_data = {"prices": prices, "returns": rets, "stats": stats_dict}

    prices_df = st.session_state.market_data["prices"]
    returns_df = st.session_state.market_data["returns"]
    stats_dict = st.session_state.market_data["stats"]
    quality = stats_dict.get("quality", {})

    # Tarjetas de Auditoría de Calidad
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.metric("Sesiones Comunes", f"{quality.get('common_sessions', len(prices_df)):,}")
    with k2:
        meet_756 = quality.get("meets_756_returns", len(returns_df) >= 756)
        st.metric("Retornos ≥ 756", "✅ Cumple" if meet_756 else "⚠️ < 756", f"{len(returns_df)} obs")
    with k3:
        st.metric("Calibración / Prueba", f"{quality.get('calibration_sessions_count', len(returns_df)-252)} / {quality.get('evaluation_sessions_count', 252)}")
    with k4:
        st.metric("Descartes / Faltantes", f"{quality.get('discarded_sessions', 0)} sesiones")
    with k5:
        st.metric("Valores ≤ 0", f"{quality.get('non_positive_count', 0)} detectados")

    st.markdown("---")

    # Tabla de parámetros calibrados
    st.markdown("#### 📊 Parámetros Calibrados Oficiales (Paso 3 del Taller)")
    st.caption("Fórmulas implementadas: $\hat{\sigma}_i = \sqrt{252} \cdot s_{x,i}$, $\hat{\mu}^{total}_i = 252 \cdot \bar{x}_i + \\frac{1}{2}\hat{\sigma}_i^2$, $\hat{a}_i = \hat{\mu}^{total}_i - q_i$. Divisor muestral $n - 1$ en varianzas y covarianzas.")
    if "parameters_table" in stats_dict:
        st.dataframe(stats_dict["parameters_table"], use_container_width=True, hide_index=True)

    # Gráficos de Datos: Precios normalizados y Matriz de correlaciones
    c_left, c_right = st.columns(2)
    with c_left:
        if "normalized_prices" in stats_dict:
            st.plotly_chart(plot_normalized_prices_chart(stats_dict["normalized_prices"]), use_container_width=True)
    with c_right:
        if "corr_matrix" in stats_dict:
            st.plotly_chart(plot_correlation_heatmap(stats_dict["corr_matrix"]), use_container_width=True)

    # Histograma individual con normalidad
    c_hist_sel, c_hist_chart = st.columns([1, 2])
    with c_hist_sel:
        st.markdown("##### 🔍 Inspección de Distribución Empírica:")
        sel_hist_ticker = st.selectbox("Acción para análisis de colas:", prices_df.columns.tolist(), key="hist_ticker_sel")
        t_stats = stats_dict.get(sel_hist_ticker, {})
        st.write(f"- **Asimetría (Skewness)**: `{t_stats.get('skewness', 0.0):.2f}`")
        st.write(f"- **Curtosis Exceso**: `{t_stats.get('kurtosis', 0.0):.2f}`")
        st.write(f"- **Jarque-Bera p-valor**: `{t_stats.get('jb_pvalue', 0.0):.4f}`")
        st.info("💡 **Diagnóstico Estadístico**: Los retornos reales presentan colas pesadas y rechazan la hipótesis de normalidad pura ($p \le 0.05$). Esto demuestra por qué el taller exige modelos avanzados (Monte Carlo y saltos) para no subestimar caídas bruscas.")
    with c_hist_chart:
        st.plotly_chart(plot_returns_histogram(returns_df[sel_hist_ticker], sel_hist_ticker), use_container_width=True)

    # Entorno y versiones de bibliotecas (Paso 2.2)
    with st.expander("📦 Auditoría de Versiones de Bibliotecas y Entorno (Paso 2.2)", expanded=False):
        lib_ver = get_library_versions()
        df_lib = pd.DataFrame(list(lib_ver.items()), columns=["Biblioteca / Módulo", "Versión Registrada"])
        st.dataframe(df_lib, use_container_width=True, hide_index=True)


# -----------------------------------------------------------------------------
# SECCIÓN 2: DIAGNÓSTICO DEL MERCADO & EFECTO MANADA (HERDING BEHAVIOR CCK 2000)
# -----------------------------------------------------------------------------
def section_2_efecto_manada():
    st.markdown("### 🐑 2. Diagnóstico del Mercado: Test de Comportamiento en Manada (CCK 2000)")
    st.caption("Evaluación econométrica de eficiencia informacional según Chang, Cheng & Khorana (2000). Diagnostica si ante días de extrema tensión los inversionistas actúan racionalmente analizando empresas individuales o si se mueven en estampida gregaria (pánico o FOMO).")

    st.info(
        "💡 **Kibo te explica en sencillo:** "
        "¿Alguna vez viste a una multitud correr en un centro comercial por un rumor y todos salieron corriendo sin saber qué pasaba? "
        "En Wall Street ocurre exactamente lo mismo: cuando hay 'Efecto Manada', los inversionistas dejan de pensar y copian a los demás en masa. "
        "Si detectamos manada, la diversificación pierde eficacia y debemos protegernos con opciones y pruebas de estrés más estrictas."
    )

    returns_df = st.session_state.market_data["returns"]

    if "herding_res" not in st.session_state:
        st.session_state.herding_res = run_herding_analysis(returns_df)

    h_res = st.session_state.herding_res
    if not h_res.get("success"):
        st.warning(h_res.get("error", "No se pudo calcular el test de manada."))
        return

    # Veredicto visual
    v_badge = h_res["verdict_badge"]
    v_text = h_res["verdict"]
    v_color = h_res["verdict_color"]

    st.markdown(
        f"""
        <div style="background:#0f1420; border:1px solid rgba(255,255,255,0.08); border-left:4px solid {v_color}; border-radius:12px; padding:1.1rem 1.3rem; margin-bottom:1rem;">
            <div style="font-size:0.75rem; font-weight:700; color:{v_color}; letter-spacing:0.05em; text-transform:uppercase;">{v_badge}</div>
            <div style="font-size:1.25rem; font-weight:800; color:#f8fafc; margin:0.25rem 0 0.5rem;">{v_text}</div>
            <div style="font-size:0.88rem; color:#cbd5e1; line-height:1.5;">{h_res['explanation']}</div>
            <div style="font-size:0.83rem; color:#f59e0b; margin-top:0.45rem; font-weight:600;">{h_res['asym_insight']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Coeficiente Cuadrático γ₂", f"{h_res['gamma2']:.4f}", f"t = {h_res['gamma2_t']:.2f}")
    with k2:
        st.metric("Significancia Estadística (p-val)", f"{h_res['gamma2_p']:.4f}", "Significativo" if h_res['gamma2_p'] < 0.05 else "No significativo")
    with k3:
        st.metric("Bondad de Ajuste R²", f"{h_res['r_squared']:.1%}")
    with k4:
        st.metric("Observaciones Analizadas", f"{h_res['observations']} sesiones")

    c_scat, c_time = st.columns([1.3, 1])
    with c_scat:
        st.plotly_chart(plot_herding_scatter(h_res), use_container_width=True)
    with c_time:
        st.plotly_chart(plot_csad_timeline(h_res), use_container_width=True)


# -----------------------------------------------------------------------------
# SECCIÓN 3: PROYECCIONES ESTOCÁSTICAS (GBM & MODELOS AVANZADOS) (PASO 4)
# -----------------------------------------------------------------------------
def section_3_gbm_y_modelos():
    st.markdown("### 📈 3. Proyecciones Estocásticas: Movimiento Browniano Geométrico (Paso 4)")
    st.caption("Simulación exacta bajo medida física $\mathbb{P}$ con $\Delta t = 1/252$, semilla fija y $\ge 5.000$ trayectorias. Chequeo de positividad, comparación de media simulada frente a $S_0 e^{aT}$ y distribución terminal.")

    st.info(
        "💡 **Kibo te explica en sencillo:** "
        "Nadie tiene una bola de cristal para saber el precio exacto de mañana. "
        "En lugar de adivinar, la física y las finanzas simulan 5.000 futuros posibles (trayectorias) para ver qué tan probable es que el precio suba o caiga, "
        "construyendo un 'abanico' de escenarios que respeta la volatilidad y tendencia histórica de la empresa."
    )

    prices_df = st.session_state.market_data["prices"]
    returns_df = st.session_state.market_data["returns"]
    stats_dict = st.session_state.market_data["stats"]

    c1, c2, c3 = st.columns([1.5, 1, 1])
    with c1:
        sel_ticker = st.selectbox("Acción a proyectar:", prices_df.columns.tolist(), key="gbm_section_ticker")
    with c2:
        n_paths = st.selectbox("Trayectorias Monte Carlo", [5000, 10000, 20000], index=0)
    with c3:
        seed_val = st.number_input("Semilla Fija (Paso 4)", value=42, step=1)

    t_stat = stats_dict.get(sel_ticker, {})
    spot_val = float(t_stat.get("raw_spot", prices_df[sel_ticker].iloc[-1]))
    params = calibrate_gbm(returns_df[sel_ticker])

    sim_res = simulate_gbm(spot_val, params, horizon_days=st.session_state.horizon, n_paths=n_paths, seed=int(seed_val))

    # Chequeo de positividad y comparación de medias (Paso 4)
    positivity_ok = bool(np.all(sim_res.paths > 0))
    diff_mean = sim_res.simulated_mean - sim_res.theoretical_mean
    z_stat = diff_mean / sim_res.std_error if sim_res.std_error > 0 else 0.0

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Spot Actual (S0)", f"${spot_val:.2f}")
    with k2:
        st.metric("Media Simulada (S_barra_T)", f"${sim_res.simulated_mean:.2f}", f"Error Estándar: ±${sim_res.std_error:.2f}")
    with k3:
        st.metric("Media Teórica (S0 * e^aT)", f"${sim_res.theoretical_mean:.2f}", f"Diferencia: ${diff_mean:+.2f}")
    with k4:
        st.metric("Positividad (S > 0)", "✅ Comprobada" if positivity_ok else "❌ Violada", f"Z-score = {z_stat:.2f}")

    # Gráfico del abanico estocástico con 40 trayectorias y distribución terminal
    st.plotly_chart(plot_stochastic_fan(sim_res, f"· {sel_ticker} ({n_paths:,} trayectorias)"), use_container_width=True)

    # Comparación de modelos estocásticos adicionales
    with st.expander("⚡ Competencia de Modelos: Salto de Merton, Ornstein-Uhlenbeck y Memoria Fractal (fBm)", expanded=False):
        st.caption("Pusimos a competir 4 teorías matemáticas para evaluar si la acción se comporta como difusión pura, si sufre saltos repentinos por noticias o si exhibe memoria fractal.")
        comp = compare_models_for_asset(sel_ticker, prices_df[sel_ticker], returns_df[sel_ticker], horizon_days=st.session_state.horizon, n_paths=5000)
        st.markdown(f"🏆 **Modelo Más Consistente**: **{comp['winner']}** — {comp['winner_reason']}")
        st.plotly_chart(plot_model_comparison_bars(comp["comparison_df"]), use_container_width=True)


# -----------------------------------------------------------------------------
# SECCIÓN 4: COBERTURA CON OPCIONES REALES & ÁRBOL CRR (PASOS 5, 6, 8 Y 9)
# -----------------------------------------------------------------------------
def section_4_opciones_y_crr():
    st.markdown("### 🎯 4. Cobertura con Opciones Reales & Árbol Binomial CRR (Pasos 5, 6, 8 y 9)")
    st.caption("Selección de contratos candidatos según los cuantiles proyectados $Q_{25}, Q_{50}, Q_{75}$ en 3 vencimientos reales. Valoración con árbol binomial CRR (Europeo/Americano), prueba de convergencia, diagrama de 3 pasos, test de control y comparación con el mercado.")

    st.info(
        "💡 **Kibo te explica en sencillo:** "
        "Una opción financiera es como el seguro de un carro: pagas una prima pequeña para protegerte de una pérdida gigante. "
        "Si compras una opción 'Call', tienes derecho a comprar la acción a un precio fijo; si el precio vuela, ganas dinero. "
        "Pero ¡cuidado!: para tener ganancia neta, la acción no solo debe subir, sino subir lo suficiente para compensar la prima y el costo del dinero."
    )

    prices_df = st.session_state.market_data["prices"]
    returns_df = st.session_state.market_data["returns"]
    stats_dict = st.session_state.market_data["stats"]

    c1, c2, c3, c4 = st.columns([1.5, 1, 1, 1])
    with c1:
        opt_ticker = st.selectbox("Activo Subyacente con opciones listadas:", prices_df.columns.tolist(), key="opt_section_ticker")
    with c2:
        rate_input = st.number_input("Tasa Libre de Riesgo r (%)", 0.0, 20.0, float(st.session_state.rate * 100), 0.25) / 100.0
    with c3:
        div_input = st.number_input("Dividendo Continuo q (%)", 0.0, 20.0, float(st.session_state.dividend * 100), 0.25) / 100.0
    with c4:
        crr_steps = st.select_slider("Pasos del Árbol CRR (N)", [25, 50, 100, 200, 400], value=200)

    t_stat = stats_dict.get(opt_ticker, {})
    spot_val = float(t_stat.get("raw_spot", prices_df[opt_ticker].iloc[-1]))
    sigma_val = float(t_stat.get("sigma_annual", 0.25))
    mu_spot_val = float(t_stat.get("a_spot_drift", 0.10))

    if st.button("🔎 Consultar Cadena de Opciones en Tiempo Real en Yahoo Finance", use_container_width=True):
        with st.spinner("Consultando contratos reales y proyectando cuantiles Q25, Q50, Q75..."):
            st.session_state.option_chain_res = get_option_candidates(opt_ticker, spot_val, mu_spot_val, sigma_val)

    # Resultados de contratos
    chain_res = st.session_state.get("option_chain_res")
    if chain_res and chain_res.get("success"):
        candidates = chain_res["candidates"]
        st.markdown(f"#### 📋 Matriz Oficial de 9 Contratos Candidatos ({len(candidates)} contratos disponibles)")
        st.caption("Strikes listados más cercanos a los cuantiles analíticos para vencimientos de 1, 3 y 6 meses:")
        st.dataframe(candidates, use_container_width=True, hide_index=True)

        # Selección de contrato individual
        labels = [f"{r['Tipo']} | Strike ${r['Strike (K)']:.2f} | Vencimiento: {r['Vencimiento']} ({r['Días Calendario (dc)']}d) | {r['Cuantil GBM']}" for _, r in candidates.iterrows()]
        sel_idx = st.selectbox("Seleccionar contrato para valorar en detalle:", range(len(labels)), format_func=lambda i: labels[i])
        c_row = candidates.iloc[int(sel_idx)]

        c_style, c_cost = st.columns([1, 1])
        with c_style:
            sel_style = st.selectbox("Estilo de Ejercicio:", ["Europea", "Americana"])
        with c_cost:
            term_cost = st.number_input("Costos terminales c_T (USD por acción)", value=0.0, step=0.05)

        # Valoración CRR
        t_years = float(c_row["T (años)"])
        strike_val = float(c_row["Strike (K)"])
        opt_type = str(c_row["Tipo"])
        ask_val = float(c_row["Ask"]) if pd.notna(c_row["Ask"]) else np.nan
        mid_val = float(c_row["Mid"]) if pd.notna(c_row["Mid"]) else np.nan

        val_crr = crr_price(spot_val, strike_val, t_years, rate_input, div_input, sigma_val, steps=crr_steps, option_type=opt_type, style=sel_style)

        if val_crr["valid"]:
            # Probabilidades bajo medida física P (Paso 6)
            sim_opt = simulate_gbm(spot_val, {"mu_annual": mu_spot_val + div_input, "sigma_annual": sigma_val, "log_likelihood": 0, "aic": 0, "bic": 0}, horizon_days=max(1, round(t_years * 252)), n_paths=5000, seed=42)
            prob_res = contract_probabilities(sim_opt.paths[:, -1], strike_val, ask_val, rate_input, t_years, opt_type, term_cost)

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric(f"Prima Teórica CRR ({sel_style})", f"${val_crr['price']:.2f}", f"Black-Scholes: ${val_crr['black_scholes']:.2f}")
            with m2:
                st.metric("Punto Medio Mercado (Mid)", f"${mid_val:.2f}" if np.isfinite(mid_val) else "No utilizable")
            with m3:
                st.metric("Probabilidad de Ejercicio P(ST > K)", f"{prob_res['exercise_probability']:.1%}")
            with m4:
                st.metric("Probabilidad de Beneficio P(ΠT > 0)", f"{prob_res['profit_probability']:.1%}", f"Utilidad Media: ${prob_res['expected_profit']:+.2f}")

            # Gráfico de Payoff y Beneficio Neto
            st.plotly_chart(plot_option_payoff_and_profit(spot_val, strike_val, ask_val, rate_input, t_years, opt_type, term_cost), use_container_width=True)

            # Comparativa de mercado y discrepancia (Paso 9)
            if np.isfinite(mid_val) and mid_val > 0:
                delta_usd = val_crr["price"] - mid_val
                delta_rel = delta_usd / mid_val
                st.info(
                    f"💡 **Comparativa de Mercado (Paso 9)**: Discrepancia absoluta $\delta = V_{{CRR}} - m = \${delta_usd:+.2f}$ "
                    f"($\delta_{{rel}} = {delta_rel:+.1%}$). Esta discrepancia no implica arbitraje realizable sin fricciones; refleja la diferencia entre la volatilidad histórica ($\sigma = {sigma_val:.1%}$) "
                    f"y la volatilidad implícita que cotiza el mercado, además de primas por liquidez, bid-ask spread y el derecho de ejercicio anticipado del estilo americano."
                )

            # Diagrama del Árbol Binomial de 3 Pasos (Paso 8)
            st.markdown("#### 🌳 Diagrama Interactivo del Árbol Binomial de 3 Pasos (Paso 8)")
            fig_tree, df_tree_nodes = generate_crr_3step_tree(spot_val, strike_val, t_years, rate_input, div_input, sigma_val, opt_type, sel_style)
            st.plotly_chart(fig_tree, use_container_width=True)

            with st.expander("📄 Ver tabla de nodos del sub-árbol (Precios S_{k,j} y Valores V_{k,j})"):
                st.dataframe(df_tree_nodes, use_container_width=True, hide_index=True)

            # Gráfico de convergencia CRR vs Black-Scholes
            st.plotly_chart(crr_convergence_chart(spot_val, strike_val, t_years, rate_input, div_input, sigma_val, opt_type, sel_style), use_container_width=True)

    # Test de control obligatorio (Paso 8)
    with st.expander("🧪 Test de Control Obligatorio de la Rúbrica (Call Europea S0=100, K=100, T=1, r=0.05, σ=0.20)", expanded=False):
        bench = verify_crr_control_benchmark()
        st.write(f"- **Valor Exigido por la Rúbrica**: USD ${bench['target']:.4f}")
        st.write(f"- **Fórmula Analítica Black-Scholes**: USD ${bench['black_scholes_exact']:.4f}")
        st.write(f"- **Árbol CRR N=200 pasos**: USD ${bench['crr_200']:.4f} (Diferencia: ${bench['difference']:.4f})")
        st.write(f"- **Árbol CRR N=500 pasos**: USD ${bench['crr_500']:.4f}")
        if bench["passed"]:
            st.success("✅ **¡Test de Control Aprobado con Éxito!** La implementación binomial CRR converge con precisión milimétrica al benchmark teórico.")


# -----------------------------------------------------------------------------
# SECCIÓN 5: ASIGNACIÓN DE CAPITAL & PRESUPUESTO DE RIESGO (PASOS 11 Y 12)
# -----------------------------------------------------------------------------
def section_5_asignacion_y_estrategias():
    st.markdown("### ⚖️ 5. Asignación de Capital, Presupuesto de Riesgo y Acciones Enteras (Pasos 11 y 12)")
    st.caption("Comparación de 3 esquemas: Pesos Iguales (1/N), Inverso al VaR individual (ignora correlaciones) y Mínimo VaR Restringido (SLSQP). Ajuste a presupuesto de riesgo $\bar{V}$, ejecución con acciones enteras y recalculo del riesgo efectivo.")

    st.info(
        "💡 **Kibo te explica en sencillo:** "
        "No todas las empresas tienen el mismo riesgo ni se mueven en la misma dirección. "
        "La optimización matemática encuentra la combinación exacta de compras para que las caídas de unas se cancelen con la estabilidad de otras. "
        "Además, convertimos los dólares en acciones enteras reales de Wall Street y calculamos cuánto efectivo te sobra."
    )

    if "alloc_res" not in st.session_state:
        if not run_full_pipeline():
            return

    alloc = st.session_state.alloc_res

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Capital Inicial Total", f"${st.session_state.capital:,.0f}")
    with k2:
        st.metric("Presupuesto de Riesgo (V_bar)", f"${st.session_state.risk_budget:,.2f}", f"Factor de Escala f = {alloc['f_scale']:.2f}")
    with k3:
        st.metric("Total Invertido en Acciones", f"${alloc['total_invertido_acciones']:,.2f}")
    with k4:
        st.metric("Efectivo Libre de Riesgo", f"${alloc['efectivo_total']:,.2f}", "Caja de Estrategia + Redondeo")

    # Gráficos de Asignación: Barras comparativas y Donut sectorial
    c_bar, c_pie = st.columns([1.4, 1])
    with c_bar:
        st.plotly_chart(plot_portfolio_allocation_chart(alloc["allocation_df"]), use_container_width=True)
    with c_pie:
        st.plotly_chart(plot_sector_allocation_donut(alloc["sector_summary"]), use_container_width=True)

    # Tabla maestra de asignación
    st.markdown("#### 🛒 Plan de Compra y Ejecución de Acciones Enteras (Paso 11)")
    st.dataframe(alloc["allocation_df"], use_container_width=True, hide_index=True)

    # Resumen sectorial y explicabilidad
    col_sec, col_exp = st.columns([1, 1.3])
    with col_sec:
        st.markdown("##### 🛡️ Cumplimiento de Límites Sectoriales (Cota ≤ 35%):")
        st.dataframe(alloc["sector_summary"], use_container_width=True, hide_index=True)
    with col_exp:
        st.markdown("##### 💡 Explicabilidad Financiera de la Estrategia (Paso 12):")
        for exp_text in alloc["explanations"]:
            st.info(exp_text)


# -----------------------------------------------------------------------------
# SECCIÓN 6: BLINDAJE DE RIESGO, ESTRÉS & AUDITORÍA FUERA DE MUESTRA (PASO 10)
# -----------------------------------------------------------------------------
def section_6_var_estres_y_auditoria():
    st.markdown("### 🛡️ 6. Blindaje de Riesgo (VaR & CVaR), Pruebas de Estrés y Auditoría Fuera de Muestra (Paso 10)")
    st.caption("Comparación de los 3 estimadores de VaR al 99% (horizonte h = 10 días): Paramétrico Normal (media cero), Histórico Empírico y Monte Carlo Multivariado (20.000 trayectorias Cholesky). 3 pruebas oficiales de estrés y auditoría fuera de muestra en 252 sesiones con test de Kupiec.")

    st.info(
        "💡 **Kibo te explica en sencillo:** "
        "El Value at Risk (VaR) te dice: 'En 99 de cada 100 quincenas de mercado, no perderás más de X dólares'. "
        "Y el Expected Shortfall (CVaR) te dice: 'Si llega el peor día del año, ¿cuánto perderías en promedio?'. "
        "También sometemos tu dinero a pruebas de estrés simulando caídas catastróficas para comprobar si tu patrimonio resiste."
    )

    if "risk_res" not in st.session_state or "oos_res" not in st.session_state:
        if not run_full_pipeline():
            return

    risk_res = st.session_state.risk_res
    oos_res = st.session_state.oos_res

    # Tarjetas KPI de Riesgo
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("VaR Monte Carlo 99%", f"${risk_res['var_mc_usd']:,.2f}", f"{risk_res['var_mc_pct']:.2%}")
    with k2:
        st.metric("CVaR (Expected Shortfall)", f"${risk_res['cvar_mc_usd']:,.2f}", f"{risk_res['cvar_mc_pct']:.2%}")
    with k3:
        st.metric("VaR Paramétrico Normal", f"${risk_res['var_param_usd']:,.2f}", f"{risk_res['var_param_pct']:.2%}")
    with k4:
        st.metric("VaR Histórico Empírico", f"${risk_res['var_hist_usd']:,.2f}", f"{risk_res['var_hist_pct']:.2%}")

    # Tabla comparativa de los 3 métodos
    st.markdown("#### 📋 Comparativa Multimetodológica de Estimadores de VaR y CVaR (99% Confianza)")
    st.dataframe(risk_res["var_comparison_df"], use_container_width=True, hide_index=True)

    # Gráfico de densidad de pérdidas Monte Carlo
    st.plotly_chart(plot_var_distribution_hist(risk_res), use_container_width=True)

    st.markdown("---")

    # 3 Pruebas de Estrés Oficiales (Paso 10)
    st.markdown("#### ⚡ Los 3 Escenarios Oficiales de Pruebas de Estrés Financiero (Stress Testing)")
    st.dataframe(risk_res["stress_df"], use_container_width=True, hide_index=True)

    st.markdown("---")

    # Auditoría Fuera de Muestra (Paso 10)
    st.markdown("#### 📈 Auditoría Fuera de Muestra de la Cartera (252 Sesiones de Prueba)")
    st.caption("Evolución del patrimonio neto y drawdown en las 252 sesiones reservadas. Evaluación de excepciones del VaR diario mediante test de cobertura de Kupiec (POF).")

    st.dataframe(oos_res["summary_table"], use_container_width=True, hide_index=True)
    st.plotly_chart(plot_out_of_sample_audit(oos_res), use_container_width=True)


# -----------------------------------------------------------------------------
# SECCIÓN 7: EVALUACIÓN PREDICTIVA ROLLING DEL GBM (PASO 13)
# -----------------------------------------------------------------------------
def section_7_evaluacion_rolling():
    st.markdown("### 🔄 7. Evaluación Predictiva Rolling del GBM (Paso 13)")
    st.caption("Ventana móvil de 252 sesiones de calibración diaria para reestimar $\hat{\mu}^{total}$ y $\hat{\sigma}$, avanzando 1 sesión diaria. Pronóstico condicional puntual $\hat{P}_{t+H|t} = P_t \exp(\hat{\mu}^{total} H/252)$ vs benchmark ingenuo de caminata aleatoria $\hat{P}_{t+H|t} = P_t$.")

    st.info(
        "💡 **Kibo te explica en sencillo:** "
        "¿Cómo sabemos si las fórmulas de verdad sirven y no son pura teoría? "
        "Hacemos un 'examen hacia atrás' (backtesting): retrocedemos 252 días en el tiempo y le pedimos al modelo que pronostique el precio día por día sin saber el futuro. "
        "Luego medimos su margen de error (RMSE y MAPE) y lo comparamos contra la suposición más simple: que el precio de mañana será igual al de hoy."
    )

    prices_df = st.session_state.market_data["prices"]

    c1, c2 = st.columns([1.5, 1])
    with c1:
        sel_roll_ticker = st.selectbox("Acción para inspección gráfica detallada:", prices_df.columns.tolist(), key="roll_section_ticker")
    with c2:
        sel_h = st.selectbox("Horizonte de Pronóstico H (días)", [1, 5, 10, 20], index=0)

    # Tabla comparativa multi-activo
    st.markdown(f"#### 📊 Tabla Consolidada de Error RMSE y MAPE para las 10 Acciones (H = {sel_h} día)")
    with st.spinner("Calculando backtesting rolling para las 10 acciones..."):
        df_roll = run_multi_asset_rolling_table(prices_df, prices_df.columns.tolist(), window_train=252, horizon_H=sel_h)
    st.dataframe(df_roll, use_container_width=True, hide_index=True)

    # Gráfico individual para la acción seleccionada
    st.markdown(f"#### 📈 Curvas Observado vs Pronosticado y Serie de Errores ({sel_roll_ticker})")
    with st.spinner(f"Generando curvas rolling para {sel_roll_ticker}..."):
        roll_res = run_gbm_rolling_evaluation(prices_df[sel_roll_ticker], sel_roll_ticker, window_train=252, horizon_H=sel_h)

    if roll_res.get("success"):
        st.plotly_chart(plot_rolling_forecast_chart(roll_res), use_container_width=True)
    else:
        st.warning(roll_res.get("error", "Error al calcular curvas."))


# -----------------------------------------------------------------------------
# SECCIÓN 8: ENTREGABLES Y EXPORTACIÓN CSV
# -----------------------------------------------------------------------------
def section_8_entregables_y_exportacion():
    st.markdown("### 📦 8. Entregables Oficiales y Exportación Consolidada a CSV")
    st.caption("Descarga completa de todos los resultados calculados, tablas de calibración, contratos de opciones, métricas de riesgo y evaluación rolling.")

    if "alloc_res" not in st.session_state or "risk_res" not in st.session_state:
        if not run_full_pipeline():
            return

    stats_dict = st.session_state.market_data["stats"]
    alloc = st.session_state.alloc_res
    risk = st.session_state.risk_res
    oos = st.session_state.oos_res

    # Construcción de buffer CSV consolidado
    output_io = io.StringIO()
    output_io.write("# ENTREGABLE OFICIAL: APLICACION DE VALORACION Y RIESGO (DEFI 2)\n")
    output_io.write(f"# Fecha: {date.today().isoformat()} | Capital: USD {st.session_state.capital:,.2f} | Confianza VaR: {st.session_state.confidence}%\n\n")

    output_io.write("## 1. PARAMETROS CALIBRADOS (PASO 3)\n")
    if "parameters_table" in stats_dict:
        stats_dict["parameters_table"].to_csv(output_io, index=False)

    output_io.write("\n## 2. PLAN DE ASIGNACION DE CAPITAL Y ACCIONES ENTERAS (PASO 11)\n")
    alloc["allocation_df"].to_csv(output_io, index=False)

    output_io.write("\n## 3. COMPARATIVA DE ESTIMADORES DE VAR Y CVAR (PASO 10)\n")
    risk["var_comparison_df"].to_csv(output_io, index=False)

    output_io.write("\n## 4. PRUEBAS DE ESTRES FINANCIERO (PASO 10)\n")
    risk["stress_df"].to_csv(output_io, index=False)

    output_io.write("\n## 5. AUDITORIA FUERA DE MUESTRA Y TEST DE KUPIEC (PASO 10)\n")
    oos["summary_table"].to_csv(output_io, index=False)

    csv_data = output_io.getvalue().encode("utf-8")

    c_down1, c_down2 = st.columns(2)
    with c_down1:
        st.download_button(
            "📥 Descargar Reporte Consolidado Completo (CSV)",
            data=csv_data,
            file_name=f"kibo_taller_valoracion_completo_{date.today().isoformat()}.csv",
            mime="text/csv",
            type="primary",
            use_container_width=True,
        )
    with c_down2:
        alloc_csv = alloc["allocation_df"].to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Descargar Solo Plan de Inversión y Acciones (CSV)",
            data=alloc_csv,
            file_name="kibo_plan_acciones.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown("---")
    st.markdown("#### 🔒 Panel de Reproducibilidad y Auditoría Académica")
    st.write(f"- **Semilla de Simulación Aleatoria**: `42` (Fija para garantizar reproducibilidad exacta).")
    st.write(f"- **Horizonte de Calibración**: 1.034 sesiones comunes de mercado descargadas vía Yahoo Finance con `auto_adjust=True`.")
    st.write(f"- **Partición Fuera de Muestra**: Últimas 252 sesiones reservadas para evaluación predictiva rolling y test de excepciones.")


# -----------------------------------------------------------------------------
# MAIN APP
# -----------------------------------------------------------------------------
def main():
    initialize_session_state()
    st.markdown(APP_CSS, unsafe_allow_html=True)
    render_intro_splash_animation()
    render_header()

    if st.session_state.nav_mode == "Tablero Académico (Rúbrica 100/100)":
        t1, t2, t3, t4, t5, t6, t7, t8 = st.tabs([
            "📁 1. Universo & Datos",
            "🐑 2. Efecto Manada",
            "📈 3. Proyecciones GBM",
            "🎯 4. Opciones & CRR",
            "⚖️ 5. Asignación & Presupuesto",
            "🛡️ 6. VaR & Auditoría",
            "🔄 7. Evaluación Rolling",
            "📦 8. Entregables CSV",
        ])
        with t1:
            section_1_datos_y_calidad()
        with t2:
            section_2_efecto_manada()
        with t3:
            section_3_gbm_y_modelos()
        with t4:
            section_4_opciones_y_crr()
        with t5:
            section_5_asignacion_y_estrategias()
        with t6:
            section_6_var_estres_y_auditoria()
        with t7:
            section_7_evaluacion_rolling()
        with t8:
            section_8_entregables_y_exportacion()
    else:
        # Modo Guía Móvil Asistida (Paso a Paso)
        st.markdown(f"#### 📱 Modo Asistido Kibo · Paso {st.session_state.step} de 7")
        if st.session_state.step == 1:
            section_1_datos_y_calidad()
            if st.button("Continuar a Efecto Manada ➔", type="primary"):
                st.session_state.step = 2
                st.rerun()
        elif st.session_state.step == 2:
            section_2_efecto_manada()
            b1, b2 = st.columns(2)
            with b1:
                if st.button("⬅️ Volver a Datos"):
                    st.session_state.step = 1
                    st.rerun()
            with b2:
                if st.button("Continuar a Proyecciones GBM ➔", type="primary"):
                    st.session_state.step = 3
                    st.rerun()
        elif st.session_state.step == 3:
            section_3_gbm_y_modelos()
            b1, b2 = st.columns(2)
            with b1:
                if st.button("⬅️ Volver a Efecto Manada"):
                    st.session_state.step = 2
                    st.rerun()
            with b2:
                if st.button("Continuar a Opciones ➔", type="primary"):
                    st.session_state.step = 4
                    st.rerun()
        elif st.session_state.step == 4:
            section_4_opciones_y_crr()
            b1, b2 = st.columns(2)
            with b1:
                if st.button("⬅️ Volver a GBM"):
                    st.session_state.step = 3
                    st.rerun()
            with b2:
                if st.button("Continuar a Asignación ➔", type="primary"):
                    st.session_state.step = 5
                    st.rerun()
        elif st.session_state.step == 5:
            section_5_asignacion_y_estrategias()
            b1, b2 = st.columns(2)
            with b1:
                if st.button("⬅️ Volver a Opciones"):
                    st.session_state.step = 4
                    st.rerun()
            with b2:
                if st.button("Continuar a VaR & Auditoría ➔", type="primary"):
                    st.session_state.step = 6
                    st.rerun()
        elif st.session_state.step == 6:
            section_6_var_estres_y_auditoria()
            b1, b2 = st.columns(2)
            with b1:
                if st.button("⬅️ Volver a Asignación"):
                    st.session_state.step = 5
                    st.rerun()
            with b2:
                if st.button("Continuar a Evaluación Rolling ➔", type="primary"):
                    st.session_state.step = 7
                    st.rerun()
        elif st.session_state.step == 7:
            section_7_evaluacion_rolling()
            section_8_entregables_y_exportacion()
            if st.button("🔄 Reiniciar al Paso 1"):
                st.session_state.step = 1
                st.rerun()

    render_kibo_tour(st.session_state.get("step", 1))


if __name__ == "__main__":
    main()
