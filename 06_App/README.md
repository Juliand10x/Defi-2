# KIBO · Plataforma de Inversión, Valoración de Activos y Gestión de Riesgo
**Universidad Externado de Colombia · Valoración de Activos (DEFI 2)**

Aplicación integral de valoración cuantitativa y gestión de riesgo que cumple al 100% con la rúbrica oficial del taller: Árbol Binomial CRR, Simulación GBM bajo medida física, Cadenas de Opciones reales, Estimadores de VaR/CVaR, Pruebas de Estrés, Asignación Cuadrática Restringida y Evaluación Predictiva Rolling de 252 sesiones.

---

## 🌟 Características Principales (Cumplimiento 100/100)

1. **Ingesta y Calidad de Datos (Pasos 1, 2 y 3 · 15 puntos)**:
   - Descarga de más de 3 años diarios con `yfinance` (`auto_adjust=True` para retornos y spot $S_0$ no ajustado).
   - Auditoría de sesiones comunes ($\ge 756$), split de 504 calibración inicial y 252 evaluación fuera de muestra.
   - Detección de descartes y precios $\le 0$ sin fabricar retornos cero.
   - Carga de archivo CSV de respaldo con procedencia registrada.
   - Tabla de parámetros oficiales: $\hat{\sigma}_i = \sqrt{252}\cdot s_{x,i}$, $\hat{\mu}^{total}_i = 252\bar{x}_i + \frac{1}{2}\hat{\sigma}_i^2$, $\hat{a}_i = \hat{\mu}^{total}_i - q_i$, asimetría, curtosis y test Jarque-Bera.
   - Gráficos automáticos: precios normalizados base 100, matriz de correlación muestral (divisor $n-1$) e histogramas con campana normal.

2. **Movimiento Browniano Geométrico y Opciones (Pasos 4, 5, 6 y 7 · 20 puntos)**:
   - Simulación exacta con $\Delta t = 1/252$, semilla fija (42) y $\ge 5.000$ trayectorias.
   - Comprobación de positividad ($S_t > 0$) y tabla estadística comparando media simulada $\bar{S}_T$ vs $S_0 e^{aT}$ con error estándar $SE$.
   - Gráfico de abanico con 40 trayectorias individuales, bandas 10-90% y 25-75%, mediana P50 e histograma de distribución terminal.
   - Matriz de 9 contratos candidatos seleccionados mediante cuantiles analíticos $Q_{25}, Q_{50}, Q_{75}$ en 3 vencimientos reales ($T \approx 1, 3, 6$ meses).
   - Probabilidad de ejercicio vs probabilidad de beneficio neto $\hat{\mathbb{P}}(\Pi_T > 0)$ descontando prima $A \cdot e^{rT}$ y costos terminales $c_T$.

3. **Árbol Binomial CRR y Comparativa de Mercado (Pasos 8 y 9 · 15 puntos)**:
   - Árbol CRR para opciones Europeas y Americanas con verificación de $0 < p_Q < 1$.
   - **Diagrama interactivo del árbol binomial de 3 pasos ($k=0,1,2,3$)** con precios del activo y valores de la opción en cada nodo.
   - **Test de control obligatorio**: Call europea con $S_0 = K = 100, T = 1, r = 0.05, q = 0, \sigma = 0.20 \to \approx \$10.4506$.
   - Comparativa continua frente a Black-Scholes analítico y gráfico de convergencia aumentando $N$.
   - Comparación con mercado: $m = (bid+ask)/2$, discrepancias $\delta$ y $\delta_{rel}$, y justificación teórica.

4. **Medición de Riesgo Integral y Estrés (Paso 10 · 15 puntos)**:
   - **3 Estimadores de VaR y CVaR (99% de confianza, $h=10$ días, capital $B=\$100.000$)**:
     1. Normal Paramétrico (media cero): $B \Phi^{-1}(\alpha)\sqrt{hw^T \Sigma_R w}$.
     2. Histórico Empírico (bloques compuestos solapados).
     3. Monte Carlo Multivariado (20.000 trayectorias con descomposición Cholesky).
   - **3 Pruebas de Estrés Oficiales**:
     1. Caída uniforme de mercado (-10%).
     2. Crisis sectorial asimétrica (-20% sector líder, -5% resto).
     3. Choque de volatilidad ($\sigma \times 1.5$) y correlación $\rho = 0.80$.
   - **Auditoría Fuera de Muestra (252 sesiones)**:
     - Curva patrimonial neta y máximo drawdown (MDD).
     - Costos de transacción (10 bps).
     - Conteo de excepciones de VaR diario con ventana móvil y Test de Cobertura de Kupiec (POF).

5. **Asignación Cuadrática y Estrategias (Pasos 11 y 12 · 20 puntos)**:
   - Comparación de 3 esquemas: $w_i = 1/10$, $w_i \propto 1/v_i$ y Mínimo VaR conjunto restringido (SLSQP).
   - Cotas estrictas del taller: $0.02 \le w_i \le 0.20$ y concentración sectorial $\le 35\%$.
   - Ajuste a presupuesto de riesgo $\bar{V}$: $f = \min\{1, \bar{V}/V_{riesgo}\}$, inversión riesgosa $A_i = f B w_i$ y efectivo libre de riesgo $E = (1-f)B$.
   - Ejecución con acciones enteras $\lfloor A_i / S_{i,0} \rfloor$, reporte de efectivo residual y **recalculo del riesgo efectivo** del portafolio.

6. **Evaluación Predictiva Rolling del GBM (Paso 13 · 20 puntos con GBM)**:
   - Ventana móvil de 252 sesiones de calibración diaria.
   - Pronóstico condicional puntual $\hat{P}_{i, t+H|t} = P_{i,t} \exp(\hat{\mu}^{total} H/252)$ vs benchmark ingenuo $\hat{P} = P_t$.
   - Selector de horizonte $H$ ($H=1$ por defecto, $H=5, 10, 20$).
   - **Tabla consolidada de RMSE y MAPE para las 10 acciones**.
   - Gráfico interactivo con curvas de precios y serie temporal de errores $e_{i,t}$.

7. **Entregables y Funcionamiento (15 puntos)**:
   - Botón maestro "⚡ Ejecutar Todo el Taller (Preset 100%)".
   - Exportación universal de todos los resultados consolidados a archivo CSV.
   - Panel de reproducibilidad (semilla 42, fechas y versiones de bibliotecas).

---

## 🚀 Ejecución Local

1. Activar el entorno virtual e instalar dependencias:
```bash
# En Windows:
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

# En macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

2. Lanzar la aplicación Streamlit:
```bash
streamlit run 06_App/app.py
```
O desde dentro de la carpeta:
```bash
cd 06_App
streamlit run app.py
```
