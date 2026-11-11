import json
import os

def build_presentation_suite():
    md_path = '08_Exposicion/LIBRETO_Y_DIAPOSITIVAS_STORYTELLING.md'
    ipynb_path = '08_Exposicion/guia_y_planeacion_diapositivas_opciones_reales.ipynb'

    # =========================================================================
    # 1. CONTENIDO COMPLETO DEL MARKDOWN
    # =========================================================================
    md_content = r"""# LIBRETO MAESTRO DE EXPOSICIÓN ORAL: OPCIONES REALES
## Guía Completa de Presentación Oral + Rigor Matemático y Ejemplos Cotidianos
**Asignatura:** Finanzas Descentralizadas 2 (DEFI 2) — Universidad Externado de Colombia  
**Expositores:**  
* **Julián Duarte:** Exposición Teórica, Fundamentos Cuantitativos y Modelado Discreto (Diapositivas 1 a 8).  
* **Felipe Pulido:** Laboratorio Práctico Computacional y Simulación Interactiva en Vivo.  

**Bibliografía Oficial del Curso:**
* **Francisco Venegas Martínez (2009).** *Riesgos Financieros y Económicos: Productos Derivados y Decisiones Económicas bajo Incertidumbre*. 2.ª ed., Cengage Learning / Alfaomega. **Capítulo 69 completo: págs. 800–816**.
* **Avinash K. Dixit y Robert S. Pindyck (1994).** *Investment under Uncertainty*. Princeton University Press.
* **Stewart C. Myers (1977).** *"Determinants of Corporate Borrowing"*. *Journal of Financial Economics*, 5(2), págs. 147–175.
* **John C. Cox, Stephen A. Ross y Mark Rubinstein (1979).** *"Option Pricing: A Simplified Approach"*. *Journal of Financial Economics*, 7(3), págs. 229–263.
* **Tom Copeland y Vladimir Antikarov (2001).** *Real Options: A Practitioner's Guide*. Texere. *(Supuesto MAD - Marketed Asset Disclaimer)*.

---

### 🗺️ El Hilo Conductor Narrativo de la Exposición Teórica (Julián Duarte)
Toda la presentación está coordinada diapositiva por diapositiva con el PDF final y el archivo HTML (`Presentacion_Opciones_Reales_Final.pdf`):

```text
[PORTADA] Opciones Reales - Finanzas Descentralizadas 2 (Julián Duarte & Felipe Pulido)
    ↓
[DIAPOSITIVA 1: LA FALACIA DEL VPN Y EL VPN MODIFICADO]
  • El dilema del VPN tradicional frente al negocio real de una cafetería o panadería.
  • La ecuación fundamental: VPN modificado = VPN estático + c.
  • Pregunta puente: "¿Y qué es esa letra 'c' que rescata el proyecto? Pasemos a la lámina 2".
    ↓
[DIAPOSITIVA 2: ¿QUÉ ES UNA OPCIÓN REAL?]
  • Definición canónica (Venegas p. 800; Dixit & Pindyck 1994) y las 3 condiciones de existencia.
  • El caso colombiano de Tiendas D1: contratos de arriendo y estanterías modulares como opciones reales.
  • Pregunta puente: "¿Cómo traducimos un local comercial o una fábrica al lenguaje de derivados?".
    ↓
[DIAPOSITIVA 3: CORRESPONDENCIA DERIVADOS VS. ACTIVOS REALES]
  • El diccionario de 5 variables (S, K, r, σ, T-t) y la Paradoja de la Volatilidad.
  • Pregunta puente: "¿Qué catálogo de decisiones estratégicas concretas tiene el gerente?".
    ↓
[DIAPOSITIVA 4: CATÁLOGO DE 6 OPCIONES REALES Y PAYOFFS]
  • Timing (Dixit & Pindyck), Expansión (Call), Contracción (Put), Abandono (Put), Switching y Compuestas.
  • Pregunta puente: "¿Por qué no usamos simplemente la fórmula analítica de Black-Scholes?".
    ↓
[DIAPOSITIVA 5: TIEMPO CONTINUO: BLACK-SCHOLES]
  • La EDP de Black-Scholes (Ec. 69.22): Theta, Gamma, Delta y descuento libre de riesgo r.
  • Las 2 limitaciones en activos reales: opciones americanas y mercados incompletos (supuesto MAD).
  • Pregunta puente: "¿Cómo resuelve la industria estos obstáculos? Con árboles discretos".
    ↓
[DIAPOSITIVA 6: SOLUCIÓN DISCRETA: ÁRBOL BINOMIAL CRR]
  • El modelo de Cox, Ross y Rubinstein: factores u y d, probabilidad neutral al riesgo q.
  • Inducción hacia atrás nodo a nodo con evaluación de ejercicio americano.
  • Pregunta puente: "Veamos cómo funciona esto en la práctica con un caso numérico exacto".
    ↓
[DIAPOSITIVA 7: CASO EN VIVO: OPCIÓN AMERICANA DE ABANDONO] (Venegas págs. 811-813)
  • El árbol completo de 3 períodos en SVG (precios S y valor C en cada nodo).
  • El análisis crítico del nodo t=1: liquidar por 60 supera continuar a 59.58 (el valor pasivo puro es 45).
  • Demostración: La opción rescata +$5.70M sobre el VPN neutro de cero.
  • Pregunta puente: "Cerremos con las tres lecciones directivas fundamentales".
    ↓
[DIAPOSITIVA 8: SÍNTESIS ESTRATÉGICA Y CONCLUSIONES DIRECTIVAS]
  • Las 3 ideas clave para la toma de decisiones corporativas.
  • Frase inspiradora de cierre y pase formal a Felipe Pulido para el laboratorio práctico en Python.
```

---

## DIAPOSITIVA 0: PORTADA
* **Contenido Visual:** Título "Opciones reales", subtítulo "Finanzas descentralizadas 2", integrantes: Julián Duarte y Felipe Pulido, con ilustración de flecha verde ascendente y monedas.
* **Tiempo sugerido:** 1 minuto.
* **Tu Discurso en Voz Alta (Apertura de Julián):**
  > *"Buenos días, profesor y compañeros. Hoy les vamos a presentar la fundamentación teórica y cuantitativa de una de las herramientas más potentes de las finanzas corporativas modernas: **las Opciones Reales**.*  
  > *Mi nombre es Julián Duarte y voy a estar a cargo de toda la fundamentación teórica, matemática y analítica del modelo; y al finalizar, mi compañero Felipe Pulido tomará el control para dirigir nuestro laboratorio práctico computacional con un simulador interactivo en Python.*  
  > *Para empezar, quiero hacerles una pregunta sencilla: ¿cuántas veces han escuchado en sus clases que si el Valor Presente Neto (VPN) de un negocio da negativo, el proyecto debe rechazarse de inmediato? Hoy vamos a demostrar que esa regla tradicional, aunque útil, comete un error conceptual grave: ignora que los directivos tienen cerebro y capacidad de adaptación. Comencemos."*

---

## DIAPOSITIVA 1: LA FALACIA DEL VPN TRADICIONAL Y EL VPN MODIFICADO
* **Contenido Visual:** Comparativa "VPN Tradicional: Enfoque pasivo y rígido de 'ahora o nunca'" vs "Realidad Corporativa: Los gerentes son activos; se adaptan y toman decisiones intermedias", recuadro central $\text{VPN}_{\text{Modificado}} = \text{VPN}_{\text{Estático}} + c$, con $c \ge 0$ el valor de la opción real.
* **Tiempo sugerido:** 3 minutos.

### 📐 Desglose de la Ecuación
* **Ecuación Central:**
  $$\text{VPN}_{\text{Modificado}} = \text{VPN}_{\text{Estático}} + c$$
* **Explicación Matemática:**
  El VPN tradicional o estático es la sumatoria de flujos de caja esperados descontados al costo de capital (WACC) menos la inversión inicial ($I_0$): $\sum_{t=1}^T \frac{E[CF_t]}{(1+WACC)^t} - I_0$. El término $c$ representa el valor económico de un contrato de opción (financiera o real). Como el derecho a decidir tiene una estructura de payoff asimétrica $\max(Payoff, 0)$, su valor siempre es no negativo ($c \ge 0$). Por lo tanto, el valor real de una empresa con flexibilidad directiva es estrictamente mayor o igual a su valoración pasiva estática.
* **Explicación Financiera Sencilla:**
  Imaginen que van a abrir una panadería o cafetería de barrio. Hacen el flujo de caja en Excel asumiendo que compran hornos de 60 millones y firman un contrato forzoso a 5 años. El Excel les dice que el VPN da **menos 5 millones**. La regla tradicional les dice: *"No abran el negocio, van a perder dinero"*.  
  Pero en la vida real ningún emprendedor sensato se amarra así. Uno arrienda el local con contrato a 1 año y compra maquinaria modular. Si el barrio se llena de clientes, el negocio despega; y si nadie entra a comprar, se cancela el arriendo, se venden los hornos y se corta la pérdida de raíz. Esa capacidad de reaccionar y adaptarse sobre la marcha vale plata: es una **opción real** ($c$). Si esa flexibilidad vale 15 millones, el verdadero valor del negocio no es $-5$, sino: $-5 + 15 = \mathbf{+10\text{ millones}}$. ¡El proyecto sí se debe hacer!

---

## DIAPOSITIVA 2: ¿QUÉ ES UNA OPCIÓN REAL?
* **Contenido Visual:** Definición adaptada de Francisco Venegas (pág. 800) y Dixit & Pindyck (1994). Las 3 condiciones obligatorias de existencia (Irreversibilidad, Incertidumbre estocástica, Margen de maniobra temporal) y contraste entre Opción Financiera vs. Opción Real.
* **Tiempo sugerido:** 3.5 minutos.

### 📐 Fundamentación Teórica
* **Definición Canónica:**  
  *"Una opción real es el derecho, mas no la obligación, de tomar o modificar decisiones estratégicas sobre un activo productivo o tangible en una fecha futura, a medida que la incertidumbre del mercado se resuelve."*
* **Las 3 Condiciones Obligatorias (Dixit & Pindyck 1994):**
  1. **Irreversibilidad:** La inversión inicial implica costos hundidos que no se pueden recuperar totalmente si se cancela el proyecto.
  2. **Incertidumbre Estocástica:** Los ingresos futuros, precios y costos son variables aleatorias que no se conocen con certeza hoy.
  3. **Margen de Maniobra Temporal (Flexibilidad / Timing):** El directivo no está atado a un ultimátum de "ahora o nunca"; puede decidir cuándo invertir, cuánto ampliar, o cuándo liquidar.

### 🎙️ Guion en Modo Storytelling (El Caso de Tiendas D1)
* **Tu Discurso en Voz Alta:**
  > *"¿Cómo llevamos esto a un ejemplo que todos vemos todos los días en Colombia? Miren el caso de **Tiendas D1**.*  
  > *¿Cómo hizo D1 para abrir miles de tiendas en todo el país sin quebrar en el intento? Muy simple: diseñaron su negocio entero basado en opciones reales y en las tres condiciones de Dixit y Pindyck que ven en la diapositiva:*  
  > *Primero: **Irreversibilidad**. D1 casi nunca compra locales comerciales; sabe que comprar un inmueble amarra capital irreversible. Ellos arriendan locales de barrio sencillos.*  
  > *Segundo: **Incertidumbre**. Cuando abren en un barrio nuevo, no tienen idea exacta de cuántos vecinos van a entrar a comprar o si prefieren seguir yendo a la tienda de la esquina.*  
  > *Y tercero: **Margen de maniobra**. Miren sus tiendas por dentro: no gastan millones en acabados de lujo; usan estanterías metálicas modulares y firman arriendos con cláusulas de salida a un año.*  
  > *¿Qué lograron con esto? Crearon opcionalidad pura: si la tienda es un éxito rotundo, ejercen la **opción de expansión** y abren otra sede a 10 cuadras. Pero si el punto de venta no vende lo esperado, en 24 horas meten las estanterías en un camión, las llevan a otro barrio, cancelan el arriendo y ejercen la **opción de abandono** perdiendo solo unos meses de canon.*  
  > *D1 no es solo un supermercado de descuento: financieramente es una gigantesca máquina corporativa de ejecutar opciones reales."*

---

## DIAPOSITIVA 3: CORRESPONDENCIA DERIVADOS VS. ACTIVOS REALES
* **Contenido Visual:** Tabla comparativa del Cuadro 69.1 de Venegas ($S_t, K, r, \sigma, T-t$) y en el lado derecho la **Paradoja de la Volatilidad** con el contraste entre finanzas tradicionales y opciones reales, junto con el mecanismo de convexidad.
* **Tiempo sugerido:** 4 minutos.

### 📐 Desglose de Variables y Paradoja de la Volatilidad
* **El Diccionario de Correspondencia (Venegas pág. 802):**
  * $S_t$: En Wall Street es el precio de una acción; en la economía real es el **Valor Presente de los Flujos de Caja del Proyecto**.
  * $K$: En bolsa es el precio de ejercicio (*strike*); en la empresa es el **Costo de Inversión (CAPEX)**.
  * $r$: Tasa libre de riesgo (en Colombia, los títulos de deuda pública **TES**).
  * $\sigma$: Volatilidad de los rendimientos del proyecto.
  * $T - t$: Ventana de tiempo contractual para tomar la decisión (plazo de arriendo, concesión o patente).
* **La Paradoja de la Volatilidad:**
  * En finanzas tradicionales: $\sigma \uparrow \implies \text{Riesgo} \uparrow \implies \text{WACC} \uparrow \implies \text{VPN} \downarrow$. (Mayor dispersión castiga la tasa de descuento y destruye valor).
  * En Opciones Reales: $\sigma \uparrow \implies \text{Valor Call} \uparrow, \; \text{Valor Put} \uparrow$. (La volatilidad expande la dispersión de resultados futuros).
* **Explicación Financiera Sencilla:**
  * *¿Por qué en opciones reales más incertidumbre da más valor?* Por la **convexidad del payoff**:
    * Si la demanda explota positivamente al triple, tú tienes la opción de expandirte y te ganas todo el beneficio (**Upside ilimitado**).
    * Pero si la economía entra en crisis profunda y las ventas caen a cero, tú NO estás obligado a invertir; simplemente no ejerces o liquidas el negocio (**Downside truncado**).
    * El directivo se queda con las ganancias extraordinarias y le pone un piso blindado a las pérdidas. Por eso, entre más volátil sea el entorno, más vale tener la opción en la mano.

---

## DIAPOSITIVA 4: CATÁLOGO DE OPCIONES REALES
* **Contenido Visual:** 6 tarjetas en cuadrícula limpia (2 filas de 3 columnas): 1. Posponer (Timing), 2. Expansión (Call), 3. Contracción (Put de escala), 4. Abandono (Put), 5. Cambio Operativo (Switching) y 6. Compuesta/Secuencial.
* **Tiempo sugerido:** 4.5 minutos.

### 📐 Desglose Riguroso de cada Fórmula y Significado
1. **Opción de Posponer / Esperar (Timing) [Dixit & Pindyck 1994]:**
   $$S_t - K \ge C_{\text{espera}} \iff \text{VPN} > \text{Valor de la Opción de Esperar}$$
   * *Explicación:* No basta con que el VPN sea positivo ($S_t - K > 0$) para invertir hoy. Invertir destruye la opción de postergar. Hay que invertir solo si las ganancias inmediatas superan el valor de esperar nueva información.  
   * *Ejemplo cotidiano:* Si compras un lote de terreno, aunque construir un edificio hoy te dé ganancia, esperar 6 meses a ver si pavimentan la avenida o bajan las tasas de interés puede generar mucho más valor.
2. **Opción de Expansión (Call) [Venegas Ec. 69.7]:**
   $$\text{Payoff} = S_T + \alpha \max\left(S_T - \frac{K'}{\alpha}, \; 0\right)$$
   * *Explicación:* $S_T$ es el negocio base. Si las ventas despegan, pagas un capital adicional $K'$ y multiplicas tu capacidad por un factor $\alpha$. Si el mercado no responde, no pagas nada adicional.  
   * *Ejemplo cotidiano:* Un restaurante que alquila el local contiguo solo si en los primeros seis meses tiene filas de clientes esperando mesa.
3. **Opción de Contracción (Put de escala) [Venegas Sec. 69.5.2]:**
   $$\text{Payoff} = S_T + \max(A - \gamma S_T, \; 0)$$
   * *Explicación:* Si la economía se enfría, reduces tu escala operativa en un porcentaje $\gamma$ y te ahorras un costo fijo $A$.  
   * *Ejemplo cotidiano:* Una empresa de buses intermunicipales que en temporada baja guarda la mitad de la flota en garaje y ahorra gasolina, peajes y mantenimiento.
4. **Opción de Abandono / Liquidación (Put) [Venegas Ec. 69.17]:**
   $$\text{Payoff} = \max(S_T, V) = S_T + \max(V - S_T, \; 0)$$
   * *Explicación:* Si el negocio fracasa ($S_T < V$), liquidas los activos por un valor de rescate $V$ y no te vas a la quiebra. Es un seguro de vida con precio de ejercicio $V$.
5. **Opción de Cambio Operativo (Switching):**
   $$\text{Payoff} = \max\left(S_T^{(1)}, \; S_T^{(2)}\right)$$
   * *Explicación:* Operar con el insumo o producto más rentable según los precios relativos.  
   * *Ejemplo cotidiano:* Un vehículo con motor dual (gasolina y gas vehicular): si la gasolina sube, rueda a gas; si el gas escasea, rueda a gasolina.
6. **Opción Compuesta / Secuencial [Myers 1977]:**
   $$C_1 = \max(C_2 - K_1, \; 0)$$
   * *Explicación:* Desembolsar la inversión inicial $K_1$ compra el derecho a decidir si se realiza la gran inversión comercial $C_2$ en una segunda fase.  
   * *Ejemplo cotidiano:* Crear un prototipo piloto en una sola ciudad antes de arriesgar el patrimonio entero a nivel nacional.

---

## DIAPOSITIVA 5: TIEMPO CONTINUO: BLACK-SCHOLES
* **Contenido Visual:** Ecuación diferencial parcial (EDP) en recuadro destacado, 4 tarjetas de colores desglosando Theta, Gamma, Delta y el costo financiero $r$, y en la parte inferior las 2 limitaciones en activos reales (opciones americanas y supuesto MAD).
* **Tiempo sugerido:** 3.5 minutos.

### 📐 Desglose de la EDP de Black-Scholes (Venegas pág. 806, Ec. 69.22)
* **La Ecuación:**
  $$\frac{\partial c}{\partial t} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 c}{\partial S^2} + r S \frac{\partial c}{\partial S} - r c = 0$$
* **Explicación Matemática y Financiera de los 4 Términos:**
  * $\frac{\partial c}{\partial t}$ **(Theta - Decaimiento Temporal):** El reloj de la opción. A medida que pasa el tiempo ($t \to T$), la opción pierde valor porque queda menos tiempo para que ocurran sorpresas favorables.
  * $\frac{1}{2} \sigma^2 S^2 \frac{\partial^2 c}{\partial S^2}$ **(Gamma - Volatilidad y Convexidad):** El motor de valor. Proviene de la expansión de Taylor de segundo orden (Lema de Itô). Demuestra matemáticamente que la volatilidad $\sigma$ genera valor gracias a la curvatura asimétrica del payoff.
  * $r S \frac{\partial c}{\partial S}$ **(Delta - Deriva Neutral al Riesgo):** La sensibilidad ante cambios en el activo subyacente ajustada por el retorno neutral al riesgo.
  * $- r c$ **(Costo de Oportunidad Financiero):** El descuento temporal del valor de la opción a la tasa libre de riesgo $r$.

### ⚠️ ¿Por qué Black-Scholes no es suficiente para activos reales?
1. **Son Opciones Americanas:** Black-Scholes asume ejercicio únicamente al vencimiento fijo $T$ (estilo europeo). En una empresa, el gerente puede cerrar, pausar o expandir en cualquier día del año ($t \le T$). La fórmula cerrada no permite evaluar el ejercicio anticipado continuo.
2. **Mercados Incompletos y el Supuesto MAD:** En Wall Street, para cubrir una opción compras acciones líquidas en bolsa. Una panadería, una mina o una fábrica no cotizan en bolsa. *Copeland y Antikarov (2001)* resuelven esto con el **Marketed Asset Disclaimer (MAD)**: demuestran que el valor presente del proyecto sin flexibilidad ($S$) es el mejor activo gemelo para replicar el riesgo.

---

## DIAPOSITIVA 6: SOLUCIÓN DISCRETA: ÁRBOL BINOMIAL
* **Contenido Visual:** Diagrama SVG vectorial de ramificación de 1 período ($S \to uS, dS$), 3 tarjetas con factores de subida/bajada $u, d$, probabilidad neutral $q$ e inducción hacia atrás, y banner explicativo inferior.
* **Tiempo sugerido:** 3.5 minutos.

### 📐 Modelo de Cox, Ross y Rubinstein (1979 / Venegas Ec. 69.28)
* **1. Factores de Calibración:**
  $$u = e^{\sigma \sqrt{\Delta t}}, \qquad d = e^{-\sigma \sqrt{\Delta t}} = \frac{1}{u}$$
  * Se calibran de forma que la media y la varianza del árbol discreto converjan exactamente al movimiento browniano geométrico de Black-Scholes cuando el paso de tiempo $\Delta t \to 0$.
* **2. Probabilidad Neutral al Riesgo:**
  $$q = \frac{e^{r \Delta t} - d}{u - d}$$
  * No es la probabilidad subjetiva o histórica de que el negocio crezca. Es una probabilidad matemática sintética bajo la cual todos los activos crecen a la tasa libre de riesgo ($r$ = TES), permitiéndonos descontar flujos futuros con la tasa libre de riesgo sin tener que adivinar una prima de riesgo subjetiva.
* **3. Algoritmo de Inducción Hacia Atrás (Backward Induction):**
  $$C_t = \max\left(E, \; e^{-r \Delta t} [q C_u + (1 - q) C_d]\right)$$
  * *¿Cómo se resuelve?* Como jugar ajedrez hacia atrás: te paras en la fecha final de vencimiento $T$, calculas el payoff en cada nodo terminal, y vienes retrocediendo período por período hasta hoy ($t=0$). En cada nodo intermedio comparas: *"¿Me conviene ejercer hoy y cobrar $E$, o me conviene seguir operando esperando que el negocio mejore?"*.

---

## DIAPOSITIVA 7: CASO EN VIVO: OPCIÓN AMERICANA DE ABANDONO
* **Contenido Visual:** Parámetros didácticos superiores ($S_0=90, I_0=90, V=60, u=2, d=0.5, e^r=4/3, q=5/9$). Diagrama SVG vectorial completo de 3 períodos con todos los nodos de precios $S$ y valores $C$, nodos amarillos de abandono, tarjeta destacada del nodo crítico $t=1$, y métricas finales al pie.
* **Tiempo sugerido:** 5 minutos.

### 📐 El Caso Canónico de Francisco Venegas (págs. 811–813)
* **Parámetros del Proyecto:**
  * Inversión inicial $I_0 = 90$ | Flujos esperados base $S_0 = 90 \implies \text{VPN Estático} = 90 - 90 = 0$.
  * Valor de liquidación contractual (rescate de maquinaria/activos): $V = 60$.
  * Dinámica: $u = 2.0$, $d = 0.5$, tasa libre de riesgo $r = \ln(4/3) \implies e^{-r} = 0.75$, probabilidad neutral $q = 5/9$.

### 🎙️ Tu Discurso en Voz Alta (Explicando el Árbol en Vivo)
* **Tu Discurso:**
  > *"Compañeros y profesor, miren este caso numérico exacto que resuelve el libro de Francisco Venegas.  
  > Una empresa manufacturera requiere una inversión de 90 millones y sus flujos esperados traídos a hoy valen 90 millones. El VPN tradicional es $90 - 90 = 0$; un proyecto estancado en punto muerto neutro.  
  > Pero la empresa negoció una cláusula de salvamento: si las cosas salen mal, puede desmantelar la planta y liquidar los equipos por un valor de rescate garantizado de 60 millones ($V = 60$) en cualquier momento de los próximos 3 años.*  
  > *Miren el árbol en pantalla: en $t=3$, en los dos nodos inferiores ($S=45$ y $S=11.25$), el negocio operando valdría muy poco, pero la empresa ejerce el rescate y cobra 60 (marcados en amarillo).*  
  > *Ahora retrocedamos por inducción hacia atrás y fijémonos en el nodo más importante de toda la exposición: **el nodo inferior en el año 1 ($t=1$)**.*  
  > *Si el mercado cae en el año 1, los flujos del proyecto caen a **$S = 45$ millones**.*  
  > *Si el gerente fuera pasivo y no tuviera opciones, se resignaría a perder y su negocio valdría solo 45.*  
  > *Si decidiera seguir abierto conservando la opción de liquidar en el año 2 o 3, ese camino de continuación vale formalmente:  
  > $$0.75 \left[ \frac{5}{9}(95) + \frac{4}{9}(60) \right] = \mathbf{59.58\text{ millones}}$$*  
  > *Pero en su mano tiene una oferta en firme de liquidar hoy mismo por **60 millones**.*  
  > *El gerente compara: ¿quedarse operando por 59.58 o liquidar hoy y recibir 60 en efectivo?  
  > Como **60 es mayor que 59.58**, la gerencia ejerce el abandono temprano hoy, frena el deterioro y rescata el capital.*  
  > *Cuando descontamos todas las decisiones óptimas nodo a nodo hasta hoy ($t=0$), el proyecto no vale 90 millones: **vale 95.70 millones de dólares**.*  
  > *Restando el valor base sin flexibilidad ($S_0 = 90$), la opción de abandono aporta **más 5.70 millones de dólares netos** ($c_0 = +5.70$).  
  > El VPN pasa de 0 a **+5.70 millones de dólares**. ¡Esa ganancia pura es el valor económico de la flexibilidad directiva!"*

---

## DIAPOSITIVA 8: SÍNTESIS ESTRATÉGICA Y CIERRE
* **Contenido Visual:** Tres tarjetas con las 3 lecciones corporativas clave y banner inferior con la cita inspiradora.
* **Tiempo sugerido:** 2 minutos.

### 🎙️ Tu Discurso de Cierre y Pase a Felipe Pulido
* **Tu Discurso en Voz Alta (Cierre de Julián):**
  > *"Para cerrar esta fundamentación teórica de nuestra clase, quiero que nos llevemos tres principios que transforman la toma de decisiones empresariales:*  
  > *Primero: **La incertidumbre es una fuente de valor**. Si una empresa tiene flexibilidad gerencial, la volatilidad amplía las ganancias potenciales al alza sin agrandar las pérdidas a la baja. La volatilidad deja de ser un enemigo en la tasa de descuento para convertirse en un activo estratégico.*  
  > *Segundo: **Los proyectos deben diseñarse con opcionalidad incorporada**. Como vimos con Tiendas D1, el valor de un negocio no depende solo de cuánto proyecta vender, sino de cómo se estructura la inversión: contratos modulares, plantas escalables y cláusulas de salida.*  
  > *Y tercero: **El VPN se complementa, no se descarta**. El VPN tradicional sigue siendo el punto de partida indispensable; pero cuando hay incertidumbre y margen de maniobra, las opciones reales completan su valor con el rigor de los derivados.*  
  > *Como dice la frase en pantalla: 'El verdadero valor de una empresa reside también en las opciones estratégicas que construye hoy para reinventarse mañana'.*  
  > *Y ahora, para poner a prueba todas estas ecuaciones, mover los parámetros en tiempo real y ver cómo responde el simulador interactivo en la pantalla, **le doy la palabra a mi compañero Felipe Pulido para dar inicio a nuestro laboratorio computacional práctico**.*  
  > *Muchísimas gracias."*
"""

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"Markdown actualizado con éxito en: {md_path}")

    # =========================================================================
    # 2. GENERACIÓN DEL NOTEBOOK JUPYTER SINCRONIZADO
    # =========================================================================
    nb_cells = []

    def add_cell(cell_type, source_text):
        nb_cells.append({
            "cell_type": cell_type,
            "metadata": {},
            "source": [line + "\n" for line in source_text.split("\n")]
        })

    # Header cell
    add_cell("markdown", "# GUÍA MAESTRA Y PLANEACIÓN DE LA EXPOSICIÓN ORAL: OPCIONES REALES\n## Finanzas Descentralizadas 2 — Universidad Externado de Colombia\n**Expositor Teórico:** Julián Duarte | **Expositor Práctico:** Felipe Pulido\n\nEste cuaderno contiene la guía celda a celda de la presentación teórica, los fundamentos matemáticos rigurosos y las explicaciones intuitivas para la clase de mañana.")

    # Diapositiva 0
    add_cell("markdown", "## DIAPOSITIVA 0: PORTADA\n* **Título:** Opciones reales — Finanzas descentralizadas 2\n* **Integrantes:** Julián Duarte & Felipe Pulido\n\n### 🎙️ Guion Oral (Apertura de Julián):\n> *\"Buenos días, profesor y compañeros. Hoy les vamos a presentar la fundamentación teórica y cuantitativa de una de las herramientas más potentes de las finanzas corporativas modernas: las Opciones Reales. Mi nombre es Julián Duarte y voy a estar a cargo de la teoría y el modelado discreto; y al finalizar, mi compañero Felipe Pulido dirigirá nuestro laboratorio práctico computacional interactivo...\"*")

    # Diapositiva 1
    add_cell("markdown", "## DIAPOSITIVA 1: LA FALACIA DEL VPN TRADICIONAL Y EL VPN MODIFICADO\n* **Ecuación:** $\\text{VPN}_{\\text{Modificado}} = \\text{VPN}_{\\text{Estático}} + c$\n* **Idea Central:** El VPN estático asume gerentes pasivos; la realidad corporativa exige adaptación activa.\n\n### 📐 Doble Explicación:\n* **Matemática:** Descuento estándar estático frente al valor no negativo de la opción ($c \\ge 0$).\n* **Financiera sencilla:** El caso de la cafetería de barrio: si calculas comprar maquinaria y arriendo forzoso a 5 años, el VPN da negativo ($-5$M). Pero si arriendas a 1 año con opción de salida, tu pérdida máxima está acotada. Esa flexibilidad vale $15$M, haciendo que el verdadero valor sea $+10$M.")

    # Diapositiva 2
    add_cell("markdown", "## DIAPOSITIVA 2: ¿QUÉ ES UNA OPCIÓN REAL?\n* **Definición Canónica:** Derecho, no obligación, de tomar o modificar decisiones estratégicas sobre activos físicos futuros (Venegas p. 800; Dixit & Pindyck 1994).\n* **Las 3 Condiciones:** Irreversibilidad, Incertidumbre y Flexibilidad temporal.\n\n### 🎙️ Storytelling de Tiendas D1:\n> *\"D1 diseñó su negocio basado en opciones reales: arrienda locales en vez de comprarlos (evita irreversibilidad), no sabe de antemano la demanda del barrio (incertidumbre), y usa estanterías modulares con contratos a 1 año (flexibilidad). Si el punto vende mucho, expande; si no vende, en 24 horas sube los estantes a un camión, cancela el arriendo y abandona perdiendo casi nada. D1 es una máquina de ejecutar opciones reales...\"*")

    # Diapositiva 3
    add_cell("markdown", "## DIAPOSITIVA 3: CORRESPONDENCIA DERIVADOS VS. ACTIVOS REALES\n* **Diccionario de 5 Variables:** $S_t$ (Valor flujos), $K$ (CAPEX), $r$ (TES), $\\sigma$ (Incertidumbre), $T-t$ (Ventana temporal).\n* **La Paradoja de la Volatilidad:**\n  * VPN estático: $\\sigma \\uparrow \\implies \\text{WACC} \\uparrow \\implies \\text{VPN} \\downarrow$.\n  * Opciones Reales: $\\sigma \\uparrow \\implies \\text{Valor} \\uparrow$.\n* **Mecanismo de Convexidad:** Upside ilimitado si el mercado explota favorablemente y Downside acotado a la pérdida máxima si el mercado cae.")

    # Diapositiva 4
    add_cell("markdown", "## DIAPOSITIVA 4: CATÁLOGO DE 6 OPCIONES REALES Y PAYOFFS\n1. **Timing (Dixit & Pindyck):** $S_t - K \\ge C_{\\text{espera}}$ (Esperar nueva información antes de hundir capital).\n2. **Expansión Call (Venegas Ec. 69.7):** $S_T + \\alpha \\max(S_T - K'/\\alpha, 0)$ (Pagar $K'$ para ampliar escala en $\\alpha$).\n3. **Contracción Put (Venegas Sec. 69.5.2):** $S_T + \\max(A - \\gamma S_T, 0)$ (Reducir escala en $\\gamma$ y recuperar ahorro $A$).\n4. **Abandono Put (Venegas Ec. 69.17):** $S_T + \\max(V - S_T, 0) = \\max(S_T, V)$ (Piso de rescate $V$).\n5. **Switching:** $\\max(S_T^{(1)}, S_T^{(2)})$ (Alternar insumos como gas vs fuel-oil según rentabilidad).\n6. **Compuesta (Myers 1977):** $C_1 = \\max(C_2 - K_1, 0)$ (Fase piloto compra derecho a fase comercial).")

    # Diapositiva 5
    add_cell("markdown", "## DIAPOSITIVA 5: TIEMPO CONTINUO: BLACK-SCHOLES\n* **La EDP de Black-Scholes (Venegas pág. 806, Ec. 69.22):**\n  $$\\frac{\\partial c}{\\partial t} + \\frac{1}{2} \\sigma^2 S^2 \\frac{\\partial^2 c}{\\partial S^2} + r S \\frac{\\partial c}{\\partial S} - r c = 0$$\n* **Desglose de Términos:** Theta (tiempo), Gamma (convexidad y volatilidad), Delta (retorno neutral al riesgo) y $-rc$ (costo de financiamiento).\n* **Las 2 Limitaciones en Activos Reales:**\n  1. *Opciones Americanas:* Black-Scholes solo evalúa ejercicio europeo final; los gerentes deciden en cualquier momento $t \\le T$.\n  2. *Mercados Incompletos:* Los proyectos no cotizan en bolsa. Copeland y Antikarov (2001) formulan el **supuesto MAD** (Marketed Asset Disclaimer): usar el VPN estático como activo gemelo.")

    # Diapositiva 6
    add_cell("markdown", "## DIAPOSITIVA 6: SOLUCIÓN DISCRETA: ÁRBOL BINOMIAL\n* **Modelo CRR (Cox, Ross y Rubinstein, 1979 / Venegas Ec. 69.28):**\n  $$u = e^{\\sigma \\sqrt{\\Delta t}}, \\quad d = e^{-\\sigma \\sqrt{\\Delta t}} = \\frac{1}{u}, \\quad q = \\frac{e^{r \\Delta t} - d}{u - d}$$\n* **Inducción Hacia Atrás:** $C_t = \\max(E, e^{-r \\Delta t}[q C_u + (1-q) C_d])$.\n* **Propósito:** Evaluar nodo a nodo la decisión óptima de ejercer anticipadamente frente a continuar operando.")

    # Diapositiva 7
    add_cell("markdown", "## DIAPOSITIVA 7: CASO EN VIVO: OPCIÓN AMERICANA DE ABANDONO\n* **Parámetros de Venegas (págs. 811–813):** $S_0=90, I_0=90, V=60, u=2, d=0.5, e^r=4/3, q=5/9$.\n* **El Nodo Clave en $t=1$ ($S_d = 45$):**\n  * Valor pasivo puro: $S = 45$.\n  * Continuar operando: $0.75 [\\frac{5}{9}(95) + \\frac{4}{9}(60)] = \\mathbf{59.58}$.\n  * Liquidar hoy: $\\mathbf{60.00}$.\n  * **Decisión:** Como $60 > 59.58$, ¡se liquida y abandona de inmediato!\n* **Valor Final:** $C_0 = 95.70 \\implies c_0 = 95.70 - 90 = \\mathbf{+5.70\\text{ MUSD}}$.")

    # Diapositiva 8
    add_cell("markdown", "## DIAPOSITIVA 8: SÍNTESIS ESTRATÉGICA Y CIERRE\n* **3 Principios Directivos:**\n  1. La incertidumbre es fuente de valor bajo flexibilidad gerencial.\n  2. Diseñar proyectos con opcionalidad modular y contractual.\n  3. El VPN se complementa, no se descarta.\n* **Cierre y Transición:**\n  > *\"Y ahora, para poner a prueba estas ecuaciones y ver cómo responde el árbol en tiempo real, le doy la palabra a mi compañero Felipe Pulido para dar inicio al laboratorio práctico computacional. ¡Muchísimas gracias!\"*")

    # Código Python de verificación rápida del árbol
    code_check = r"""# Verificación numérica en vivo del caso de Venegas Martínez (2009, págs. 811-813)
import numpy as np

S0 = 90.0
I0 = 90.0
V = 60.0
u = 2.0
d = 0.5
q = 5.0 / 9.0
df = 0.75 # e^(-r) = 3/4 = 0.75

# Nivel t=3 (Payoff: max(S_3, 60))
c_uuu = max(S0 * (u**3), V)     # 720
c_uud = max(S0 * (u**2) * d, V) # 180
c_udd = max(S0 * u * (d**2), V) # max(45, 60) = 60 (Abandona)
c_ddd = max(S0 * (d**3), V)     # max(11.25, 60) = 60 (Abandona)

# Nivel t=2 (max(Continuación, 60))
c_uu = max(df * (q * c_uuu + (1-q) * c_uud), V) # max(360, 60) = 360
c_ud = max(df * (q * c_uud + (1-q) * c_udd), V) # max(95, 60) = 95
c_dd = max(df * (q * c_udd + (1-q) * c_ddd), V) # max(45, 60) = 60 (Abandona)

# Nivel t=1 (El nodo clave c_d)
c_u = max(df * (q * c_uu + (1-q) * c_ud), V)    # max(181.67, 60) = 181.67
cont_d = df * (q * c_ud + (1-q) * c_dd)          # 0.75 * (5/9*95 + 4/9*60) = 59.58
c_d = max(cont_d, V)                             # max(59.58, 60) = 60 (Abandona)

# Nivel t=0 (Valor hoy con flexibilidad)
C0 = df * (q * c_u + (1-q) * c_d)                # 0.75 * (5/9*181.67 + 4/9*60) = 95.70
c0 = C0 - S0                                     # Prima pura de la opción = +5.70

print(f"=== RESULTADOS NUMÉRICOS EXACTOS ===")
print(f"Valor en t=1 (Continuar): {cont_d:.2f} MUSD vs Liquidar: {V:.2f} MUSD -> Decisión: {c_d:.2f} MUSD")
print(f"Valor del proyecto con opción (C0): {C0:.2f} MUSD")
print(f"Valor puro de la opción de abandono (c0): +{c0:.2f} MUSD")
"""
    add_cell("code", code_check)

    notebook_dict = {
        "cells": nb_cells,
        "metadata": {
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    with open(ipynb_path, 'w', encoding='utf-8') as f:
        json.dump(notebook_dict, f, indent=2, ensure_ascii=False)
    print(f"Notebook actualizado con éxito en: {ipynb_path}")

if __name__ == '__main__':
    build_presentation_suite()
