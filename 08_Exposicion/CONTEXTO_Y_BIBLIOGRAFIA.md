# Marco Teórico, Contexto y Bibliografía Oficial: Opciones Reales

**Asignatura:** Valoración de Activos (DEFI 2)  
**Institución:** Universidad Externado de Colombia  
**Tema:** Opciones Reales (*Real Options Valuation - ROV*)  
**Fecha de preparación:** Noviembre de 2026  

---

## 1. Fuentes Bibliográficas Rigurosas (Sin Invenciones)

Toda la información teórica, conceptual y matemática de esta exposición proviene estrictamente de la literatura económica y financiera de referencia disponible en el curso:

1. **Fuente Principal del Curso:**
   * **Venegas Martínez, Francisco (2009).** *Riesgos Financieros y Económicos: Productos Derivados y Decisiones Económicas bajo Incertidumbre*. 2.ª edición. México: Cengage Learning / Alfaomega.
     * **Capítulo 69:** *"Opciones reales, valuación financiera de proyectos de inversión y estrategias de negocios"*, páginas 800–816.
     * Libro oficial disponible en el repositorio: `01_Libros_y_Lecturas/Libros/Francisco Venegas Martinez - Riesgos Financieros y Economicos (2009).pdf`.

2. **Obras Fundacionales Complementarias:**
   * **Myers, Stewart C. (1977).** *"Determinants of Corporate Borrowing"*. *Journal of Financial Economics*, 5(2), págs. 147–175. *(Artículo pionero donde se acuña por primera vez el término "Real Options" al reconocer que las oportunidades de crecimiento empresarial son equivalentes a opciones de compra sobre activos reales).*
   * **Dixit, Avinash K., & Pindyck, Robert S. (1994).** *Investment under Uncertainty*. Princeton, NJ: Princeton University Press. *(Obra canónica que formalizó la teoría microeconómica del comportamiento de inversión bajo irreversibilidad e incertidumbre estocástica).*
   * **Trigeorgis, Lenos (1996).** *Real Options: Managerial Flexibility and Strategy in Resource Allocation*. Cambridge, MA: The MIT Press. *(Texto canónico de taxonomía y valoración de flexibilidad gerencial).*
   * **Cox, John C., Ross, Stephen A., & Rubinstein, Mark (1979).** *"Option Pricing: A Simplified Approach"*. *Journal of Financial Economics*, 7(3), págs. 229–263. *(Modelo binomial discreto que fundamenta la valuación de opciones americanas en finanzas cuantitativas).*
   * **Copeland, Tom, & Antikarov, Vladimir (2001).** *Real Options: A Practitioner's Guide*. Texere. *(Introducción del supuesto MAD - Marketed Asset Disclaimer para resolver la valuación bajo mercados incompletos).*
   * **Hull, John C. (2012).** *Options, Futures, and Other Derivatives*. 8.ª edición. Boston: Prentice Hall / Pearson. *(Capítulo sobre Opciones Reales y valoración de proyectos de materias primas y energía).*

---

## 2. Definición Formal y Justificación Teórica

### 2.1 La Crisis del Valor Presente Neto (VPN) Tradicional
De acuerdo con **Venegas Martínez (2009, pág. 800)**:
> *"Con el criterio del valor presente neto (VPN), un nuevo proyecto o estrategia se acepta o se rechaza hoy, si $\text{VPN} > 0$ o $\text{VPN} < 0$, respectivamente, y no existe otra posibilidad. Una vez que un proyecto es aceptado con este criterio, rígido y pasivo, los planes de inversión no se modifican, es decir, la inversión es irreversible.*  
> *Por otro lado, bajo el criterio del VPN, no se puede valuar, hoy, la posibilidad de que si el entorno de negocios y el ambiente económico son favorables dentro de cinco años un proyecto o estrategia se expanda. Simplemente, porque hoy no se sabe si en el futuro se tendrán o no condiciones favorables para tomar esta nueva decisión."*

### 2.2 El Valor Presente Neto Modificado / Ampliado (Expanded NPV)
Para incorporar el valor de la flexibilidad gerencial (la capacidad de la dirección de reaccionar en el futuro a medida que se resuelve la incertidumbre), se define el **VPN Modificado** (**Venegas Martínez, pág. 801, Ecuación 69.1**; **Trigeorgis, 1996**):

$$\text{VPN}_{\text{modificado}} = \text{VPN}_{\text{estático}} + c \tag{69.1}$$

Donde:
* $\text{VPN}_{\text{estático}}$: Valor presente neto convencional obtenido mediante el descuento de flujos de efectivo esperados a una tasa de costo de capital (WACC) constante, asumiendo una gestión pasiva.
* $c$: Valor presente de la opción real (prima de flexibilidad directiva para posponer, expandir, contraer, suspender o abandonar el proyecto).

**Consecuencia económica clave:** Un proyecto que el VPN tradicional rechazaría ($\text{VPN}_{\text{estático}} < 0$) puede resultar viable y económicamente rentable si la opcionalidad futura tiene un valor superior al déficit inicial, es decir, si:
$$\text{VPN}_{\text{estático}} + c > 0$$

---

## 3. Correspondencia Formal: Opciones Financieras vs. Opciones Reales

En el **Cuadro 69.1 de Venegas Martínez (2009, pág. 802)** se formaliza el mapeo analítico entre los parámetros de un derivado financiero y los de un proyecto de inversión en activos reales:

| Parámetro Clásico | Opción Financiera (Call sobre Acción) | Opción Real sobre Proyecto de Inversión |
| :---: | :--- | :--- |
| **$S_t$** | Precio del activo subyacente en el tiempo $t$ | **Valor presente de los flujos de efectivo esperados del proyecto en $t$** |
| **$K$** | Precio de ejercicio (*Strike*) | **Costo de desembolso de la inversión requerida en $T$** |
| **$r$** | Tasa de interés libre de riesgo | **Tasa de interés libre de riesgo** |
| **$\sigma$** | Volatilidad instantánea de los rendimientos del subyacente | **Volatilidad de los flujos de efectivo generados por el proyecto** |
| **$T - t$** | Tiempo restante hasta el vencimiento del contrato | **Ventana de tiempo en la cual la oportunidad de invertir o decidir desaparece** |

---

## 4. Taxonomía de Opciones Reales y Ecuaciones de Payoff

Según la clasificación de **Venegas Martínez (2009, Sección 69.5)** y **Trigeorgis (1996)**, existen diversas tipologías de opciones según la decisión gerencial disponible:

### 4.1 Opción de Expansión (Call)
Permite incrementar la escala del proyecto en un factor $\alpha$ desembolsando una inversión adicional $K'$ en el tiempo $T$.
* **Valor intrínseco (Venegas Martínez, pág. 803, Ecuación 69.7):**
  $$c_e(S_T, T; \alpha, K') = \max\left( (1 + \alpha)S_T - K', \; S_T \right) = S_T + \alpha \max\left(S_T - \frac{K'}{\alpha}, \; 0\right)$$
  Equivale al valor del proyecto base $S_T$ más $\alpha$ opciones de compra (*calls*) europeas con precio de ejercicio $K = K'/\alpha$.

### 4.2 Opción de Abandono (Put)
Permite a la gerencia vender los activos o liquidar el negocio en el tiempo $T$ recibiendo un valor de rescate o valor de recuperación fijo $V_T = K$.
* **Valor intrínseco (Venegas Martínez, pág. 805, Ecuación 69.17):**
  $$c_a(S_T, T) = \max(S_T, V_T) = \max(S_T - K, 0) + K$$
  Por paridad Put-Call, esto equivale a tener el flujo del proyecto más una opción de venta (*put*) de suelo de valor:
  $$\max(S_T, K) = S_T + \max(K - S_T, 0)$$

### 4.3 Opción de Posponer o Esperar (Timing Option / Call)
Permite diferir el inicio del proyecto de $t=0$ a un momento futuro $t=1, \dots, T$ para recopilar más información sobre el mercado, la demanda o los precios de los productos (Venegas Martínez, pág. 802).

### 4.4 Opciones Reales Compuestas (Staged Investment / Inversión por Etapas)
Común en proyectos de Investigación y Desarrollo (I+D), patentes farmacéuticas y exploración de hidrocarburos. La inversión en la fase 1 otorga el derecho (no la obligación) de realizar la fase 2 (Venegas Martínez, pág. 806, Sección 69.5.7).

---

## 5. Modelación Matemática y Métodos de Valuación

### 5.1 Enfoque Continuo: Ecuación Diferencial Parcial (EDP)
Bajo el supuesto de que el valor presente de los flujos sigue un **Movimiento Geométrico Browniano neutral al riesgo**:
$$dS_t = r S_t dt + \sigma S_t dW_t \tag{69.8}$$

Por argumentos de no arbitraje y el Lema de Itô, el valor de la opción real $c(S, t)$ satisface la EDP determinista de Black-Scholes (**Venegas Martínez, pág. 808, Ecuación 69.22**):
$$\frac{\partial c}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 c}{\partial S^2} + r S \frac{\partial c}{\partial S} - rc = 0 \tag{69.22}$$
Sujeta a la condición terminal $c(S, T) = h(S_T)$, donde $h(\cdot)$ es la función de pago de la opción real.

> ⚠️ **Advertencia fundamental del libro sobre Mercados Incompletos (Venegas Martínez, pág. 804):**  
> *"Es importante destacar que los flujos de efectivo esperados no son un activo que se compre o venda en el mercado, lo que genera una situación de mercados incompletos. Por lo tanto, los resultados que arroja la fórmula de Black-Scholes hay que tomarlos con cierta reserva."*

### 5.2 Enfoque Discreto: Árbol Binomial de Cox-Ross-Rubinstein (CRR)
Dado que la mayoría de las opciones reales son de tipo **americano** (pueden ejercerse en cualquier instante antes del vencimiento) y enfrentan mercados incompletos, el **método de árboles binomiales** es el estándar predilecto (**Venegas Martínez, Sección 69.7, págs. 808–813**).

* **Parámetros del árbol:**
  $$u = e^{\sigma \sqrt{\Delta t}}, \quad d = e^{-\sigma \sqrt{\Delta t}} = \frac{1}{u}$$
* **Probabilidad neutral al riesgo (Ecuación 69.28):**
  $$q = \frac{e^{r \Delta t} - d}{u - d}$$
* **Inducción hacia atrás (Backward Induction):**
  En cada nodo intermedio $(i, j)$ en el tiempo $t$:
  $$c_{i,j} = \max\left( \text{Valor de Ejercicio Inmediato}, \; e^{-r \Delta t} \left[ q c_{i+1, j+1} + (1-q) c_{i+1, j} \right] \right)$$

---

## 6. Caso Numérico Exacto del Libro: Opción Americana de Abandono

En la **Sección 69.8 de Venegas Martínez (págs. 811–813)** se presenta un ejemplo resuelto completo que utilizaremos en la exposición:

* **Parámetros del proyecto:**
  * Valor presente inicial de los flujos: $S_0 = 90$ millones.
  * Inversión inicial: $I_0 = 90$ millones.
  * Valor de recuperación / rescate constante: $V = 60$ millones.
  * Horizonte: $T = 3$ años ($\Delta t = 1$).
  * Factores del árbol: $u = 2$, $d = 0.5$.
  * Tasa de interés continua: $r = \ln(4/3) \approx 0.287682 \dots$ (en el texto pág. 811 define $e^{r} = 4/3 \approx 1.3333$).
  * Probabilidades neutrales al riesgo:
    $$q = \frac{e^r - d}{u - d} = \frac{4/3 - 1/2}{2 - 1/2} = \frac{5/6}{3/2} = \frac{5}{9} \approx 0.5556, \quad 1-q = \frac{4}{9} \approx 0.4444$$
  * Factor de descuento: $e^{-r} = 3/4 = 0.75$.

* **Resultados numéricos del árbol (Venegas, págs. 811–812):**
  * Nodos en $t=3$:
    * $S_{uuu} = 90 \times 8 = 720 \implies c_{uuu} = \max(720, 60) = 720$
    * $S_{uud} = 90 \times 2 = 180 \implies c_{uud} = \max(180, 60) = 180$
    * $S_{udd} = 90 \times 0.5 = 45 \implies c_{udd} = \max(45, 60) = 60$ *(¡se ejerce abandono!)*
    * $S_{ddd} = 90 \times 0.125 = 11.25 \implies c_{ddd} = \max(11.25, 60) = 60$ *(¡se ejerce abandono!)*
  * Nodos en $t=2$:
    * $c_{uu} = \max\left(e^{-r}[q(720) + (1-q)(180)], 60\right) = \max\left(\frac{3}{4}\left[\frac{5}{9}(720) + \frac{4}{9}(180)\right], 60\right) = \max(360, 60) = 360$
    * $c_{ud} = \max\left(\frac{3}{4}\left[\frac{5}{9}(180) + \frac{4}{9}(60)\right], 60\right) = \max\left(\frac{3}{4}[100 + 26.67], 60\right) = \max(95, 60) = 95$
    * $c_{dd} = \max\left(\frac{3}{4}\left[\frac{5}{9}(60) + \frac{4}{9}(60)\right], 60\right) = \max(45, 60) = 60$ *(¡se ejerce abandono temprano!)*
  * Nodos en $t=1$:
    * $c_u = \max\left(\frac{3}{4}\left[\frac{5}{9}(360) + \frac{4}{9}(95)\right], 60\right) = \max\left(\frac{3}{4}[200 + 42.22], 60\right) = \max(181.67, 60) = 181.67$
    * $c_d = \max\left(\frac{3}{4}\left[\frac{5}{9}(95) + \frac{4}{9}(60)\right], 60\right) = \max\left(\frac{3}{4}[52.78 + 26.67], 60\right) = \max(59.58, 60) = 60$ *(¡se ejerce abandono temprano en $t=1$!)*
  * Nodo inicial en $t=0$:
    * $c_0 = \max\left(\frac{3}{4}\left[\frac{5}{9}(181.67) + \frac{4}{9}(60)\right], 60\right) = \max\left(\frac{3}{4}[100.93 + 26.67], 60\right) = \max(95.70, 60) = 95.70$

* **Conclusión Financiera:**
  El valor del proyecto con la opción de abandono es de **95.70 millones**. Sin la opción de abandono, el valor esperado pasivo descontado sería estrictamente inferior (o el proyecto quebraría en los estados adversos). La opción real de abandono añade un colchón de seguridad de más de **5.70 millones** por encima de la inversión inicial de 90.

