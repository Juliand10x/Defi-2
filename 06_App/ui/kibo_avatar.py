"""Kibo Avatar & Mascot: Visuales y animaciones estilo Astro Bot."""

import base64
import os

ASSETS_DIR = os.path.dirname(__file__)
MASCOT_PATH = os.path.join(ASSETS_DIR, "kibo_mascot.jpg")


def get_kibo_image_base64() -> str:
    """Retorna la imagen 3D de Kibo en base64 para incrustarla limpiamente en HTML/Streamlit."""
    if os.path.exists(MASCOT_PATH):
        try:
            with open(MASCOT_PATH, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
                return f"data:image/jpeg;base64,{encoded}"
        except Exception:
            pass
    return ""


def get_kibo_hero_banner(title: str = "¡Hola! Soy Kibo 🚀", subtitle: str = "Tu copiloto inteligente para aprender a invertir sin miedo.") -> str:
    """Genera el Hero Banner animado de entrada con la mascota 3D y brillo fintech."""
    img_b64 = get_kibo_image_base64()
    
    avatar_html = (
        f'<img src="{img_b64}" class="kibo-hero-img" alt="Kibo Mascot" />'
        if img_b64
        else get_kibo_svg(mood="happy", size=110)
    )

    return f"""
    <div class="kibo-hero-card">
        <div class="kibo-hero-left">
            <div class="kibo-avatar-halo">
                {avatar_html}
            </div>
        </div>
        <div class="kibo-hero-body">
            <div class="kibo-badge">🤖 COPILOTO INTELIGENTE ACTIVO</div>
            <h2 class="kibo-hero-title">{title}</h2>
            <p class="kibo-hero-sub">{subtitle}</p>
            <div class="kibo-chips">
                <span class="kibo-chip">✨ Explicaciones sencillas</span>
                <span class="kibo-chip">🛡️ Simulación sin riesgo real</span>
                <span class="kibo-chip">🎯 Aprende a tu ritmo</span>
            </div>
        </div>
    </div>
    """


def get_kibo_svg(mood: str = "happy", size: int = 120) -> str:
    """Retorna el código SVG interactivo de Kibo con animaciones CSS fluidas."""
    if mood == "shield":
        eyes_svg = """
        <ellipse cx="64" cy="62" rx="7" ry="9" fill="#00f0ff" filter="url(#eyeGlow)" />
        <ellipse cx="96" cy="62" rx="7" ry="9" fill="#00f0ff" filter="url(#eyeGlow)" />
        <path d="M58 54 Q64 51 70 54" stroke="#00f0ff" stroke-width="2.5" fill="none" stroke-linecap="round" />
        <path d="M90 54 Q96 51 102 54" stroke="#00f0ff" stroke-width="2.5" fill="none" stroke-linecap="round" />
        """
    elif mood == "rocket":
        eyes_svg = """
        <polygon points="64,52 66,58 72,59 67,63 69,69 64,65 59,69 61,63 56,59 62,58" fill="#ffd700" filter="url(#eyeGlowGold)" />
        <polygon points="96,52 98,58 104,59 99,63 101,69 96,65 91,69 93,63 88,59 94,58" fill="#ffd700" filter="url(#eyeGlowGold)" />
        """
    else:
        eyes_svg = """
        <path d="M57 65 Q64 54 71 65" stroke="#00f0ff" stroke-width="5" fill="none" stroke-linecap="round" filter="url(#eyeGlow)" />
        <path d="M89 65 Q96 54 103 65" stroke="#00f0ff" stroke-width="5" fill="none" stroke-linecap="round" filter="url(#eyeGlow)" />
        <circle cx="64" cy="57" r="1.5" fill="#ffffff" />
        <circle cx="96" cy="57" r="1.5" fill="#ffffff" />
        """

    return f"""
    <div class="kibo-container" style="display:inline-block; width:{size}px; height:{int(size * 1.15)}px; vertical-align:middle;">
    <svg viewBox="0 0 160 185" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <filter id="eyeGlow" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur stdDeviation="3.5" result="blur" />
                <feMerge>
                    <feMergeNode in="blur" />
                    <feMergeNode in="SourceGraphic" />
                </feMerge>
            </filter>
            <filter id="eyeGlowGold" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur stdDeviation="3" result="blur" />
                <feMerge>
                    <feMergeNode in="blur" />
                    <feMergeNode in="SourceGraphic" />
                </feMerge>
            </filter>
            <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#ffffff" />
                <stop offset="60%" stop-color="#f0f5ff" />
                <stop offset="100%" stop-color="#d4e2f8" />
            </linearGradient>
            <linearGradient id="blueAccent" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#38bdf8" />
                <stop offset="100%" stop-color="#2563eb" />
            </linearGradient>
            <linearGradient id="visorGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#0f172a" />
                <stop offset="100%" stop-color="#020617" />
            </linearGradient>
            <linearGradient id="plasmaGlow" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.9" />
                <stop offset="60%" stop-color="#06b6d4" stop-opacity="0.5" />
                <stop offset="100%" stop-color="#06b6d4" stop-opacity="0" />
            </linearGradient>
        </defs>

        <style>
            @keyframes kiboHover {{
                0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
                50% {{ transform: translateY(-7px) rotate(1.5deg); }}
            }}
            @keyframes kiboWaveArm {{
                0%, 100% {{ transform: rotate(0deg); }}
                50% {{ transform: rotate(-22deg); }}
            }}
            @keyframes kiboThrusterPulse {{
                0%, 100% {{ transform: scaleY(1); opacity: 0.85; }}
                50% {{ transform: scaleY(1.35); opacity: 1; }}
            }}
            @keyframes antennaPulse {{
                0%, 100% {{ opacity: 0.7; r: 3.5px; }}
                50% {{ opacity: 1; r: 4.8px; }}
            }}
            .kibo-hover-group {{
                animation: kiboHover 3s ease-in-out infinite;
                transform-origin: 80px 90px;
            }}
            .kibo-arm-right {{
                animation: kiboWaveArm 1.8s ease-in-out infinite;
                transform-origin: 124px 108px;
            }}
            .kibo-plasma {{
                animation: kiboThrusterPulse 0.9s ease-in-out infinite alternate;
                transform-origin: 80px 145px;
            }}
            .kibo-antenna-orb {{
                animation: antennaPulse 1.4s ease-in-out infinite;
            }}
        </style>

        <g class="kibo-hover-group">
            <ellipse class="kibo-plasma" cx="80" cy="154" rx="14" ry="16" fill="url(#plasmaGlow)" />
            <ellipse cx="80" cy="151" rx="8" ry="7" fill="#e0f2fe" opacity="0.9" />
            <path d="M72 138 Q80 144 88 138 Z" fill="#1e293b" />
            <g>
                <rect x="25" y="104" width="14" height="24" rx="7" fill="url(#bodyGrad)" transform="rotate(18 25 104)" stroke="#cbd5e1" stroke-width="1.2" />
                <circle cx="28" cy="126" r="6.5" fill="url(#blueAccent)" />
            </g>
            <g class="kibo-arm-right">
                <rect x="120" y="96" width="14" height="25" rx="7" fill="url(#bodyGrad)" transform="rotate(-35 120 96)" stroke="#cbd5e1" stroke-width="1.2" />
                <circle cx="138" cy="88" r="7" fill="url(#blueAccent)" />
                <ellipse cx="140" cy="85" rx="3.5" ry="5" fill="#38bdf8" opacity="0.6" />
            </g>
            <rect x="52" y="96" width="56" height="46" rx="20" fill="url(#bodyGrad)" stroke="#cbd5e1" stroke-width="1.8" />
            <rect x="62" y="104" width="36" height="22" rx="9" fill="#0f172a" />
            <circle cx="80" cy="115" r="4" fill="#00f0ff" filter="url(#eyeGlow)" />
            <rect x="68" y="113.5" width="24" height="3" rx="1.5" fill="rgba(0,240,255,0.3)" />
            <rect x="70" y="86" width="20" height="12" rx="4" fill="#334155" />
            <rect x="36" y="28" width="88" height="64" rx="28" fill="url(#bodyGrad)" stroke="#cbd5e1" stroke-width="2" />
            <rect x="28" y="44" width="10" height="26" rx="5" fill="url(#blueAccent)" stroke="#1d4ed8" stroke-width="1" />
            <rect x="122" y="44" width="10" height="26" rx="5" fill="url(#blueAccent)" stroke="#1d4ed8" stroke-width="1" />
            <circle cx="33" cy="57" r="2.5" fill="#e0f2fe" />
            <circle cx="127" cy="57" r="2.5" fill="#e0f2fe" />
            <rect x="44" y="38" width="72" height="46" rx="19" fill="url(#visorGrad)" stroke="#1e293b" stroke-width="1.5" />
            <path d="M48 48 C54 42, 70 41, 80 41 C90 41, 106 42, 112 48" stroke="rgba(255,255,255,0.22)" stroke-width="2" fill="none" stroke-linecap="round" />
            {eyes_svg}
            <rect x="78" y="14" width="4" height="15" rx="2" fill="#64748b" />
            <circle class="kibo-antenna-orb" cx="80" cy="12" r="4.5" fill="#00f0ff" filter="url(#eyeGlow)" />
        </g>
    </svg>
    </div>
    """
