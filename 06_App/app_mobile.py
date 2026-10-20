from datetime import date, timedelta

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Nexa | Tu portafolio",
    page_icon="N",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ASSET_CATALOG = {
    "AAPL": "Tecnología",
    "AMZN": "Consumo cíclico",
    "GOOGL": "Comunicaciones",
    "JNJ": "Salud",
    "JPM": "Servicios financieros",
    "MSFT": "Tecnología",
    "NEE": "Servicios públicos",
    "NVDA": "Tecnología",
    "PG": "Consumo defensivo",
    "TSLA": "Consumo cíclico",
    "UNH": "Salud",
    "V": "Servicios financieros",
    "XOM": "Energía",
}
SECTORS = sorted(set(ASSET_CATALOG.values()))
DEFAULT_TICKERS = ["AAPL", "MSFT", "GOOGL", "JPM", "XOM", "JNJ", "AMZN", "PG", "NEE", "NVDA"]

APP_CSS = """
<style>
    :root { --ink: #172033; --muted: #657083; --paper: #f7f7f4; --line: #dce1e7; --blue: #174a7e; --blue-dark: #113960; --soft-blue: #eaf1f8; }
    .stApp { background: var(--paper); color: var(--ink); }
    [data-testid="stHeader"], [data-testid="stSidebar"] { background: transparent; }
    [data-testid="stSidebar"] { display: none; }
    .block-container { max-width: 760px; padding: 1.25rem 1.25rem 3rem; }
    .app-header { align-items: center; border-bottom: 1px solid var(--line); display: flex; gap: .5rem; margin-bottom: 2.2rem; padding-bottom: 1rem; }
    .brand-mark { align-items: center; background: var(--blue); border-radius: 7px; color: white; display: inline-flex; font-size: .85rem; font-weight: 800; height: 26px; justify-content: center; width: 26px; }
    .brand-name { font-size: 1.05rem; font-weight: 750; letter-spacing: -.02em; } .header-note { color: var(--muted); font-size: .83rem; margin-left: auto; }
    .progress { display: flex; gap: .25rem; margin: 0 0 2.4rem; } .progress-item { align-items: center; color: #9aa3ae; display: flex; flex: 1; font-size: .78rem; gap: .4rem; min-width: 0; } .progress-item::after { background: var(--line); content: ''; flex: 1; height: 1px; margin-left: .2rem; } .progress-item:last-child::after { display: none; } .progress-item span { align-items: center; border: 1px solid currentColor; border-radius: 50%; display: inline-flex; flex: 0 0 auto; font-size: .7rem; height: 21px; justify-content: center; width: 21px; } .progress-item small { font-size: .74rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; } .progress-item.is-active { color: var(--blue); font-weight: 700; } .progress-item.is-done { color: #3c6d55; }
    .eyebrow { color: var(--blue); font-size: .72rem; font-weight: 800; letter-spacing: .11em; margin-bottom: .55rem; } h1 { font-size: clamp(2rem, 7vw, 3.15rem) !important; font-weight: 720 !important; letter-spacing: -.05em; line-height: 1.06; margin-bottom: .7rem !important; } .lead { color: var(--muted); font-size: 1.05rem; line-height: 1.6; margin-bottom: 2rem; }
    [data-testid="stVerticalBlockBorderWrapper"] { background: white; border: 1px solid var(--line) !important; border-radius: 12px; box-shadow: none; padding: .4rem; } .stRadio label { border: 1px solid var(--line); border-radius: 10px; margin-bottom: .5rem; padding: .7rem .75rem; } .stRadio label:has(input:checked) { background: var(--soft-blue); border-color: var(--blue); }
    .stButton > button { border: 1px solid var(--blue); border-radius: 8px; font-weight: 700; min-height: 2.8rem; } .stButton > button[kind="primary"] { background: var(--blue); color: white; } .stButton > button[kind="primary"]:hover { background: var(--blue-dark); border-color: var(--blue-dark); }
    .stTextInput input, .stNumberInput input, [data-baseweb="select"] > div { background: white; border-color: #c9d0d9; border-radius: 8px; } .quiet-summary { background: var(--soft-blue); border-radius: 8px; color: var(--blue-dark); margin: 1.25rem 0; padding: .75rem .9rem; } .summary-number { background: white; border: 1px solid var(--line); border-radius: 12px; padding: 1.25rem; } .summary-number span, .summary-number small { color: var(--muted); display: block; } .summary-number strong { display: block; font-size: 1.85rem; letter-spacing: -.04em; margin: .25rem 0; } .explanation { background: #edf5ef; border-left: 3px solid #41765a; color: #28513a; line-height: 1.55; margin: 1.4rem 0; padding: 1rem; }
    [data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 8px; overflow: hidden; } [data-testid="stMetric"] { background: white; border: 1px solid var(--line); border-radius: 10px; padding: .9rem; }
    @media (max-width: 640px) { .block-container { padding: 1rem 1rem 2.5rem; } .header-note { display: none; } .progress { gap: .1rem; } .progress-item { flex: 0 0 auto; } .progress-item::after { width: 14px; flex: 0 0 14px; } .progress-item small { display: none; } .stRadio label { font-size: .92rem; } }
</style>
"""


def portfolio_from_tickers(tickers):
    return pd.DataFrame({"Ticker": tickers, "Sector": [ASSET_CATALOG.get(ticker, "Por clasificar") for ticker in tickers]})


def initialize_state():
    defaults = {
        "step": 1,
        "capital": 100000,
        "profile": "Moderado",
        "tickers": DEFAULT_TICKERS,
        "portfolio": portfolio_from_tickers(DEFAULT_TICKERS),
        "confidence": 99,
        "horizon": 10,
        "start_date": date.today() - timedelta(days=365 * 3 + 30),
        "end_date": date.today(),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def move_to(step):
    st.session_state.step = step
    st.rerun()


def render_progress(current_step):
    steps = [(1, "Tu punto de partida"), (2, "Tus activos"), (3, "Confirma")]
    items = []
    for number, label in steps:
        state = "is-active" if number == current_step else "is-done" if number < current_step else ""
        items.append(f"<div class='progress-item {state}'><span>{number}</span><small>{label}</small></div>")
    st.markdown(f"<div class='progress'>{''.join(items)}</div>", unsafe_allow_html=True)


def header():
    st.markdown("<div class='app-header'><span class='brand-mark'>N</span><span class='brand-name'>Nexa</span><span class='header-note'>Valoración y riesgo</span></div>", unsafe_allow_html=True)


def welcome_step():
    render_progress(1)
    st.markdown("<p class='eyebrow'>CONFIGURACIÓN INICIAL</p><h1>Empecemos por lo importante.</h1><p class='lead'>Con tres decisiones prepararemos un análisis que se adapte a ti. Podrás cambiar todo antes de calcular.</p>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("#### ¿Cuánto quieres analizar?")
        st.session_state.capital = st.number_input("Capital inicial (USD)", min_value=1000, max_value=10000000, value=st.session_state.capital, step=5000, label_visibility="collapsed")
        st.caption("No se invierte dinero ni se ejecutan órdenes desde esta aplicación.")
    st.markdown("#### ¿Cómo te sientes frente al riesgo?")
    profile_copy = {"Conservador": "Prefiero limitar movimientos fuertes, incluso si el potencial de retorno es menor.", "Moderado": "Busco un equilibrio entre estabilidad y crecimiento.", "Agresivo": "Acepto variaciones mayores para buscar mayor crecimiento."}
    st.session_state.profile = st.radio("Perfil de riesgo", options=list(profile_copy), index=list(profile_copy).index(st.session_state.profile), format_func=lambda item: f"{item} — {profile_copy[item]}", label_visibility="collapsed")
    st.button("Continuar", type="primary", use_container_width=True, on_click=move_to, args=(2,))


def assets_step():
    render_progress(2)
    st.markdown("<p class='eyebrow'>UNIVERSO DE INVERSIÓN</p><h1>Elige los activos que quieres explorar.</h1><p class='lead'>Comenzamos con una selección diversificada para el taller. Puedes quitar activos o añadir otros; sus sectores se podrán corregir después.</p>", unsafe_allow_html=True)
    selected = st.multiselect("Acciones disponibles", options=list(ASSET_CATALOG), default=st.session_state.tickers, help="Escribe para buscar y toca una acción para añadirla o retirarla.")
    st.session_state.tickers = selected
    st.session_state.portfolio = portfolio_from_tickers(selected)
    asset_count = len(selected)
    sector_count = st.session_state.portfolio["Sector"].nunique() if asset_count else 0
    st.markdown(f"<div class='quiet-summary'><strong>{asset_count} activos</strong> · {sector_count} sectores seleccionados</div>", unsafe_allow_html=True)
    if asset_count < 10:
        st.info("El taller utiliza 10 acciones; puedes continuar con menos si deseas explorar un caso personalizado.")
    back, next_step = st.columns(2)
    with back:
        st.button("Atrás", use_container_width=True, on_click=move_to, args=(1,))
    with next_step:
        st.button("Revisar selección", type="primary", use_container_width=True, on_click=move_to, args=(3,))


def confirmation_step():
    render_progress(3)
    st.markdown("<p class='eyebrow'>CONFIRMACIÓN</p><h1>Esto es lo que analizaremos.</h1><p class='lead'>Primero organizamos tus datos. Después la app generará proyecciones, riesgo y una asignación explicable.</p>", unsafe_allow_html=True)
    left, right = st.columns([1, 1], gap="large")
    with left:
        st.markdown(f"<div class='summary-number'><span>Capital a analizar</span><strong>USD {st.session_state.capital:,.0f}</strong><small>Perfil {st.session_state.profile.lower()}</small></div>", unsafe_allow_html=True)
    with right:
        st.markdown("#### Activos seleccionados")
        st.dataframe(st.session_state.portfolio, hide_index=True, use_container_width=True)
    st.markdown("<div class='explanation'><strong>Qué ocurrirá después</strong><br>Validaremos precios y sectores, mostraremos la calidad de los datos y, cuando apruebes esa etapa, activaremos los modelos financieros.</div>", unsafe_allow_html=True)
    back, next_step = st.columns(2)
    with back:
        st.button("Modificar activos", use_container_width=True, on_click=move_to, args=(2,))
    with next_step:
        st.button("Ver mi resumen", type="primary", use_container_width=True, on_click=move_to, args=(4,))


def overview():
    st.markdown("<p class='eyebrow'>TU CONFIGURACIÓN</p><h1>Tu análisis está listo para comenzar.</h1><p class='lead'>Revisa la configuración o modifícala cuando quieras. Los cálculos se incorporarán en el siguiente módulo.</p>", unsafe_allow_html=True)
    first, second, third = st.columns(3)
    with first:
        st.metric("Capital", f"USD {st.session_state.capital:,.0f}")
    with second:
        st.metric("Perfil", st.session_state.profile)
    with third:
        st.metric("Activos", len(st.session_state.portfolio))
    st.markdown("#### Distribución por sector")
    if st.session_state.portfolio.empty:
        st.info("Añade al menos un activo para ver la distribución.")
    else:
        st.bar_chart(st.session_state.portfolio.groupby("Sector").size().sort_values(ascending=True), color="#174a7e", horizontal=True)
    with st.expander("Modificar mi configuración"):
        st.session_state.capital = st.number_input("Capital a analizar (USD)", min_value=1000, max_value=10000000, value=st.session_state.capital, step=5000)
        st.session_state.profile = st.selectbox("Perfil de riesgo", ["Conservador", "Moderado", "Agresivo"], index=["Conservador", "Moderado", "Agresivo"].index(st.session_state.profile))
        edited = st.data_editor(st.session_state.portfolio, hide_index=True, use_container_width=True, num_rows="dynamic", column_config={"Ticker": st.column_config.TextColumn("Ticker", required=True), "Sector": st.column_config.SelectboxColumn("Sector", options=SECTORS, required=True)})
        if st.button("Guardar cambios", type="primary"):
            st.session_state.portfolio = edited.assign(Ticker=lambda frame: frame["Ticker"].astype(str).str.upper().str.strip())
            st.session_state.tickers = st.session_state.portfolio["Ticker"].tolist()
            st.rerun()
    st.button("Empezar de nuevo", use_container_width=True, on_click=move_to, args=(1,))


def main():
    initialize_state()
    st.markdown(APP_CSS, unsafe_allow_html=True)
    header()
    if st.session_state.step == 1:
        welcome_step()
    elif st.session_state.step == 2:
        assets_step()
    elif st.session_state.step == 3:
        confirmation_step()
    else:
        overview()


if __name__ == "__main__":
    main()
