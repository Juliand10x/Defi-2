"""
Estilos Fintech Premium Mobile-First: Paleta Obsidiana, Esmeralda Financiero y Oro Champaña.
Inspirado en interfaces de autor (Cash App, Revolut Metal, Linear, Robinhood Gold).
"""

APP_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

    :root {
        --ink: #f8fafc;
        --muted: #8e9bb0;
        --bg-obsidian: #080b12;
        --card-carbon: #0f1420;
        --card-elevated: #161d2d;
        --border-subtle: rgba(255, 255, 255, 0.08);
        --border-hover: rgba(16, 185, 129, 0.4);
        
        /* Paleta Financiera de Autor */
        --emerald-core: #10b981;
        --emerald-glow: rgba(16, 185, 129, 0.3);
        --emerald-dark: #047857;
        --gold-core: #f59e0b;
        --gold-glow: rgba(245, 158, 11, 0.25);
        --cobalt-core: #2563eb;
        --cobalt-dark: #1d4ed8;
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }

    /* Fondo Obsidiana con profundidad natural y sutil iluminación ambiental */
    .stApp {
        background: radial-gradient(circle at 50% -10%, rgba(16, 185, 129, 0.09) 0%, transparent 50%),
                    radial-gradient(circle at 90% 30%, rgba(245, 158, 11, 0.06) 0%, transparent 45%),
                    #080b12;
        color: var(--ink);
    }

    [data-testid="stHeader"], [data-testid="stSidebar"] {
        background: transparent !important;
    }
    [data-testid="stSidebar"] {
        display: none !important;
    }

    /* Canvas Móvil Centrado (Phone Screen Canvas) */
    .block-container {
        max-width: 560px !important;
        margin: 0 auto !important;
        padding: 1.1rem 1.15rem 4.8rem !important;
        animation: pageEntrance 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    }

    @keyframes pageEntrance {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* ------------------------------------------------------------------
       SPLASH SCREEN INTRO ANIMATION
       ------------------------------------------------------------------ */
    #kibo-splash-screen {
        position: fixed;
        inset: 0;
        width: 100vw;
        height: 100vh;
        background: #07090e;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 999999;
        transition: opacity 0.5s cubic-bezier(0.16, 1, 0.3, 1), transform 0.5s ease;
        pointer-events: auto;
    }
    #kibo-splash-screen.fade-out {
        opacity: 0;
        transform: scale(1.04);
        pointer-events: none;
    }
    .splash-glow-halo {
        position: relative;
        width: 120px;
        height: 120px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.28) 0%, transparent 70%);
        margin-bottom: 1.2rem;
        animation: splashHalo 2s ease-in-out infinite alternate;
    }
    @keyframes splashHalo {
        0% { transform: scale(0.95); box-shadow: 0 0 25px rgba(16, 185, 129, 0.3); }
        100% { transform: scale(1.05); box-shadow: 0 0 50px rgba(16, 185, 129, 0.6); }
    }
    .splash-avatar-img {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        border: 2.5px solid var(--emerald-core);
        object-fit: cover;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
        animation: splashLevitate 2.6s ease-in-out infinite;
    }
    @keyframes splashLevitate {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-7px) rotate(2deg); }
    }
    .splash-brand-title {
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        color: #ffffff;
        margin: 0 0 0.4rem 0;
        text-transform: uppercase;
        background: linear-gradient(135deg, #ffffff 40%, #10b981 85%, #f59e0b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: splashReveal 0.9s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    @keyframes splashReveal {
        from { opacity: 0; letter-spacing: 0.35em; transform: translateY(6px); }
        to { opacity: 1; letter-spacing: 0.12em; transform: translateY(0); }
    }
    .splash-brand-sub {
        font-size: 0.88rem;
        font-weight: 600;
        color: var(--muted);
        letter-spacing: 0.05em;
        margin-bottom: 1.2rem;
        text-align: center;
        max-width: 300px;
    }
    .splash-context-card {
        background: rgba(13, 19, 31, 0.92);
        border: 1px solid rgba(16, 185, 129, 0.35);
        border-radius: 20px;
        padding: 1.25rem 1.35rem 1.15rem;
        max-width: 400px;
        margin: 0 1rem 1.4rem;
        text-align: center;
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6), 0 0 25px rgba(16, 185, 129, 0.18);
        backdrop-filter: blur(12px);
    }
    .splash-context-title {
        font-size: 1.05rem;
        font-weight: 750;
        color: #ffffff;
        margin-bottom: 0.45rem;
    }
    .splash-context-text {
        font-size: 0.88rem;
        line-height: 1.5;
        color: #cbd5e1;
        margin-bottom: 1.15rem;
    }
    .splash-btn-row {
        display: flex;
        flex-direction: column;
        gap: 0.6rem;
        width: 100%;
    }
    .splash-cta-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 11px 18px;
        border-radius: 12px;
        font-weight: 750;
        font-size: 0.88rem;
        border: none;
        cursor: pointer;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        width: 100%;
    }
    .splash-cta-tour {
        background: linear-gradient(135deg, #10b981, #059669);
        color: #ffffff;
        box-shadow: 0 4px 18px rgba(16, 185, 129, 0.45);
    }
    .splash-cta-tour:hover {
        transform: translateY(-2px);
        background: #059669;
        box-shadow: 0 6px 26px rgba(16, 185, 129, 0.65);
    }
    .splash-cta-skip {
        background: rgba(255, 255, 255, 0.08);
        color: #cbd5e1;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .splash-cta-skip:hover {
        background: rgba(255, 255, 255, 0.16);
        color: #ffffff;
        border-color: rgba(255, 255, 255, 0.3);
    }
    .kibo-tour-target-active {
        position: relative !important;
        z-index: 99998 !important;
        pointer-events: auto !important;
        filter: none !important;
        -webkit-filter: none !important;
    }
    .splash-bar-track {
        width: 160px;
        height: 4px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 999px;
        overflow: hidden;
    }
    .splash-bar-fill {
        width: 0%;
        height: 100%;
        background: linear-gradient(90deg, var(--emerald-core), var(--gold-core));
        border-radius: 999px;
        animation: splashProgress 1.4s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }
    @keyframes splashProgress {
        0% { width: 0%; }
        60% { width: 75%; }
        100% { width: 100%; }
    }

    /* ------------------------------------------------------------------
       CABECERA MÓVIL ESTILO APP
       ------------------------------------------------------------------ */
    .mobile-app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.4rem 0.1rem 1rem;
        margin-bottom: 1.1rem;
        border-bottom: 1px solid var(--border-subtle);
    }
    .mobile-brand {
        display: flex;
        align-items: center;
        gap: 0.7rem;
    }
    .mobile-logo-circle {
        position: relative;
        width: 40px;
        height: 40px;
        border-radius: 12px;
        background: linear-gradient(135deg, #162032, #0d121c);
        border: 1.5px solid rgba(16, 185, 129, 0.45);
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.25);
    }
    .mobile-logo-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .mobile-brand-title {
        font-size: 1.22rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #ffffff;
        line-height: 1.1;
    }
    .mobile-brand-sub {
        font-size: 0.72rem;
        color: var(--emerald-core);
        font-weight: 700;
        letter-spacing: 0.04em;
    }
    .mobile-step-pill {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #6ee7b7;
        padding: 0.32rem 0.75rem;
        border-radius: 999px;
        font-size: 0.73rem;
        font-weight: 750;
    }

    /* Stepper móvil refinado */
    .mobile-stepper {
        display: flex;
        align-items: center;
        gap: 0.45rem;
        margin-bottom: 1.6rem;
    }
    .mobile-step-dot {
        flex: 1;
        height: 4px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.1);
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .mobile-step-dot.active {
        background: linear-gradient(90deg, var(--emerald-core), #34d399);
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.6);
        height: 5px;
    }
    .mobile-step-dot.done {
        background: #047857;
    }

    /* Tipografía y Textos */
    .step-eyebrow {
        color: var(--gold-core);
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }
    h1.step-title {
        font-size: 1.7rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em;
        line-height: 1.2;
        margin: 0 0 0.45rem 0 !important;
        color: #ffffff !important;
    }
    .step-lead {
        color: var(--muted);
        font-size: 0.92rem;
        line-height: 1.5;
        margin-bottom: 1.35rem;
    }

    /* ------------------------------------------------------------------
       HERO BANNER DE KIBO (CON IMAGEN 3D Y ANIMACIONES)
       ------------------------------------------------------------------ */
    .kibo-hero-card {
        background: linear-gradient(135deg, rgba(18, 24, 38, 0.95) 0%, rgba(13, 18, 28, 0.98) 100%);
        border: 1px solid rgba(16, 185, 129, 0.28);
        border-radius: 22px;
        padding: 1.25rem 1.35rem;
        margin-bottom: 1.4rem;
        display: flex;
        align-items: center;
        gap: 1.2rem;
        box-shadow: 0 14px 34px rgba(0, 0, 0, 0.45), 0 0 20px rgba(16, 185, 129, 0.08);
        backdrop-filter: blur(12px);
    }
    .kibo-avatar-halo {
        position: relative;
        width: 86px;
        height: 86px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.25) 0%, transparent 70%);
        animation: kiboGlowPulse 3s ease-in-out infinite alternate;
        flex-shrink: 0;
    }
    @keyframes kiboGlowPulse {
        0% { box-shadow: 0 0 12px rgba(16, 185, 129, 0.25); transform: scale(0.98); }
        100% { box-shadow: 0 0 26px rgba(16, 185, 129, 0.55); transform: scale(1.02); }
    }
    .kibo-hero-img {
        width: 78px;
        height: 78px;
        object-fit: cover;
        border-radius: 50%;
        border: 2px solid var(--emerald-core);
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.5);
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
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
        padding: 0.2rem 0.65rem;
        border-radius: 999px;
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        color: #6ee7b7;
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

    /* Píldora de seguridad */
    .safe-simulation-pill {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-radius: 16px;
        padding: 0.9rem 1.05rem;
        color: #d1fae5;
        font-size: 0.85rem;
        line-height: 1.45;
        margin-bottom: 1.4rem;
    }

    /* Botones rápidos de valor */
    .quick-chips-group {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin: 0.6rem 0 1.2rem;
    }

    /* Medidor de Diversificación */
    .diversification-gauge-card {
        background: linear-gradient(135deg, #111724 0%, #161e30 100%);
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-radius: 18px;
        padding: 1.15rem 1.25rem;
        margin: 1.2rem 0;
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.35);
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
        color: var(--emerald-core);
    }
    .gauge-bar-track {
        background: rgba(255, 255, 255, 0.08);
        height: 8px;
        border-radius: 999px;
        overflow: hidden;
        margin-bottom: 0.6rem;
    }
    .gauge-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--emerald-core), var(--gold-core));
        border-radius: 999px;
        transition: width 0.45s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Veredicto de Modelos Estocásticos */
    .verdict-glass-card {
        background: linear-gradient(135deg, #141b2b 0%, #1a2236 100%);
        border: 1.5px solid rgba(245, 158, 11, 0.4);
        border-radius: 18px;
        padding: 1.25rem 1.35rem;
        margin-bottom: 1.3rem;
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.12);
    }

    /* Tarjeta de Veredicto de Manada (Herding Behavior & Eficiencia) */
    .herding-verdict-card {
        background: linear-gradient(135deg, #131a29 0%, #1a2236 100%);
        border: 1.5px solid rgba(16, 185, 129, 0.45);
        border-radius: 20px;
        padding: 1.35rem 1.45rem;
        margin-bottom: 1.35rem;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45);
    }
    .herding-stat-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.75rem;
        margin: 1rem 0;
    }
    .herding-stat-box {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 0.75rem 0.9rem;
    }
    .herding-stat-lbl {
        font-size: 0.7rem;
        font-weight: 750;
        text-transform: uppercase;
        color: var(--muted);
        letter-spacing: 0.05em;
    }
    .herding-stat-val {
        font-size: 1.25rem;
        font-weight: 800;
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        margin-top: 0.15rem;
    }
    .herding-stat-sub {
        font-size: 0.72rem;
        color: var(--emerald-core);
        font-weight: 600;
    }
    .verdict-badge {
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--gold-core);
        margin-bottom: 0.25rem;
    }
    .verdict-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.4rem;
    }
    .verdict-desc {
        font-size: 0.88rem;
        color: #cbd5e1;
        line-height: 1.5;
        margin: 0;
    }

    /* Wallet Resumen Grid */
    .kpi-wallet-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.75rem;
        margin-bottom: 1.25rem;
    }
    .wallet-card {
        background: #111726;
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 1rem 1.1rem;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .wallet-card:hover {
        transform: translateY(-2px);
        border-color: rgba(16, 185, 129, 0.35);
    }
    .wallet-label {
        font-size: 0.7rem;
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
        font-size: 0.74rem;
        color: var(--emerald-core);
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
        background: #111726;
        border: 1px solid var(--border-subtle);
        border-radius: 15px;
        padding: 0.9rem 1.05rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .stock-item-row:hover {
        transform: translateY(-2px);
        border-color: rgba(16, 185, 129, 0.35);
    }
    .stock-left {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .stock-avatar {
        width: 38px;
        height: 38px;
        border-radius: 11px;
        background: #182236;
        border: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.15rem;
    }
    .stock-name {
        font-size: 0.95rem;
        font-weight: 800;
        color: #ffffff;
    }
    .stock-sector {
        font-size: 0.73rem;
        color: var(--muted);
    }
    .stock-right {
        text-align: right;
    }
    .stock-shares {
        font-size: 0.96rem;
        font-weight: 800;
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
    }
    .stock-amount {
        font-size: 0.75rem;
        color: var(--emerald-core);
        font-weight: 700;
    }

    /* ------------------------------------------------------------------
       INPUTS Y SELECTORES
       ------------------------------------------------------------------ */
    .stTextInput input, .stNumberInput input,
    div[data-baseweb="input"] input, div[data-baseweb="base-input"] input {
        background-color: #111726 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        caret-color: var(--emerald-core) !important;
        font-size: 1.25rem !important;
        font-weight: 800 !important;
        border: 1.5px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 14px !important;
        padding: 0.75rem 1rem !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus,
    div[data-baseweb="input"]:focus-within, div[data-baseweb="base-input"]:focus-within {
        border-color: var(--emerald-core) !important;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.25) !important;
        color: #ffffff !important;
    }

    /* Radio buttons como tarjetas táctiles elegantes */
    .stRadio label {
        background: #111726 !important;
        border: 1.5px solid var(--border-subtle) !important;
        border-radius: 16px !important;
        margin-bottom: 0.65rem !important;
        padding: 0.95rem 1.1rem !important;
        transition: all 0.2s ease !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    .stRadio label:hover {
        border-color: rgba(16, 185, 129, 0.35) !important;
        transform: translateY(-1px);
    }
    .stRadio label:has(input:checked) {
        background: rgba(16, 185, 129, 0.12) !important;
        border-color: var(--emerald-core) !important;
        box-shadow: 0 0 16px rgba(16, 185, 129, 0.2) !important;
    }
    .stRadio label p, .stRadio label span {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-size: 0.92rem !important;
    }

    /* Selectbox y multiselect */
    [data-baseweb="select"] > div {
        background-color: #111726 !important;
        border: 1.5px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 14px !important;
        color: #ffffff !important;
    }
    [data-baseweb="tag"] {
        background-color: rgba(16, 185, 129, 0.15) !important;
        border: 1px solid rgba(16, 185, 129, 0.35) !important;
        color: #6ee7b7 !important;
        border-radius: 8px !important;
    }

    /* Botones primarios (Verde Esmeralda Fintech) */
    .stButton > button {
        border-radius: 14px !important;
        font-weight: 750 !important;
        min-height: 3.1rem !important;
        font-size: 0.98rem !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #10b981 0%, #047857 100%) !important;
        border: none !important;
        color: #ffffff !important;
        box-shadow: 0 4px 18px rgba(16, 185, 129, 0.35) !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 24px rgba(16, 185, 129, 0.55) !important;
    }
    .stButton > button[kind="primary"]:active {
        transform: scale(0.98) !important;
    }
    .stButton > button:not([kind="primary"]) {
        background: #111726 !important;
        border: 1.5px solid rgba(255, 255, 255, 0.12) !important;
        color: #cbd5e1 !important;
    }
    .stButton > button:not([kind="primary"]):hover {
        background: #172134 !important;
        color: #ffffff !important;
        border-color: rgba(255, 255, 255, 0.22) !important;
    }

    /* Burbuja interactiva de Kibo flotante (Con imagen 3D) */
    .kibo-bubble {
        position: fixed;
        bottom: 1.25rem;
        right: 1.25rem;
        z-index: 9000;
        display: flex;
        align-items: center;
        gap: 0.65rem;
        background: rgba(14, 20, 32, 0.95);
        border: 1.8px solid var(--emerald-core);
        border-radius: 999px;
        padding: 0.45rem 1.05rem 0.45rem 0.5rem;
        color: white;
        cursor: pointer;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.55), 0 0 18px rgba(16, 185, 129, 0.35);
        backdrop-filter: blur(10px);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .kibo-bubble:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 34px rgba(0, 0, 0, 0.65), 0 0 26px rgba(16, 185, 129, 0.6);
    }
    .kibo-face-wrapper {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        overflow: hidden;
        border: 1.5px solid var(--emerald-core);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
    }
    .kibo-face-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
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
        color: #6ee7b7;
    }

    @media (max-width: 640px) {
        .block-container { padding: 0.75rem 0.85rem 3.5rem !important; }
        .kibo-hero-card { flex-direction: column; text-align: center; }
        .kpi-wallet-grid { grid-template-columns: 1fr; }
        .kibo-bubble small { display: none; }
    }
</style>
"""
