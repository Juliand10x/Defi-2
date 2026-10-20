# Plan Maestro de Implementación: Aplicación de Valoración y Riesgo
**Asignatura:** Valoración de Activos (DEFI 2) - 5to Semestre de Ciencia de Datos  
**Institución:** Universidad Externado de Colombia  
**Estudiante:** Julián Duarte  
**Portafolio:** Dinámico (Preset base: USD 100.000 | 10 Acciones | $\ge 4$ Sectores)  
**Enfoque:** Rigor Matemático y Estocástico + Experiencia Interactiva Fintech (Estilo eToro) con Máxima Flexibilidad

---

## 1. Visión General y Filosofía de Diseño: "Rigor Académico + Libertad de Usuario"

El aplicativo cumplirá **estricta y automáticamente** con todos los requisitos exigidos por el docente para obtener la máxima nota (100/100), pero **no será un sistema rígido ni estático**. Siguiendo la filosofía de plataformas profesionales como eToro y Bloomberg Terminal, el usuario tendrá control total para personalizar y experimentar:

### Principios Clave:
1. **Modo Rúbrica Taller (1-Click Preset):**
   - Carga predeterminada con 10 acciones balanceadas en más de 4 sectores, capital de USD 100.000, horizonte de 10 días, confianza 99% y cotas de optimización ($2\% \le w_i \le 20\%$, sector $\le 35\%$).
   - Permite sustentar y evaluar todo el taller de inmediato sin fricción.
2. **Modo Libre / Dinámico (Flexibilidad Total para el Usuario):**
   - **Número de Acciones Flexible:** El usuario puede añadir o remover tickers a voluntad (ej. 5, 8, 10, 15 acciones).
   - **Detección Automática de Sector con Reclasificación Manual:** Al ingresar un ticker, el sistema consulta automáticamente su sector en Yahoo Finance (`info['sector']`), pero el usuario puede editarlo o forzarlo manualmente si difiere de su criterio o para simular escenarios de estrés personalizados.
   - **Límites y Restricciones Configurables:** Los límites de peso individual ($w_{min}, w_{max}$) y concentración sectorial se recalculan de forma coherente según la cantidad de activos seleccionados.
3. **Experiencia de Usuario (eToro UI/UX):**
   - Modo oscuro premium, tarjetas interactivas de métricas clave, buscador de activos y gráficos en tiempo real con Plotly.
   - Lenguaje claro y explicaciones intuitivas para cualquier perfil de inversionista, con desglose técnico accesible para la sustentación matemática.

---

## 2. Arquitectura de Software y Estructura de Archivos

```text
06_App/
│
├── Docs/
│   └── Taller_Valoracion_Plantilla.pdf
│
├── data/                             # Datos en caché y datasets de respaldo
│   ├── cache_precios.csv
│   └── backup_acciones.csv
│
├── src/                              # Lógica matemática y financiera pura
│   ├── __init__.py
│   ├── data_engine.py                # Descarga yfinance, autodetección de sectores, validación
│   ├── gbm_engine.py                 # Simulación GBM (medida P), cuantiles, bandas
│   ├── options_engine.py             # Cadenas de opciones, selección K y T, probabilidades
│   ├── pricing_engine.py             # Árbol CRR (Europeo/Americano), Black-Scholes, comparación mercado
│   ├── risk_engine.py                # VaR & CVaR (Histórico, Normal, Monte Carlo), pruebas de estrés
│   ├── allocation_engine.py          # Pesos iguales, inverso VaR, Mínimo VaR con restricciones, perfiles
│   └── backtest_engine.py            # Rolling 252 sesiones, pronóstico H días, RMSE y MAPE
│
├── ui/                               # Componentes visuales y diseño
│   ├── __init__.py
│   ├── styles.css                    # Estilos modernos fintech (glassmorphism, tema oscuro)
│   ├── components.py                 # Tarjetas KPI, semáforos, tablas editables
│   └── charts.py                     # Generadores de gráficos Plotly interactivos
│
├── app.py                            # Punto de entrada principal (Streamlit Dashboard)
├── requirements.txt                  # Dependencias del proyecto
└── PLAN_IMPLEMENTACION.md            # Este documento
```

---

## 3. Plan de Trabajo Fase por Fase (Desarrollo Incremental)

---

### Módulo 1: Ingesta Dinámica, Auditoría de Calidad y Preprocesamiento de Datos
*Correspondencia en Taller:* Pasos 1, 2 y 3 (15% de la nota final).

- [ ] **1.1 Selección Dinámica de Activos y Detección de Sectores:**
  - **Selector Flexible de Acciones:** Permitir al usuario seleccionar cualquier número de acciones (preset de 10 acciones: `AAPL`, `MSFT`, `GOOGL`, `JPM`, `XOM`, `JNJ`, `AMZN`, `PG`, `NEE`, `NVDA`).
  - **Autodetección de Sector:** Consulta automática de la clasificación sectorial oficial vía `yfinance`.
  - **Edición / Reclasificación Manual:** Tabla editable en la UI donde el usuario puede modificar el sector asignado a cualquier ticker con un simple menú desplegable.
- [ ] **1.2 Descarga y Validación Robusta:**
  - Descarga de historial de al menos 3 años de datos diarios.
  - Precios ajustados (`auto_adjust=True`) para retornos y precio de cierre no ajustado como spot $S_0$.
  - Validación de al menos 756 sesiones comunes (504 calibración inicial, 252 evaluación fuera de muestra).
  - Detección y reporte de datos faltantes/descartes sin inventar retornos cero.
  - Opción de carga de archivo CSV de respaldo si falla la descarga web.
- [ ] **1.3 Calibración de Parámetros:**
  - Retornos continuos y discretos.
  - Volatilidad anualizada $\hat{\sigma}_i = \sqrt{252}\cdot s_{x,i}$.
  - Drift total $\hat{\mu}^{total}_i = 252\cdot \bar{x}_i + \frac{1}{2}\hat{\sigma}_i^2$.
  - Tasa continua de dividendos $q_i$ y drift spot $\hat{a}_i = \hat{\mu}^{total}_i - q_i$.
  - Matrices muestrales de covarianza y correlación.
- [ ] **1.4 UI / Salidas Visuales del Módulo 1:**
  - Semáforo interactivo de calidad de datos.
  - Gráfico de precios normalizados con comparativa sectorial.
  - Matriz interactiva de correlaciones y distribuciones de retornos.

---

### Módulo 2: Motor de Proyección GBM y Análisis de Opciones Reales
*Correspondencia en Taller:* Pasos 4, 5, 6 y 7 (20% de la nota final).

- [ ] **2.1 Simulación GBM bajo Medida Física $\mathbb{P}$:**
  - Simulación exacta con paso $\Delta t = 1/252$ y semilla fija configurable:
    $$S_{t+\Delta t} = S_t \exp\left(\left(a - \frac{1}{2}\sigma^2\right)\Delta t + \sigma\sqrt{\Delta t} Z\right)$$
  - $\ge 5.000$ trayectorias, mediana, percentiles 10–90% y chequeo de positividad.
  - Comparación de media simulada con $S_0 e^{aT}$ y reporte de error estándar.
- [ ] **2.2 Explorador Dinámico de Cadenas de Opciones:**
  - Consulta en tiempo real de cadenas de opciones para la acción elegida.
  - Identificación de 3 vencimientos reales ($T = d_c / 365$) cercanos a 1, 3 y 6 meses.
  - Proyección de cuantiles $Q_{25}, Q_{50}, Q_{75}$ y selección automática de los strikes de mercado más cercanos (matriz de 9 contratos candidatos).
  - Flexibilidad para que el usuario pueda explorar contratos adicionales fuera de los 9 predeterminados.
- [ ] **2.3 Probabilidades y Justificación de Contrato:**
  - Elección de Call o Put y justificación basada en métricas.
  - Probabilidad de ejercicio: $\mathbb{P}(S_T > K)$ o $\mathbb{P}(S_T < K)$.
  - Probabilidad de beneficio neto: $\hat{\mathbb{P}}(\Pi_T > 0)$ descontando prima ask $A$ y costo $r$.
  - Explicación visual interactiva en la UI de la diferencia entre ejercer y obtener ganancia neta.
- [ ] **2.4 UI / Salidas Visuales del Módulo 2:**
  - Gráfico interactivo de trayectorias GBM con histograma terminal y bandas de confianza.
  - Tabla dinámica de los 9 contratos con Bid, Ask, Volumen e Interés Abierto.
  - Gráfica de payoff y distribución de utilidad neta $\Pi_T$.

---

### Módulo 3: Valoración por Árbol Binomial (CRR) y Comparativa de Mercado
*Correspondencia en Taller:* Pasos 8 y 9 (15% de la nota final).

- [ ] **3.1 Motor de Árbol Binomial CRR bajo Medida Riesgo-Neutral $\mathbb{Q}$:**
  - Parámetros $u, d, p_{\mathbb{Q}}$ con verificación de no arbitraje $0 < p_{\mathbb{Q}} < 1$.
  - Soporte para opciones Europeas y Americanas (inducción hacia atrás con chequeo de ejercicio anticipado).
  - Tratamiento del vencimiento $T=0$.
  - Validación con benchmark obligatorio: Call europea $S_0=100, K=100, T=1, r=0.05, q=0, \sigma=0.20 \to \approx \$10.4506$.
- [ ] **3.2 Comparativa con Black-Scholes y Análisis de Pasos:**
  - Cálculo simultáneo con Black-Scholes analítico.
  - Gráfico interactivo de convergencia al aumentar el número de pasos $N$.
- [ ] **3.3 Comparativa frente al Mercado Real:**
  - Cálculo de precio Mid $m = (\text{bid} + \text{ask})/2$, discrepancia $\delta = V_{CRR} - m$ y discrepancia relativa $\delta_{rel}$.
  - Análisis guiado en la interfaz sobre las razones de la discrepancia (volatilidad implícita vs histórica, liquidez, dividendos).
- [ ] **3.4 UI / Salidas Visuales del Módulo 3:**
  - Visualización interactiva de sub-árbol binomial representativo (3 a 5 pasos).
  - Gráfico de convergencia CRR vs Black-Scholes.
  - Comparador visual del valor teórico posicionado dentro del spread Bid-Ask.

---

### Módulo 4: Estimación Integral de Riesgo (VaR y CVaR), Pruebas de Estrés y Perfiles
*Correspondencia en Taller:* Paso 10 y Perfiles de Inversión (15% de la nota final).

- [ ] **4.1 Tres Métodos de VaR y CVaR (99% de confianza, $h=10$ días):**
  - **VaR Histórico:** Bloques compuestos de retornos a 10 días y cuantil muestral.
  - **VaR Paramétrico (Normal):** Con matriz de covarianza diaria $\Sigma_R$ y media cero:
    $$\text{VaR}_{\alpha, h}^0(w) = B \Phi^{-1}(\alpha) \sqrt{h w^T \Sigma_R w}$$
  - **VaR Monte Carlo:** $\ge 20.000$ escenarios conjuntos correlacionados bajo $\mathbb{P}$ (descomposición Cholesky).
  - Cálculo de Expected Shortfall (CVaR) para los tres métodos.
- [ ] **4.2 Pruebas de Estrés Regulatorias y Personalizables:**
  - Escenario 1: Caída uniforme de 10% en todas las acciones.
  - Escenario 2: Caída de 20% en el sector con mayor peso y -5% en los demás.
  - Escenario 3: Volatilidad $\times 1.5$ y correlación uniforme $\rho = 0.8$.
  - *Opción Libre:* Permitir al usuario definir shocks personalizados de estrés.
- [ ] **4.3 Auditoría Fuera de Muestra (Backtesting de VaR):**
  - Registro diario de excepciones de VaR sobre las 252 sesiones de prueba.
  - Gráfico de evolución de drawdown y curva patrimonial.
- [ ] **4.4 Perfiles de Inversionista eToro:**
  - Perfiles preconfigurados:
    - **Conservador:** Presupuesto de riesgo bajo ($V$), alta proporción en caja/tasa libre de riesgo $E = (1-f)B$.
    - **Moderado:** Presupuesto de riesgo equilibrado.
    - **Agresivo:** 100% en portafolio de acciones ($f = 1$).
  - Factor dinámico de escala $f = \min\{1, V / V_{riesgo}\}$.
- [ ] **4.5 UI / Salidas Visuales del Módulo 4:**
  - Dashboard de métricas de riesgo con tarjetas KPI.
  - Gráfico de densidad de pérdidas con zonas de VaR 99% y CVaR.
  - Resultados visuales de las pruebas de estrés y registro de excepciones.

---

### Módulo 5: Asignación de Capital Dinámica, Restricciones y Explicabilidad
*Correspondencia en Taller:* Pasos 11 y 12 (20% de la nota final).

- [ ] **5.1 Tres Esquemas de Asignación:**
  - **Equiponderado:** $w_i = 1/N$.
  - **Inverso al VaR Individual:** $w_i \propto 1/v_i$ (explicando por qué ignora correlaciones).
  - **Mínimo VaR Conjunto (Optimización Restringida):**
    $$\min_w B \Phi^{-1}(\alpha) \sqrt{h w^T \Sigma_R w}$$
    Sujeto a $\sum w_i = 1$, límites por activo y límites sectoriales.
- [ ] **5.2 Adaptabilidad de Restricciones:**
  - Con el preset de 10 acciones: límites estrictos del taller ($0.02 \le w_i \le 0.20$ y sector $\le 35\%$).
  - Con $N$ acciones variables: límites escalables y personalizables por el usuario para garantizar siempre la factibilidad matemática.
- [ ] **5.3 Ejecución de Mercado y Acciones Enteras:**
  - Asignación de capital $A_i = f \cdot B \cdot w_i$.
  - Cantidad de acciones enteras $\lfloor A_i / S_{i,0} \rfloor$.
  - Reporte de efectivo residual y recalculo del VaR efectivo.
- [ ] **5.4 Motor de Explicabilidad Financiera:**
  - Explicación automática en lenguaje claro de las ponderaciones asignadas, impacto de la diversificación y efecto de las restricciones sectoriales.
- [ ] **5.5 UI / Salidas Visuales del Módulo 5:**
  - Gráficos interactivos de dona y barras de pesos por acción y por sector.
  - Tabla de ejecución de órdenes de compra con acciones enteras y efectivo residual.

---

### Módulo 6: Backtesting Rolling del GBM y Exportación Consolidada
*Correspondencia en Taller:* Paso 13 y Entregables Finales (15% de funcionamiento + exportación).

- [ ] **6.1 Ventana Móvil de Calibración (Rolling 252 Sesiones):**
  - Calibración continua con los 252 días anteriores para cada fecha $t$.
  - Pronóstico condicional $H=1$ día (y selector interactivo para horizontes mayores $H=5, 10$):
    $$\hat{P}_{i, t+H|t} = P_{i,t} \exp\left(\hat{\mu}^{total}_{i,t} \frac{H}{252}\right), \quad e_{i,t} = P_{i,t+H} - \hat{P}_{i, t+H|t}$$
- [ ] **6.2 Evaluación con Métricas RMSE y MAPE:**
  - Cálculo automático de RMSE y MAPE por acción.
  - Comparación frente al pronóstico ingenuo (*naive*: $\hat{P}_{t+H|t} = P_t$).
- [ ] **6.3 Exportador Universal de Resultados:**
  - Descarga consolidada en archivo CSV de todas las tablas de asignación, parámetros, contratos y métricas de error.
  - Panel de reproducibilidad con registro de semillas y versiones de librerías.
- [ ] **6.4 UI / Salidas Visuales del Módulo 6:**
  - Curvas de precio real observado vs pronóstico GBM rolling.
  - Gráfico comparativo de barras de RMSE y MAPE (GBM vs Modelo Ingenuo).
  - Panel de descarga y resumen ejecutivo de sustentación.

---

## 4. Matriz de Cumplimiento de la Rúbrica Académica (100 / 100)

| Criterio Evaluado | Ponderación | Cobertura en la Aplicación |
| :--- | :---: | :--- |
| **Datos y Calidad** | 15% | Auditoría de $\ge 756$ sesiones, parámetros $\mu, \sigma, a$, autodetección + edición manual de sectores, respaldo CSV. |
| **Opciones y Mercado** | 15% | Cadenas reales, matriz de 9 contratos según cuantiles GBM, prima CRR, comparación Bid/Ask/Mid. |
| **GBM, Rolling y RMSE/MAPE** | 20% | $\ge 5.000$ trayectorias con semilla, bandas 10-90%, rolling de 252 sesiones con RMSE/MAPE vs modelo ingenuo. |
| **VaR y Expected Shortfall** | 15% | 3 estimadores (Histórico, Normal, Monte Carlo $\ge 20.000$), 3 pruebas de estrés, backtesting de excepciones. |
| **Asignación y Estrategias** | 20% | Mínimo VaR con cotas del taller y personalizables, acciones enteras, perfiles de riesgo y explicabilidad. |
| **Funcionamiento y Sustentación** | 15% | App interactiva estilo eToro, botón de cálculo integral, exportación a CSV y código limpio y modular. |

---

## 5. Metodología de Trabajo y Aprobación Paso a Paso

1. **Aprobación de este Plan:** Revisión y ajustes por parte de Julián.
2. **Ciclo por Módulo:**
   - **Desarrollo:** Creación del código modular en `src/` y su vista en `ui/`.
   - **Prueba & Validación:** Ejecución de pruebas matemáticas y de consistencia de datos.
   - **Revisión conjunta:** Julián prueba la funcionalidad y valida el diseño.
   - **Luz verde:** Una vez aprobado, pasamos al siguiente módulo.
