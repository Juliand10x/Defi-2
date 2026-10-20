# Taller 1: CAPM en Dos Mercados

**Materia:** Valoracion de Activos (DEFI 2)  
**Estudiante:** Julian Duarte  
**Tema:** La Beta de los Pobres: SOL frente al NCI y acciones de bajo precio frente a ETF sectoriales.

## Que Entregar

Los archivos principales de entrega estan organizados asi:

```text
00_enunciado/
  TallerDefi1CAPM.pdf

01_datos/
  NCI.csv
  datos_taller_1_julian_duarte.csv
  tabla_maestra_resultados.csv
  evidencia_seleccion_activos.csv

02_notebooks/
  taller_1_capm.ipynb
  taller_1_capm_executed.ipynb

03_informe/
  informe_ejecutivo_taller_1.tex
  ficha_personajes_activos.tex
  checklist_cumplimiento_taller_1.md

04_graficos/
  grafico_1_precios_normalizados.png
  grafico_2_recta_capm_todos.png
  grafico_3_forest_plot_betas.png
  grafico_4_beta_movil_todos.png
  grafico_5_mapa_riesgo_retorno.png
  grafico_6_drawdown_acumulado_todos.png
  grafico_7_matriz_percentiles.png
```

## Estructura de Trabajo

- `00_enunciado/`: enunciado oficial del taller.
- `01_datos/`: bases limpias, tabla maestra y evidencia de seleccion de activos.
- `02_notebooks/`: notebook reproducible y notebook ya ejecutado.
- `03_informe/`: informe ejecutivo, ficha de personajes y checklist de cumplimiento.
- `04_graficos/`: las siete visualizaciones obligatorias finales.
- `05_scripts/`: script que reconstruye datos, metricas, graficos, informe y notebook.
- `99_respaldo_versiones/`: versiones anteriores y archivos auxiliares que no se deben entregar salvo que el profesor los pida.

## Expediente Analizado

- Criptoactivo: `SOL` frente al `NCI`.
- Tecnologia: `KOPN`, `MVIS`, `LIDR` frente a `XLK`.
- Biotecnologia: `GERN`, `CTMX`, `OCGN` frente a `XBI`.
- Energia: `BORR`, `KLXE`, `TTI` frente a `XLE`.

`TTI` se documenta como accion de bajo precio bajo la excepcion permitida por el enunciado: precio menor a USD 10, no como penny stock estricta.

## Reproducibilidad

Para reconstruir todo desde la raiz del proyecto:

```bash
python3 05_scripts/rebuild_entregables.py
jupyter nbconvert --to notebook --execute 02_notebooks/taller_1_capm.ipynb --output taller_1_capm_executed.ipynb --output-dir 02_notebooks --ExecutePreprocessor.timeout=240
```

El script descarga precios y volumen desde Yahoo Finance, usa `01_datos/NCI.csv` para el Nasdaq Crypto Index y obtiene la tasa libre de riesgo DGS3MO desde FRED; si FRED no responde, usa la serie de respaldo en el CSV existente.

## Estado de Verificacion

- Dataset final: 499 filas, 88 columnas, 0 faltantes, 0 fechas duplicadas.
- Tabla maestra: 10 activos, 38 columnas, 0 faltantes.
- Evidencia de seleccion: 10 activos, 0 faltantes.
- Notebook ejecutado correctamente de principio a fin.
- Siete graficos finales presentes en `04_graficos/`.

## Taller Segunda Edición (SOL y KOPN)

Se ha creado la carpeta especializada `07_taller_segunda_edicion/` dedicada exclusivamente al análisis econométrico riguroso (OLS vs HC1 vs Newey-West HAC) y estudio empresarial/financiero de los activos **SOL** y **KOPN**.

Ver detalle completo en [07_taller_segunda_edicion/README.md](file:///wsl.localhost/Ubuntu/home/julianxd/code/DEFI%202/TALLER%201/07_taller_segunda_edicion/README.md).

Pendiente manual: compilar `03_informe/informe_ejecutivo_taller_1.tex` y `03_informe/ficha_personajes_activos.tex` en Overleaf o en un equipo con LaTeX instalado, porque este entorno no tiene `pdflatex`.
