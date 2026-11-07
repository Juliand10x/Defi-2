"""Estilos Fintech Mobile-First inspirados en Nu, Nequi, Binance, MetaMask y eToro."""

APP_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

    :root {
        --ink: #f8fafc;
        --muted: #94a3b8;
        --bg-deep: #080d1a;
        --bg-card: #0f172a;
        --border-subtle: rgba(255, 255, 255, 0.09);
        --nu-purple: #820ad1;
        --nu-purple-light: #9d4edd;
        --cyan-neon: #00d2ff;
        --cyan-glow: rgba(0, 210, 255, 0.35);
        --emerald: #10b981;
        --amber: #f59e0b;
        --rose: #f43f5e;
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }

    /* Fondo de App estilo Fintech Dark Mode con sutil iluminación */
    .stApp {
        background: radial-gradient(circle at 50% 0%, rgba(130, 10, 209, 0.16) 0%, transparent 45%),
                    radial-gradient(circle at 100% 20%, rgba(0, 210, 255, 0.12) 0%, transparent 40%),
                    #080d1a;
        color: var(--ink);
    }

    [data-testid="stHeader"], [data-testid="stSidebar"] {
        background: transparent !important;
    }
    [data-testid="stSidebar"] {
        display: none !important;
    }

    /* Formato Móvil Centrado (Phone Screen Canvas) */
    .block-container {
        max-width: 580px !important;
        margin: 0 auto !important;
        padding: 1rem 1.1rem 4.5rem !important;
    }

    /* Cabecera Móvil de la App */
    .mobile-app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.6rem 0.2rem 1.1rem;
        margin-bottom: 1.2rem;
        border-bottom: 1px solid var(--border-subtle);
    }
    .mobile-brand {
        display: flex;
        align-items: center;
        gap: 0.65rem;
    }
    .mobile-logo {
        background: linear-gradient(135deg, var(--nu-purple), var(--cyan-neon));
        color: white;
        font-weight: 800;
        font-size: 1.1rem;
        width: 36px;
        height: 36px;
        border-radius: 11px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 14px var(--cyan-glow);
    }
    .mobile-title {
        font-size: 1.18rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #ffffff;
        line-height: 1.1;
    }
    .mobile-subtitle {
        font-size: 0.73rem;
        color: #38bdf8;
        font-weight: 700;
        letter-spacing: 0.04em;
    }
    .mobile-step-pill {
        background: rgba(0, 210, 255, 0.12);
        border: 1px solid rgba(0, 210, 255, 0.35);
        color: #38bdf8;
        padding: 0.3rem 0.75rem;
        border-radius: 999px;
        font-size: 0.74rem;
        font-weight: 800;
    }

    /* Stepper móvil minimalista */
    .mobile-stepper {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        margin-bottom: 1.5rem;
    }
    .mobile-step-dot {
        flex: 1;
        height: 5px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.12);
        transition: all 0.3s ease;
    }
    .mobile-step-dot.active {
        background: linear-gradient(90deg, var(--nu-purple), var(--cyan-neon));
        box-shadow: 0 0 10px rgba(0, 210, 255, 0.5);
    }
    .mobile-step-dot.done {
        background: var(--emerald);
    }

    /* Tipografía amigable para principiantes */
    .step-eyebrow {
        color: var(--cyan-neon);
        font-size: 0.74rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }
    h1.step-title {
        font-size: 1.75rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em;
        line-height: 1.2;
        margin: 0 0 0.5rem 0 !important;
        color: #ffffff !important;
    }
    .step-lead {
        color: #94a3b8;
        font-size: 0.94rem;
        line-height: 1.5;
        margin-bottom: 1.4rem;
    }

    /* Hero Card de Kibo estilo Astro Bot */
    .kibo-hero-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(22, 32, 56, 0.85) 100%);
        border: 1px solid rgba(0, 210, 255, 0.35);
        border-radius: 20px;
        padding: 1.25rem 1.35rem;
        margin-bottom: 1.4rem;
        display: flex;
        align-items: center;
        gap: 1.15rem;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45);
        backdrop-filter: blur(10px);
    }
    .kibo-avatar-halo {
        position: relative;
        width: 82px;
        height: 82px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(0, 210, 255, 0.3) 0%, transparent 70%);
        animation: kiboGlow 3s ease-in-out infinite alternate;
        flex-shrink: 0;
    }
    @keyframes kiboGlow {
        0% { box-shadow: 0 0 12px rgba(0, 210, 255, 0.3); transform: scale(0.98); }
        100% { box-shadow: 0 0 25px rgba(0, 210, 255, 0.7); transform: scale(1.02); }
    }
    .kibo-hero-img {
        width: 76px;
        height: 76px;
        object-fit: cover;
        border-radius: 50%;
        border: 2px solid var(--cyan-neon);
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
        background: rgba(0, 210, 255, 0.15);
        border: 1px solid rgba(0, 210, 255, 0.4);
        padding: 0.2rem 0.65rem;
        border-radius: 999px;
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        color: var(--cyan-neon);
        margin-bottom: 0.35rem;
    }
    .kibo-hero-title {
        font-size: 1.35rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0 0 0.25rem 0;
        letter-spacing: -0.02em;
    }
    .kibo-hero-sub {
        font-size: 0.88rem;
        color: #cbd5e1;
        line-height: 1.45;
        margin: 0;
    }

    /* Tarjetas generales de la interfaz */
    .fintech-card {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid var(--border-subtle);
        border-radius: 18px;
        padding: 1.25rem 1.3rem;
        margin-bottom: 1.1rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(12px);
    }

    /* Botones rápidos de valor (Chips estilo Nequi / Nu) */
    .quick-pills-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin: 0.75rem 0 1.25rem;
    }
    .quick-pill {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #e2e8f0;
        padding: 0.45rem 0.85rem;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.15s ease;
    }
    .quick-pill:hover, .quick-pill.selected {
        background: rgba(0, 210, 255, 0.2);
        border-color: var(--cyan-neon);
        color: #ffffff;
        box-shadow: 0 0 10px rgba(0, 210, 255, 0.3);
    }

    /* Píldora de garantía de simulación */
    .safe-simulation-pill {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 14px;
        padding: 0.85rem 1rem;
        color: #a7f3d0;
        font-size: 0.84rem;
        line-height: 1.45;
        margin-bottom: 1.4rem;
    }

    /* Medidor de Diversificación (eToro style) */
    .diversification-gauge-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(26, 36, 64, 0.9));
        border: 1px solid rgba(0, 210, 255, 0.3);
        border-radius: 18px;
        padding: 1.15rem 1.25rem;
        margin: 1.2rem 0;
    }
    .gauge-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.6rem;
    }
    .gauge-title {
        font-size: 0.86rem;
        font-weight: 750;
        color: #ffffff;
    }
    .gauge-score {
        font-size: 0.85rem;
        font-weight: 800;
        color: var(--cyan-neon);
    }
    .gauge-bar-track {
        background: rgba(255, 255, 255, 0.1);
        height: 9px;
        border-radius: 999px;
        overflow: hidden;
        margin-bottom: 0.6rem;
    }
    .gauge-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #10b981, #00d2ff);
        border-radius: 999px;
        transition: width 0.4s ease;
    }

    /* Veredicto de Modelos Estocásticos */
    .verdict-glass-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 27, 75, 0.85));
        border: 1.5px solid var(--nu-purple-light);
        border-radius: 18px;
        padding: 1.25rem 1.35rem;
        margin-bottom: 1.3rem;
        box-shadow: 0 10px 30px rgba(130, 10, 209, 0.25);
    }
    .verdict-badge {
        font-size: 0.74rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #c084fc;
        margin-bottom: 0.3rem;
    }
    .verdict-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.45rem;
    }
    .verdict-desc {
        font-size: 0.88rem;
        color: #e2e8f0;
        line-height: 1.5;
        margin: 0;
    }

    /* Wallet Resumen Grid (Estilo Nu / Binance) */
    .kpi-wallet-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.75rem;
        margin-bottom: 1.25rem;
    }
    .wallet-card {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 1rem 1.1rem;
    }
    .wallet-label {
        font-size: 0.72rem;
        font-weight: 750;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--muted);
        margin-bottom: 0.3rem;
    }
    .wallet-value {
        font-size: 1.35rem;
        font-weight: 800;
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.02em;
    }
    .wallet-sub {
        font-size: 0.75rem;
        color: var(--cyan-neon);
        font-weight: 600;
        margin-top: 0.2rem;
    }

    /* Tarjetas de compra de acciones individuales */
    .stocks-plan-container {
        display: flex;
        flex-direction: column;
        gap: 0.6rem;
        margin-bottom: 1.3rem;
    }
    .stock-item-row {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid var(--border-subtle);
        border-radius: 15px;
        padding: 0.9rem 1.05rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: transform 0.15s ease;
    }
    .stock-item-row:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 210, 255, 0.4);
    }
    .stock-left {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .stock-avatar {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.08);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
    }
    .stock-name {
        font-size: 0.95rem;
        font-weight: 800;
        color: #ffffff;
    }
    .stock-sector {
        font-size: 0.74rem;
        color: #94a3b8;
    }
    .stock-right {
        text-align: right;
    }
    .stock-shares {
        font-size: 0.98rem;
        font-weight: 800;
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
    }
    .stock-amount {
        font-size: 0.75rem;
        color: #38bdf8;
        font-weight: 600;
    }

    /* Estilos de Controles de Streamlit */
    .stTextInput input, .stNumberInput input,
    div[data-baseweb="input"] input, div[data-baseweb="base-input"] input {
        background-color: #0f172a !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        caret-color: var(--cyan-neon) !important;
        font-size: 1.25rem !important;
        font-weight: 800 !important;
        border: 1.5px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 14px !important;
        padding: 0.75rem 1rem !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus,
    div[data-baseweb="input"]:focus-within, div[data-baseweb="base-input"]:focus-within {
        border-color: var(--cyan-neon) !important;
        box-shadow: 0 0 0 3px rgba(0, 210, 255, 0.3) !important;
        color: #ffffff !important;
    }

    /* Radio buttons como tarjetas seleccionables */
    .stRadio label {
        background: rgba(15, 23, 42, 0.75) !important;
        border: 1.5px solid var(--border-subtle) !important;
        border-radius: 15px !important;
        margin-bottom: 0.65rem !important;
        padding: 0.9rem 1.05rem !important;
        transition: all 0.15s ease !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    .stRadio label:hover {
        border-color: rgba(0, 210, 255, 0.4) !important;
    }
    .stRadio label:has(input:checked) {
        background: rgba(130, 10, 209, 0.15) !important;
        border-color: var(--cyan-neon) !important;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.25) !important;
    }
    .stRadio label p, .stRadio label span {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-size: 0.92rem !important;
    }

    /* Selectbox y multiselect */
    [data-baseweb="select"] > div {
        background-color: #0f172a !important;
        border: 1.5px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 14px !important;
        color: #ffffff !important;
    }
    [data-baseweb="tag"] {
        background-color: rgba(0, 210, 255, 0.15) !important;
        border: 1px solid rgba(0, 210, 255, 0.4) !important;
        color: #38bdf8 !important;
        border-radius: 8px !important;
    }

    /* Botones principales y de navegación */
    .stButton > button {
        border-radius: 14px !important;
        font-weight: 750 !important;
        min-height: 3.1rem !important;
        font-size: 0.98rem !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #7952f5 0%, #0284c7 100%) !important;
        border: none !important;
        color: #ffffff !important;
        box-shadow: 0 6px 20px rgba(2, 132, 199, 0.4) !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 26px rgba(0, 210, 255, 0.6) !important;
    }
    .stButton > button:not([kind="primary"]) {
        background: rgba(255, 255, 255, 0.06) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.14) !important;
        color: #cbd5e1 !important;
    }
    .stButton > button:not([kind="primary"]):hover {
        background: rgba(255, 255, 255, 0.12) !important;
        color: #ffffff !important;
    }

    /* Burbuja interactiva de Kibo flotante */
    .kibo-bubble {
        position: fixed;
        bottom: 1.25rem;
        right: 1.25rem;
        z-index: 9000;
        display: flex;
        align-items: center;
        gap: 0.65rem;
        background: rgba(14, 21, 38, 0.94);
        border: 2px solid var(--cyan-neon);
        border-radius: 999px;
        padding: 0.5rem 1.05rem 0.5rem 0.55rem;
        color: white;
        cursor: pointer;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.5), 0 0 16px rgba(0, 210, 255, 0.45);
        backdrop-filter: blur(8px);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .kibo-bubble:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 34px rgba(0, 0, 0, 0.65), 0 0 26px rgba(0, 210, 255, 0.7);
    }
    .kibo-face {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--cyan-neon), #7952f5);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        box-shadow: 0 0 10px rgba(0, 210, 255, 0.6);
    }
    .kibo-bubble strong {
        display: block;
        font-size: 0.86rem;
        color: #ffffff;
        font-weight: 800;
    }
    .kibo-bubble small {
        display: block;
        font-size: 0.68rem;
        color: #38bdf8;
    }

    @media (max-width: 640px) {
        .block-container { padding: 0.75rem 0.85rem 3.5rem !important; }
        .kibo-hero-card { flex-direction: column; text-align: center; }
        .kpi-wallet-grid { grid-template-columns: 1fr; }
        .kibo-bubble small { display: none; }
    }
</style>
"""
