# KIBO · Plataforma Móvil de Inversión, Estocástica y Gestión de Riesgo
**Universidad Externado de Colombia · Valoración de Activos**

Tu copiloto inteligente y cuantitativo con diseño *mobile-first* (inspirado en *Nu, Nequi y Binance*) para aprender a invertir y gestionar portafolios en Wall Street sin miedo.

---

## 🌟 Características Principales

1. **Diseño Mobile-First & Copiloto 3D ("Kibo")**:
   - Paleta de diseño: *Obsidiana Profundo* (`#080b12`), *Esmeralda Financiero* (`#10b981`) y *Oro Champaña* (`#f59e0b`).
   - Mascota 3D Kibo con animaciones y tutorial interactivo enfocado (**Spotlight** con difuminado y oscurecimiento de fondo).
   - Redacción amigable y humana: explicaciones claras para principiantes y rigor matemático formal para expertos y jurados.

2. **Ecosistema de 4 Modelos Estocásticos**:
   - **Movimiento Browniano Geométrico (GBM)**: Medida física con drift y volatilidad anualizada ($k=2$).
   - **Salto-Difusión de Merton (Jump-Diffusion)**: Difusión continua + saltos Poisson ($k=5$) para colas pesadas y cisnes negros.
   - **Reversión a la Media de Ornstein-Uhlenbeck (O-U)**: Velocidad de reversión ($\theta$), vida media ($t_{1/2}$) y precio de equilibrio fundamental ($k=3$).
   - **Browniano Fraccionario (fBm) & Hurst**: Estimación del Exponente de Hurst ($H$) con Análisis $R/S$ de Mandelbrot para detectar memoria larga/momentum ($H > 0.55$) vs reversión ($H < 0.45$).
   - **Backtesting Rolling de 252 Sesiones**: Calibración en ventana móvil y pronóstico a $H=1$ día evaluado con métricas **RMSE y MAPE** frente al pronóstico ingenuo (*random walk*).

3. **Test Econométrico de Manada (Herding Behavior - CCK 2000)**:
   - Detección de ineficiencia informacional con Desviación Absoluta Transversal ($CSAD_t$).
   - Regresión cuadrática con errores robustos a heterocedasticidad (White/HAC).
   - Contraste de asimetría para diagnosticar si el contagio ocurre por **pánico en desplomes** o por **FOMO en euforias**.

4. **Medición de Riesgo Integral (Paso 10 del PDF)**:
   - **3 Estimadores de VaR al 99% a 10 días**:
     1. Paramétrico Normal.
     2. Histórico Empírico (bloques compuestos).
     3. Monte Carlo Multivariado (20.000+ escenarios con correlaciones de Cholesky).
   - **Expected Shortfall (CVaR)**: Pérdida media en la cola extrema al 99%.
   - **3 Pruebas de Estrés Oficiales**:
     1. Caída uniforme de mercado (-10%).
     2. Crisis sectorial asimétrica (-20% sector mayoritario, -5% resto).
     3. Pánico de volatilidad ($\sigma \times 1.5$) y correlación extrema ($\rho = 0.80$).

5. **Optimización Cuadrática SLSQP (Mínimo VaR Restringido)**:
   - Asignación con cotas individuales ($2\% \le w_i \le 20\%$) y límite sectorial ($\le 35\%$).
   - Cálculo de acciones enteras y reporte transparente del efectivo residual.

---

## 📂 Organización del Proyecto para la Sustentación

- 📱 **Aplicación Web**: [`app.py`](app.py)
- 📓 **Notebook de Sustentación**: [`notebooks/laboratorio_modelos_y_sustentacion.ipynb`](notebooks/laboratorio_modelos_y_sustentacion.ipynb)
- 📘 **Memoria Técnica y Respuestas a Jurados**: [`MEMORIA_TECNICA_Y_SUSTENTACION.md`](MEMORIA_TECNICA_Y_SUSTENTACION.md)
- ⚙️ **Motores de Cálculo**: Carpeta [`src/`](src/) con módulos desacoplados y testeados.

---

## 🚀 Ejecución Local

```bash
cd 06_App
python3 -m streamlit run app.py
```

Enlace en la nube: [https://defi2-valoracion.streamlit.app](https://defi2-valoracion.streamlit.app)
