# KIBO · Plataforma de Inversión, Estocástica y Gestión de Riesgo

Tu copiloto inteligente y cuantitativo inspirado en Astro Bot para aprender y gestionar portafolios de inversión sin miedo.

## Características Principales

1. **Copiloto Inteligente & Mascota Guía ("Kibo")**:
   - Ilustración y mascota 3D estilo Astro Bot con animaciones flotantes, ojos LED cyan y reactor de plasma.
   - Hero banner animado y eslogan: *"Kibo: Tu copiloto inteligente para aprender a invertir sin miedo."*
   - Tour interactivo paso a paso guiado por Kibo con explicaciones claras, humanas y libres de tecnicismos ("finanzas en cristiano").
   - Pestaña de asesoría cuantitativa con justificaciones analíticas para sustentación académica.

2. **Modelos Estocásticos Implementados**:
   - **Movimiento Browniano Geométrico (GBM)**: Simulación analítica y Monte Carlo ($k=2$).
   - **Modelo de Salto de Merton (Jump-Diffusion)**: Componentes continuos más saltos Poisson compuestos ($k=5$), capturando colas pesadas y riesgo de cisne negro.
   - **Proceso Ornstein-Uhlenbeck (O-U)**: Calibración AR(1) de velocidad de reversión ($\theta$), vida media ($t_{1/2}$) y precio de equilibrio.

3. **Comparación Cuantitativa y Criterios de Información**:
   - Cálculo automático de **Log-Likelihood ($\ln L$)**, **AIC** y **BIC** para determinar estadísticamente el mejor modelo.
   - Diagnósticos de asimetría, curtosis y test de normalidad Jarque-Bera.
   - Abanicos de percentiles (10%, 25%, 50%, 75%, 90%) y trayectorias interactivas en Plotly.

4. **Toma de Decisión por Perfil de Riesgo y Asignación**:
   - **Conservador (Modo Escudo)**: Prioriza el CVaR del Modelo de Salto de Merton y activos de reversión (O-U).
   - **Moderado (Modo Equilibrio)**: Aplica el modelo con mejor puntuación BIC y balance riesgo/retorno.
   - **Agresivo (Modo Impulso)**: Maximiza la captura del drift ($\mu$) y convexidad en colas alcistas.
   - **Optimización de Portafolio**: Pesos Iguales, Inverso al VaR y **Mínimo VaR Restringido** (SLSQP: cotas $2\% \le w_i \le 20\%$ y sector $\le 35\%$) con cantidades de acciones enteras y efectivo residual.

## Ejecución

```bash
cd 06_App
python3 -m streamlit run app.py
```
