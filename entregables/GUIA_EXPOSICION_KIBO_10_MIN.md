# Guía de exposición de Kibo

**Duración máxima:** 10 minutos  
**Objetivo:** explicar qué problema resuelve la app, cómo convierte datos de mercado en una propuesta de portafolio y qué límites tiene el análisis.

## Hilo conductor

Presenta Kibo como un copiloto de análisis financiero. La persona define un capital simulado, un perfil y un universo de acciones; la app estima riesgo, compara modelos y muestra una asignación con opciones de protección. La idea que conecta toda la exposición es: **hacer visible cómo cambian las decisiones cuando cambian el riesgo y los supuestos**.

## Agenda cronometrada

| Tiempo | Sección | Qué decir o mostrar |
|---|---|---|
| 0:00–0:45 | Apertura | Presenta el reto: comparar alternativas de inversión y riesgo sin operar con dinero real. |
| 0:45–1:40 | Recorrido de la app | Explica el flujo de seis pasos: capital, perfil, acciones, modelos, opciones y portafolio. |
| 1:40–2:40 | Parámetros | Muestra el presupuesto de riesgo y las opciones avanzadas de horizonte y confianza. Señala que los valores sugeridos se pueden ajustar. |
| 2:40–4:00 | Acciones y modelos | Explica la diversificación por sectores y que la app compara varios modelos para describir escenarios posibles. |
| 4:00–5:45 | Opciones y simulador | Compara un Put y un Call en términos sencillos. Mueve el escenario de precio y muestra cómo cambian el resultado de las acciones, de la opción y el combinado. |
| 5:45–7:45 | Portafolio y riesgo | Enseña la asignación, el VaR, las pruebas de estrés y el efectivo que queda tras comprar acciones enteras. |
| 7:45–9:00 | Decisión | Resume qué aportan el horizonte, la confianza, el presupuesto de riesgo y los costos de transacción. |
| 9:00–10:00 | Límites y cierre | Aclara que son estimaciones sujetas a datos y supuestos; cierra con la utilidad de comparar escenarios antes de decidir. |

## Guion sugerido

### 0:00–0:45 · Apertura

> Buenos días. Kibo es una aplicación para explorar decisiones de inversión y gestión de riesgo en un solo recorrido. Su propósito es traducir herramientas cuantitativas a resultados que podamos comparar y entender. El capital de la demostración es simulado: no se ejecutan compras ni se conecta una cuenta bancaria.

### 0:45–1:40 · Recorrido

> La experiencia tiene seis pasos. Primero definimos el capital; luego el perfil y las acciones que queremos analizar. Después revisamos los modelos, exploramos contratos de opciones y finalmente vemos la asignación del portafolio y sus medidas de riesgo.

Muestra brevemente el indicador de avance y evita leer todos los controles.

### 1:40–2:40 · Parámetros

> El perfil propone valores iniciales, pero una persona que quiera profundizar puede cambiar el horizonte de análisis y el nivel de confianza. También puede fijar un presupuesto de riesgo. Estos parámetros alteran los cálculos posteriores, por eso los resultados deben leerse junto con los supuestos elegidos.

Abre el panel avanzado, enseña las opciones y continúa. No te detengas a explicar cada campo.

### 2:40–4:00 · Acciones y modelos

> La selección de acciones determina el universo de análisis. La diversificación permite observar exposiciones por sector. Luego Kibo compara modelos con comportamientos distintos: algunos representan variaciones continuas y otros incorporan saltos o reversión a la media. Ninguno predice el futuro; cada uno ofrece una forma diferente de explorar escenarios.

Muestra una comparación o un gráfico. No enumeres todas las fórmulas.

### 4:00–5:45 · Opciones y simulador

> Una opción es un contrato cuyo resultado depende del precio futuro de una acción. Un Put puede compensar una caída por debajo del strike; un Call puede aportar valor si el precio supera el strike. Ambos tienen una prima.

En la app, selecciona un contrato y mueve el control de variación del precio. Muestra los tres resultados: acciones, opción y combinación. Explica que el ejemplo representa 100 acciones y un contrato estándar, y que la prima se resta del resultado de la opción.

### 5:45–7:45 · Portafolio y riesgo

> En el último paso vemos cuánto asigna el modelo a cada acción, el riesgo estimado para el horizonte elegido y el efectivo que sobra al convertir montos teóricos en acciones enteras. Las pestañas permiten revisar VaR, escenarios de estrés y evaluación histórica.

Señala que el VaR es una estimación asociada a un horizonte y nivel de confianza; no es una pérdida máxima garantizada. Muestra el resumen y una tabla, sin recorrer todas las filas.

### 7:45–9:00 · Decisión

> La utilidad de Kibo está en comparar cómo cambia la propuesta cuando modificamos los supuestos. Un horizonte mayor, otra confianza, un presupuesto más bajo o costos distintos pueden cambiar el riesgo y la asignación. La app deja esos supuestos visibles para que la decisión no dependa de un único número.

### 9:00–10:00 · Límites y cierre

> Kibo es una herramienta de análisis y aprendizaje, no una promesa de rentabilidad ni una recomendación personalizada. Los resultados dependen de los datos disponibles y de los modelos elegidos. Su aporte es reunir escenarios, opciones y riesgo en una secuencia que facilita comparar decisiones antes de actuar. Muchas gracias.

## Preparación de la demostración

1. Abre la app antes de comenzar y confirma que carga los datos.
2. Lleva una ruta breve: perfil → acciones → modelos → opción → portafolio.
3. En el simulador de opciones, cambia el precio al menos una vez para mostrar la actualización de los resultados.
4. Abre solo los paneles avanzados que ayuden a explicar una decisión.
5. Si la consulta de mercado no está disponible, presenta los resultados ya cargados o una captura preparada y explica que la fuente de datos puede no responder.
6. Deja al menos 30 segundos para cerrar y evita navegar por tablas completas.

## Preguntas que pueden hacerte

- **¿El VaR dice cuánto se perderá con certeza?** No. Es una estimación bajo supuestos, un horizonte y un nivel de confianza.
- **¿La app ejecuta operaciones?** No; el capital se usa para simulación y análisis.
- **¿Por qué comparar modelos?** Porque cada uno representa dinámicas distintas y permite ver cuánto dependen las conclusiones del modelo escogido.
- **¿El Put elimina todo el riesgo?** No. Su protección depende del strike, vencimiento y prima; además, persisten otros riesgos del portafolio.
- **¿Qué puede cambiar los resultados?** Los datos, el horizonte, la confianza, las acciones, el presupuesto y los costos asumidos.

## Reparto opcional entre dos personas

Si exponen dos personas, quien inicia puede cubrir el problema, el flujo y los parámetros hasta el minuto 4. La segunda persona puede tomar la demostración de opciones, el portafolio, los límites y el cierre. Mantengan el mismo hilo conductor y ensayen el cambio de voz para no perder tiempo.
