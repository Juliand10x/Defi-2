import streamlit as st

import app_mobile as base


ACCESSIBILITY_CSS = """
<style>
    .stButton > button { background: #ffffff !important; border-color: #174a7e !important; color: #113960 !important; }
    .stButton > button[kind="primary"] { background: #174a7e !important; border-color: #174a7e !important; color: #ffffff !important; }
    .stButton > button[kind="primary"] p, .stButton > button[kind="primary"] span { color: #ffffff !important; }
    .stButton > button:not([kind="primary"]) p, .stButton > button:not([kind="primary"]) span { color: #113960 !important; }
    .stRadio label, .stCheckbox label, [data-testid="stMetricLabel"], [data-testid="stMetricValue"] { color: #172033 !important; }
    .nori-bubble { align-items: center; background: #172033; border: 1px solid rgba(255,255,255,.28); border-radius: 999px; bottom: 1.2rem; box-shadow: 0 10px 28px rgba(23,32,51,.25); color: white; display: flex; gap: .55rem; padding: .42rem .85rem .42rem .48rem; position: fixed; right: 1.2rem; z-index: 999; }
    .nori-face { align-items: center; background: #f3b44b; border-radius: 50%; display: flex; font-size: 1.2rem; height: 34px; justify-content: center; width: 34px; } .nori-bubble strong { display: block; font-size: .82rem; } .nori-bubble small { color: #d6dce6; display: block; font-size: .67rem; }
    @media (max-width: 640px) { .nori-bubble { bottom: .8rem; right: .8rem; } .nori-bubble small { display: none; } }
</style>
"""


def initialize_tour():
    if "tour_open" not in st.session_state:
        st.session_state.tour_open = True
    if "tour_step" not in st.session_state:
        st.session_state.tour_step = 1


def open_tour():
    st.session_state.tour_open = True
    st.session_state.tour_step = 1


@st.dialog("Conoce a Nori")
def tour_dialog():
    steps = {
        1: ("👋", "Te acompaño durante el análisis", "Primero indicas el capital que quieres estudiar y tu relación con el riesgo. No haremos operaciones ni usaremos dinero real."),
        2: ("▦", "Después eliges tus activos", "Busca, añade o retira acciones. Partimos de una selección diversificada del taller para que no tengas que empezar desde cero."),
        3: ("✓", "Por último revisas la decisión", "Verás un resumen claro antes de calcular. Más adelante aquí aparecerán datos, proyecciones y riesgo."),
    }
    icon, title, description = steps[st.session_state.tour_step]
    st.markdown(f"<div style='font-size:2rem'>{icon}</div><h3>{title}</h3><p>{description}</p>", unsafe_allow_html=True)
    st.progress(st.session_state.tour_step / 3, text=f"Paso {st.session_state.tour_step} de 3")
    previous, next_step = st.columns(2)
    with previous:
        if st.session_state.tour_step > 1:
            if st.button("Atrás", use_container_width=True):
                st.session_state.tour_step -= 1
                st.rerun()
    with next_step:
        final_step = st.session_state.tour_step == 3
        if st.button("Terminar" if final_step else "Siguiente", type="primary", use_container_width=True):
            if final_step:
                st.session_state.tour_open = False
            else:
                st.session_state.tour_step += 1
            st.rerun()


def assistant_bubble():
    st.markdown("<div class='nori-bubble'><div class='nori-face'>🤖</div><div><strong>Nori</strong><small>Guía de la app</small></div></div>", unsafe_allow_html=True)


def help_area():
    with st.expander("🤖 Ayuda de Nori"):
        st.write("Nori está en modo tutorial. Pronto podrás hacerle preguntas sobre cada resultado del análisis.")
        st.button("Repetir tutorial", on_click=open_tour)


def main():
    base.initialize_state()
    initialize_tour()
    st.markdown(base.APP_CSS + ACCESSIBILITY_CSS, unsafe_allow_html=True)
    base.header()
    if st.session_state.step == 1:
        base.welcome_step()
    elif st.session_state.step == 2:
        base.assets_step()
    elif st.session_state.step == 3:
        base.confirmation_step()
    else:
        base.overview()
        help_area()
    assistant_bubble()
    if st.session_state.tour_open:
        tour_dialog()


if __name__ == "__main__":
    main()
