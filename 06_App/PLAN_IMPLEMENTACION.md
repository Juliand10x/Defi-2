# Plan Maestro de Implementación: Aplicación de Valoración y Riesgo
**Asignatura:** Valoración de Activos (DEFI 2) - 5to Semestre de Ciencia de Datos  
**Institución:** Universidad Externado de Colombia  
**Estudiante:** Julián Duarte  
**Portafolio:** Dinámico (Preset base: USD 100.000 | 10 Acciones | $\ge 4$ Sectores)  
**Enfoque:** Rigor Matemático y Estocástico + Experiencia Interactiva Fintech (Estilo eToro) con Máxima Flexibilidad

---

## 1. Visión General y Filosofía de Diseño: "Rigor Académico + Libertad de Usuario"

El aplicativo cumple **estricta y automáticamente** con todos los requisitos exigidos por el docente para obtener la máxima nota (100/100):

### Principios Clave Implementados:
1. **Modo Rúbrica Taller (1-Click Preset 100/100):**
   - Carga predeterminada con 10 acciones balanceadas en más de 4 sectores, capital de USD 100.000, horizonte de 10 días, confianza 99% y cotas de optimización ($2\% \le w_i \le 20\%$, sector $\le 35\%$).
   - Botón maestro "⚡ Ejecutar Todo el Taller (Preset 100%)" que calcula y muestra todos los resultados de una sola vez sin intervención manual fuera del app.
2. **Modo Libre / Dinámico (Flexibilidad Total para el Usuario):**
   - **Número de Acciones Flexible:** El usuario puede seleccionar o modificar la canasta a voluntad.
   - **Reclasificación Manual de Sectores:** Menús desplegables para forzar o corregir sectores en caso de duda o pruebas de estrés.
   - **Respaldo CSV con Procedencia Registrada:** Posibilidad de cargar un CSV externo si fallara la descarga en vivo.
3. **Experiencia de Usuario (eToro UI/UX):**
   - Modo oscuro premium, tarjetas interactivas de métricas clave, buscador de activos, diagramas de árbol binomial interactivos y gráficos en tiempo real con Plotly.

---

## 2. Arquitectura de Software y Estructura de Archivos

```text
06_App/
│
├── Docs/
│   └── Taller_Valoracion_Plantilla.pdf
│
├── data/                             # Datos en caché y datasets de respaldo
│   ├── cache_precios.csv             # 10 activos, >1.000 sesiones ajustadas
│   ├── cache_precios_raw.csv         # Spot de cierre sin ajustar
│   └── kibo_mascot.jpg
│
├── src/                              # Lógica matemática y financiera pura
│   ├── __init__.py
│   ├── data_engine.py                # Ingesta yfinance, auditoría 756 retornos, parámetros oficiales
│   ├── stochastic_engine.py          # GBM transición exacta, positividad, media vs S0*e^aT, SE
│   ├── options_engine.py             # 9 contratos candidatos (cuantiles GBM), CRR europeo/americano, árbol 3 pasos, control benchmark
│   ├── risk_engine.py                # 3 estimadores VaR/CVaR (99%, 10d), 3 pruebas estrés, auditoría fuera de muestra (Kupiec)
│   ├── portfolio_engine.py           # 3 esquemas (1/N, inv VaR, SLSQP mínimo VaR), presupuesto V_bar, acciones enteras, recalculo riesgo
│   ├── rolling_engine.py             # Rolling 252 sesiones, pronóstico puntual GBM vs ingenuo, RMSE y MAPE
│   └── model_comparison.py          # Comparación con saltos de Merton, Ornstein-Uhlenbeck y fBm (Hurst)
│
├── ui/                               # Componentes visuales y diseño
│   ├── __init__.py
│   ├── styles.py                     # Estilos fintech premium obsidian & emerald
│   ├── charts.py                     # Plotly: abanico estocástico con histograma terminal, precios normalizados, correlaciones, VaR
│   ├── kibo_avatar.py                # Avatar y badges Kibo
│   └── tour.py                       # Tour guiado interactivo
│
├── app.py                            # Tablero Académico Oficial y Modo Asistido Kibo
└── requirements.txt                  # Dependencias del proyecto
```

---

## 3. Plan de Trabajo Fase por Fase (100% Completado)

---

### Módulo 1: Ingesta Dinámica, Auditoría de Calidad y Preprocesamiento de Datos
*Correspondencia en Taller:* Pasos 1, 2 y 3 (15% de la nota final).

- [x] **1.1 Selección Dinámica de Activos y Detección de Sectores:**
  - **Selector Flexible de Acciones:** Preset de 10 acciones: `AAPL`, `MSFT`, `GOOGL`, `JPM`, `XOM`, `JNJ`, `AMZN`, `PG`, `NEE`, `NVDA`.
  - **Autodetección de Sector:** Consulta automática de la clasificación sectorial oficial vía `yfinance`.
  - **Edición / Reclasificación Manual:** Menú interactivo en la UI donde el usuario puede modificar el sector asignado a cualquier ticker con un simple menú desplegable.
- [x] **1.2 Descarga y Validación Robusta:**
  - Descarga de historial de más de 3 años de datos diarios con `yfinance`.
  - Precios ajustados (`auto_adjust=True`) para retornos continuos y discretos, y precio de cierre no ajustado como spot $S_0$. Fecha `end` exclusiva.
  - Validación de al menos 756 sesiones comunes (504 calibración inicial, 252 evaluación fuera de muestra).
  - Detección y reporte de datos faltantes/descartes sin inventar retornos cero.
  - Carga de archivo CSV de respaldo si falla la descarga web con procedencia registrada.
- [x] **1.3 Calibración de Parámetros:**
  - Retornos continuos $x_{i,t} = \ln(P_{i,t}/P_{i,t-1})$ y discretos $R_{i,t} = P_{i,t}/P_{i,t-1} - 1$.
  - Volatilidad anualizada $\hat{\sigma}_i = \sqrt{252}\cdot s_{x,i}$ (con divisor $n-1$).
  - Drift total $\hat{\mu}^{total}_i = 252\cdot \bar{x}_i + \frac{1}{2}\hat{\sigma}_i^2$.
  - Tasa continua de dividendos $q_i$ y drift spot exdividendo $\hat{a}_i = \hat{\mu}^{total}_i - q_i$.
  - Matrices muestrales de covarianza y correlación en las mismas fechas con divisor $n-1$.
- [x] **1.4 UI / Salidas Visuales del Módulo 1:**
  - Semáforo y tarjetas de calidad de datos (sesiones comunes, descartes, precios $\le 0$).
  - Gráfico interactivo de precios normalizados (Base 100).
  - Matriz interactiva de correlaciones (Heatmap).
  - Distribuciones de retornos con ajuste de campana normal y test Jarque-Bera.
  - Tabla de versiones de bibliotecas y entorno de ejecución.

---

### Módulo 2: Motor de Proyección GBM y Análisis de Opciones Reales
*Correspondencia en Taller:* Pasos 4, 5, 6 y 7 (20% de la nota final).

- [x] **2.1 Simulación GBM bajo Medida Física $\mathbb{P}$:**
  - Simulación exacta con paso $\Delta t = 1/252$ y semilla fija configurable:
    $$S_{t+\Delta t} = S_t \exp\left(\left(a - \frac{1}{2}\sigma^2\right)\Delta t + \sigma\sqrt{\Delta t} Z\right)$$
  - $\ge 5.000$ trayectorias, mediana, percentiles 10–90%, 25-75% y chequeo de positividad ($S_t > 0$).
  - Comparación de media simulada $\bar{S}_T$ con $S_0 e^{aT}$, reporte de error estándar $SE = s/\sqrt{M}$, diferencia y z-score.
- [x] **2.2 Explorador Dinámico de Cadenas de Opciones:**
  - Consulta en tiempo real de cadenas de opciones para la acción elegida.
  - Identificación de 3 vencimientos reales ($T = d_c / 365$) cercanos a 1, 3 y 6 meses.
  - Proyección de cuantiles $Q_{25}, Q_{50}, Q_{75}$ y selección automática de los strikes de mercado más cercanos (matriz de 9 contratos candidatos).
  - Expansión a strikes vecinos si cuantiles coinciden, garantizando contratos utilizables.
- [x] **2.3 Probabilidades y Justificación de Contrato:**
  - Elección de Call o Put y justificación cuantitativa.
  - Probabilidad de ejercicio: $\mathbb{P}(S_T > K)$ o $\mathbb{P}(S_T < K)$.
  - Probabilidad de beneficio neto: $\hat{\mathbb{P}}(\Pi_T > 0)$ descontando prima ask $A \cdot e^{rT}$ y costos terminales $c_T$.
  - Explicación interactiva en la UI de la diferencia entre ejercer y obtener ganancia neta, y sensibilidad ante cambios en $a$ y $\sigma$.
- [x] **2.4 UI / Salidas Visuales del Módulo 2:**
  - Gráfico interactivo de trayectorias GBM con histograma terminal y bandas de confianza (40 trayectorias mostradas).
  - Tabla dinámica de los 9 contratos con Bid, Ask, Mid, Volumen e Interés Abierto.

---

### Módulo 3: Valoración por Árbol Binomial (CRR) y Comparativa de Mercado
*Correspondencia en Taller:* Pasos 8 y 9 (15% de la nota final).

- [x] **3.1 Motor de Árbol Binomial CRR bajo Medida Riesgo-Neutral $\mathbb{Q}$:**
  - Parámetros $u = e^{\sigma\sqrt{\Delta t}}, d = 1/u, p_{\mathbb{Q}} = \frac{e^{(r-q)\Delta t}-d}{u-d}$ con verificación de no arbitraje $0 < p_{\mathbb{Q}} < 1$.
  - Soporte para opciones Europeas y Americanas (inducción hacia atrás con chequeo de ejercicio anticipado).
  - Tratamiento robusto del vencimiento $T=0$ con el payoff intrínseco.
  - **Validación con benchmark obligatorio de la rúbrica:** Call europea $S_0=100, K=100, T=1, r=0.05, q=0, \sigma=0.20 \to \approx \$10.4506$.
- [x] **3.2 Comparativa con Black-Scholes y Análisis de Pasos:**
  - Cálculo simultáneo con Black-Scholes analítico como cota continua.
  - Gráfico interactivo de convergencia al aumentar el número de pasos $N \in [5, 400]$.
- [x] **3.3 Comparativa frente al Mercado Real:**
  - Cálculo de precio Mid $m = (\text{bid} + \text{ask})/2$, discrepancia $\delta = V_{CRR} - m$ y discrepancia relativa $\delta_{rel} = (V_{CRR}-m)/m$.
  - Análisis guiado en la interfaz sobre las razones de la discrepancia (volatilidad implícita vs histórica, liquidez, estilo americano, dividendos).
- [x] **3.4 UI / Salidas Visuales del Módulo 3:**
  - Diagrama interactivo del árbol binomial de 3 pasos ($k=0, 1, 2, 3$) con precios de la acción y valores de la opción en cada nodo.
  - Gráfico de convergencia CRR vs Black-Scholes.

---

### Módulo 4: Estimación Integral de Riesgo (VaR y CVaR), Pruebas de Estrés y Auditoría Fuera de Muestra
*Correspondencia en Taller:* Paso 10 (15% de la nota final).

- [x] **4.1 Tres Métodos de VaR y CVaR (99% de confianza, $h=10$ días, capital $B=100.000$):**
  - **VaR Histórico:** Bloques compuestos solapados de retornos a 10 días y cuantil muestral de pérdidas.
  - **VaR Paramétrico (Normal):** Con matriz de covarianza diaria $\Sigma_R$ y media cero:
    $$\text{VaR}_{\alpha, h}^0(w) = B \Phi^{-1}(\alpha) \sqrt{h w^T \Sigma_R w}$$
  - **VaR Monte Carlo:** $\ge 20.000$ escenarios conjuntos correlacionados bajo $\mathbb{P}$ (descomposición Cholesky).
  - Cálculo de Expected Shortfall (CVaR) para los tres métodos documentando empates.
- [x] **4.2 Tres Pruebas de Estrés Oficiales:**
  - Escenario 1: Caída uniforme de 10% en todas las acciones.
  - Escenario 2: Caída de 20% en el sector con mayor peso y -5% en los demás.
  - Escenario 3: Choque de volatilidad $\times 1.5$ y correlación uniforme $\rho = 0.8$.
- [x] **4.3 Auditoría Fuera de Muestra (Backtesting de Cartera en 252 Sesiones):**
  - Curva de evolución de patrimonio neto $V_t = B \prod (1 + R_{p,t})$ considerando costos de transacción (10 bps).
  - Medición de Máximo Drawdown (MDD).
  - Conteo de excepciones del VaR diario al 99% mediante ventana móvil previa de 252 sesiones.
  - Test de cobertura incondicional de Kupiec (POF Likelihood Ratio) con estadístico $\chi^2(1)$ y veredicto regulatorio.
- [x] **4.4 UI / Salidas Visuales del Módulo 4:**
  - Tabla comparativa de los 3 estimadores de VaR y CVaR.
  - Gráfico de densidad de pérdidas Monte Carlo con líneas de corte VaR y CVaR 99%.
  - Gráfico de curva patrimonial y drawdown en las 252 sesiones de prueba.

---

### Módulo 5: Asignación de Capital Dinámica, Restricciones y Presupuesto de Riesgo
*Correspondencia en Taller:* Pasos 11 y 12 (20% de la nota final).

- [x] **5.1 Tres Esquemas de Asignación Comparados:**
  - **Equiponderado:** $w_i = 1/N$.
  - **Inverso al VaR Individual:** $w_i \propto 1/v_i$ (documentando por qué ignora correlaciones).
  - **Mínimo VaR Conjunto (Optimización Restringida SLSQP):**
    $$\min_w B \Phi^{-1}(\alpha) \sqrt{h w^T \Sigma_R w}$$
    Sujeto a $\sum w_i = 1$, $0.02 \le w_i \le 0.20$ y $\sum_{i \in I_s} w_i \le 0.35$ para cada sector $s$.
- [x] **5.2 Ajuste a Presupuesto de Riesgo (Paso 12):**
  - Factor de escala dinámico:
    $$f = \min\{1, \bar{V} / V_{riesgo}\}, \quad A_i = f B w_i, \quad E = (1 - f)B$$
  - Preservación de efectivo libre de riesgo si el riesgo total excede el presupuesto $\bar{V}$.
- [x] **5.3 Ejecución de Mercado y Acciones Enteras:**
  - Cantidad de acciones enteras $\lfloor A_i / S_{i,0} \rfloor$.
  - Reporte de efectivo residual por redondeo y total disponible.
  - **Recalculo del riesgo efectivo de cartera:** VaR efectivo real en USD y % sobre capital con los pesos efectivamente comprados.
- [x] **5.4 Motor de Explicabilidad Financiera:**
  - Explicación automática de los activos más blindados, impacto de las restricciones sectoriales y efecto de la diversificación.
- [x] **5.5 UI / Salidas Visuales del Módulo 5:**
  - Gráfico de barras comparando los 3 esquemas de pesos.
  - Tabla de ejecución de órdenes de compra con acciones enteras y montos reales.
  - Resumen sectorial verificando que ningún sector supere el 35%.

---

### Módulo 6: Backtesting Rolling del GBM y Exportación Consolidada
*Correspondencia en Taller:* Paso 13 y Entregables Finales (15% de funcionamiento + exportación).

- [x] **6.1 Ventana Móvil de Calibración (Rolling 252 Sesiones):**
  - Calibración diaria continua con los 252 días anteriores para cada fecha $t$.
  - Pronóstico condicional puntual:
    $$\hat{P}_{i, t+H|t} = P_{i,t} \exp\left(\hat{\mu}^{total}_{i,t} \frac{H}{252}\right), \quad e_{i,t} = P_{i,t+H} - \hat{P}_{i, t+H|t}$$
  - Selector interactivo de horizonte $H$ ($H=1$ por defecto, $H=5, 10, 20$).
  - Benchmark ingenuo de caminata aleatoria: $\hat{P}_{t+H|t} = P_t$.
- [x] **6.2 Evaluación con Métricas RMSE y MAPE para las 10 Acciones:**
  - Cálculo automático de RMSE (en unidades del precio) y MAPE (%) para cada una de las 10 acciones del portafolio.
- [x] **6.3 Exportador Universal de Resultados en CSV:**
  - Botón de descarga consolidada de todas las tablas en un único archivo CSV.
  - Botón de descarga individual del plan de compras de acciones.
  - Panel de reproducibilidad con registro de semilla (42), fechas y versiones.
- [x] **6.4 UI / Salidas Visuales del Módulo 6:**
  - Gráfico dual: Curva de precio real vs pronóstico GBM rolling (arriba) y serie de errores $e_t$ (abajo).
  - Tabla consolidada de RMSE y MAPE para las 10 acciones.

---

## 4. Matriz de Cumplimiento de la Rúbrica Académica (100 / 100)

| Criterio Evaluado | Ponderación | Cobertura en la Aplicación | Estado |
| :--- | :---: | :--- | :---: |
| **Datos y Calidad** | 15% | Auditoría de $\ge 756$ sesiones (1034 descargadas), parámetros $\mu, \sigma, a$, autodetección + edición manual de sectores, respaldo CSV y versiones de librerías. | **100% Completo** |
| **Opciones y Mercado** | 15% | Cadenas reales, matriz de 9 contratos según cuantiles GBM, prima CRR europeo y americano, árbol 3 pasos, control benchmark ($10.4506), comparación Bid/Ask/Mid. | **100% Completo** |
| **GBM, Rolling y RMSE/MAPE** | 20% | $\ge 5.000$ trayectorias con semilla, bandas 10-90% y 25-75%, positividad, rolling de 252 sesiones con RMSE/MAPE vs modelo ingenuo para las 10 acciones. | **100% Completo** |
| **VaR y Expected Shortfall** | 15% | 3 estimadores (Histórico, Normal media cero, Monte Carlo 20.000 trayectorias Cholesky), 3 pruebas de estrés, auditoría fuera de muestra en 252 sesiones con test Kupiec. | **100% Completo** |
| **Asignación y Estrategias** | 20% | Mínimo VaR con cotas del taller ($0.02 \le w_i \le 0.20$ y sector $\le 35\%$), acciones enteras, recalculo de riesgo efectivo, presupuesto de riesgo $\bar{V}$ y explicabilidad. | **100% Completo** |
| **Funcionamiento y Sustentación** | 15% | App interactiva con botón de cálculo integral, tablero académico de 7 pestañas, exportación universal a CSV y código limpio y reproducible. | **100% Completo** |
