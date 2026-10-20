# NEXA · Valoración y Riesgo

Primera base visual de la aplicación del taller. Permite configurar un universo de acciones, editar sectores, definir parámetros de riesgo y revisar la decisión antes de calcular.

## Ejecutar

```bash
cd 06_App
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```

## Estado actual

- Interfaz navegable y persistente durante la sesión.
- Preset académico de 10 acciones y edición dinámica de tickers/sectores.
- Configuración de capital, perfil, VaR, tasa y período de análisis.
- Validaciones visuales para los requisitos de 10 activos y 4 sectores.

La conexión con Yahoo Finance y los motores cuantitativos se implementarán tras aprobar esta experiencia de usuario.
