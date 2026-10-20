from datetime import date, timedelta

import pandas as pd
import streamlit as st

from ui.styles import APP_CSS


st.set_page_config(page_title="NEXA | Valoración y Riesgo", page_icon="◈", layout="wide", initial_sidebar_state="expanded")

SECTORS = ["Tecnología", "Servicios financieros", "Energía", "Salud", "Consumo cíclico", "Consumo defensivo", "Servicios públicos", "Industriales", "Materiales", "Inmobiliario", "Comunicaciones"]
PRESET_PORTFOLIO = [("AAPL", "Tecnología"), ("MSFT", "Tecnología"), ("GOOGL", "Comunicaciones"), ("JPM", "Servicios financieros"), ("XOM", "Energía"), ("JNJ", "Salud"), ("AMZN", "Consumo cíclico"), ("PG", "Consumo defensivo"), ("NEE", "Servicios públicos"), ("NVDA", "Tecnología")]


def portfolio_frame(assets=PRESET_PORTFOLIO):
    return pd.DataFrame(assets, columns=["Ticker", "Sector"]).assign(Mercado="NYSE / NASDAQ", Estado="Listo")


def initialize_state():
    defaults = {"portfolio": portfolio_frame(), "capital": 100000, "confidence": 99, "horizon": 10, "risk_free_rate": 4.5, "investment_profile": "Moderado", "start_date": date.today() - timedelta(days=365 * 3 + 30), "end_date": date.today()}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def metric_card(label, value, note):
    st.markdown(f"<div class='glass-card'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div><div class='metric-note'>{note}</div></div>", unsafe_allow_html=True)


def sidebar():
    with st.sidebar:
        st.markdown("<div class='eyebrow'>NEXA FINANCE</div>", unsafe_allow_html=True)
        st.markdown("## Constructor de portafolio")
        st.caption("Valoración, riesgo y decisiones explicables.")
        st.divider()
        for number, title, active in [("01", "Universo de inversión", True), ("02", "Parámetros de análisis", False), ("03", "Resumen y ejecución", False)]:
            active_class = " step-active" if active else ""
            st.markdown(f"<div class='step-card{active_class}'><div class='step-number'>{number}</div><div class='step-name'>{title}</div></div>", unsafe_allow_html=True)
        st.divider()
        st.caption("Base de interfaz · Fase 0")
        st.caption("Los cálculos se activarán después de validar esta experiencia.")


def asset_tab():
    st.markdown("<div class='section-title'>Universo de inversión</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-copy'>Parte del preset académico o personaliza cada posición. El sector es editable para corregir la clasificación automática futura.</div>", unsafe_allow_html=True)
    action_left, action_right, _ = st.columns([1.25, 1.25, 4])
    with action_left:
        if st.button("Restaurar preset del taller", use_container_width=True):
            st.session_state.portfolio = portfolio_frame()
            st.rerun()
    with action_right:
        if st.button("Limpiar selección", use_container_width=True):
            st.session_state.portfolio = portfolio_frame([])
            st.rerun()

    with st.form("add_asset", clear_on_submit=True):
        ticker_col, sector_col, add_col = st.columns([1.1, 1.8, .75])
        with ticker_col:
            ticker = st.text_input("Nuevo ticker", placeholder="Ej. TSLA").upper().strip()
        with sector_col:
            sector = st.selectbox("Sector", SECTORS)
        with add_col:
            st.write("")
            submitted = st.form_submit_button("Añadir activo", use_container_width=True, type="primary")
        if submitted:
            existing = st.session_state.portfolio["Ticker"].str.upper().tolist()
            if not ticker:
                st.warning("Escribe un ticker antes de añadirlo.")
            elif ticker in existing:
                st.warning(f"{ticker} ya pertenece al universo.")
            else:
                new_row = pd.DataFrame([[ticker, sector, "NYSE / NASDAQ", "Pendiente"]], columns=st.session_state.portfolio.columns)
                st.session_state.portfolio = pd.concat([st.session_state.portfolio, new_row], ignore_index=True)
                st.rerun()

    edited_portfolio = st.data_editor(st.session_state.portfolio, hide_index=True, use_container_width=True, num_rows="dynamic", column_config={"Ticker": st.column_config.TextColumn("Ticker", required=True, help="Símbolo bursátil en mayúsculas."), "Sector": st.column_config.SelectboxColumn("Sector", options=SECTORS, required=True), "Mercado": st.column_config.TextColumn("Mercado", disabled=True), "Estado": st.column_config.TextColumn("Estado", disabled=True)}, key="portfolio_editor")
    st.session_state.portfolio = edited_portfolio.assign(Ticker=lambda frame: frame["Ticker"].astype(str).str.upper().str.strip())
    asset_count = len(st.session_state.portfolio)
    sector_count = st.session_state.portfolio["Sector"].nunique()
    if asset_count < 10:
        st.info(f"Faltan {10 - asset_count} activos para el requisito base del taller. Puedes continuar en modo libre.")
    elif sector_count < 4:
        st.warning("Añade o reclasifica activos para cubrir al menos cuatro sectores.")
    else:
        st.success("Tu selección cumple la estructura base del taller: 10 activos y al menos 4 sectores.")


def parameters_tab():
    st.markdown("<div class='section-title'>Marco de riesgo</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-copy'>Estas decisiones acompañarán los cálculos en las siguientes fases. Por ahora puedes probar cómo se siente la configuración.</div>", unsafe_allow_html=True)
    left, right = st.columns(2, gap="large")
    with left:
        st.session_state.capital = st.number_input("Capital a invertir (USD)", min_value=1000, max_value=10000000, value=st.session_state.capital, step=5000)
        st.session_state.investment_profile = st.select_slider("Perfil de inversión", options=["Conservador", "Moderado", "Agresivo"], value=st.session_state.investment_profile)
        st.session_state.risk_free_rate = st.number_input("Tasa libre de riesgo anual (%)", min_value=0.0, max_value=25.0, value=st.session_state.risk_free_rate, step=.1)
    with right:
        st.session_state.confidence = st.select_slider("Nivel de confianza VaR", options=[90, 95, 97.5, 99], value=st.session_state.confidence)
        st.session_state.horizon = st.select_slider("Horizonte VaR (sesiones)", options=[1, 5, 10, 20], value=st.session_state.horizon)
        date_range = st.date_input("Historial para analizar", value=(st.session_state.start_date, st.session_state.end_date), max_value=date.today())
        if isinstance(date_range, tuple) and len(date_range) == 2:
            st.session_state.start_date, st.session_state.end_date = date_range


def review_tab():
    st.markdown("<div class='section-title'>Tu decisión, antes de calcular</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-copy'>Este resumen convierte la configuración en una confirmación clara antes de conectarla a datos de mercado y modelos cuantitativos.</div>", unsafe_allow_html=True)
    summary_left, summary_right = st.columns([1.35, 1])
    with summary_left:
        summary = st.session_state.portfolio.groupby("Sector", as_index=False).agg(Activos=("Ticker", "count"))
        st.bar_chart(summary.set_index("Sector"), color="#30d5c8", horizontal=True)
    with summary_right:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### Configuración seleccionada")
        st.write(f"**Perfil:** {st.session_state.investment_profile}")
        st.write(f"**Capital:** USD {st.session_state.capital:,.0f}")
        st.write(f"**VaR:** {st.session_state.confidence}% a {st.session_state.horizon} sesiones")
        st.write(f"**Periodo:** {st.session_state.start_date:%d %b %Y} — {st.session_state.end_date:%d %b %Y}")
        st.caption("La ejecución cuantitativa se habilitará al aprobar esta base de interfaz.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.button("Preparar análisis cuantitativo", type="primary", use_container_width=True, disabled=True, help="Disponible en la siguiente fase.")


def main():
    initialize_state()
    st.markdown(APP_CSS, unsafe_allow_html=True)
    sidebar()
    st.markdown("<div class='eyebrow'>CONFIGURACIÓN DEL ANÁLISIS</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-title'>Construye una cartera con criterio.</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-copy'>Selecciona tus activos, ajusta su clasificación y define el marco de riesgo. La aplicación preparará esta decisión para los módulos de datos, GBM, opciones y asignación.</div>", unsafe_allow_html=True)
    asset_count = len(st.session_state.portfolio)
    sector_count = st.session_state.portfolio["Sector"].nunique()
    validation = "Cumple base" if asset_count == 10 and sector_count >= 4 else "Modo personalizado"
    metrics = st.columns(4)
    with metrics[0]: metric_card("Capital inicial", f"USD {st.session_state.capital:,.0f}", "Editable en parámetros")
    with metrics[1]: metric_card("Activos", str(asset_count), "Universo seleccionado")
    with metrics[2]: metric_card("Sectores", str(sector_count), "Diversificación actual")
    with metrics[3]: metric_card("Validación", validation, "Requisito del taller")
    assets, parameters, review = st.tabs(["01 · Activos", "02 · Parámetros", "03 · Revisión"])
    with assets: asset_tab()
    with parameters: parameters_tab()
    with review: review_tab()


if __name__ == "__main__":
    main()
