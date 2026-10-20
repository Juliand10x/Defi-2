# 🎭 GUÍA DE PRESENTACIÓN Y STORYTELLING PARA EL ONE-PAGER
## *Guion de Sustentación Ejecutiva: La Beta de los Pobres y el Espejismo del 25%*
**Materia:** Valoración de Activos (DEFI 2)  
**Expositor:** Julián Duarte | Universidad Externado de Colombia  
**Soporte Visual:** Dashboard Interactivo One-Pager (`one_pager_dashboard.html`)

---

## 🗺️ GUÍA RÁPIDA DE NAVEGACIÓN VISUAL EN EL DASHBOARD

Para no perderte durante la exposición, el Dashboard Interactivo de la pantalla tiene **3 Paneles Principales**:

1. **Panel Izquierdo (Expedientes por Sector):** Contiene las tarjetas interactivas de los 10 activos (`SOL`, `KOPN`, `MVIS`, `LIDR`, `GERN`, `CTMX`, `OCGN`, `BORR`, `KLXE`, `TTI`).
2. **Panel Central (Evidencia Conectora - 4 Pestañas de Gráficas):**
   * 🔘 Botón 1: **`🗺️ Beta vs MDD`** (Muestra el mapa de Beta vs Caída Máxima Acumulada).
   * 🔘 Botón 2: **`📈 Brecha CAPM`** (Muestra el gráfico comparativo de Retorno Real vs Retorno Exigido CAPM).
   * 🔘 Botón 3: **`🏆 Percentiles`** (Muestra la matriz de evaluación sintética multicriterio).
   * 🔘 Botón 4: **`💧 Liquidez`** (Muestra la iliquidez de Amihud y días de retorno cero).
3. **Panel Derecho (`⚖️ Decisión Doña Victoria`):** Las 3 tarjetas de mandatos de inversión (*Conservación*, *Crecimiento*, *Especulación*).

---

## 🏢 RADIOGRAFÍA DE LOS 10 ACTIVOS Y BENCHMARKS

* **ETFs (Exchange-Traded Funds / Fondos Cotizados):** Canastas diversificadas que cotizan en bolsa. Usamos **XLK** (Tecnología), **XBI** (Biotecnología), **XLE** (Energía) y **NCI** (Nasdaq Crypto Index).
* **Tecnología (Benchmark XLK):**
  * **KOPN (Kopin Corp):** Fabrica micropantallas ópticas de alta resolución para cascos de aviación militar.
  * **MVIS (MicroVision Inc):** Desarrolla sensores LiDAR y escaneo láser para conducción autónoma.
  * **LIDR (AEye Inc):** Desarrolla sistemas de percepción espacial adaptativa LiDAR para vehículos.
* **Biotecnología (Benchmark XBI):**
  * **GERN (Geron Corp):** Biofarmacéutica comercial en oncología (*Rytelo* para cáncer de médula).
  * **CTMX (CytomX Therapeutics):** Oncología de precisión con plataforma de anticuerpos *Probody*.
  * **OCGN (Ocugen Inc):** Desarrolla terapias génicas contra la ceguera y vacunas.
* **Energía (Benchmark XLE):**
  * **BORR (Borr Drilling):** Opera plataformas de perforación petrolera marina en aguas someras (*jack-ups*).
  * **KLXE (KLX Energy Services):** Servicios de intervención y equipos para pozos de hidrocarburos.
  * **TTI (TETRA Technologies):** Química de fluidos y tratamiento de agua para *fracking* (excepción < $10 USD).
* **Criptoactivos (Benchmark NCI):**
  * **SOL (Solana):** Blockchain de capa 1 de alta velocidad para finanzas descentralizadas.

---

## 🎬 ACTO I: EL GANCHO Y LA ILUSIÓN DEL 25% SIN RIESGO
*(Duración estimada: 2.5 minutos)*

### 🔘 DÓNDE UBICARTE EN EL DASHBOARD:
1. Haz clic en el **Panel Izquierdo** para mostrar los 10 activos organizados por sector.
2. En el **Panel Central**, asegúrate de tener seleccionada la pestaña **`📈 Brecha CAPM`**.

### 🗣️ GUION NARRATIVO (QUÉ DECIR):

> *"Buenas tardes, Profesor, y buenas tardes a todos los presentes.*
>
> *Hoy venimos a resolver un desafío cuantitativo y humano. Doña Victoria, representante de una familia inversionista, nos planteó una meta financiera que atrae a cualquiera: **¿Es posible obtener una rentabilidad del 25% anual sin exponer nuestro capital a caídas?***
>
> *Para responder a esto, construimos un procedimiento riguroso en **7 Pasos**: descargamos 499 días de cotizaciones de Yahoo Finance, registramos el índice Nasdaq Crypto Index (NCI) y tomamos la tasa de los Títulos del Tesoro a 3 meses (FRED DGS3MO al 5.2% anual) como nuestro activo libre de riesgo.*
>
> *Evaluamos 10 expedientes de inversión divididos en tres sectores clave de acciones de bajo precio —Tecnología (Kopin, MicroVision, AEye), Biotecnología (Geron, CytomX, Ocugen) y Energía (Borr Drilling, KLX Energy, TETRA Technologies)— más el criptoactivo Solana.*
>
> *Cada uno fue emparejado contra su **ETF sectorial propio**: XLK para tecnología, XBI para biotecnología, XLE para energía y NCI para cripto. **Recordemos una regla de oro de la valoración de activos: jamás se compara la Beta de una criptomoneda con el sector energía.** Cada activo compite dentro de su ecosistema.*
>
> *Acompáñenme al Acto II para ver el veredicto del modelo econométrico."*

---

## 🎬 ACTO II: EL PASO A PASO ECONOMÉTRICO Y EL VEREDICTO DE ALFA
*(Duración estimada: 4 minutos)*

### 🔘 DÓNDE UBICARTE EN EL DASHBOARD:
1. Mantén abierta en el **Panel Central** la pestaña **`📈 Brecha CAPM`**.
2. Muestra las barras verdes (que superan lo exigido por el modelo) y las barras rojas (que destruyen valor).

### 🗣️ GUION NARRATIVO (QUÉ DECIR):

> *"Para procesar los datos, transformamos los precios en retornos logarítmicos y corrimos regresiones econométricas bajo el modelo CAPM:*
>
> $$\text{Exceso Activo}_t = \alpha + \beta \cdot \text{Exceso Mercado}_t + \epsilon_t$$
>
> *Profesor, sabemos que las series financieras sufren de **Heterocedasticidad** (días de volatilidad salvaje mezclados con días calmos). Si usáramos regresión OLS convencional, obtendríamos p-valores falsos. Por ello, estimamos los parámetros usando **errores estándar robustos HAC (Newey-West) y White HC1**, además de verificar la **Beta de Dimson** para ajustar por retrasos en la liquidez.*
>
> *Mirando nuestra gráfica de **`📈 Brecha CAPM`**, observamos qué nos dijeron la Beta ($\beta$) y el Alfa ($\alpha$):*
> 1. * **La Beta:** Mide la sensibilidad. Una beta de 1.82 en KOPN o 1.94 en KLXE significa que estas acciones son amplificadores: si el sector sube, vuelan; pero si el sector cae, se desploman el doble.*
> 2. * **El Alfa de Jensen:** Mide la recompensa neta real tras pagar el peaje del riesgo.*
>
> *El resultado econométrico fue contundente:* **Solo 4 de los 10 activos lograron generar Alfa positivo real (barras verdes en pantalla).**
>
> * * **Los 4 Ganadores de Alfa:** **KOPN** ($\alpha = +80.7\%$, retorno real del +130%), **CTMX** ($\alpha = +72.8\%$), **LIDR** ($\alpha = +60.1\%$) y **TTI** ($\alpha = +29.8\%$).*
> * * **Los 6 Destructores de Valor (barras rojas):** **MVIS** ($\alpha = -82.9\%$), **KLXE** ($\alpha = -67.8\%$), **GERN** ($\alpha = -64.1\%$), **BORR** ($\alpha = -29.5\%$) y **Solana (SOL)** ($\alpha = -28.9\%$).*
>
> *Fíjense en **Solana**: aunque tuvo un retorno nominal positivo del +4.6%, su beta de 1.25 exigía un 33.5% bajo CAPM. Solana destruyó 28.9 puntos porcentuales de valor ajustado por riesgo."*

---

## 🎬 ACTO III: LA CUEVA DE LOS MONSTRUOS (DRAWDOWNS E ILIQUIDEZ)
*(Duración estimada: 3.5 minutos)*

### 🔘 DÓNDE UBICARTE EN EL DASHBOARD (SIGUE ESTOS PASOS):
1. **Paso 1:** En el Panel Central, **HAZ CLIC EN EL BOTÓN `🗺️ Beta vs MDD`**.
2. **Paso 2:** Luego, **HAZ CLIC EN EL BOTÓN `💧 Liquidez`**.
3. **Paso 3:** Para resumir, **HAZ CLIC EN EL BOTÓN `🏆 Percentiles`**.

### 🗣️ GUION NARRATIVO (QUÉ DECIR):

> *(Al hacer clic en **`🗺️ Beta vs MDD`**):*
> *"Ahora bien, Doña Victoria podría decirnos: 'Julián, si KOPN rindió 130% o LIDR rindió 95%, ¡compremos eso y listo!'.*
>
> *Aquí es donde la Ciencia de Datos salva al inversionista. Los promedios ocultan el dolor del proceso. Al mirar nuestra gráfica de **`🗺️ Beta vs MDD`**, observen la esquina inferior derecha:*
> * * **MicroVision (MVIS)** sufrió un **Max Drawdown (Caída Máxima) del -93.9%**. Poner $100,000 USD allí significó ver desplomarse la cuenta a menos de $6,100 USD.*
> * * **LIDR**, a pesar de su alfa positivo, sufrió un drawdown del **-83.0%** y una volatilidad anualizada astronómica del **165.9%**.*
> * * **Solana (SOL)** registró una caída acumulada del **-75.4%**.*
>
> *(Haz clic ahora en el botón **`💧 Liquidez`**):*
> * *'A esto se suma la fragilidad operativa. Al cambiar a la pestaña de **`💧 Liquidez`**, vemos que **MVIS tuvo un 11.0% de días con retorno cero** (días sin operaciones por falta de compradores), y **KLXE** mostró una iliquidez de Amihud muy alta, lo que significa que intentar vender una posición grande destruye el precio en pantalla.'*
>
> *(Haz clic en **`🏆 Percentiles`** para mostrar la síntesis):*
> * *'En nuestra **`🏆 Matriz de Percentiles`** confirmamos de forma multicriterio que el veredicto para Doña Victoria es ineludible:* **El 25% anual sin caídas de capital es un espejismo.** Quien busque ese 25% debe estar preparado para ver caer su saldo más del 60% en el camino."*

---

## 🎬 ACTO IV: DE LA TEORÍA A LA ACCIÓN (LOS 3 MANDATOS)
*(Duración estimada: 2 minutos)*

### 🔘 DÓNDE UBICARTE EN EL DASHBOARD:
Dirígete al **Panel Derecho (`⚖️ Decisión Doña Victoria`)** y señala las 3 tarjetas de recomendación.

### 🗣️ GUION NARRATIVO (QUÉ DECIR):

> *"Para cerrar nuestra asesoría cuantitativa, observen el panel derecho de **`⚖️ Decisión Doña Victoria`**. Organizamos la recomendación en **Tres Mandatos de Inversión Claros**:*
>
> 1. **Mandato 1: Conservador / Preservación Familiar (Tarjeta Roja - Para Doña Victoria):**
>    * **Estrategia:** 100% en Títulos del Tesoro (DGS3MO al 5.2% anual) o 70% Treasuries + 30% ETFs sectoriales diversificados (XLE/XLK).
>    * **Resultado:** Rentabilidad esperada del **7.5% al 9.5% anual**, con una caída máxima limitada a **< -8%**. Tranquilidad absoluta.
>
> 2. **Mandato 2: Moderado / Crecimiento Equilibrado (Tarjeta Amarilla):**
>    * **Estrategia:** Indexarse a los ETFs sectoriales (`XLK`, `XLE`, `XBI`) + 30% Treasuries + 20% en Ganadores de Alfa (`TTI`, `KOPN`).
>    * **Resultado:** Rentabilidad del **14% al 18% anual**, soportando caídas temporales de hasta el **-22%**.
>
> 3. **Mandato 3: Especulación Acotada (Tarjeta Verde):**
>    * **Estrategia:** Asignar un cupo máximo del 1% al 2% en los campeones de Alfa (`KOPN`, `CTMX`, `LIDR`) o `SOL` con stop-loss del 15%.
>    * **Resultado:** Capturar rendimiento especulativo sin poner en riesgo el patrimonio familiar.
>
> *Muchas gracias, Profesor y jurado. Quedamos abiertos a sus preguntas."*

---

## ❓ PREGUNTAS DIFÍCILES ANTICIPADAS Y RESPUESTAS DE ALTO NIVEL

### P1: ¿Por qué usó errores estándar HAC / Newey-West en la estimación OLS?
* **Respuesta Técnica:** *"Las series financieras de retornos diarios presentan clústeres de volatilidad (heterocedasticidad) y autocorrelación. El estimador OLS convencional subestima los errores estándar, produciendo p-valores falsamente significativos. La corrección HAC (Heteroskedasticity and Autocorrelation Consistent) ajusta la matriz de covarianza con 5 rezagos, garantizando inferencia estadística insesgada."*

### P2: ¿Qué es la Beta de Dimson y cómo afectó a las acciones ilíquidas?
* **Respuesta Técnica:** *"En acciones de bajo precio como MVIS o KLXE, el volumen diario es bajo y la información de mercado se incorpora con rezago. La Beta de Dimson añade retornos de mercado del día anterior ($\text{Market}_{t-1}$) para capturar la sensibilidad diferida. Al calcular $\beta_{\text{Dimson Sum}}$, confirmamos que la alta sensibilidad de mercado persiste."*

### P3: ¿Qué significa exactamente un ETF?
* **Respuesta Técnica:** *"Un Exchange-Traded Fund es un instrumento financiero diversificado que replica un índice sectorial (como XLK en tecnología o XLE en energía). Nos sirve como Benchmark neutro para aislar el retorno del sector frente al Alfa propio de cada empresa."*
