from datetime import date, timedelta
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Kibo | Tu copiloto de inversión",
    page_icon="🤖",
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
    :root { 
        --ink: #0f172a; 
        --muted: #475569; 
        --paper: #f8fafc; 
        --line: #cbd5e1; 
        --blue: #0284c7; 
        --blue-dark: #0369a1; 
        --soft-blue: #e0f2fe; 
    }
    .stApp { background: var(--paper); color: var(--ink); }
    [data-testid="stHeader"], [data-testid="stSidebar"] { background: transparent; }
    [data-testid="stSidebar"] { display: none; }
    .block-container { max-width: 760px; padding: 1.25rem 1.25rem 3rem; }
    
    /* Header Kibo */
    .app-header { 
        align-items: center; 
        border-bottom: 1.5px solid var(--line); 
        display: flex; 
        gap: .65rem; 
        margin-bottom: 2rem; 
        padding-bottom: 0.9rem; 
    }
    .brand-mark { 
        align-items: center; 
        background: linear-gradient(135deg, #0284c7, #2563eb); 
        border-radius: 8px; 
        color: white; 
        display: inline-flex; 
        font-size: .95rem; 
        font-weight: 800; 
        height: 30px; 
        justify-content: center; 
        width: 30px; 
        box-shadow: 0 2px 8px rgba(2, 132, 199, 0.4);
    }
    .brand-name { font-size: 1.15rem; font-weight: 800; letter-spacing: -.02em; color: #0f172a; } 
    .header-note { color: var(--muted); font-size: .83rem; margin-left: auto; font-weight: 600; }
    
    /* Stepper */
    .progress { display: flex; gap: .25rem; margin: 0 0 2.2rem; } 
    .progress-item { align-items: center; color: #94a3b8; display: flex; flex: 1; font-size: .78rem; gap: .4rem; min-width: 0; } 
    .progress-item::after { background: var(--line); content: ''; flex: 1; height: 1.5px; margin-left: .2rem; } 
    .progress-item:last-child::after { display: none; } 
    .progress-item span { align-items: center; border: 1.5px solid currentColor; border-radius: 50%; display: inline-flex; flex: 0 0 auto; font-size: .72rem; font-weight: 700; height: 22px; justify-content: center; width: 22px; } 
    .progress-item small { font-size: .75rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; } 
    .progress-item.is-active { color: var(--blue); font-weight: 750; } 
    .progress-item.is-done { color: #16a34a; }
    
    /* Tipografía amigable */
    .eyebrow { color: var(--blue); font-size: .72rem; font-weight: 800; letter-spacing: .12em; margin-bottom: .45rem; text-transform: uppercase; } 
    h1 { font-size: clamp(1.85rem, 6vw, 2.75rem) !important; font-weight: 800 !important; letter-spacing: -.04em; line-height: 1.1; margin-bottom: .6rem !important; color: #0f172a !important; } 
    .lead { color: var(--muted); font-size: 1.02rem; line-height: 1.55; margin-bottom: 1.8rem; }
    
    [data-testid="stVerticalBlockBorderWrapper"] { background: white; border: 1.5px solid var(--line) !important; border-radius: 14px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); padding: .5rem; } 
    .stRadio label { border: 1.5px solid var(--line); border-radius: 12px; margin-bottom: .55rem; padding: .75rem .85rem; transition: all 0.15s ease; } 
    .stRadio label:has(input:checked) { background: var(--soft-blue); border-color: var(--blue); font-weight: 700; }
    
    .stButton > button { border: 1.5px solid var(--blue); border-radius: 10px; font-weight: 750; min-height: 2.85rem; } 
    .stButton > button[kind="primary"] { background: linear-gradient(135deg, #0284c7, #2563eb); color: white; border: none; box-shadow: 0 4px 14px rgba(2, 132, 199, 0.3); } 
    .stButton > button[kind="primary"]:hover { background: var(--blue-dark); }
    
    .stTextInput input, .stNumberInput input, div[data-baseweb="input"] input, div[data-baseweb="base-input"] input { 
        background-color: white !important; 
        color: #0f172a !important; 
        -webkit-text-fill-color: #0f172a !important; 
        caret-color: #0284c7 !important; 
        font-size: 1.15rem !important; 
        font-weight: 700 !important; 
        border: 1.5px solid var(--line) !important; 
        border-radius: 10px !important; 
    } 
    [data-baseweb="select"] > div { background: white !important; color: #0f172a !important; border-color: var(--line) !important; border-radius: 10px !important; } 
    [data-baseweb="select"] input { color: #0f172a !important; -webkit-text-fill-color: #0f172a !important; } 
    
    .quiet-summary { background: var(--soft-blue); border: 1px solid #bae6fd; border-radius: 10px; color: #0369a1; margin: 1.25rem 0; padding: .8rem 1rem; font-size: 0.9rem; } 
    .summary-number { background: white; border: 1.5px solid var(--line); border-radius: 14px; padding: 1.25rem; } 
    .summary-number span, .summary-number small { color: var(--muted); display: block; font-weight: 600; } 
    .summary-number strong { display: block; font-size: 1.9rem; letter-spacing: -.03em; margin: .25rem 0; color: #0f172a; font-weight: 800; } 
    .explanation { background: #f0fdf4; border-left: 3.5px solid #22c55e; color: #15803d; line-height: 1.55; margin: 1.4rem 0; padding: 1.05rem; border-radius: 0 10px 10px 0; }
    
    [data-testid="stDataFrame"] { border: 1.5px solid var(--line); border-radius: 10px; overflow: hidden; } 
    [data-testid="stMetric"] { background: white; border: 1.5px solid var(--line); border-radius: 12px; padding: .9rem; }
    
    @media (max-width: 640px) { 
        .block-container { padding: 1rem 1rem 2.5rem; } 
        .header-note { display: none; } 
        .progress { gap: .1rem; } 
        .progress-item { flex: 0 0 auto; } 
        .progress-item::after { width: 14px; flex: 0 0 14px; } 
        .progress-item small { display: none; } 
        .stRadio label { font-size: .92rem; } 
    }
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
    steps = [(1, "1. Tu punto de partida"), (2, "2. Tus activos"), (3, "3. Confirmación")]
    items = []
    for number, label in steps:
        state = "is-active" if number == current_step else "is-done" if number < current_step else ""
        items.append(f"<div class='progress-item {state}'><span>{number}</span><small>{label}</small></div>")
    st.markdown(f"<div class='progress'>{''.join(items)}</div>", unsafe_allow_html=True)


def header():
    st.markdown(
        "<div class='app-header'>"
        "<span class='brand-mark'>K</span>"
        "<span class='brand-name'>Kibo</span>"
        "<span class='header-note'>Aprende a invertir sin miedo</span>"
        "</div>",
        unsafe_allow_html=True,
    )


def welcome_step():
    render_progress(1)
    st.markdown(
        "<p class='eyebrow'>PASO 1 · TU PUNTO DE PARTIDA</p>"
        "<h1>Configuremos tu estrategia inicial.</h1>"
        "<p class='lead'>Con solo dos decisiones prepararemos un análisis matemático adaptado a ti. Puedes cambiar todo antes de calcular.</p>",
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        st.markdown("#### 💰 ¿Cuánto dinero simulado quieres analizar?")
        st.session_state.capital = st.number_input(
            "Capital inicial (USD)",
            min_value=1000,
            max_value=10000000,
            value=st.session_state.capital,
            step=5000,
            label_visibility="collapsed",
        )
        st.caption("🛡️ Tranquilo: es una simulación educativa 100% segura. Aquí no se invierte dinero real ni se tocan tus cuentas bancarias.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🎯 ¿Cómo te sientes frente al riesgo?")
    profile_copy = {
        "Conservador": "🛡️ Modo Escudo: Cuidar mi dinero es lo primero. Prefiero tranquilidad y estabilidad antes que buscar ganancias explosivas.",
        "Moderado": "⚖️ Modo Equilibrio: Busco que mi dinero crezca con calma, aceptando pequeños vaivenes normales del mercado.",
        "Agresivo": "🚀 Modo Impulso: Busco el mayor crecimiento posible a largo plazo y no me asustan las caídas temporales.",
    }
    st.session_state.profile = st.radio(
        "Perfil de riesgo",
        options=list(profile_copy),
        index=list(profile_copy).index(st.session_state.profile),
        format_func=lambda item: f"{item} — {profile_copy[item]}",
        label_visibility="collapsed",
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("Continuar a Seleccionar Activos ➡️", type="primary", use_container_width=True, on_click=move_to, args=(2,))


def assets_step():
    render_progress(2)
    st.markdown(
        "<p class='eyebrow'>PASO 2 · UNIVERSO DE ACCIONES</p>"
        "<h1>Elige las empresas que quieres analizar.</h1>"
        "<p class='lead'>La regla de oro de la inversión es <strong>repartir los huevos en varias canastas</strong> (diversificación). Elige empresas de distintas industrias para mayor protección.</p>",
        unsafe_allow_html=True,
    )
    selected = st.multiselect(
        "Acciones disponibles",
        options=list(ASSET_CATALOG),
        default=st.session_state.tickers,
        help="Escribe para buscar o toca una acción para añadirla o retirarla de tu lista.",
    )
    st.session_state.tickers = selected
    st.session_state.portfolio = portfolio_from_tickers(selected)
    asset_count = len(selected)
    sector_count = st.session_state.portfolio["Sector"].nunique() if asset_count else 0

    st.markdown(
        f"<div class='quiet-summary'>🎯 <strong>{asset_count} empresas seleccionadas</strong> · Distribuidas en <strong>{sector_count} sectores económicos</strong>.</div>",
        unsafe_allow_html=True,
    )

    if sector_count < 4:
        st.warning("⚠️ Consejo de Kibo: Intenta elegir empresas de al menos 4 sectores diferentes. Así aseguras que tu portafolio esté protegido ante crisis de una sola industria.")
    else:
        st.success("✅ ¡Excelente diversificación! Tus empresas cubren suficientes sectores para proteger tu capital.")

    st.markdown("<br>", unsafe_allow_html=True)
    back, next_step = st.columns(2)
    with back:
        st.button("⬅️ Atrás", use_container_width=True, on_click=move_to, args=(1,))
    with next_step:
        st.button("Revisar Mi Selección ➡️", type="primary", use_container_width=True, on_click=move_to, args=(3,))


def confirmation_step():
    render_progress(3)
    st.markdown(
        "<p class='eyebrow'>PASO 3 · REVISIÓN FINAL</p>"
        "<h1>Todo listo para que Kibo calcule.</h1>"
        "<p class='lead'>Revisa los parámetros que evaluaremos con los motores matemáticos de riesgo estocástico.</p>",
        unsafe_allow_html=True,
    )
    left, right = st.columns([1, 1], gap="large")
    with left:
        st.markdown(
            f"""
            <div class='summary-number'>
                <span>Capital a Simular</span>
                <strong>USD {st.session_state.capital:,.0f}</strong>
                <small>Perfil seleccionado: {st.session_state.profile}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown("#### Empresas Seleccionadas")
        st.dataframe(st.session_state.portfolio, hide_index=True, use_container_width=True)

    st.markdown(
        """
        <div class='explanation'>
            <strong>🤖 Lo que hará Kibo a continuación:</strong><br>
            Analizaremos 3 años de cotizaciones históricas reales, pondremos a competir 3 cerebros matemáticos (Movimiento Browniano, Salto de Merton y Ornstein-Uhlenbeck) y te diremos exactamente cuántas acciones comprar para minimizar tu riesgo.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    back, next_step = st.columns(2)
    with back:
        st.button("⬅️ Modificar Activos", use_container_width=True, on_click=move_to, args=(2,))
    with next_step:
        st.button("🚀 Ver Mi Estrategia Completa", type="primary", use_container_width=True, on_click=move_to, args=(4,))


def overview():
    st.markdown(
        "<p class='eyebrow'>RESUMEN DE ESTRATEGIA</p>"
        "<h1>¡Tu estrategia está configurada!</h1>"
        "<p class='lead'>Aquí tienes el resumen de tu portafolio listo para ser procesado por los modelos estocásticos.</p>",
        unsafe_allow_html=True,
    )
    first, second, third = st.columns(3)
    with first:
        st.metric("Capital a Simular", f"USD {st.session_state.capital:,.0f}")
    with second:
        st.metric("Perfil de Riesgo", st.session_state.profile)
    with third:
        st.metric("Total Empresas", len(st.session_state.portfolio))

    st.markdown("<br>#### 📊 Distribución de tus empresas por sector", unsafe_allow_html=True)
    if st.session_state.portfolio.empty:
        st.info("Añade al menos un activo para ver la distribución.")
    else:
        st.bar_chart(
            st.session_state.portfolio.groupby("Sector").size().sort_values(ascending=True),
            color="#0284c7",
            horizontal=True,
        )

    with st.expander("⚙️ Ajustar parámetros de la simulación"):
        st.session_state.capital = st.number_input(
            "Capital a analizar (USD)",
            min_value=1000,
            max_value=10000000,
            value=st.session_state.capital,
            step=5000,
        )
        st.session_state.profile = st.selectbox(
            "Perfil de riesgo",
            ["Conservador", "Moderado", "Agresivo"],
            index=["Conservador", "Moderado", "Agresivo"].index(st.session_state.profile),
        )
        edited = st.data_editor(
            st.session_state.portfolio,
            hide_index=True,
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "Ticker": st.column_config.TextColumn("Ticker", required=True),
                "Sector": st.column_config.SelectboxColumn("Sector", options=SECTORS, required=True),
            },
        )
        if st.button("Guardar Cambios", type="primary"):
            st.session_state.portfolio = edited.assign(
                Ticker=lambda frame: frame["Ticker"].astype(str).str.upper().str.strip()
            )
            st.session_state.tickers = st.session_state.portfolio["Ticker"].tolist()
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.button("🔄 Reiniciar Simulación desde el Paso 1", use_container_width=True, on_click=move_to, args=(1,))


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
