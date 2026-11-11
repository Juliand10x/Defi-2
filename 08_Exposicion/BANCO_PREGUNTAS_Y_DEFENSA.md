# Banco de Preguntas y Defensa Oral: Opciones Reales

**Asignatura:** Valoración de Activos (DEFI 2)  
**Institución:** Universidad Externado de Colombia  
**Estudiante expositor:** Julián Duarte  
**Tema:** Valuación Financiera de Proyectos con Opciones Reales (*Real Options*)  
**Fuentes Oficiales:** Francisco Venegas Martínez (2009, Cap. 69), Dixit & Pindyck (1994), Hull (2012).

---

## 🛡️ Las 4 Preguntas Clave y Cómo Defenderte Frente al Profesor y Compañeros

### Pregunta 1 (La clásica del profesor de finanzas corporativas):
> *"Julián, en valoración de empresas siempre nos insisten en que los flujos de un proyecto riesgoso deben descontarse a la tasa del costo de capital (WACC o $K_e$). ¿Por qué en la fórmula del árbol binomial (CRR) descuentan los flujos con la tasa libre de riesgo $r$ y no con el WACC?"*

* **Tu Respuesta Maestra:**
  > *"Excelente pregunta, profesor. Si descontáramos con el WACC en el árbol binomial estaríamos cometiendo un **doble castigo por riesgo**.  
  > En la metodología de Cox, Ross y Rubinstein (y como explica Venegas en la ecuación 69.28), el ajuste por riesgo ya no se hace en la tasa de descuento del denominador, sino en el numerador, a través del cambio de medida a las **probabilidades neutrales al riesgo ($q$)**.  
  > En ese 'mundo neutral al riesgo ficticio', todos los activos crecen a la tasa libre de riesgo $r$, y por el Teorema Fundamental de Valoración de Activos (ausencia de arbitraje), el único factor de descuento matemáticamente consistente es $e^{-r\Delta t}$. Si usáramos el WACC, estaríamos penalizando el riesgo dos veces."*

---

### Pregunta 2 (La del compañero escéptico sobre la práctica):
> *"Eso se ve muy bonito en la teoría matemática, pero si la fábrica o la mina no cotizan en bolsa, ¿de dónde sacas la volatilidad $\sigma$ de los flujos en la vida real?"*

* **Tu Respuesta Maestra:**
  > *"Es la crítica más común a las opciones reales y tiene tres soluciones estándar en la industria (planteadas por Copeland & Antikarov y Damodaran):  
  > 1. **Activo gemelo (*Twin Security*):** Si evaluamos un pozo de petróleo o una mina de cobre, la volatilidad $\sigma$ se extrae directamente de los contratos de futuros del crudo (WTI/Brent) o del cobre en el mercado de materias primas.  
  > 2. **Empresas comparables puras (*Pure-play peers*):** Usamos la volatilidad no apalancada ($\sigma_{unlevered}$) de acciones de empresas públicas del mismo sector y tamaño.  
  > 3. **Simulación de Monte Carlo:** Modelamos las variables operativas (precio de venta, demanda, costos) con distribuciones de probabilidad, simulamos 10.000 trayectorias del VPN del proyecto y calculamos la desviación estándar de sus rendimientos intertemporales."*

---

### Pregunta 3 (El dilema de la competencia):
> *"¿Qué pasa si decidimos 'esperar' (opción de posponer), pero mientras esperamos entra un competidor y nos quita el mercado?"*

* **Tu Respuesta Maestra:**
  > *"Ese es el concepto de **Opciones Reales Compartidas vs. Exclusivas** formulado por Dixit y Pindyck (1994).  
  > Una patente farmacéutica o una concesión minera exclusiva es una opción **propietaria** (nadie nos la puede quitar). Pero en mercados abiertos sin barreras de entrada, la opción es **compartida**: el costo de diferir la inversión no es solo el valor del dinero en el tiempo, sino el riesgo de que un competidor nos 'canibalice' el mercado.  
  > Matemáticamente, esto se modela reduciendo el valor del subyacente $S_t$ mediante una tasa continua de dividendos $\delta$ (que representa la pérdida de cuota de mercado por esperar), similar a valuar un Call sobre una acción que paga dividendos."*

---

### Pregunta 4 (Sobre el modelo continuo vs. discreto):
> *"¿Por qué no usamos simplemente la fórmula directa de Black-Scholes y nos evitamos dibujar todo el árbol binomial?"*

* **Tu Respuesta Maestra:**
  > *"Por dos razones estructurales que advierte Venegas Martínez en el capítulo 69:  
  > 1. **La condición americana:** Black-Scholes estándar asume opciones europeas (ejercicio únicamente en el vencimiento $T$). Pero la flexibilidad gerencial real es **americana**: la decisión de liquidar la planta o ampliarla se puede tomar en cualquier mes o año intermedio.  
  > 2. **Transparencia gerencial:** Un árbol binomial permite a la junta directiva y a los directores de operaciones ver las reglas de decisión explícitas en cada nodo y horizonte de tiempo, algo que una fórmula cerrada de integrales oculta como una 'caja negra'."*

