# 📘 MEMORIA TÉCNICA Y GUÍA DE SUSTENTACIÓN ACADÉMICA
## Plataforma Cuantitativa "Kibo" · Valoración de Activos y Gestión de Riesgo
**Universidad Externado de Colombia · Facultad de Finanzas, Gobierno y Relaciones Internacionales**

---

## 1. Resumen Ejecutivo y Propósito del Proyecto
**Kibo** es una plataforma financiera de grado profesional desarrollada bajo arquitectura *mobile-first step-by-step*, inspirada en interfaces fintech líderes (*Nu, Nequi, Binance, eToro*), con el objetivo de democratizar modelos matemáticos estocásticos avanzados, pruebas econométricas de eficiencia de mercado y optimización cuadrática de portafolios.

El proyecto cumple de forma estricta los requerimientos del taller de **Valoración de Activos**:
- Simulación sobre un capital base de **USD 100.000**.
- Canasta multi-activo de **10 acciones líderes en USD** cubriendo al menos **4 sectores económicos** (Tecnología, Salud, Financiero, Energía, Consumo, etc.).
- Descarga automatizada y limpieza de más de **3 años de cotizaciones diarias** desde Yahoo Finance con auto-ajuste de dividendos y splits.
- Comparación multimodelo de difusión estocástica, saltos y memoria fractal.
- Optimización de asignación de capital restringida mediante **SLSQP (Mínimo VaR)** con límites por activo ($2\% \le w_i \le 20\%$) y sectoriales ($\le 35\%$).
- Medición de riesgo integral mediante **3 estimadores de VaR y CVaR al 99% a 10 días** y **3 escenarios de pruebas de estrés (Stress Testing)**.
- Evaluación fuera de muestra con **Backtesting Rolling de 252 sesiones** y métricas **RMSE / MAPE**.

---

## 2. Organización Limpia del Repositorio y Carpetas

La carpeta del aplicativo `06_App/` se encuentra estructurada de manera modular para garantizar máxima reproducibilidad en la sustentación:

```
06_App/
├── app.py                                   # Aplicación principal Streamlit en producción
├── requirements.txt                         # Dependencias exactas para despliegue local y en nube
├── README.md                                # Guía rápida de instalación y ejecución
├── MEMORIA_TECNICA_Y_SUSTENTACION.md        # Documento maestro técnico y respuestas a jurados
├── notebooks/
│   └── laboratorio_modelos_y_sustentacion.ipynb  # Laboratorio interactivo ejecutable paso a paso
├── src/                                     # Motores analíticos y matemáticos desacoplados
│   ├── data_engine.py                       # Extracción de yfinance, filtros de calidad y retornos
│   ├── stochastic_engine.py                 # Calibración y Monte Carlo de GBM, Merton y O-U
│   ├── fractional_engine.py                 # Browniano Fraccionario (fBm) y Exponente de Hurst (R/S)
│   ├── herding_engine.py                    # Test econométrico CCK (2000) y Desviación CSAD
│   ├── risk_engine.py                       # 3 Estimadores de VaR/CVaR y Stress Testing oficial
│   ├── portfolio_engine.py                  # Optimización cuadrática SLSQP restringida
│   ├── rolling_engine.py                    # Backtest rolling 252d, RMSE, MAPE y pronóstico naive
│   └── model_comparison.py                 # Orquestador comparativo con AIC/BIC y selección
├── ui/                                      # Capa de experiencia de usuario y diseño
│   ├── styles.py                            # Paleta Obsidiana, Esmeralda Financiero y Oro Champaña
│   ├── tour.py                              # Motor de tutorial interactivo con foco Spotlight
│   ├── kibo_avatar.py                       # Render e integración de la mascota 3D Kibo
│   └── charts.py                            # Visualizaciones financieras interactivas con Plotly
└── legacy/                                  # Archivos de prototipos antiguos archivados
```

---

## 3. Fundamentos Matemáticos de los Modelos Estocásticos

### 3.1. Movimiento Browniano Geométrico (GBM)
Bajo la medida física $\mathbb{P}$, el precio evoluciona como:
$$dS_t = \mu S_t dt + \sigma S_t dW_t$$
Solución analítica exacta por el Lema de Itô:
$$S_{t+\Delta t} = S_t \exp\left( \left(\mu - \frac{1}{2}\sigma^2\right)\Delta t + \sigma \sqrt{\Delta t} Z \right), \quad Z \sim \mathcal{N}(0, 1)$$
- **Calibración**: $\hat{\sigma} = \sqrt{252} \cdot s_x$, $\hat{\mu} = 252 \cdot \bar{x} + \frac{1}{2}\hat{\sigma}^2$.
- **Supuesto clave**: Los retornos logarítmicos son independientes e idénticamente distribuidos (i.i.d.) con distribución Normal.

### 3.2. Modelo de Salto-Difusión de Merton (MJD)
Permite capturar colas pesadas (*fat tails*) y saltos bruscos provocados por noticias macroeconómicas o anuncios corporativos:
$$\frac{dS_t}{S_{t^-}} = (\mu - \lambda k)dt + \sigma dW_t + (J - 1)dN_t$$
donde $N_t \sim \text{Poisson}(\lambda t)$ y el tamaño del salto en log-retorno es $\ln J \sim \mathcal{N}(\mu_j, \sigma_j^2)$.
- **Simulación**: Trayectorias con componente de difusión continua más saltos discretos según Poisson.
- **Log-verosimilitud mixta**:
  $$\ln \mathcal{L} = \sum_{t=1}^T \ln \left( \sum_{n=0}^\infty \frac{e^{-\lambda \Delta t}(\lambda \Delta t)^n}{n!} f_{\mathcal{N}}\left(r_t; \mu_n, \sigma_n^2\right) \right)$$

### 3.3. Proceso de Reversión a la Media de Ornstein-Uhlenbeck (O-U)
Apropiado para empresas en sectores maduros o de commodities regulados que fluctúan alrededor de un costo marginal de largo plazo:
$$dS_t = \theta (\bar{\mu} - S_t)dt + \sigma dW_t$$
- **Velocidad de reversión ($\theta$)**: Velocidad con la que el precio regresa a $\bar{\mu}$.
- **Vida media (*Half-life*)**: $\tau_{1/2} = \frac{\ln 2}{\theta} \times 252$ días.

### 3.4. Movimiento Browniano Fraccionario (fBm) & Exponente de Hurst ($H$)
Formalizado por Benoît Mandelbrot y H.E. Hurst para superar la hipótesis de independencia temporal:
$$S(t) = S_0 \exp\left( \left(\mu - \frac{1}{2}\sigma^2\right)t + \sigma B_H(t) \right)$$
donde la función de autocovarianza de los incrementos fraccionarios ($fGn$) es:
$$\gamma(k) = \frac{1}{2}\left( |k+1|^{2H} - 2|k|^{2H} + |k-1|^{2H} \right)$$
- **Algoritmo de estimación**: Análisis de Rango Reescalado ($R/S$ Analysis) en regresión logarítmica: $\ln(R/S)_\tau = \ln c + H \ln \tau$.
- **Régimen según $H$**:
  - $H \approx 0.50$: Paseo aleatorio estándar (mercado eficiente).
  - $H > 0.55$: **Proceso Persistente (Memoria Larga / Inercia de Tendencia)**.
  - $H < 0.45$: **Proceso Antipersistente (Reversión Continua)**.

---

## 4. Test Econométrico de Comportamiento en Manada (Herding Behavior - CCK 2000)

El modelo de **Chang, Cheng & Khorana (2000)** evalúa si ante momentos de tensión o volatilidad extrema los participantes del mercado se comportan como una manada (*herding*), imitando colectivamente a los demás y provocando que la dispersión transversal de retornos se comprima de manera no lineal.

1. **Desviación Absoluta Transversal ($CSAD_t$)**:
   $$CSAD_t = \frac{1}{N} \sum_{i=1}^N |R_{i,t} - R_{m,t}|$$
2. **Ecuación Cuadrática CCK**:
   $$CSAD_t = \alpha + \gamma_1 |R_{m,t}| + \gamma_2 R_{m,t}^2 + \varepsilon_t$$
3. **Criterio de Eficiencia Informacional**:
   - En un mercado racional (modelo CAPM): $\gamma_2 \ge 0$. A mayor movimiento del mercado ($|R_m|$), cada activo diverge según su Beta individual, aumentando la dispersión.
   - En presencia de **Comportamiento en Manada**: $\gamma_2 < 0$ con significancia estadística ($t < -1.96$, $p < 0.05$). La dispersión colapsa porque los inversores copian a la masa sin analizar los balances individuales.
4. **Contraste de Asimetría Bull / Bear**:
   $$CSAD_t = \alpha + \gamma_1 |R_{m,t}| + \gamma_2^{\text{down}} D_{\text{down}} R_{m,t}^2 + \gamma_2^{\text{up}} D_{\text{up}} R_{m,t}^2 + \varepsilon_t$$
   Permite distinguir si el contagio surge por **pánico en desplomes** o por **euforia/FOMO en burbujas alcistas**.

---

## 5. Medición de Riesgo: Los 3 Métodos de VaR y Pruebas de Estrés (Paso 10 del PDF)

Para un capital $B = \$100.000$, vector de pesos $w$, horizonte $h = 10$ días y nivel de confianza $\alpha = 99\%$:

| Estimador de VaR | Formulación Matemática | Supuesto y Aplicación |
| :--- | :--- | :--- |
| **1. Paramétrico (Normal)** | $\text{VaR}_{0.99, 10} = B \Phi^{-1}(0.99) \sqrt{h \, w^T \Sigma w}$ | Distribución elíptica gaussiana multivariada. Rápido, pero asume simetría. |
| **2. Histórico Empírico** | $\text{VaR}_{0.99, 10} = Q_{0.99}(-R_{p, 10d})$ | Retornos acumulados por bloques de 10 días reales. Libre de supuestos paramétricos. |
| **3. Monte Carlo (25.000 sims)** | $\text{VaR}_{0.99, 10} = Q_{0.99}(-w^T R_{\text{sim, 10d}})$ | Simulación de retornos conjuntos con descomposición de Cholesky $\Sigma = L L^T$. |

### Pruebas de Estrés Oficiales del PDF:
1. **Estrés 1 (Caída Uniforme)**: Choque homogéneo de $-10\%$ en todas las acciones del portafolio.
2. **Estrés 2 (Crisis Sectorial Asimétrica)**: Caída de $-20\%$ en el sector con mayor peso de la cartera y caída de $-5\%$ en el resto.
3. **Estrés 3 (Pánico de Volatilidad)**: Incremento de la volatilidad en un $50\%$ ($\sigma_i \times 1.5$) y colapso de la correlación hacia $\rho_{ij} = 0.80$, simulando la pérdida del beneficio de diversificación.

---

## 6. Optimización Cuadrática de Portafolio: Mínimo VaR Restringido (Paso 11 del PDF)

Se resuelve el problema de programación no lineal:
$$\min_{w} \quad B \Phi^{-1}(\alpha)\sqrt{h \, w^T \Sigma_R w}$$
sujeto a:
1. $\sum_{i=1}^{10} w_i = 1$ (Inversión completa del capital).
2. $0.02 \le w_i \le 0.20$ (Límites individuales: ninguna acción tiene menos del 2% ni más del 20%).
3. $\sum_{i \in \text{Sector } s} w_i \le 0.35$ para todo sector $s$ (Tope máximo de concentración sectorial del 35%).
4. Estimación con matriz de covarianza de entrenamiento y **media cero** (no se incluye Sharpe ni rentabilidad esperada para aislar puramente el riesgo).
5. **Redondeo discreto**: Cálculo de acciones enteras $A_i = \lfloor B w_i / S_{i,0} \rfloor$ y reporte transparente del **efectivo residual** no invertido.

---

## 7. Evaluación Rolling del GBM (Paso 13 del PDF)

- **Esquema de ventana móvil**: Se toman $252$ log-retornos para calibrar $(\hat{\mu}, \hat{\sigma})$ y pronosticar el precio a $H=1$ día fuera de muestra:
  $$\hat{P}_{i, t+1|t} = P_{i,t} \exp\left( \hat{\mu}_{\text{total}, i, t} \frac{1}{252} \right)$$
- **Benchmark Ingenuo (Random Walk)**: $\hat{P}_{i, t+1|t}^{\text{naive}} = P_{i,t}$.
- **Métricas calculadas sobre las 252 sesiones de prueba**:
  $$\text{RMSE}_i = \sqrt{\frac{1}{m}\sum_{t=1}^m \left( P_{i, t+1} - \hat{P}_{i, t+1|t} \right)^2}, \quad \text{MAPE}_i = \frac{100}{m}\sum_{t=1}^m \frac{|P_{i, t+1} - \hat{P}_{i, t+1|t}|}{P_{i, t+1}}$$

---

## 8. Banco de Preguntas Típicas para la Sustentación ante Jurados

#### P1: ¿Por qué calibrar el portafolio con media cero en lugar de maximizar el Ratio de Sharpe?
> **Respuesta**: El enunciado del taller (Paso 11) exige expresamente determinar la asignación utilizando **únicamente riesgo y límites de concentración**, sin incluir rentabilidad esperada, momentum ni Sharpe. Esto se debe a que los estimadores muestrales del drift $\hat{\mu}$ presentan un error estándar muy elevado en horizontes cortos, mientras que la matriz de covarianza $\Sigma$ es notablemente más estable y predecible.

#### P2: ¿Por qué el VaR Histórico o Monte Carlo difiere del VaR Paramétrico Normal?
> **Respuesta**: El VaR Paramétrico asume una distribución normal simétrica. Sin embargo, los retornos financieros reales presentan **asimetría negativa y exceso de curtosis (colas pesadas)**. El VaR Histórico y el Monte Carlo capturan estas pérdidas extremas con mayor fidelidad, arrojando estimaciones más conservadoras y realistas de la cola izquierda.

#### P3: ¿Qué ventaja matemática ofrece el Movimiento Browniano Fraccionario sobre el GBM clásico?
> **Respuesta**: El GBM asume incrementos independientes sin memoria ($H = 0.5$). En contraste, el fBm cuantifica si una acción posee memoria de largo plazo o persistencia de tendencia ($H > 0.55$) mediante el exponente de Hurst, lo que permite modelar activos con fuerte inercia bursátil o reversión estructural.

#### P4: ¿Cómo garantiza la app que no se violen las restricciones sectoriales del 35%?
> **Respuesta**: El optimizador cuadrático `SLSQP` formula restricciones de desigualdad no lineales de la forma $0.35 - \sum_{i \in \text{Sector } s} w_i \ge 0$. El algoritmo evalúa el gradiente en cada iteración y fuerza que la masa combinada de acciones pertenecientes a un mismo sector jamás sobrepase el umbral permitido.

