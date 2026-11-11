"""Kibo Copilot: Tu Copiloto Inteligente y Mascota Guía (Estilo Astro Bot)."""

from typing import Dict, Optional
import streamlit as st
from ui.kibo_avatar import get_kibo_svg, get_kibo_hero_banner


STEP_GUIDES = {
    1: {
        "title": "Paso 1: Configurando tu nave (Capital y Perfil)",
        "badge": "Punto de Partida",
        "description": "Elige cuánto capital simulado quieres evaluar (base USD 100.000) y cómo reaccionas al riesgo. Kibo adaptará los modelos matemáticos para proteger tu capital o buscar mayor rendimiento según lo que elijas.",
        "simple_explanation": "🛡️ Tranquilo: aquí no arriesgas ni un centavo real. Es un laboratorio seguro donde aprendes cómo se comportaría tu dinero en el mundo real.",
        "tip": "💡 Consejo de Kibo: Si eliges **Conservador**, priorizaremos blindar tu cartera ante caídas extremas con el modelo de Salto de Merton.",
    },
    2: {
        "title": "Paso 2: Eligiendo tu tripulación (Activos y Diversificación)",
        "badge": "La Regla de Oro",
        "description": "Seleccionamos 10 activos líderes en más de 6 sectores de la economía. Evaluamos 3 años de historia real para medir volatilidad, asimetría y curtosis de cada empresa.",
        "simple_explanation": "🧺 'Nunca pongas todos los huevos en la misma canasta': Si una acción o sector tropieza (ej. tecnología), otros sectores defensivos (salud, servicios públicos) compensan y salvan tu cartera.",
        "tip": "💡 Consejo de Kibo: La regla de la clase exige un mínimo de 4 sectores económicos diferentes para garantizar que tu inversión esté verdaderamente protegida.",
    },
    3: {
        "title": "Paso 3: El laboratorio cuántico (3 Modelos Estocásticos)",
        "badge": "Cerebros Matemáticos",
        "description": "Ponemos a competir tres modelos financieros avanzados: Movimiento Browniano Geométrico (GBM), Salto de Merton (Jump-Diffusion) y Ornstein-Uhlenbeck (Reversión a la media), evaluados mediante AIC y BIC.",
        "simple_explanation": "🤖 Tres formas de predecir el futuro: 1) El camino continuo estándar (GBM), 2) El detector de sorpresas y caídas repentinas (Merton), y 3) El imán que regresa siempre a su precio medio (Ornstein-Uhlenbeck). Kibo elige el ganador estadístico para cada acción.",
        "tip": "💡 Consejo de Kibo: El criterio BIC premia la precisión pero castiga la complejidad innecesaria. Para acciones como Tesla o Nvidia casi siempre gana Merton por sus saltos inesperados.",
    },
    4: {
        "title": "Paso 4: Tu plan de vuelo (Portafolio Óptimo y Acciones Enteras)",
        "badge": "Decisión Inteligente",
        "description": "Resolvemos la optimización cuadrática de Mínimo VaR 99% con restricciones sectoriales (máximo 35% por sector y 2%-20% por acción) convirtiendo los porcentajes teóricos en acciones enteras reales con efectivo residual.",
        "simple_explanation": "🎯 Tu receta exacta: Te decimos con precisión cuántas acciones comprar de cada empresa para que tu riesgo sea el mínimo matemáticamente posible, dejando un pequeño saldo en efectivo para lo que sobre.",
        "tip": "💡 Consejo de Kibo: ¡Felicidades! Ya tienes un portafolio profesional de nivel institucional, comprensible y listo para sustentar en clase.",
    },
}


def render_step_insight(step: int, profile: str = "Moderado", extra_context: Optional[str] = None):
    info = STEP_GUIDES.get(step, STEP_GUIDES[1])
    context_text = f"<br><strong>Recomendación para perfil {profile}:</strong> {extra_context}" if extra_context else ""
    st.markdown(
        f"""
        <div class="kibo-hero-card" style="margin: 1rem 0; padding: 1.1rem 1.4rem;">
            <div style="display:flex; align-items:center; gap: 1rem;">
                <div style="font-size: 2.2rem; filter: drop-shadow(0 0 10px rgba(56,189,248,0.5));">🤖</div>
                <div style="flex:1;">
                    <div style="font-size:0.75rem; font-weight:800; color:#38bdf8; text-transform:uppercase; letter-spacing:0.06em;">Kibo Copiloto · {info['badge']}</div>
                    <div style="font-size:0.95rem; font-weight:700; color:#ffffff; margin:0.15rem 0;">{info['title']}</div>
                    <div style="font-size:0.86rem; color:#cbd5e1; line-height:1.45;">{info['simple_explanation']}{context_text}</div>
                    <div style="margin-top:0.45rem; color:#38bdf8; font-size:0.8rem; font-weight:600;">{info['tip']}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


@st.dialog("🚀 Kibo — Copiloto Inteligente & Guía de Inversión")
def open_copilot_modal(active_step: int = 1):
    tab_tour, tab_simple, tab_models, tab_profiles = st.tabs([
        "❓ Ayuda rápida",
        "👶 Finanzas en Cristiano",
        "🧠 Modelos Matemáticos",
        "🎯 Perfiles de Riesgo",
    ])

    with tab_tour:
        info = STEP_GUIDES.get(active_step, STEP_GUIDES[1])
        st.markdown(f"### {info['title']}")
        st.info(info["simple_explanation"])
        st.markdown(f"**Detalle técnico:** {info['description']}")
        st.markdown(f"*{info['tip']}*")
        
        st.markdown("---")
        st.markdown("#### 🗺️ Tu viaje con Kibo en 4 pasos:")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown("**1. Parámetros**\nCapital & Perfil")
        with c2:
            st.markdown("**2. Activos**\nDiversificación")
        with c3:
            st.markdown("**3. Modelos**\nBrowniano, Merton, O-U")
        with c4:
            st.markdown("**4. Portafolio**\nMínimo VaR & Decisión")

    with tab_simple:
        st.markdown("### 💡 Conceptos Clave Explicados Sin Tecnicismos")
        st.markdown("""
        - **¿Qué es el Riesgo (VaR 99%)?**  
          Imagina que es el peor día de lluvia del mes. Si tu VaR 99% a 10 días es del 4%, significa que en el 99% de los casos normales nunca perderás más de 4% de tu dinero en ese periodo.
        
        - **¿Por qué diversificar en 4 sectores?**  
          Si inviertes todo en tecnología y hay una crisis en chips, se cae todo tu dinero. Si tienes además salud, energía y servicios básicos, las pérdidas se suavizan porque la gente sigue yendo al médico y encendiendo la luz.
        
        - **¿Por qué compiten 3 modelos estocásticos?**  
          Cada acción tiene personalidad propia. Acciones estables como Johnson & Johnson o energía se comportan como resortes que vuelven a la media (Ornstein-Uhlenbeck). Acciones explosivas como Tesla o Nvidia dan saltos imprevistos (Merton). Kibo busca el modelo a la medida para cada una.
        """)

    with tab_models:
        st.markdown("### Comparativa Rigurosa de Modelos Cuantitativos")
        
        with st.expander("1. Movimiento Browniano Geométrico (GBM)", expanded=True):
            st.markdown(r"""
            **Ecuación Diferencial Estocástica:**
            $$dS_t = \mu S_t dt + \sigma S_t dW_t$$
            - **Solución Exacta:** $S_t = S_0 \exp\left((\mu - \frac{1}{2}\sigma^2)t + \sigma \sqrt{t} Z\right), \quad Z \sim \mathcal{N}(0, 1)$
            - **Fortalezas:** Modelo estándar y parsimonioso ($k=2$). Fácil interpretación.
            - **Limitaciones:** Asume retornos normales con colas delgadas. Subestima pérdidas catastróficas (fat tails).
            """)
            
        with st.expander("2. Modelo de Salto de Merton (Jump-Diffusion)", expanded=True):
            st.markdown(r"""
            **Ecuación Diferencial Estocástica:**
            $$dS_t = (\mu - \lambda \bar{k}) S_t dt + \sigma S_t dW_t + (Y - 1)S_t dN_t$$
            - **Componente de Salto:** $N_t \sim \text{Poisson}(\lambda)$, tamaño del salto $\ln(Y) \sim \mathcal{N}(\mu_J, \sigma_J^2)$.
            - **Fortalezas:** Captura caídas abruptas y sorpresas de mercado (Black Swans). Genera colas pesadas (kurtosis > 3).
            - **Uso Crítico:** Esencial para perfiles **Conservadores** para no infravalorar el VaR y CVaR 99%.
            """)
            
        with st.expander("3. Modelo Ornstein-Uhlenbeck (Reversión a la Media)", expanded=True):
            st.markdown(r"""
            **Ecuación Diferencial Estocástica:**
            $$dX_t = \theta (\mu_{ou} - X_t)dt + \sigma_{ou} dW_t$$
            - **Parámetros:** $\theta$ (velocidad de reversión), $\mu_{ou}$ (precio medio de equilibrio), Half-Life $t_{1/2} = \frac{\ln 2}{\theta}$.
            - **Fortalezas:** Excelente para activos defensivos, utilities (NEE) y dividendos que oscilan alrededor de fundamentales.
            """)

    with tab_profiles:
        st.markdown("### ¿Cómo condiciona el Perfil de Riesgo la Decisión?")
        st.markdown(r"""
        - 🛡️ **Conservador (Modo Escudo):**
          - Prioriza protección absoluta ante caídas inesperadas (Merton Jump-Diffusion y reversión Ornstein-Uhlenbeck).
          - Restringe activos con alta frecuencia de saltos negativos ($\lambda$).
        - ⚖️ **Moderado (Modo Equilibrio):**
          - Balance perfecto entre crecimiento y control de volatilidad mediante el Criterio Bayesiano (BIC).
          - Diversificación balanceada con tope sectorial estricto del 35%.
        - 🚀 **Agresivo (Modo Impulso):**
          - Maximiza la captura del drift ($\mu > 15\%$) aprovechando tendencias alcistas a largo plazo.
        """)


def render_copilot_badge(active_step: int = 1):
    col_l, col_r = st.columns([5, 2])
    with col_r:
        if st.button("🤖 Abrir Copiloto Kibo", use_container_width=True, help="Consulta la guía interactiva, fórmulas y explicaciones paso a paso de Kibo"):
            open_copilot_modal(active_step)

