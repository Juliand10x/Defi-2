# DEFI 2 · Valoración de Activos

Repositorio de trabajo para la asignatura **Valoración de Activos** de la Universidad Externado de Colombia. Reúne lecturas, datos, talleres, notebooks y el desarrollo incremental de una aplicación de valoración y riesgo.

## Aplicación

La aplicación vive en [`06_App/`](06_App). Su primera versión se enfoca en la experiencia de usuario: permite seleccionar y editar acciones, clasificar sectores, configurar capital y parámetros de riesgo, y revisar el portafolio antes de iniciar los cálculos cuantitativos.

### Ejecutar localmente

```bash
cd 06_App
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

### Despliegue con Streamlit Community Cloud

1. Conecta este repositorio en [Streamlit Community Cloud](https://share.streamlit.io/).
2. Elige la rama `main` y como archivo principal `06_App/app.py`.
3. La plataforma instalará automáticamente las dependencias de `06_App/requirements.txt`.
4. Comparte el enlace generado para revisar cada avance de la aplicación.

## Estructura

```text
01_Libros_y_Lecturas/  Bibliografía, artículos y papers
02_Simulador_CME/      Material del simulador CME
03_Datos_y_Tablas/     Datos y tablas de apoyo
04_Codigos_Clase/      Notebooks de clase
05_Talleres/           Talleres desarrollados
06_App/                Aplicación de valoración y riesgo
07_Preparcial_Final/   Material de preparación final
```

## Próximo hito

Validar la interfaz inicial de `06_App` y luego integrar descarga de datos, validación de calidad y motores de valoración/riesgo de acuerdo con el taller.
