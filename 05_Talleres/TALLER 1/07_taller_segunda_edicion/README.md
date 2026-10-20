# Taller Segunda Edición: CAPM en SOL y KOPN

**Materia:** Valoración de Activos (DEFI 2)  
**Estudiante:** Julián Duarte  
**Tema:** Análisis Econométrico CAPM (Robustez OLS, HC1 y Newey-West HAC) y Evaluación Financiera/Empresarial de SOL y KOPN  

---

## 1. Descripción del Proyecto

Esta carpeta contiene la **Segunda Edición del Taller CAPM**, en la cual se restringe y profundiza el análisis exclusivamente en dos activos seleccionados:

1. **SOL (Solana):** Criptoactivo Layer-1 evaluado frente al **Nasdaq Crypto Index (NCI)** ($K = 365$ días).
2. **KOPN (Kopin Corporation):** Acciones de bajo precio / *penny stock* tecnológica ($< \text{USD } 1.00$) especializada en micro-pantallas militares y médicas, evaluada frente al **Technology Select Sector SPDR Fund (XLK)** ($K = 252$ días bursátiles).

El proyecto integra un doble enfoque:
- **Enfoque de Ciencia de Datos y Econometría:** Comparativa y justificación teórica/empírica entre la matriz OLS homocedástica, la corrección por heterocedasticidad **HC1 (White / MacKinnon-White)** y la corrección por heterocedasticidad y autocorrelación **Newey-West (HAC)** con núcleo de Bartlett ($L=5$).
- **Enfoque Financiero y Empresarial:** Perfil de negocio, modelo de ingresos, clientes clave (Departamento de Defensa de EE. UU., Raytheon, Collins Aerospace), canales oficiales (SEC filings 10-K/10-Q, solana.com), e interpretación económica de la Beta.

---

## 2. Estructura de Entregables

```text
07_taller_segunda_edicion/
├── 01_datos/
│   ├── datos_taller_2_edicion.csv             # Base limpia con precios, retornos y excesos
│   ├── tabla_maestra_segunda_edicion.csv      # Métricas CAPM, riesgo, iliquidez de Amihud y betas robustas
│   ├── comparativa_modelos_hac_hc1_ols.csv    # Cuadro comparativo de SE e Intervalos de Confianza al 95%
│   └── evidencia_seleccion_activos.csv        # Precios de selección, fuentes y justificación
├── 02_notebooks/
│   ├── taller_segunda_edicion_capm.ipynb          # Notebook reproducible
│   └── taller_segunda_edicion_capm_executed.ipynb # Notebook ejecutado de principio a fin
├── 03_informe/
│   ├── informe_ejecutivo_segunda_edicion.md   # Informe ejecutivo final con dictamen de inversión
│   ├── ficha_empresa_kopn_sol.md              # Ficha analítica empresarial y financiera de KOPN y SOL
│   ├── guia_teorica_h1c_newey_west.md         # Guía pedagógica explicada en palabras sencillas (OLS vs HC1 vs HAC)
│   └── checklist_cumplimiento.md              # Verificación contra los requerimientos
├── 04_graficos/
│   ├── grafico_1_precios_normalizados.png     # Precios ajustados normalizados base 100
│   ├── grafico_2_recta_capm.png               # Dispersión y recta de regresión CAPM
│   ├── grafico_3_intervalos_confianza_modelos.png # Forest plot comparativo OLS vs HC1 vs Newey-West HAC
│   ├── grafico_4_beta_movil.png               # Estabilidad temporal de la Beta móvil (90 días)
│   ├── grafico_5_mapa_riesgo_retorno.png     # Mapa riesgo-retorno con tamaño por Iliquidez de Amihud
│   ├── grafico_6_drawdown_acumulado.png       # Curvas de caídas máximas acumuladas (MDD)
│   └── grafico_7_diagnostico_residuos_hac.png # Diagnóstico econométrico de residuos (ACF y heterocedasticidad)
├── 05_scripts/
│   └── rebuild_taller_segunda_edicion.py      # Script ejecutable de reconstrucción completa
└── README.md
```

---

## 3. Resumen de Resultados Principales

| Activo | Benchmark | Beta Newey-West ($\hat{\beta}_{\text{HAC}}$) | SE OLS vs HAC | IC 95% (HAC) | $R^2$ | Maximum Drawdown (MDD) | Amihud |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SOL** | **NCI** | **1.2529** | 0.0400 $\rightarrow$ 0.0458 | [1.1632 , 1.3427] | **66.4%** | **-75.45%** | $2.41 \times 10^{-10}$ |
| **KOPN** | **XLK** | **1.8228** | 0.1503 $\rightarrow$ 0.1270 | [1.5739 , 2.0717] | **22.8%** | **-63.55%** | $1.28 \times 10^{-6}$ |

---

## 4. Reproducibilidad

Para ejecutar nuevamente todo el pipeline y regenerar los CSVs, gráficos y notebooks desde la raíz del proyecto:

```bash
# 1. Reconstruir datos, métricas y visualizaciones:
wsl python3 '/home/julianxd/code/DEFI 2/TALLER 1/07_taller_segunda_edicion/05_scripts/rebuild_taller_segunda_edicion.py'

# 2. Ejecutar y actualizar el notebook Jupyter:
wsl python3 -m nbconvert --to notebook --execute '/home/julianxd/code/DEFI 2/TALLER 1/07_taller_segunda_edicion/02_notebooks/taller_segunda_edicion_capm.ipynb' --output taller_segunda_edicion_capm_executed.ipynb --output-dir '/home/julianxd/code/DEFI 2/TALLER 1/07_taller_segunda_edicion/02_notebooks'
```
