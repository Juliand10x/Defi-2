import streamlit as st

import app_mobile as base
from ui.tour import render_kibo_tour
from ui.kibo_avatar import get_kibo_hero_banner


ACCESSIBILITY_CSS = """
<style>
    [data-testid="stVerticalBlockBorderWrapper"] { background: transparent !important; border: 0 !important; padding: 0 !important; }
    .stButton > button { background: #ffffff !important; border-color: #0284c7 !important; color: #0369a1 !important; font-weight: 700 !important; }
    .stButton > button[kind="primary"] { background: linear-gradient(135deg, #0284c7, #2563eb) !important; border: none !important; color: #ffffff !important; box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35) !important; }
    .stButton > button[kind="primary"] p, .stButton > button[kind="primary"] span { color: #ffffff !important; }
    .stButton > button:not([kind="primary"]) p, .stButton > button:not([kind="primary"]) span { color: #0369a1 !important; }
    
    /* Corrección crítica: texto de inputs 100% visible al escribir en tiempo real */
    .stTextInput input, .stNumberInput input,
    div[data-baseweb="input"] input, div[data-baseweb="base-input"] input {
        background-color: #ffffff !important;
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        caret-color: #0284c7 !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        opacity: 1 !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus,
    div[data-baseweb="input"]:focus-within, div[data-baseweb="base-input"]:focus-within {
        border-color: #0284c7 !important;
        box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.25) !important;
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
    }
    
    /* Botones de incremento (+ / -) en number input */
    .stNumberInput button, [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] {
        color: #0284c7 !important;
        fill: #0284c7 !important;
    }

    /* Opciones y etiquetas con alto contraste */
    .stRadio label, .stCheckbox label, [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
    }
    .stRadio label p, .stRadio label span, .stRadio div[role="radiogroup"] label {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        font-weight: 600 !important;
    }

    /* Selectbox y multiselect */
    [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border-color: #cbd5e1 !important;
    }
    [data-baseweb="select"] input {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
    }
    [data-baseweb="tag"] {
        background-color: #e0f2fe !important;
        color: #0369a1 !important;
    }
    [data-baseweb="tag"] span {
        color: #0369a1 !important;
    }

    /* Hero Banner de Kibo */
    .kibo-hero-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1.5px solid #38bdf8;
        border-radius: 20px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.8rem;
        display: flex;
        align-items: center;
        gap: 1.4rem;
        box-shadow: 0 10px 30px -10px rgba(2, 132, 199, 0.35);
    }
    .kibo-hero-left {
        flex: 0 0 auto;
    }
    .kibo-avatar-halo {
        position: relative;
        width: 90px;
        height: 90px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.3) 0%, transparent 70%);
        animation: kiboGlow 3s ease-in-out infinite alternate;
    }
    @keyframes kiboGlow {
        0% { box-shadow: 0 0 12px rgba(56, 189, 248, 0.4); transform: scale(0.98); }
        100% { box-shadow: 0 0 24px rgba(56, 189, 248, 0.7); transform: scale(1.02); }
    }
    .kibo-hero-img {
        width: 82px;
        height: 82px;
        object-fit: cover;
        border-radius: 50%;
        border: 2px solid #38bdf8;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.4);
        animation: kiboFloating 2.8s ease-in-out infinite;
    }
    @keyframes kiboFloating {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-5px) rotate(2deg); }
    }
    .kibo-hero-body {
        flex: 1;
    }
    .kibo-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.4);
        padding: 0.2rem 0.65rem;
        border-radius: 999px;
        font-size: 0.7rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        color: #38bdf8;
        margin-bottom: 0.4rem;
    }
    .kibo-hero-title {
        font-size: 1.45rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0 0 0.3rem 0;
        letter-spacing: -0.02em;
    }
    .kibo-hero-sub {
        font-size: 0.92rem;
        color: #cbd5e1;
        line-height: 1.45;
        margin: 0 0 0.7rem 0;
    }
    .kibo-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
    }
    .kibo-chip {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 999px;
        padding: 0.2rem 0.65rem;
        font-size: 0.72rem;
        color: #93c5fd;
        font-weight: 600;
    }

    /* Burbuja interactiva de Kibo (Estilo Astro Bot) */
    .kibo-bubble {
        align-items: center;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 2px solid #38bdf8;
        border-radius: 999px;
        bottom: 1.2rem;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.4), 0 0 16px rgba(56, 189, 248, 0.35);
        color: white;
        cursor: pointer;
        display: flex;
        gap: .65rem;
        padding: .5rem 1.05rem .5rem .55rem;
        position: fixed;
        right: 1.2rem;
        z-index: 9000;
        transition: transform .2s, box-shadow .2s;
    }
    .kibo-bubble:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 34px rgba(15, 23, 42, 0.55), 0 0 24px rgba(56, 189, 248, 0.55);
    }
    .kibo-face {
        align-items: center;
        background: linear-gradient(135deg, #38bdf8, #2563eb);
        border-radius: 50%;
        display: flex;
        font-size: 1.25rem;
        height: 36px;
        justify-content: center;
        width: 36px;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.6);
    }
    .kibo-bubble strong {
        display: block;
        font-size: .86rem;
        color: #ffffff;
        font-weight: 750;
    }
    .kibo-bubble small {
        color: #93c5fd;
        display: block;
        font-size: .68rem;
    }
    @media (max-width: 640px) {
        .kibo-bubble { bottom: .8rem; right: .8rem; }
        .kibo-bubble small { display: none; }
        .kibo-hero-card { flex-direction: column; text-align: center; }
        .kibo-chips { justify-content: center; }
    }
</style>
"""


def assistant_bubble():
    st.markdown(
        "<div class='kibo-bubble' title='Tócame para activar a Kibo'>"
        "<div class='kibo-face'>🤖</div>"
        "<div><strong>Kibo</strong><small>Tu copiloto financiero</small></div>"
        "</div>",
        unsafe_allow_html=True,
    )


def main():
    base.initialize_state()
    st.markdown(base.APP_CSS + ACCESSIBILITY_CSS, unsafe_allow_html=True)
    base.header()
    
    # Hero Banner animado de Kibo al inicio
    st.markdown(get_kibo_hero_banner(), unsafe_allow_html=True)

    if st.session_state.step == 1:
        base.welcome_step()
    elif st.session_state.step == 2:
        base.assets_step()
    elif st.session_state.step == 3:
        base.confirmation_step()
    else:
        base.overview()
        
    assistant_bubble()
    render_kibo_tour()


if __name__ == "__main__":
    main()
