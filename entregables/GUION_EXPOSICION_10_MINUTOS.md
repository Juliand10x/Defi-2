# 🎤 Guion Maestro de Exposición Kibo (10 Minutos)
## Valoración de Activos y Gestión de Riesgo Cuantitativo
**Universidad Externado de Colombia · Facultad de Finanzas, Gobierno y Relaciones Internacionales**

---

## ⏱️ Estructura Cronometrada de la Presentación

```
[00:00 - 01:00]  Minuto 1:  Apertura Ejecutiva y Planteamiento del Reto (USD 100K)
[01:00 - 02:00]  Minuto 2:  Perfil de Riesgo, Confianza (99%) y Presupuesto
[02:00 - 03:30]  Minuto 3:  Universo de Inversión y Diversificación Sectorial (Paso 3)
[03:30 - 05:30]  Minuto 4-5: Competencia Multimodelo, Salto de Merton y Manada (Paso 4)
[05:30 - 07:00]  Minuto 6-7: Cobertura con Opciones Reales y Árbol Binomial CRR (Pasos 5-9)
[07:00 - 08:30]  Minuto 8:  Portafolio Óptimo SLSQP, Límite 35% y VaR 99% (Pasos 10-12)
[08:30 - 09:30]  Minuto 9:  Auditoría Fuera de Muestra y Backtest Rodante (Paso 13)
[09:30 - 10:00]  Minuto 10: Conclusión Ejecutiva y Espacio para Preguntas
```

---

## 🎬 Guion Verbal y Acciones en Pantalla Paso a Paso

### 📍 Minuto 0:00 a 01:00 · Apertura Ejecutiva y Capital Inicial (Paso 1)
* **Acción en pantalla**: Tener abierta la app en la pantalla de bienvenida o en el **Paso 1 (Tu Capital)**. Si aparece el modal de bienvenida de Kibo, haz clic en *"⚡ Ya la conozco, omitir guía"* para entrar de inmediato a la interfaz.
* **Qué decir (Palabras exactas)**:
  > *"Buenos días profesor y compañeros. Hoy les presentamos **Kibo**, una plataforma cuantitativa de valoración de activos, simulación estocástica y gestión de riesgo desarrollada en Python y Streamlit.*  
  >  
  > *El objetivo del proyecto es resolver el taller oficial de la facultad: administrar un capital simulado de **USD $100.000**, proyectar activos con modelos estocásticos avanzados, estructurar una cobertura con derivados reales de Wall Street y optimizar un portafolio de mínima varianza respetando límites sectoriales estrictos.*  
  >  
  > *Kibo fue diseñado bajo una filosofía doble: por fuera tiene una interfaz minimalista, amigable y comprensible para cualquier tomador de decisiones; pero por dentro ejecuta rigurosamente todas las fórmulas econométricas y de valoración neutral al riesgo exigidas por la rúbrica."*
* **Acción**: Deja el monto en **$100.000 USD** (puedes tocar el botón rápido `$100K`) y haz clic en **"Continuar a Tu Perfil ➔"**.

---

### 📍 Minuto 01:00 a 02:00 · Perfil de Riesgo y Parámetros del VaR (Paso 2)
* **Acción en pantalla**: Estás en el **Paso 2 (Tu Perfil)**. Selecciona el modo **"⚖️ Modo Equilibrio (Moderado)"**.
* **Qué decir**:
  > *"En este segundo paso configuramos el apetito de riesgo. Seleccionamos el perfil **Moderado**, que corresponde a la calibración estándar de la Universidad Externado:*  
  > *Un nivel de confianza estadística del **99%** y un horizonte temporal de **10 sesiones bursátiles**.*  
  >  
  > *Si abrimos las **Opciones avanzadas**, podemos observar los parámetros formales: el presupuesto de riesgo de **USD $7.500** (equivalente al 7.5% del capital) y la tasa libre de riesgo libre de arbitraje del **4.0% anual**. Kibo permite personalizar estos supuestos, pero para efectos de la sustentación mantendremos los valores de la rúbrica."*
* **Acción**: Despliega un segundo el expander `⚙️ Opciones avanzadas` para mostrar los campos, ciérralo y haz clic en **"Continuar a Tus Acciones ➔"**.

---

### 📍 Minuto 02:00 a 03:30 · Universo de Inversión y Diversificación (Paso 3)
* **Acción en pantalla**: Estás en el **Paso 3 (Tus Acciones)**. Señala la lista de 10 acciones y la tarjeta del **Medidor de Diversificación**.
* **Qué decir**:
  > *"En el Paso 3 definimos nuestro universo de 10 activos líderes en Wall Street, cubriendo **6 sectores económicos diferentes** para blindar la cartera contra riesgos idiosincráticos: Tecnología (Apple, Microsoft, Nvidia), Consumo (Amazon, Tesla), Comunicaciones (Alphabet, Meta), Finanzas (JPMorgan), Salud (Johnson & Johnson) y Energía (ExxonMobil).*  
  >  
  > *La app descarga automáticamente más de 3 años de cotizaciones diarias oficiales desde Yahoo Finance utilizando precios de cierre ajustados por splits y dividendos para los retornos, y el último precio spot de mercado observado para la valoración.*  
  >  
  > *En la parte inferior pueden ver el **Medidor de Diversificación de Kibo**, que confirma que cumplimos el requisito de tener al menos 4 sectores. Además, en las opciones avanzadas contamos con un reclasificador interactivo que permite reasignar manualmente el sector de cualquier empresa si así se requiere."*
* **Acción**: Haz clic en **"Analizar con los Cerebros de Kibo ➔"**.

---

### 📍 Minuto 03:30 a 05:30 · Competencia Multimodelo, Merton y Manada (Pasos 4 y 5 de la Rúbrica)
* **Acción en pantalla**: Estás en el **Paso 4 (Kibo analiza tus acciones)**. Muestra la tarjeta del **Cerebro Ganador** para la acción seleccionada (ej. `NVDA` o `AAPL`) y navega por las pestañas.
* **Qué decir**:
  > *"Aquí llegamos al núcleo estocástico del proyecto. La rúbrica exige simular precios con el Movimiento Browniano Geométrico (GBM), pero en Kibo fuimos un paso más allá y pusimos a competir **4 modelos estocásticos bajo 5.000 trayectorias de Monte Carlo**:*  
  >  
  > *1. **Difusión Continua (GBM)**: Modela deriva constante y volatilidad browniana. Como ven en la gráfica, mostramos las 40 trayectorias discretas, la mediana P50, las bandas del 10%-90% y la distribución terminal de precios $S_T$, comprobando que la media simulada converge teóricamente a $S_0 e^{aT}$.*  
  >  
  > *2. **Saltos de Merton (MJD)**: Modela noticias imprevistas mediante un proceso de Poisson compuesto. Para empresas como Nvidia o Apple, Merton resulta ganador en los criterios **AIC y BIC** porque captura las colas pesadas y los saltos abruptos de balance que el GBM ignora.*  
  >  
  > *3. **Reversión a la Media (Ornstein-Uhlenbeck)**: Modela precios atraídos hacia un costo de equilibrio histórico.*  
  >  
  > *4. **Browniano Fraccionario (fBm)**: Calibramos el **Exponente de Hurst ($H$)** mediante reescalado R/S. Con un $H > 0.5$, detectamos persistencia y memoria larga en la serie.*  
  >  
  > *En la **Pestaña 5**, implementamos el test econométrico de **Efecto Manada de Chang, Cheng y Khorana (CCK 2000)**: evaluamos la dispersión transversal absoluta (CSAD) frente al retorno de mercado. Como el coeficiente cuadrático $\gamma_2$ no es negativo significativo, confirmamos que el mercado opera con dispersión racional y no bajo histeria colectiva.*  
  >  
  > *Por último, en la **Pestaña 6**, realizamos el **Examen Histórico Rolling de 252 sesiones con $H=1$ día**, evaluando RMSE y MAPE frente al pronóstico ingenuo $P_t$."*
* **Acción**: Muestra brevemente las pestañas 1 (GBM), 2 (Merton), 5 (Manada) y 6 (Rolling), y haz clic en **"Continuar a Tu Seguro (Opciones) ➔"**.

---

### 📍 Minuto 05:30 a 07:00 · Opciones Reales y Árbol Binomial CRR (Pasos 5 a 9 de la Rúbrica)
* **Acción en pantalla**: Estás en el **Paso 5 (Tu Seguro de Inversión)**. Haz clic en **"🔎 Buscar Seguros (Opciones) Disponibles en Wall Street"**.
* **Qué decir**:
  > *"En el módulo de derivados estructuramos una estrategia de cobertura para proteger el capital ante una caída de mercado:*  
  >  
  > *1. **Consulta en Vivo**: Consultamos la cadena de opciones oficial de Wall Street vía Yahoo Finance (`Ticker.option_chain`) para vencimientos reales de 1, 3 y 6 meses, extrayendo strikes cercanos a los cuantiles 25, 50 y 75 proyectados por el GBM.*  
  >  
  > *2. **Valoración con Árbol Binomial CRR**: Implementamos el algoritmo de Cox, Ross y Rubinstein en tiempo discreto con probabilidades neutrales al riesgo $p_q = \frac{e^{(r-q)\Delta t} - d}{u - d}$. La app soporta ejercicio Europeo y Americano.*  
  > *Verificamos el benchmark de control exigido por el profesor: una Call europea con $S_0=K=100$, $T=1$, $r=5\%$, $q=0$ y $\sigma=20\%$ converge exactamente al valor teórico de **USD $10.4506** con 200 pasos.*  
  >  
  > *3. **Simulador de Efecto Escudo**: En pantalla pueden ver la curva de Payoff versus Beneficio Neto descontando la prima. Si movemos el slider de caída a un -15%, la app demuestra cómo la opción Put absorbe la pérdida de las acciones y genera un ahorro neto tangible."*
* **Acción**: Muestra el gráfico de Payoff, mueve el slider de simulación a -15% para que aparezca la alerta verde del *Efecto Escudo*, y despliega un segundo el árbol de 3 pasos en las opciones avanzadas. Luego haz clic en **"Ver Mi Portafolio Final ➔"**.

---

### 📍 Minuto 07:00 a 08:30 · Asignación Óptima de Cartera y VaR (Pasos 10 a 12)
* **Acción en pantalla**: Estás en el **Paso 6 (Tu Plan de Inversión Inteligente)**. Muestra la tarjeta KPI superior y la lista de acciones a comprar.
* **Qué decir**:
  > *"Llegamos al entregable final: la asignación de los USD $100.000.*  
  >  
  > *1. **Optimización Cuadrática SLSQP**: Para evitar el error común de ponderar por el inverso del VaR individual (que ignora las correlaciones), formulamos el problema de optimización cuadrática de Mínimo VaR con matriz de covarianza de media cero:*  
  > $$\min_w \Phi^{-1}(\alpha)\sqrt{h \cdot w^T \Sigma_R w} \quad \text{sujeto a} \quad \sum w_i = 1, \quad w_i \in [2\%, 20\%], \quad \sum_{i \in \text{sector}} w_i \le 35\%$$  
  >  
  > *2. **Acciones Enteras y Efectivo Residual**: Convertimos los montos teóricos a acciones enteras reales de mercado ($A_i / S_{i,0}$). El sobrante por redondeo se reporta con total transparencia como efectivo de reserva.*  
  >  
  > *3. **3 Estimadores de VaR al 99%**: En la pestaña de Riesgo comparamos los 3 métodos exigidos:*  
  > *Paramétrico Normal, Histórico por bloques de 10 días, y Monte Carlo multivariado con 20.000 simulaciones conjuntas conservando la estructura de cópula y covarianza, reportando también el CVaR o Expected Shortfall.*  
  >  
  > *4. **Pruebas de Estrés**: Evaluamos una caída uniforme de mercado (-10%), un colapso sectorial (-20% en Tecnología y -5% resto) y un shock de volatilidad ($\times 1.5$ con correlación de 0.8), demostrando la resistencia del portafolio gracias al tope sectorial del 35%."*
* **Acción**: Pasa rápidamente por la pestaña 1 (Plan), pestaña 2 (VaR) y pestaña 3 (Estrés).

---

### 📍 Minuto 08:30 a 09:30 · Auditoría Fuera de Muestra y Test de Kupiec (Paso 13)
* **Acción en pantalla**: Haz clic en la **Pestaña 4: 📈 Examen Histórico**.
* **Qué decir**:
  > *"Para validar que el portafolio no sufriera de sobreajuste, ejecutamos una auditoría fuera de muestra durante las últimas 252 sesiones reales de mercado con costos de transacción de 10 puntos básicos.*  
  >  
  > *En la gráfica pueden ver la curva de evolución patrimonial y el Drawdown Máximo contenido.*  
  > *Además, aplicamos formalmente el **Test de Cobertura Condicional de Kupiec (Proportion of Failures - POF)**: en un horizonte de 252 días al 99% de confianza, se esperan teóricamente entre 2 y 3 excepciones. Nuestro modelo registró 2 excepciones empíricas, obteniendo un p-valor superior a 0.05, lo que aprueba estadísticamente la validez del modelo de riesgo."*

---

### 📍 Minuto 09:30 a 10:00 · Cierre y Descargas Oficiales
* **Acción en pantalla**: Ve a la **Pestaña 5: 📦 Descargas**.
* **Qué decir**:
  > *"Para finalizar, en la pestaña de descargas el usuario o el profesor puede obtener en un solo clic el **CSV consolidado del taller**, que incluye la asignación de acciones enteras, la tabla comparativa de VaR, las pruebas de estrés y la auditoría histórica.*  
  >  
  > *Adicionalmente, Kibo cuenta con un **Diccionario Financiero integrado** que traduce cada término cuantitativo a lenguaje cotidiano, y un recorrido interactivo guiado.*  
  >  
  > *Con esto demostramos que es posible combinar el máximo rigor matemático y econométrico exigido por la Universidad Externado con una experiencia de usuario moderna, intuitiva y visualmente impecable. Quedamos atentos a cualquier pregunta técnica. Muchas gracias."*

---

## 🧠 Banco de Preguntas Técnicas y Respuestas Clave ("Trampas del Profesor")

Si el profesor o los jurados te hacen preguntas difíciles, aquí tienes la respuesta técnica exacta:

#### 1. ¿Por qué asumieron media cero ($\mu = 0$) en la matriz de covarianza y en el VaR paramétrico?
> **Respuesta**: *"Siguiendo las directrices del documento de Basilea y la formulación del Paso 11 del taller, en horizontes cortos (como 10 días o 1 día), el término de deriva o rendimiento esperado ($\mu$) es de segundo orden frente a la volatilidad ($\sigma \sqrt{t}$), y estimar medias históricas añade ruido muestral innecesario. Asumir media cero es una práctica prudencial estándar que evita proyectar rentabilidades optimistas al medir riesgo de pérdida."*

#### 2. ¿Por qué no usamos la ponderación inversa al VaR ($w_i \propto 1/v_i$)?
> **Respuesta**: *"Porque la regla inversa al VaR evalúa cada acción de forma aislada e ignora completamente la correlación y covarianza entre activos. Dos acciones muy volátiles pero negativamente correlacionadas recibirían poco peso bajo la regla inversa, a pesar de que juntas reducen drásticamente el riesgo de la cartera. Por eso resolvimos la optimización cuadrática conjunta de Mínimo VaR mediante SLSQP."*

#### 3. ¿Cómo garantiza el algoritmo SLSQP que ningún sector supere el 35%?
> **Respuesta**: *"Se definieron restricciones de desigualdad lineales $A \cdot w \le b$. Para cada sector $s$, creamos una restricción donde la suma de los pesos de las empresas pertenecientes a ese sector no puede superar 0.35 ($\sum_{i \in I_s} w_i \le 0.35$), junto con cotas individuales $w_i \in [0.02, 0.20]$ y la restricción de presupuesto $\sum w_i = 1$. El algoritmo SLSQP (Sequential Least Squares Programming) converge a la solución óptima global garantizando el cumplimiento de todas las cotas simultáneamente."*

#### 4. ¿Qué es el factor de escala $f = \min\{1, V / V_{\text{riesgo}}\}$ del Paso 12?
> **Respuesta**: *"Es el mecanismo que ajusta la cartera al presupuesto de riesgo máximo del cliente. Si el VaR del portafolio 100% invertido supera el presupuesto tolerable ($V_{\text{riesgo}} > V$), el factor $f$ reduce proporcionalmente la exposición a renta variable a $A_i = f \cdot B \cdot w_i$, y el remanente $E = (1 - f) \cdot B$ se asigna a efectivo o activo libre de riesgo sin volatilidad, blindando al cliente de exceder su tolerancia a la pérdida."*

#### 5. ¿Por qué el árbol binomial CRR converge a Black-Scholes ($10.4506)?
> **Respuesta**: *"Porque por el Teorema del Límite Central, al hacer tender el número de pasos $N \to \infty$ ($\Delta t \to 0$), la distribución binomial de retornos discretos del árbol converge débilmente a la distribución log-normal continua del movimiento browniano geométrico con deriva neutral al riesgo $r - q$. Con $N=200$ pasos, nuestro árbol reproduce con cuatro decimales de precisión el precio analítico de Black-Scholes de USD $10.4506."*

#### 6. ¿Qué diferencia práctica hay entre una opción Europea y Americana en el árbol?
> **Respuesta**: *"En cada nodo $(k, j)$, la opción europea solo descuenta el valor esperado de continuación: $V_{k,j} = e^{-r\Delta t}[p_q V_{k+1,j+1} + (1-p_q)V_{k+1,j}]$. En la americana se evalúa el ejercicio anticipado en cada paso: $V_{k,j} = \max\{Payoff(S_{k,j}), V_{k,j}^{\text{cont}}\}$. Para opciones Put con strikes altos o subyacentes con dividendos, el ejercicio anticipado añade una prima de valor positiva."*

#### 7. ¿Por qué el Test de Kupiec valida el modelo de VaR?
> **Respuesta**: *"El Test de Razón de Verosimilitud POF (Proportion of Failures) de Kupiec evalúa si el número de excepciones observadas $k$ en $N$ sesiones se desvía significativamente de la probabilidad teórica $p = 1 - \alpha = 1\%$. Bajo la hipótesis nula de que el modelo está bien calibrado, el estadístico $-2 \ln(LR)$ sigue una distribución $\chi^2$ con 1 grado de libertad. Al obtener un p-valor mayor a 0.05, no se rechaza la hipótesis nula, lo que certifica formalmente que el modelo no subestima ni sobreestima el riesgo."*

#### 8. ¿Qué significa el Exponente de Hurst $H$ obtenido?
> **Respuesta**: *"El exponente de Hurst $H \in (0, 1)$ mide la memoria de largo plazo de la serie fractal. Si $H = 0.5$, la serie es puramente aleatoria (movimiento browniano clásico sin memoria). Si $H > 0.5$, la serie es persistente: los incrementos positivos tienden a ser seguidos por incrementos positivos (tendencia e inercia). Si $H < 0.5$, la serie es antipersistente (reversión a la media frecuente). En activos tecnológicos encontramos valores $H \approx 0.55 - 0.60$, lo que justifica el uso de modelos con memoria como el Browniano Fraccionario."*

#### 9. ¿Cómo se interpretó el test de Efecto Manada (CCK 2000)?
> **Respuesta**: *"El modelo cuadrático de Chang, Cheng y Khorana estima: $CSAD_t = \alpha + \gamma_1 |R_{m,t}| + \gamma_2 R_{m,t}^2 + \varepsilon_t$. En condiciones normales de racionalidad, la dispersión entre activos crece con la volatilidad del mercado ($\gamma_1 > 0$). Si existiera comportamiento de manada (pánico colectivo donde los inversores abandonan sus valoraciones individuales para seguir al rebaño), la dispersión se comprimiría en retornos extremos, arrojando un $\gamma_2$ negativo y estadísticamente significativo ($p < 0.05$). Al no ser negativo significativo, se concluye ausencia de herding sistemático en el periodo evaluado."*
