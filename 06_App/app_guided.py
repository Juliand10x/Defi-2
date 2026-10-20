import streamlit as st

import app_mobile as base
from ui.tour import render_nori_tour


ACCESSIBILITY_CSS = """
<style>
    [data-testid="stVerticalBlockBorderWrapper"] { background: transparent !important; border: 0 !important; padding: 0 !important; }
    .stButton > button { background: #ffffff !important; border-color: #174a7e !important; color: #113960 !important; }
    .stButton > button[kind="primary"] { background: #174a7e !important; border-color: #174a7e !important; color: #ffffff !important; }
    .stButton > button[kind="primary"] p, .stButton > button[kind="primary"] span { color: #ffffff !important; }
    .stButton > button:not([kind="primary"]) p, .stButton > button:not([kind="primary"]) span { color: #113960 !important; }
    .stRadio label, .stCheckbox label, [data-testid="stMetricLabel"], [data-testid="stMetricValue"] { color: #172033 !important; }
    .nori-bubble { align-items: center; background: #172033; border: 1px solid rgba(255,255,255,.28); border-radius: 999px; bottom: 1.2rem; box-shadow: 0 10px 28px rgba(23,32,51,.25); color: white; cursor: pointer; display: flex; gap: .55rem; padding: .42rem .85rem .42rem .48rem; position: fixed; right: 1.2rem; z-index: 9000; }
    .nori-face { align-items: center; background: #f3b44b; border-radius: 50%; display: flex; font-size: 1.2rem; height: 34px; justify-content: center; width: 34px; } .nori-bubble strong { display: block; font-size: .82rem; } .nori-bubble small { color: #d6dce6; display: block; font-size: .67rem; }
    @media (max-width: 640px) { .nori-bubble { bottom: .8rem; right: .8rem; } .nori-bubble small { display: none; } }
</style>
"""


def assistant_bubble():
    st.markdown("<div class='nori-bubble' title='Repetir guía'><div class='nori-face'>🤖</div><div><strong>Nori</strong><small>Guía interactiva</small></div></div>", unsafe_allow_html=True)


def main():
    base.initialize_state()
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
    assistant_bubble()
    render_nori_tour()


if __name__ == "__main__":
    main()
