# Guía Teórica y Econométrica: Modelos OLS, HC1 y Newey-West HAC

**Materia:** Valoración de Activos (DEFI 2)  
**Estudiante:** Julián Duarte  
**Tema:** Corrección de Errores Estándar en Regresiones CAPM en Palabras Sencillas  

---

## 1. El Desafío Econométrico en los Retornos Financieros

Cuando estimamos el modelo **CAPM** mediante Mínimos Cuadrados Ordinarios (MCO u OLS por sus siglas en inglés):

$$R_{i,t} - R_{f,t} = \alpha_i + \beta_i (R_{m,t} - R_{f,t}) + \varepsilon_{i,t}$$

Buscamos calcular dos valores clave: el **Alpha ($\alpha_i$)** (retorno anormal) y la **Beta ($\beta_i$)** (sensibilidad al riesgo de mercado). Sin embargo, el método tradicional OLS asume dos hipótesis ideales sobre el término de error $\varepsilon_{i,t}$ que **casi nunca se cumplen en los mercados financieros reales**:

1. **Homocedasticidad:** Asume que la variabilidad de los errores es constante a lo largo del tiempo ($\text{Var}(\varepsilon_t) = \sigma^2$).
2. **Ausencia de Autocorrelación:** Asume que el error de hoy no guarda ninguna relación con el error de ayer ($\text{Cov}(\varepsilon_t, \varepsilon_{t-j}) = 0$).

---

## 2. ¿Qué Falla en la Vida Real? Los Dos Problemas

### 2.1. El Agrupamiento de Volatilidad (*Volatility Clustering*)
En los activos financieros (y muy especialmente en criptoactivos como **SOL** y penny stocks como **KOPN**), existen días de calma absoluta seguidos de rachas de turbulencia extrema. La varianza de los retornos no es constante: **cambia día a día**. Esto destruye el supuesto de homocedasticidad y provoca **heterocedasticidad**.

> **Consecuencia de ignorar la heterocedasticidad:**  
> La estimación puntual de la Beta ($\hat{\beta}$) sigue siendo insesgada, pero **el Error Estándar (SE) calculado por OLS está mal**. OLS suele subestimar el verdadero riesgo del estimador, dando intervalos de confianza engañosamente estrechos y haciendo que Betas poco confiables parezcan "estadísticamente significativas".

---

### 2.2. Autocorrelación Residual y Negociación No Sincrónica
En activos con baja liquidez (como **KOPN**), los títulos no se negocian continuamente cada segundo. Los efectos de microestructura de mercado, diferencias en el horario de cierre y momentos de liquidez dispersa hacen que los retornos de un día se traslapen con los del día siguiente. Esto genera **autocorrelación en los residuos**.

---

## 3. Las Soluciones Econométricas Explicadas en Palabras Sencillas

Para corregir estos fallos sin alterar la pendiente de la recta, aplicamos estimadores robustos de la matriz de varianzas y covarianzas:

### 3.1. Modelo OLS Estándar (El Modelo Naive)
* **¿Qué hace?** Asume que el mundo es perfecto: todos los residuos tienen exactamente la misma varianza y son totalmente independientes.
* **Fórmula de Varianza de Beta:**
$$\widehat{\text{Var}}_{\text{OLS}}(\hat{\beta}) = s^2 (X^T X)^{-1}$$

---

### 3.2. Modelo HC1 / H1C (Heteroskedasticity Consistent - White con Grados de Libertad)
* **¿Qué hace?** Permite que cada residuo $e_i$ tenga su propia varianza. Ajusta el cálculo multiplicando los residuos por un factor de corrección de grados de libertad $\frac{n}{n-k}$.
* **¿Cuándo se usa?** Cuando los residuos muestran heterocedasticidad (varianza cambiante), pero **no tienen autocorrelación**.
* **Fórmula:**
$$\widehat{\text{Var}}_{\text{HC1}}(\hat{\beta}) = \frac{n}{n-k} (X^T X)^{-1} \left( \sum_{i=1}^n e_i^2 x_i x_i^T \right) (X^T X)^{-1}$$

---

### 3.3. Modelo Newey-West / HAC (Heteroskedasticity and Autocorrelation Consistent)
* **¿Qué hace?** Es la solución completa. Corrige **SIMULTÁNEAMENTE** la varianza cambiante (heterocedasticidad) **Y** la correlación entre días seguidos (autocorrelación).
* **¿Cómo lo logra?** Utiliza un núcleo de ponderación de rezagos (núcleo de *Bartlett*), donde asigna mayor peso a la correlación con el día inmediatamente anterior ($t-1$) y atenúa linealmente el peso conforme aumentan los rezagos ($L=5$ días en series diarias).
* **Fórmula:**
$$\widehat{\text{Var}}_{\text{HAC}}(\hat{\beta}) = (X^T X)^{-1} \hat{\Omega}_{\text{HAC}} (X^T X)^{-1}$$
$$\hat{\Omega}_{\text{HAC}} = \hat{\Gamma}_0 + \sum_{j=1}^{L} \left(1 - \frac{j}{L+1}\right) (\hat{\Gamma}_j + \hat{\Gamma}_j^T)$$

---

## 4. Evidencia Empírica: Comparativa en SOL y KOPN

A continuación se presentan los resultados numéricos reales obtenidos en el pipeline econométrico para **SOL** y **KOPN**:

| Activo | Modelo Econométrico | Beta ($\hat{\beta}$) | Error Estándar (SE) | Intervalo de Confianza al 95% | Ancho del IC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SOL** | **OLS (Homocedástico)** | 1.2529 | 0.03997 | [1.1744 , 1.3314] | 0.1570 |
| **SOL** | **HC1 (Robusto Volatilidad)** | 1.2529 | 0.04830 | [1.1583 , 1.3476] | 0.1893 |
| **SOL** | **Newey-West (HAC Vol.+Autocorr.)** | **1.2529** | **0.04579** | **[1.1632 , 1.3427]** | **0.1795** |
| | | | | | |
| **KOPN** | **OLS (Homocedástico)** | 1.8228 | 0.15033 | [1.5274 , 2.1182] | 0.5908 |
| **KOPN** | **HC1 (Robusto Volatilidad)** | 1.8228 | 0.12604 | [1.5758 , 2.0698] | 0.4940 |
| **KOPN** | **Newey-West (HAC Vol.+Autocorr.)** | **1.8228** | **0.12700** | **[1.5739 , 2.0717]** | **0.4978** |

---

## 5. Conclusiones y Diagnóstico Financiero

1. **La Beta puntual ($\hat{\beta}$) es idéntica:** La pendiente de la regresión no cambia ($1.2529$ para SOL y $1.8228$ para KOPN). Lo que se corrige es la **precisión estadística de nuestro conocimiento sobre esa Beta**.
2. **Impacto en SOL:** En Solana, el Error Estándar sube de $0.0400$ (OLS) a $0.0458$ (Newey-West). OLS estaba **subestimando la incertidumbre en un 14.5%** debido al agrupamiento de volatilidad en las criptomonedas.
3. **Impacto en KOPN:** En Kopin Corp, el SE baja de $0.1503$ (OLS) a $0.1270$ (Newey-West) al ajustar adecuadamente la estructura de varianza residual ponderada en días de negociación irregular.
4. **Regla de Decisión:** En valoración de activos profesionales, **siempre debemos utilizar el estimador Newey-West (HAC)** para evitar conclusiones falsas sobre la significancia de los parámetros financieros.
