# Checklist de Cumplimiento - Taller Segunda Edición (CAPM: SOL y KOPN)

- [x] **Selección Acotada de Activos:** 2 activos analizados exclusivamente (SOL frente al NCI y KOPN frente al XLK).
- [x] **Perfil Financiero y Empresarial:** Ficha de empresa y proyecto (`03_informe/ficha_empresa_kopn_sol.md`) abordando modelo de negocio, clientes clave (Departamento de Defensa de EE. UU., Raytheon, Collins Aerospace), canales oficiales (investors.kopin.com, SEC filings 10-K/10-Q, solana.com, @solana), e interpretación económica de su Beta.
- [x] **Rigor Econométrico:** Guía teórica explicada en palabras sencillas (`03_informe/guia_teorica_h1c_newey_west.md`) justificando el uso de errores estándar **HC1** y **Newey-West (HAC)** con núcleo de Bartlett ($L=5$).
- [x] **Tabla Comparativa de Modelos:** `01_datos/comparativa_modelos_hac_hc1_ols.csv` con Betas, SEs, e Intervalos de Confianza al 95% para OLS, HC1 y HAC.
- [x] **Tabla Maestra Completa:** `01_datos/tabla_maestra_segunda_edicion.csv` con métricas de Alpha, Beta, Sharpe, Sortino, Treynor, MDD, VaR 95%, CVaR 95%, Beta Bajista ($\beta^-$), Beta Dimson, Beta Winsorizada e Iliquidez de Amihud.
- [x] **Suite de Visualizaciones:** 7 gráficos obligatorios de alta resolución generados en `04_graficos/` (Precios normalizados, Recta CAPM, Forest plot de intervalos de confianza por modelo, Beta móvil 90D, Mapa Riesgo-Retorno/Amihud, Drawdowns acumulados y Diagnóstico de residuos ACF/Heterocedasticidad).
- [x] **Pipeline Reproducible:** Script ejecutable `05_scripts/rebuild_taller_segunda_edicion.py` y notebook Jupyter `02_notebooks/taller_segunda_edicion_capm.ipynb`.
- [x] **Informe Ejecutivo Final:** Documento sintético `03_informe/informe_ejecutivo_segunda_edicion.md` con recomendaciones por perfil de inversión.
