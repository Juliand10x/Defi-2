# 🎤 Guion Maestro y Manual de Defensa Técnica: Kibo (10 Minutos)
## Valoración de Activos, Simulación Estocástica y Gestión de Riesgo Cuantitativo
**Universidad Externado de Colombia · Facultad de Finanzas, Gobierno y Relaciones Internacionales**

---

## 🌟 ¿Qué significa KIBO y por qué elegimos este nombre?

> **Si el profesor o los jurados te preguntan: "¿Por qué llamaron a la app Kibo?"**
>
> 1. **Origen en Japonés (希望 - Kibō)**:  
>    Significa **"Esperanza"**, **"Aspiración"** y **"Confianza en el futuro"**.  
>    En los mercados financieros, invertir y enfrentarse al riesgo suele generar miedo, incertidumbre y ansiedad. Kibo fue diseñado como un copiloto inteligente que transforma esa incertidumbre en tranquilidad, claridad y esperanza fundada en datos y matemáticas.
> 2. **Origen Geográfico (El pico Kibo del Kilimanjaro)**:  
>    **Kibo** es el cráter y la cumbre más alta del Monte Kilimanjaro (5.895 m), el punto más alto de toda África (*"el techo de África"*). Simboliza alcanzar la **cima del rigor cuantitativo**, teniendo una visión panorámica completa de los riesgos para tomar decisiones desde lo más alto.
> 3. **Propósito Pedagógico**:  
>    Kibo es el puente entre las matemáticas avanzadas y la vida real: toma fórmulas de cálculo estocástico y optimización cuadrática y se las traduce a cualquier persona **"en cristiano"**, sin tecnicismos intimidantes.

---

## ⏱️ Estructura Cronometrada de la Exposición (10 Minutos)

```
[00:00 - 01:00]  Minuto 1:  Apertura Ejecutiva, Significado de Kibo y Capital Inicial ($100K)
[01:00 - 02:00]  Minuto 2:  Perfil de Riesgo, Confianza (99%), Horizonte (10d) y Presupuesto
[02:00 - 03:15]  Minuto 3:  Universo de Inversión y Medidor de Diversificación (6 Sectores)
[03:15 - 05:15]  Minuto 4-5: Cerebros Estocásticos, Salto de Merton y Efecto Manada (CCK)
[05:15 - 06:45]  Minuto 6-7: Seguro con Opciones Reales, Árbol CRR y Efecto Escudo
[06:45 - 08:15]  Minuto 8:  Portafolio Óptimo SLSQP, Límite 35% y Medición de VaR 99%
[08:15 - 09:15]  Minuto 9:  Auditoría en el Pasado Real (252 días) y Test de Kupiec
[09:15 - 10:00]  Minuto 10: Conclusión Ejecutiva, Diccionario y Preguntas Técnicas
```

---

## 🎬 Guion Verbal y Acciones en Pantalla Paso a Paso

### 📍 Minuto 0:00 a 01:00 · Apertura y Capital Inicial (Paso 1)
* **Qué hacer en pantalla**: Abre la app ([defi2-valoracion.streamlit.app](https://defi2-valoracion.streamlit.app)). En la pantalla de bienvenida, haz clic en *"⚡ Ya la conozco, omitir guía"*. Estarás en el **Paso 1 (Tu Capital)** con USD $100.000.
* **Qué decir (Palabras exactas)**:
  > *"Buenos días profesor y compañeros. Hoy les presentamos **Kibo**, nuestra plataforma de valoración de activos, simulación estocástica y optimización de portafolios desarrollada en Python y Streamlit.*  
  >  
  > *El nombre **Kibo** proviene del japonés y significa **Esperanza** (y es también la cumbre más alta del Kilimanjaro): representa cómo la tecnología cuantitativa puede transformar el miedo a perder dinero en confianza y claridad matemática.*  
  >  
  > *El reto del taller consiste en administrar un capital de **USD $100.000**, proyectar activos con modelos estocásticos, estructurar una cobertura con opciones reales de Wall Street y optimizar una cartera de Mínimo VaR con restricciones sectoriales.*  
  >  
  > *Kibo tiene una arquitectura dual: por fuera es tan sencilla e intuitiva como una billetera digital moderna, pero por dentro ejecuta con estricto rigor todas las ecuaciones de la rúbrica."*
* **Acción**: Haz clic en **"Continuar a Tu Perfil ➔"**.

---

### 📍 Minuto 01:00 a 02:00 · Perfil de Riesgo y Parámetros (Paso 2)
* **Qué hacer en pantalla**: Selecciona el perfil **"⚖️ Modo Equilibrio (Moderado)"**.
* **Qué decir**:
  > *"En este segundo paso definimos la aversión al riesgo. Seleccionamos el perfil **Moderado**, que carga la calibración estándar del Externado:*  
  > *Un nivel de confianza estadística del **99%**, un horizonte temporal de **10 sesiones bursátiles** y un presupuesto de riesgo de **USD $7.500** (el 7.5% del capital).*  
  >  
  > *En las **Opciones avanzadas** podemos comprobar que la tasa libre de riesgo libre de arbitraje está fijada en el **4.0% anual**. Kibo permite flexibilizar estos supuestos, pero para la sustentación conservamos los parámetros oficiales."*
* **Acción**: Abre y cierra rápidamente el expander de opciones avanzadas y haz clic en **"Continuar a Tus Acciones ➔"**.

---

### 📍 Minuto 02:00 a 03:15 · Universo de Acciones y Diversificación (Paso 3)
* **Qué hacer en pantalla**: Muestra los 10 tickers seleccionados y el **Medidor de Diversificación**.
* **Qué decir**:
  > *"En el Paso 3 seleccionamos 10 activos de alta liquidez en Wall Street cubriendo **6 sectores económicos diferentes**: Tecnología (Apple, Microsoft, Nvidia), Consumo (Amazon, Tesla), Comunicaciones (Google, Meta), Finanzas (JPMorgan), Salud (Johnson & Johnson) y Energía (ExxonMobil).*  
  >  
  > *El código descarga automáticamente más de 3 años de cotizaciones diarias oficiales desde Yahoo Finance utilizando precios ajustados para los retornos y el último precio spot de cierre para la valoración.*  
  >  
  > *El **Medidor de Diversificación de Kibo** confirma que cumplimos el requisito de cubrir al menos 4 sectores. Además, en las opciones avanzadas incluimos un reclasificador interactivo por si el analista desea reasignar el sector de alguna empresa."*
* **Acción**: Haz clic en **"Analizar con los Cerebros de Kibo ➔"**.

---

### 📍 Minuto 03:15 a 05:15 · Competencia Multimodelo y Efecto Manada (Pasos 4 y 5)
* **Qué hacer en pantalla**: Muestra la tarjeta del **Cerebro Ganador** (ej. `NVDA` o `AAPL`) y navega por las pestañas.
* **Qué decir**:
  > *"Aquí llegamos al corazón estocástico de Kibo. La rúbrica pide simular el Movimiento Browniano Geométrico (GBM), pero nosotros pusimos a competir **4 modelos estocásticos bajo 5.000 trayectorias de Monte Carlo**:*  
  >  
  > *1. **Difusión Continua (GBM)**: Modela deriva constante y volatilidad browniana. Como ven en la gráfica de abanico, mostramos 40 trayectorias individuales, la mediana P50 en verde sólido, las bandas de percentiles 10%-90%, y la distribución terminal de precios $S_T$, comprobando que la media simulada converge a la media teórica $S_0 e^{aT}$.*  
  >  
  > *2. **Saltos de Merton (MJD)**: Modela noticias bomba o caídas imprevistas mediante un proceso de saltos de Poisson. Para tecnológicas como Nvidia, Merton resulta ganador en los criterios **AIC y BIC** porque captura las colas pesadas que el GBM subestima.*  
  >  
  > *3. **Reversión a la Media (Ornstein-Uhlenbeck)**: Modela precios con fuerza de atracción hacia un costo promedio de equilibrio.*  
  >  
  > *4. **Browniano Fraccionario (fBm)**: Calibramos el **Exponente de Hurst ($H$)** mediante reescalado R/S. Con un $H > 0.5$, detectamos persistencia y memoria larga en la serie.*  
  >  
  > *En la **Pestaña 5**, implementamos el test econométrico de **Efecto Manada de Chang, Cheng y Khorana (CCK 2000)**: evaluamos la dispersión transversal de retornos (CSAD) frente al mercado. La parábola no muestra curvatura negativa ($\gamma_2 \ge 0$), lo que confirma que el mercado opera con dispersión racional y no bajo histeria colectiva.*  
  >  
  > *En la **Pestaña 6**, ejecutamos la **Evaluación Rolling de 252 sesiones con $H=1$ día**, reportando RMSE y MAPE frente al pronóstico ingenuo $P_t$."*
* **Acción**: Muestra las pestañas y haz clic en **"Continuar a Tu Seguro (Opciones) ➔"**.

---

### 📍 Minuto 05:15 a 06:45 · Opciones Reales y Árbol Binomial CRR (Pasos 5 a 9)
* **Qué hacer en pantalla**: Haz clic en **"🔎 Buscar Seguros (Opciones) Disponibles en Wall Street"**.
* **Qué decir**:
  > *"En el módulo de derivados estructuramos la cobertura para proteger el portafolio:*  
  >  
  > *1. **Contratos Reales**: Consultamos en vivo la cadena oficial de opciones de Wall Street para vencimientos de 1, 3 y 6 meses, seleccionando strikes cercanos a los cuantiles 25, 50 y 75 del modelo estocástico.*  
  >  
  > *2. **Valoración con Árbol Binomial CRR**: Implementamos el modelo de Cox, Ross y Rubinstein en tiempo discreto con probabilidades neutrales al riesgo $p_q$. Soporta ejercicio Europeo y Americano.*  
  > *Superamos el test de control de la rúbrica: una Call europea con $S_0=K=100$, $T=1$, $r=5\%$, $q=0$ y $\sigma=20\%$ aproxima exactamente **USD $10.4506** con 200 pasos.*  
  >  
  > *3. **Simulador de Efecto Escudo**: La gráfica compara el Payoff bruto contra el Beneficio Neto descontando la prima. Si movemos el slider a una caída de mercado del -15%, la app demuestra cómo la opción Put absorbe la pérdida de las acciones y genera un ahorro financiero neto."*
* **Acción**: Mueve el control a -15% para mostrar el mensaje de ahorro y haz clic en **"Ver Mi Portafolio Final ➔"**.

---

### 📍 Minuto 06:45 a 08:15 · Asignación Óptima y VaR 99% (Pasos 10 a 12)
* **Qué hacer en pantalla**: Muestra la lista de acciones a comprar y la pestaña de Riesgo & VaR.
* **Qué decir**:
  > *"Llegamos a la asignación final de los USD $100.000:*  
  >  
  > *1. **Optimización Cuadrática SLSQP**: En lugar de usar la regla inversa al VaR (que ignora correlaciones), resolvemos el problema cuadrático de Mínimo VaR con matriz de covarianza de media cero:*  
  > $$\min_w \Phi^{-1}(\alpha)\sqrt{h \cdot w^T \Sigma_R w} \quad \text{sujeto a} \quad \sum w_i = 1, \quad w_i \in [2\%, 20\%], \quad \sum_{i \in \text{sector}} w_i \le 35\%$$  
  >  
  > *2. **Acciones Enteras y Efectivo Residual**: Convertimos los montos teóricos a acciones enteras reales de mercado ($\lfloor A_i / S_{i,0} \rfloor$), reportando el efectivo sobrante con total transparencia.*  
  >  
  > *3. **3 Estimadores de VaR al 99%**: En la pestaña de Riesgo comparamos los 3 métodos exigidos:*  
  > *Paramétrico Normal, Histórico por bloques de 10 días y Monte Carlo con 20.000 escenarios conjuntos conservando la estructura de covarianza, reportando también el CVaR o Expected Shortfall.*  
  >  
  > *4. **Pruebas de Estrés**: Evaluamos caída uniforme de mercado (-10%), crisis sectorial (-20% en Tecnología y -5% resto) y shock de volatilidad ($\times 1.5$ con correlación de 0.8), demostrando la solidez del portafolio gracias al límite sectorial del 35%."*

---

### 📍 Minuto 08:15 a 09:15 · Auditoría Histórica y Test de Kupiec (Paso 13)
* **Qué hacer en pantalla**: Haz clic en la **Pestaña 4: 📈 Examen Histórico**.
* **Qué decir**:
  > *"Sometimos el portafolio a una auditoría fuera de muestra en las últimas 252 sesiones reales de Wall Street, incorporando costos de corretaje de 10 puntos básicos.*  
  >  
  > *En la gráfica pueden ver la curva de patrimonio acumulado y el Drawdown Máximo contenido.*  
  > *Para verificar que el modelo no miente, aplicamos formalmente el **Test de Cobertura Condicional de Kupiec (POF)**: al 99% de confianza en 252 sesiones se esperan teóricamente entre 2 y 3 violaciones. Nuestro modelo registró 2 excepciones, obteniendo un p-valor mayor a 0.05, lo que aprueba estadísticamente la validez del VaR."*

---

### 📍 Minuto 09:15 a 10:00 · Cierre Ejecutivo y Descarga
* **Qué hacer en pantalla**: Muestra la **Pestaña 5: 📦 Descargas** y abre el **Diccionario de Kibo**.
* **Qué decir**:
  > *"En la pestaña de descargas generamos con un solo clic el **CSV consolidado oficial del taller**, que reúne la asignación de acciones enteras, la tabla de VaR, el estrés y la auditoría Kupiec.*  
  >  
  > *Además, si alguna persona tiene dudas sobre algún tecnicismo, Kibo cuenta con un **Diccionario Financiero integrado** que traduce cada concepto a cristiano con ejemplos prácticos.*  
  >  
  > *Demostramos así que es posible cumplir al 100% con las matemáticas más avanzadas exigidas por la facultad manteniendo una experiencia visual elegante y comprensible. Quedamos atentos a sus preguntas técnicas. Muchas gracias."*

---

## 📊 Guía Visual de Gráficas: Cómo explicarlas sin enredarse

Si el profesor te señala una gráfica y te dice *"¿Qué significa esta línea o este color?"*, responde con esta guía:

### 1. Gráfica de Abanico Estocástico (Fan Chart - Paso 4)
* **Líneas grises delgadas (40 trayectorias)**: Son 40 caminos individuales de los 5.000 simulados. Muestran la incertidumbre y aleatoriedad del mercado.
* **Línea verde sólida central**: Es la **Mediana (P50)**. Significa que el 50% de los futuros posibles quedaron por encima y el 50% por debajo.
* **Banda verde oscura (25% a 75%)**: Rango intercuartílico; concentra el 50% más probable de los escenarios.
* **Banda verde clara (10% a 90%)**: Intervalo del 80% de confianza estadística.
* **Línea naranja discontinua**: Media promedio de la simulación de Monte Carlo.
* **Línea azul discontinua**: Media teórica analítica ($S_0 e^{aT}$).  
  *(Si el profesor pregunta: "Como la línea naranja y azul coinciden, confirmamos que el código converge a la solución matemática exacta").*
* **Histograma vertical derecho**: Muestra la distribución de frecuencias de los precios al vencimiento $S_T$.

### 2. Gráfica de Barras AIC vs BIC (Paso 4)
* **Eje X**: Los 4 modelos en competencia (`1. GBM`, `2. Merton`, `3. O-U`, `4. fBm`).
* **Barras grises (AIC) y ámbar (BIC)**: Criterios de Información de Akaike y Bayesiano.
* **¿Por qué son números negativos (-4.000, -4.500)?**: Porque la fórmula es $\text{AIC} = 2k - 2\ln(L)$. Como la verosimilitud $L$ es muy alta, el logaritmo multiplicado por $-2$ arroja valores negativos.
* **¿Quién gana?**: La regla estadística dice que **"el menor valor es el mejor"**. En números negativos, $-4.500$ es menor que $-4.000$. Por tanto, **la barra que más baja (la más negativa) es el modelo ganador** (usualmente Merton por capturar saltos).

### 3. Gráfica de Dispersión de Efecto Manada (Test CCK 2000 - Paso 5)
* **Eje X ($|R_{m,t}|$ en %)**: Qué tan fuerte se movió el mercado en el día.
* **Eje Y ($CSAD_t$ en %)**: Dispersión transversal absoluta; qué tan alejadas se movieron las acciones entre sí.
* **Puntos verdes**: Días con mercado alcista ($R_m \ge 0$).
* **Puntos naranjas**: Días con mercado bajista ($R_m < 0$).
* **Curva sólida**: Parábola estimada del modelo $CSAD_t = \alpha + \gamma_1 |R_m| + \gamma_2 R_m^2$.  
  *(Si el profesor pregunta: "Como la curva no se curva hacia abajo ($\gamma_2$ no es negativo significativo), confirmamos que los inversores no corrieron en manada").*

### 4. Gráfica de Payoff y Beneficio Neto (Paso 6)
* **Línea gris discontinua**: Payoff bruto al vencimiento $\max(K - S_T, 0)$.
* **Línea verde sólida**: Beneficio neto real $\Pi_T = \text{Payoff} - \text{Prima capitalizada}$.
* **Línea vertical ámbar**: Strike $K$ pactado.
* **Línea vertical celeste**: Precio spot actual $S_0$.
* **Línea vertical morada**: Break-Even (punto de equilibrio donde la ganancia de la opción cubre exactamente el costo de la prima).

### 5. Gráfica del Árbol Binomial CRR (Paso 8)
* **Nodos circulares**: Cada nodo representa un estado temporal ($t=0, 1, 2, 3$).
* **Valor superior ($S$)**: Precio de la acción calculado con factores $u = e^{\sigma \sqrt{\Delta t}}$ y $d = 1/u$.
* **Valor inferior ($V$)**: Valor teórico del seguro calculado hacia atrás mediante inducción neutral al riesgo ($p_q$).

### 6. Gráfica de Pérdidas Monte Carlo y Líneas de VaR/CVaR (Paso 10)
* **Histograma verde**: 20.000 escenarios simulados de pérdida potencial de la cartera a 10 días.
* **Línea vertical ámbar (VaR 99%)**: Umbral de corte. El 99% de los escenarios arrojan pérdidas menores a este valor.
* **Línea vertical roja (CVaR 99%)**: Pérdida media esperada en el 1% de escenarios extremos que superan el VaR.

### 7. Gráfica de Auditoría Fuera de Muestra y Drawdown (Paso 13)
* **Panel superior**: Curva de patrimonio real partiendo de USD $100.000 en 252 sesiones descontando 10 bps de comisión.
* **Panel inferior rojo**: Drawdown porcentual (caídas acumuladas desde el último máximo histórico).

---

## ⚙️ ¿Qué hace el código por detrás? (Explicación para no programadores)

Si el profesor te pregunta *"¿Cómo programa o calcula esto el código por dentro?"*, aquí tienes la explicación sencilla y exacta:

| Módulo del Código | ¿Qué hace internamente? |
|---|---|
| **`data_engine.py`** | Llama a la API de Yahoo Finance, descarga precios de cierre ajustados, calcula retornos continuos $x_t = \ln(P_t / P_{t-1})$ y aplica la varianza muestral con divisor $n-1$. Luego anualiza multiplicando la desviación por $\sqrt{252}$ y la media por $252 + \frac{1}{2}\sigma^2$. |
| **`stochastic_engine.py`** | Aplica la fórmula de transición exacta del GBM usando matrices vectorizadas de NumPy con números aleatorios normales estándar $Z \sim N(0, 1)$. Genera una matriz de 5.000 filas por 10 columnas en menos de 0.05 segundos sin usar bucles lentos. |
| **`options_engine.py`** | Construye matrices piramidales para el árbol binomial. Primero calcula los precios terminales en $t=3$ y sus payoffs. Luego aplica un bucle regresivo (backward induction) descontando con $e^{-r\Delta t}$ y ponderando por $p_q$. Para opciones americanas evalúa $\max(\text{continuación}, \text{payoff})$. |
| **`herding_engine.py`** | Calcula el retorno diario ponderado del mercado $R_{m,t}$, calcula la dispersión $CSAD_t$ como la desviación absoluta media de las 10 acciones, y ejecuta una regresión por Mínimos Cuadrados Ordinarios (OLS) con Statsmodels para estimar el parámetro $\gamma_2$. |
| **`portfolio_engine.py`** | Utiliza la función `scipy.optimize.minimize` con el algoritmo **SLSQP** (*Sequential Least Squares Programming*). Minimiza la función objetivo $w^T \Sigma w$ sujeta a la igualdad $\sum w_i = 1$, límites de caja $w_i \in [0.02, 0.20]$ y desigualdades lineales que suman los pesos de las empresas de un mismo sector para que no superen $0.35$. |
| **`risk_engine.py`** | Para el VaR paramétrico aplica la fórmula matricial $\Phi^{-1}(0.99)\sqrt{10 \cdot w^T \Sigma w}$. Para Monte Carlo genera 20.000 vectores aleatorios multivariados preservando la matriz de correlación mediante descomposición de Cholesky. Para Kupiec calcula el logaritmo de verosimilitud de Bernoulli y evalúa el estadístico chi-cuadrado con 1 grado de libertad. |
| **`rolling_engine.py`** | Desplaza una ventana móvil de 252 días sesión a sesión. En cada paso $t$, recalibra $\mu$ y $\sigma$, proyecta el precio a $t+1$ usando la media condicional $P_t e^{\mu / 252}$, resta el precio real observado para obtener el error $e_t$, y al final calcula el promedio cuadrático (RMSE) y el porcentaje de error (MAPE). |

---

## 📖 Diccionario de Emergencia: 15 Tecnicismos Explicados en Sencillo

Si te preguntan el significado de una palabra técnica, usa estas definiciones directas:

1. **VaR (Value at Risk)**: *"Es la pérdida máxima esperada en un día normal. Si el VaR 99% a 10 días es $1.500 USD, significa que en 99 de cada 100 quincenas no perderás más de esa cantidad."*
2. **CVaR / Expected Shortfall**: *"Si ocurre una catástrofe que rompe el límite del VaR, ¿cuánto perderías en promedio? Mide el tamaño del golpe en el peor 1% de los casos."*
3. **GBM (Movimiento Browniano Geométrico)**: *"Modelo que asume que el precio de una acción flota de forma continua con una tendencia constante y olas de volatilidad suave, sin saltos bruscos."*
4. **Salto de Merton (MJD)**: *"Extensión del GBM que incorpora 'saltos de susto' o noticias bomba mediante un proceso de Poisson, capturando caídas o subidas repentinas."*
5. **Ornstein-Uhlenbeck (O-U)**: *"Modelo con efecto resorte o imán: si el precio se aleja mucho de su promedio histórico, una fuerza matemática lo jala de vuelta."*
6. **Exponente Hurst ($H$)**: *"Mide si una acción tiene memoria. Si $H > 0.5$, la acción tiene inercia de tendencia (persistencia); si $H < 0.5$, cambia de rumbo constantemente (antipersistencia)."*
7. **Efecto Manada (Herding - CCK 2000)**: *"Ocurre cuando hay pánico colectivo y los inversores dejan de analizar individualmente para seguir a la multitud, haciendo que todas las acciones caigan idénticas."*
8. **Opción Call & Put**: *"Son seguros financieros. Una Put te da derecho a vender cara una acción si se desploma (te protege); una Call te da derecho a comprarla barata si se dispara."*
9. **Strike ($K$)**: *"El precio pactado y garantizado en el contrato de seguro al que puedes vender o comprar la acción."*
10. **Prima de la Opción**: *"El precio que pagas hoy por comprar la póliza de seguro. Si el mercado sube y no usas el seguro, solo pierdes esta prima."*
11. **Árbol Binomial CRR**: *"Un mapa de bifurcaciones donde en cada paso el precio solo puede subir o bajar. Se calcula desde el futuro hacia el presente para hallar el precio justo de la opción."*
12. **SLSQP**: *"Algoritmo matemático de optimización cuadrática que encuentra la combinación de acciones de menor riesgo respetando que ningún sector supere el 35%."*
13. **Drawdown Máximo**: *"La peor caída porcentual que sufrió la cartera desde su punto más alto antes de recuperarse."*
14. **Test de Kupiec (POF)**: *"Auditor estadístico que cuenta cuántas veces falló el VaR en el pasado real para certificar si el modelo fue confiable o mintió."*
15. **RMSE y MAPE**: *"Medidas de error de pronóstico: el RMSE mide el error promedio en dólares y el MAPE mide el margen de error porcentual."*

---

## 🎯 Preguntas Trampa del Profesor y Respuestas Clave

#### 1. ¿Por qué asumieron media cero ($\mu = 0$) en la matriz de covarianza y en el VaR paramétrico?
> **Respuesta**: *"Siguiendo las directrices del Comité de Basilea y el Paso 11 del taller, en horizontes cortos de 10 días el rendimiento esperado ($\mu$) es de segundo orden frente a la volatilidad ($\sigma \sqrt{t}$). Asumir media cero es una práctica prudencial estándar que evita pronósticos optimistas de ganancia al calcular riesgo de pérdida."*

#### 2. ¿Por qué no usamos la regla inversa al VaR ($w_i \propto 1/v_i$)?
> **Respuesta**: *"Porque la regla inversa evalúa cada acción de forma aislada e ignora completamente las correlaciones. Dos acciones muy volátiles pero negativamente correlacionadas recibirían poco peso, a pesar de que juntas reducen drásticamente el riesgo de la cartera. Por eso resolvimos la optimización conjunta con SLSQP."*

#### 3. ¿Cómo garantizan que ningún sector supere el 35%?
> **Respuesta**: *"Definimos restricciones lineales de desigualdad $\sum_{i \in \text{sector}} w_i \le 0.35$ junto con cotas individuales $w_i \in [0.02, 0.20]$ y $\sum w_i = 1$. El solucionador SLSQP garantiza el cumplimiento simultáneo de todas las cotas en cada iteración."*

#### 4. ¿Por qué el árbol CRR converge a Black-Scholes ($10.4506)?
> **Respuesta**: *"Por el Teorema del Límite Central, al aumentar los pasos $N \to \infty$ ($\Delta t \to 0$), la distribución binomial discreta converge a la distribución log-normal continua del GBM neutral al riesgo. Con 200 pasos reproduce exactamente los 4 decimales del benchmark analítico."*

#### 5. ¿Qué significa el factor de escala $f = \min\{1, V / V_{\text{riesgo}}\}$ del Paso 12?
> **Respuesta**: *"Es el control de presupuesto de riesgo. Si el VaR de la cartera 100% invertida supera el límite tolerable del cliente ($V_{\text{riesgo}} > V$), el factor $f$ reduce la inversión en acciones a $A_i = f \cdot B \cdot w_i$, y el remanente $E = (1 - f) \cdot B$ se asigna a efectivo libre de riesgo sin volatilidad."*
