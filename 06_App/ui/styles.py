"""Estilos modernos Fintech con Glassmorphism y Dark Theme."""

APP_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

    :root {
        --ink: #f0f4fc;
        --muted: #8e9db7;
        --panel: rgba(15, 23, 42, 0.78);
        --panel-border: rgba(148, 163, 184, 0.14);
        --accent-purple: #7952f5;
        --accent-cyan: #06b6d4;
        --accent-amber: #f59e0b;
        --accent-emerald: #10b981;
        --accent-rose: #f43f5e;
        --card-glow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 10% 0%, rgba(121, 82, 245, 0.18), transparent 35%),
                    radial-gradient(circle at 90% 15%, rgba(6, 182, 212, 0.12), transparent 30%),
                    #090d16;
        color: var(--ink);
    }

    /* Container */
    .block-container {
        max-width: 1200px;
        padding: 1.8rem 1.5rem 4rem;
    }

    /* Header */
    .nexa-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 1.2rem;
        margin-bottom: 2rem;
        border-bottom: 1px solid var(--panel-border);
    }
    .nexa-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .brand-logo {
        background: linear-gradient(135deg, var(--accent-purple), var(--accent-cyan));
        color: white;
        font-weight: 800;
        font-size: 1.1rem;
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 14px rgba(121, 82, 245, 0.35);
    }
    .brand-title {
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #ffffff;
    }
    .brand-subtitle {
        font-size: 0.8rem;
        color: var(--muted);
        letter-spacing: 0.05em;
        text-transform: uppercase;
        font-weight: 600;
    }
    .header-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(6, 182, 212, 0.12);
        border: 1px solid rgba(6, 182, 212, 0.3);
        padding: 0.35rem 0.85rem;
        border-radius: 999px;
        font-size: 0.75rem;
        color: var(--accent-cyan);
        font-weight: 600;
    }

    /* Progress bar steps */
    .stepper {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 2rem;
    }
    .stepper-item {
        flex: 1;
        display: flex;
        align-items: center;
        gap: 0.6rem;
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid var(--panel-border);
        border-radius: 12px;
        padding: 0.65rem 0.9rem;
        transition: all 0.2s ease;
    }
    .stepper-item.active {
        background: rgba(121, 82, 245, 0.15);
        border-color: rgba(121, 82, 245, 0.6);
        box-shadow: 0 0 16px rgba(121, 82, 245, 0.2);
    }
    .stepper-item.done {
        border-color: rgba(16, 185, 129, 0.4);
    }
    .stepper-num {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.08);
        color: var(--muted);
        font-size: 0.75rem;
        font-weight: 700;
    }
    .stepper-item.active .stepper-num {
        background: var(--accent-purple);
        color: white;
    }
    .stepper-item.done .stepper-num {
        background: var(--accent-emerald);
        color: white;
    }
    .stepper-label {
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--muted);
    }
    .stepper-item.active .stepper-label {
        color: #ffffff;
    }

    /* Cards */
    .glass-card {
        background: var(--panel);
        border: 1px solid var(--panel-border);
        border-radius: 16px;
        padding: 1.25rem 1.4rem;
        box-shadow: var(--card-glow);
        backdrop-filter: blur(12px);
        margin-bottom: 1.2rem;
    }
    .card-title {
        font-size: 1.05rem;
        font-weight: 750;
        color: #ffffff;
        margin-bottom: 0.4rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Nori Copilot Card */
    .nori-insight-card {
        background: linear-gradient(135deg, rgba(23, 37, 84, 0.75), rgba(15, 23, 42, 0.85));
        border: 1px solid rgba(6, 182, 212, 0.35);
        border-radius: 16px;
        padding: 1rem 1.25rem;
        margin-bottom: 1.5rem;
        display: flex;
        gap: 1rem;
        align-items: flex-start;
        box-shadow: 0 8px 24px rgba(6, 182, 212, 0.12);
    }
    .nori-avatar {
        background: linear-gradient(135deg, #f59e0b, #ef4444);
        width: 42px;
        height: 42px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        flex-shrink: 0;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
    }
    .nori-content h4 {
        margin: 0 0 0.25rem;
        font-size: 0.95rem;
        font-weight: 750;
        color: #38bdf8;
    }
    .nori-content p {
        margin: 0;
        font-size: 0.86rem;
        line-height: 1.5;
        color: #e2e8f0;
    }

    /* Badges & Metrics */
    .metric-box {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid var(--panel-border);
        border-radius: 12px;
        padding: 0.85rem 1rem;
        text-align: left;
    }
    .metric-lbl {
        color: var(--muted);
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-val {
        color: #ffffff;
        font-size: 1.45rem;
        font-weight: 800;
        margin: 0.2rem 0;
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-sub {
        font-size: 0.74rem;
        color: var(--accent-emerald);
        font-weight: 600;
    }

    /* Custom Floating Nori Trigger Pill */
    .nori-floating-trigger {
        position: fixed;
        bottom: 1.4rem;
        right: 1.4rem;
        z-index: 9999;
    }

    /* Kibo Astro Bot Hero Card & Visuals */
    .kibo-hero-card {
        background: linear-gradient(135deg, rgba(23, 37, 84, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%);
        border: 1px solid rgba(56, 189, 248, 0.28);
        border-radius: 18px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 1.6rem;
        box-shadow: 0 12px 36px -10px rgba(2, 132, 199, 0.25);
        backdrop-filter: blur(12px);
    }
    .kibo-hero-left {
        flex: 0 0 auto;
    }
    .kibo-avatar-halo {
        position: relative;
        width: 110px;
        height: 110px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.25) 0%, transparent 70%);
        animation: kiboGlow 3s ease-in-out infinite alternate;
    }
    @keyframes kiboGlow {
        0% { box-shadow: 0 0 15px rgba(56, 189, 248, 0.3); transform: scale(0.98); }
        100% { box-shadow: 0 0 30px rgba(56, 189, 248, 0.65); transform: scale(1.02); }
    }
    .kibo-hero-img {
        width: 96px;
        height: 96px;
        object-fit: cover;
        border-radius: 50%;
        border: 2px solid #38bdf8;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
        animation: kiboFloating 2.8s ease-in-out infinite;
    }
    @keyframes kiboFloating {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-6px) rotate(1.5deg); }
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
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        color: #38bdf8;
        margin-bottom: 0.5rem;
    }
    .kibo-hero-title {
        font-size: 1.65rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0 0 0.4rem 0;
        letter-spacing: -0.02em;
    }
    .kibo-hero-sub {
        font-size: 0.95rem;
        color: #cbd5e1;
        line-height: 1.5;
        margin: 0 0 0.85rem 0;
    }
    .kibo-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    .kibo-chip {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 999px;
        padding: 0.25rem 0.75rem;
        font-size: 0.74rem;
        color: #93c5fd;
        font-weight: 600;
    }

    /* Kibo Floating Bubble */
    .kibo-bubble {
        position: fixed;
        bottom: 1.2rem;
        right: 1.2rem;
        z-index: 9000;
        display: flex;
        align-items: center;
        gap: 0.65rem;
        background: rgba(15, 23, 42, 0.92);
        border: 2px solid #38bdf8;
        border-radius: 999px;
        padding: 0.5rem 1rem 0.5rem 0.55rem;
        color: white;
        cursor: pointer;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.45), 0 0 15px rgba(56, 189, 248, 0.35);
        backdrop-filter: blur(8px);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .kibo-bubble:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 34px rgba(0, 0, 0, 0.55), 0 0 25px rgba(56, 189, 248, 0.55);
    }
    .kibo-face {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: linear-gradient(135deg, #38bdf8, #2563eb);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
    }
    .kibo-bubble strong {
        display: block;
        font-size: 0.85rem;
        color: #ffffff;
        font-weight: 750;
    }
    .kibo-bubble small {
        display: block;
        font-size: 0.68rem;
        color: #93c5fd;
    }

    /* Input & Buttons */
    .stTextInput input, .stNumberInput input,
    div[data-baseweb="input"] input, div[data-baseweb="base-input"] input {
        background-color: #0f172a !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        caret-color: #38bdf8 !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        border: 1.5px solid rgba(148, 163, 184, 0.35) !important;
        border-radius: 10px !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus,
    div[data-baseweb="input"]:focus-within, div[data-baseweb="base-input"]:focus-within {
        border-color: #7952f5 !important;
        box-shadow: 0 0 0 3px rgba(121, 82, 245, 0.35) !important;
        background-color: #0f172a !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    .stButton > button {
        border-radius: 10px;
        font-weight: 700;
        min-height: 2.8rem;
        transition: all 0.2s ease;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--accent-purple), #5b21b6) !important;
        border: none !important;
        color: white !important;
        box-shadow: 0 4px 16px rgba(121, 82, 245, 0.35);
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(121, 82, 245, 0.5);
    }

    /* Dataframe Styling */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--panel-border);
        border-radius: 12px;
        background: var(--panel);
    }

    @media (max-width: 768px) {
        .block-container { padding: 1rem 0.8rem 3rem; }
        .stepper { flex-direction: column; gap: 0.3rem; }
    }
</style>
"""