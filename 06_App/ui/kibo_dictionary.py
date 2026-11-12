"""
Diccionario Financiero de Kibo: Traductor de Jerga Financiera a Cristiano.
Diseñado para que cualquier persona sin conocimientos financieros entienda
todos los conceptos avanzados del Taller de Valoración y Riesgo (DEFI 2).
"""

from typing import List, Dict, Any
import streamlit as st


FINANCIAL_TERMS: List[Dict[str, Any]] = [
    {
        "term": "VaR (Value at Risk / Valor en Riesgo)",
        "badge": "Gestión de Riesgo · Rúbrica Paso 10",
        "icon": "🛡️",
        "formal": "Cuantía máxima de pérdida esperada a un nivel de confianza α (99%) y un horizonte temporal h (10 días) bajo condiciones normales de mercado.",
        "simple": "Es el límite de lo peor que te puede pasar en un día normal. Si tu VaR a 10 días es $1.500 USD, significa que en 99 de cada 100 quincenas tus pérdidas no superarán esa cantidad.",
        "example": "Si tienes $100.000 invertidos y el VaR 99% es 1.5%, tienes un 99% de certeza de que tu pérdida máxima quincenal será de $1.500 USD.",
        "step": "Paso 6 (Portafolio & Riesgo)",
    },
    {
        "term": "CVaR (Expected Shortfall / Pérdida Extrema)",
        "badge": "Riesgo de Cola · Rúbrica Paso 10",
        "icon": "🚨",
        "formal": "Esperanza matemática de las pérdidas que superan el umbral del VaR: E[L | L > VaR]. Medida de riesgo coherente que cuantifica la severidad del desastre.",
        "simple": "Si llega el día de una catástrofe y se rompe el límite del VaR, ¿cuánto perderías en promedio? Kibo te dice el tamaño real del golpe en el peor 1% de los casos.",
        "example": "Si el VaR es $1.500 USD y el CVaR es $2.100 USD, en el peor día del año esperarías perder en promedio $2.100 USD, no solo $1.500.",
        "step": "Paso 6 (Pestaña Riesgo & VaR)",
    },
    {
        "term": "GBM (Movimiento Browniano Geométrico)",
        "badge": "Modelo Estocástico · Rúbrica Paso 4",
        "icon": "📈",
        "formal": "Proceso estocástico en tiempo continuo dS_t = μ·S_t·dt + σ·S_t·dW_t, base del modelo de Black-Scholes.",
        "simple": "Imagina una hoja flotando en un río con corriente constante y olas suaves. Asume que el precio de la acción sube o baja de forma continua, sin sobresaltos bruscos.",
        "example": "Simula 5.000 futuros posibles para Apple asumiendo que su precio flota con su rentabilidad y volatilidad habituales.",
        "step": "Paso 4 (Pestaña 1 GBM)",
    },
    {
        "term": "Salto de Merton (MJD / Jump-Diffusion)",
        "badge": "Modelo Estocástico · Rúbrica Paso 4",
        "icon": "⚡",
        "formal": "Modelo de difusión con saltos de Poisson compuestos y tamaño log-normal para capturar discontinuidades bruscas en el precio.",
        "simple": "La bolsa no siempre es tranquila. Este modelo contempla 'saltos de susto' o noticias bomba inesperadas (balances trimestrales sorpresa, crisis o quiebras) que mueven el precio de golpe.",
        "example": "Si una empresa farmacéutica anuncia que su vacuna fue aprobada, su acción puede saltar +15% en un segundo. Merton modela esa probabilidad de sobresaltos.",
        "step": "Paso 4 (Pestaña 2 Saltos)",
    },
    {
        "term": "Ornstein-Uhlenbeck (O-U / Reversión a la Media)",
        "badge": "Modelo Estocástico · Rúbrica Paso 4",
        "icon": "🧲",
        "formal": "Ecuación diferencial estocástica dx_t = θ·(μ - x_t)·dt + σ·dW_t con fuerza de atracción hacia un nivel de equilibrio μ y vida media ln(2)/θ.",
        "simple": "El modelo del 'efecto imán' o resorte. Si el precio sube demasiado o cae demasiado, una fuerza invisible lo jala de vuelta a su promedio histórico. Ideal para petróleo o energía, pero no para empresas de tecnología innovadora.",
        "example": "El precio de un barril de petróleo tiende a regresar a su costo promedio de extracción ($70 USD). Si sube a $120, O-U proyecta que tarde o temprano bajará.",
        "step": "Paso 4 (Pestaña 3 Reversión)",
    },
    {
        "term": "Browniano Fraccionario (fBm) & Hurst (H)",
        "badge": "Modelo Estocástico · Rúbrica Paso 4",
        "icon": "🌀",
        "formal": "Proceso autorregresivo gaussiano con parámetro de Hurst H ∈ (0,1). Si H > 0.5 existe memoria larga y persistencia; si H < 0.5 hay antipersistencia.",
        "simple": "¿La acción tiene memoria de su pasado? Si H > 0.5, la acción es como un tren con inercia: si viene subiendo, tiene impulso para seguir subiendo (tendencia). Si H < 0.5, cambia de dirección constantemente como un péndulo inquieto.",
        "example": "Nvidia tiene un H = 0.58, lo que indica que cuando entra en racha alcista tiende a mantener la inercia por más tiempo que una caminata puramente aleatoria.",
        "step": "Paso 4 (Pestaña 4 Memoria)",
    },
    {
        "term": "Efecto Manada (Herding - Test CCK 2000)",
        "badge": "Finanzas Conductuales · Rúbrica Paso 5",
        "icon": "🐑",
        "formal": "Evaluación econométrica no lineal de la dispersión transversal de retornos (CSAD) frente al mercado: un coeficiente γ2 < 0 estadísticamente significativo confirma manada.",
        "simple": "Cuando hay pánico en la calle, la gente deja de pensar y sale corriendo detrás de la multitud. En la bolsa ocurre igual: si hay efecto manada, todos compran o venden al mismo tiempo por miedo o euforia, ignorando el valor real de cada empresa.",
        "example": "Durante el pánico del COVID-19 en marzo 2020, todas las acciones se desplomaron juntas sin importar si sus negocios eran buenos o malos: eso es efecto manada puro.",
        "step": "Paso 4 (Pestaña 5 Manada)",
    },
    {
        "term": "Opción Financiera (Call & Put)",
        "badge": "Derivados Financieros · Rúbrica Pasos 6 y 7",
        "icon": "📜",
        "formal": "Contrato derivado asimétrico que confiere al comprador el derecho, mas no la obligación, de comprar (Call) o vender (Put) un activo a un precio fijado (Strike).",
        "simple": "Es exactamente como comprar la póliza de seguro de tu carro: pagas una prima pequeña. Si el carro se estrella (la acción se desploma), la opción Put te permite venderla cara y te salva la billetera.",
        "example": "Compras una opción Put de Apple con Strike $180 por una prima de $3. Si Apple cae a $140, tu seguro te permite venderla a $180, ahorrándote $40 de pérdida por acción.",
        "step": "Paso 5 (Tu Seguro de Inversión)",
    },
    {
        "term": "Strike (Precio de Ejercicio / K)",
        "badge": "Contratos de Opciones · Rúbrica Paso 7",
        "icon": "🎯",
        "formal": "Precio contractual acordado al que el tenedor de la opción puede ejecutar la transacción de compra o venta en o antes de la fecha de expiración.",
        "simple": "El precio pactado en el contrato de tu seguro. Es el precio garantizado al que podrás vender o comprar tus acciones sin importar lo que pase en Wall Street.",
        "example": "Si compras un seguro con Strike de $150 USD, pase lo que pase en el mundo, tienes garantizado que puedes vender tu acción a $150 USD.",
        "step": "Paso 5 (Selección de Contratos)",
    },
    {
        "term": "Prima de la Opción (Costo del Seguro)",
        "badge": "Valoración de Opciones · Rúbrica Paso 7",
        "icon": "🏷️",
        "formal": "Precio de mercado que el comprador paga al vendedor por los derechos del derivado, igual al valor esperado neutral al riesgo descontado.",
        "simple": "Lo que pagas hoy por comprar la protección. Si las acciones suben y nunca necesitas activar tu seguro, lo único que pierdes es esta pequeña prima pagada.",
        "example": "Pagas $4.50 USD por acción para blindar una inversión de $180 USD. Si no hay crisis, perdiste $4.50 pero dormiste 100% tranquilo todo el mes.",
        "step": "Paso 5 (Valoración CRR)",
    },
    {
        "term": "Árbol Binomial (Modelo CRR)",
        "badge": "Valoración de Opciones · Rúbrica Paso 8",
        "icon": "🌳",
        "formal": "Modelo en tiempo discreto formulado por Cox, Ross y Rubinstein (1979) que discretiza la trayectoria del precio en factores up (u) y down (d) bajo probabilidades neutrales al riesgo p_q.",
        "simple": "Un mapa de caminos donde en cada paso el precio solo tiene dos opciones: o sube o baja. Kibo viaja desde el futuro hacia el presente calculando el valor exacto de tu seguro en cada cruce de caminos.",
        "example": "El árbol de 3 pasos divide el tiempo de tu opción en 3 etapas y calcula cuánto valdría tu contrato en cada uno de los 4 escenarios finales posibles.",
        "step": "Paso 5 (Opciones Avanzadas)",
    },
    {
        "term": "Drawdown & Máximo Drawdown (MDD)",
        "badge": "Auditoría Histórica · Rúbrica Paso 12",
        "icon": "📉",
        "formal": "Pérdida porcentual acumulada desde el último valor máximo histórico del patrimonio hasta el piso o valle sucesivo antes de recuperarse.",
        "simple": "¿Cuánto dolió la peor racha del año? Si tu cuenta llegó a $100.000 USD, cayó a $88.000 USD y luego volvió a subir, tu peor caída (Drawdown Máximo) fue del 12%.",
        "example": "Kibo examina los últimos 252 días de Wall Street y verifica que tu cartera nunca cayó más de un porcentaje tolerable para tu perfil de riesgo.",
        "step": "Paso 6 (Pestaña Examen Histórico)",
    },
    {
        "term": "Optimización SLSQP & Límite Sectorial 35%",
        "badge": "Ingeniería de Portafolio · Rúbrica Paso 11",
        "icon": "⚖️",
        "formal": "Algoritmo de Programación Cuadrática Secuencial que minimiza w^T Σ w sujeto a sum(w) = 1, w_i >= 0 y concentración por sector <= 0.35.",
        "simple": "El chef financiero de Kibo: combina las acciones para que el plato final tenga el mínimo riesgo posible, respetando que ningún sector (como tecnología o salud) reciba más del 35% de tu dinero.",
        "example": "Aunque Apple, Microsoft y Nvidia sean excelentes, SLSQP no permite que la suma de las tres supere el 35% de tu dinero para evitar que una crisis tecnológica destruya tu cartera.",
        "step": "Paso 6 (Plan de Compra Final)",
    },
    {
        "term": "Diversificación de Portafolio",
        "badge": "Regla de Oro de Inversión · Rúbrica Paso 3",
        "icon": "🧺",
        "formal": "Distribución del capital en activos con coeficientes de correlación rho < 1 para reducir el riesgo no sistemático sin sacrificar rentabilidad esperada.",
        "simple": "La famosa regla: 'No pongas todos los huevos en la misma canasta'. Si inviertes en salud, tecnología, energía y finanzas, cuando a un sector le va mal, los otros compensan el golpe.",
        "example": "Si el precio del petróleo cae y afecta a ExxonMobil, las acciones de salud como Johnson & Johnson se mantienen estables, protegiendo tu dinero total.",
        "step": "Paso 3 (Universo de Acciones)",
    },
    {
        "term": "Test de Kupiec (Proportion of Failures - POF)",
        "badge": "Auditoría Econométrica · Rúbrica Paso 12",
        "icon": "🔍",
        "formal": "Prueba de razón de verosimilitud chi-cuadrado para contrastar si la frecuencia observada de violaciones del VaR coincide con el nivel teórico 1 - α (1%).",
        "simple": "El auditor estricto de Kibo. Cuenta cuántas veces la realidad superó el riesgo pronosticado y emite un veredicto formal de si el modelo fue confiable o si mintió.",
        "example": "En 252 días hábiles, se espera que el VaR al 99% falle entre 2 y 3 veces. Si falló 2 veces, el Test de Kupiec aprueba el modelo con honores.",
        "step": "Paso 6 (Pestaña Examen Histórico)",
    },
]


def render_kibo_dictionary_content():
    """Renderiza el traductor de jerga financiera a cristiano de Kibo de forma interactiva."""
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.12), rgba(15, 23, 42, 0.85));
                    border: 1.5px solid rgba(16, 185, 129, 0.35); border-radius: 16px; padding: 1rem 1.2rem; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 0.4rem;">
                <span style="font-size: 1.6rem;">📖</span>
                <div>
                    <div style="font-size: 1.05rem; font-weight: 800; color: #f8fafc;">Diccionario Financiero de Kibo</div>
                    <div style="font-size: 0.78rem; font-weight: 700; color: #10b981; letter-spacing: 0.05em; text-transform: uppercase;">
                        Traductor de Jerga Técnica a Cristiano
                    </div>
                </div>
            </div>
            <div style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.45;">
                ¿Encontraste una palabra rara como <em>VaR</em>, <em>Hurst</em> o <em>Merton</em>? 
                Aquí te traducimos cada tecnicismo de la bolsa a explicaciones sencillas con ejemplos reales para que nunca te sientas perdido.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    query = st.text_input("🔎 Buscar término o concepto:", placeholder="Ej: VaR, salto, strike, merton, manada...", key="kibo_dict_search")
    
    filtered = FINANCIAL_TERMS
    if query.strip():
        q_lower = query.lower()
        filtered = [
            t for t in FINANCIAL_TERMS
            if q_lower in t["term"].lower() or q_lower in t["simple"].lower() or q_lower in t["formal"].lower() or q_lower in t["badge"].lower()
        ]

    st.caption(f"Mostrando {len(filtered)} de {len(FINANCIAL_TERMS)} conceptos clave:")

    for item in filtered:
        with st.expander(f"{item['icon']} {item['term']}", expanded=(len(filtered) == 1)):
            st.markdown(
                f"""
                <div style="background: rgba(15, 23, 42, 0.6); border-left: 3px solid #10b981; border-radius: 8px; padding: 0.7rem 0.9rem; margin-bottom: 0.6rem;">
                    <div style="font-size: 0.72rem; font-weight: 800; color: #10b981; text-transform: uppercase; margin-bottom: 0.2rem;">
                        {item['badge']} · {item['step']}
                    </div>
                    <div style="font-size: 0.95rem; font-weight: 750; color: #34d399; margin-bottom: 0.35rem;">
                        💡 En cristiano con Kibo:
                    </div>
                    <div style="font-size: 0.88rem; color: #f1f5f9; line-height: 1.45; margin-bottom: 0.5rem;">
                        {item['simple']}
                    </div>
                    <div style="font-size: 0.84rem; color: #fbbf24; background: rgba(245, 158, 11, 0.1); border-radius: 6px; padding: 0.45rem 0.65rem; margin-bottom: 0.5rem;">
                        <strong>📌 Ejemplo práctico:</strong> {item['example']}
                    </div>
                    <div style="font-size: 0.76rem; color: #94a3b8; font-style: italic;">
                        <strong>Definición técnica formal:</strong> {item['formal']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


@st.dialog("📖 Diccionario Financiero de Kibo")
def show_kibo_dictionary_dialog():
    """Abre el diccionario de Kibo en un modal dialog centrado y elegante."""
    render_kibo_dictionary_content()

