# 📋 Ficha de Entrega del Proyecto: Kibo
## Taller de Aplicación de Valoración de Activos y Riesgo
**Universidad Externado de Colombia · Facultad de Finanzas, Gobierno y Relaciones Internacionales**

---

### 🌐 1. Enlaces Oficiales de Entrega

* **Aplicación Web en Producción (Cloud)**:  
  👉 **[https://defi2-valoracion.streamlit.app](https://defi2-valoracion.streamlit.app)**  
  *(Desplegada en Streamlit Community Cloud, conectada al repositorio oficial de GitHub con recarga continua y alta disponibilidad).*

* **Repositorio Oficial de Código (GitHub)**:  
  👉 **[https://github.com/Juliand10x/Defi-2](https://github.com/Juliand10x/Defi-2)**  
  *(Código abierto, estructurado modularmente en paquetes Python, con control de versiones y trazabilidad completa).*

---

### 📦 2. Resumen de Entregables Incluidos en el Proyecto

Según las especificaciones de la rúbrica (*"Entregable: una app que genere automáticamente resultados, gráficos y evaluación rolling del GBM"*):

| # | Entregable | Ubicación / Formato | Descripción |
|---|---|---|---|
| **1** | **Aplicativo Web Interactivo** | `https://defi2-valoracion.streamlit.app` | Plataforma completa en Streamlit para simulación, opciones, optimización y backtesting sin cálculos manuales. |
| **2** | **Reporte Oficial de Resultados (CSV)** | Generable en Paso 6 pestaña *📦 Descargas* | CSV consolidado con asignación de acciones enteras, comparativa de VaR 99%, pruebas de estrés y auditoría Kupiec. |
| **3** | **Guion de Exposición (10 Min)** | `entregables/GUION_EXPOSICION_10_MINUTOS.md` | Guion cronometrado paso a paso con palabras exactas y banco de respuestas a preguntas trampa del docente. |
| **4** | **Laboratorio Metodológico (Jupyter)** | `06_App/notebooks/laboratorio_modelos_y_sustentacion.ipynb` | Notebook reproducible con las 8 secciones matemáticas del taller ejecutadas paso a paso con fórmulas LaTeX. |
| **5** | **Diccionario Financiero Pedagógico** | `06_App/ui/kibo_dictionary.py` | Glosario interactivo que traduce los 15 tecnicismos clave de la rúbrica a explicaciones y ejemplos cotidianos. |
| **6** | **Código Fuente y Dependencias** | `06_App/`, `requirements.txt`, `README.md` | Arquitectura desacoplada en motores cuantitativos (`src/`) e interfaz gráfica (`ui/`). |

---

### 🛡️ 3. Plan de Contingencia para la Presentación (Modo Local Offline)

Para garantizar que la presentación funcione incluso si la universidad no tiene conexión a internet o Streamlit Cloud sufre interrupciones:

1. **Abrir la terminal en la raíz del proyecto**:
   ```powershell
   cd "c:\Users\sduar\Documents\Universidad\defi 2"
   ```

2. **Ejecutar la aplicación localmente**:
   ```powershell
   .venv\Scripts\streamlit run 06_App/app.py
   ```

3. **Abrir en el navegador**:
   ```
   http://localhost:8501
   ```
   *La app funcionará de forma 100% autónoma en tu máquina con las cotizaciones almacenadas en caché.*

---

### 📊 4. Matriz de Cumplimiento de la Rúbrica (Pasos 1 al 13)

- [x] **Paso 1 (Entradas y Pantallas)**: Flujo de 6 pasos guiados con botón de ejecución automática y diseño mobile-first.
- [x] **Paso 2 (Descarga y Validación)**: Descarga desde Yahoo Finance de 10 acciones en USD, 3 años de datos, spot sin ajustar y retornos ajustados.
- [x] **Paso 3 (Retornos y Calibración)**: Retornos logarítmicos, parámetros $\mu$ y $\sigma$, divisor $n-1$, gráfico base 100, matriz de correlación y reclasificador de sectores.
- [x] **Paso 4 (Simulación GBM)**: 5.000 trayectorias, paso $\Delta t = 1/252$, bandas 10-90%, P50 y verificación de convergencia a $S_0 e^{aT}$.
- [x] **Paso 5 (Contratos de Opciones)**: Cadena real de Wall Street para 1, 3 y 6 meses con strikes cercanos a cuantiles 25, 50 y 75.
- [x] **Paso 6 (Justificación de Contrato)**: Análisis de cobertura frente a volatilidad histórica e implícita con gráfico de Payoff vs Beneficio Neto.
- [x] **Paso 7 (Garantías y Margen)**: Modelo de requerimiento de margen y justificación de compra de opción vs venta descubierta.
- [x] **Paso 8 (Árbol Binomial CRR)**: Algoritmo CRR para opciones europeas y americanas, árbol de 3 pasos y control de convergencia a USD $10.4506.
- [x] **Paso 9 (Comparación de Mercado)**: Cálculo del punto medio bid-ask ($m$), discrepancia teórica $\delta$ y $\delta_{\text{rel}}$, y análisis de liquidez.
- [x] **Paso 10 (3 Métodos de VaR y CVaR al 99%)**: Paramétrico Normal ($\mu=0$), Histórico por bloques de 10 días, y Monte Carlo 20.000 simulaciones, más 3 pruebas de estrés.
- [x] **Paso 11 (Asignación Óptima y Restricciones)**: Optimización cuadrática SLSQP de Mínimo VaR, límites $w_i \in [2\%, 20\%]$ y sector $\le 35\%$, acciones enteras y efectivo residual.
- [x] **Paso 12 (Estrategias Explicables)**: Ajuste a presupuesto de riesgo con factor de escala $f = \min\{1, V/V_{\text{riesgo}}\}$ y efectivo libre de riesgo.
- [x] **Paso 13 (Evaluación Rolling de 252 Sesiones)**: Ventana móvil de 252 días con $H=1$, cálculo de RMSE y MAPE contra pronóstico ingenuo $P_t$, y Test de Kupiec POF.
