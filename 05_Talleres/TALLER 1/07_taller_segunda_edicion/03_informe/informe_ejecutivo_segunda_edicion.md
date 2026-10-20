# Informe Ejecutivo - Taller Segunda Edición (CAPM: SOL y KOPN)

**Materia:** Valoración de Activos (DEFI 2)  
**Estudiante:** Julián Duarte  
**Fecha:** Septiembre de 2026  

---

## 1. Resumen Ejecutivo y Pregunta de Investigación

### Pregunta Central
¿Qué nos revela el Modelo de Valoración de Activos de Capital (CAPM), robustecido mediante errores estándar **HC1** y **Newey-West (HAC)**, sobre el comportamiento de riesgo y retorno de un criptoactivo líder (**SOL**) frente al mercado cripto (**NCI**) y de una *penny stock* de tecnología militar (**KOPN**) frente al sector tecnológico general (**XLK**)?

### Principales Hallazgos
1. **Solana (SOL):** Registra una **Beta robusta ($\hat{\beta}_{\text{HAC}}$) de 1.25** frente al Nasdaq Crypto Index ($R^2 = 0.664$). Es un activo cripto de alta beta (25% más sensible que el mercado cripto general). Presenta un **Maximum Drawdown (MDD) de -75.4%** y una volatilidad anualizada del **78.4%**. No se puede prometer retorno garantizado sin riesgo: su elevado rendimiento esperado viene estrictamente condicionado a la volatilidad del ciclo cripto.
2. **Kopin Corporation (KOPN):** Presenta una **Beta robusta ($\hat{\beta}_{\text{HAC}}$) de 1.82** frente al sector tecnológico XLK, pero con un **$R^2$ de solo 0.228**. Esto demuestra que el **77.2% de la variabilidad del precio de KOPN obedece a riesgo idiosincrásico** (adjudicación de contratos del Departamento de Defensa de EE. UU., patentes de micro-pantallas y anuncios trimestrales de ganancias). Su iliquidez de Amihud ($1.28 \times 10^{-6}$) evidencia fricción de mercado típica de penny stocks.

---

## 2. Tabla Maestra de Resultados Financieros y Econométricos

| Parámetro / Métrica | Solana (SOL) | Kopin Corporation (KOPN) |
| :--- | :--- | :--- |
| **Benchmark Asignado** | Nasdaq Crypto Index (NCI) | Technology Select Sector SPDR (XLK) |
| **Calendario ($K$)** | 365 días (Continuo) | 252 días (Bursátil) |
| **Alpha Anual ($\alpha$)** | **+21.45%** | **-18.32%** |
| **Beta OLS ($\hat{\beta}_{\text{OLS}}$)** | 1.2529 (SE: 0.0400) | 1.8228 (SE: 0.1503) |
| **Beta HC1 ($\hat{\beta}_{\text{HC1}}$)** | 1.2529 (SE: 0.0483) | 1.8228 (SE: 0.1260) |
| **Beta Newey-West ($\hat{\beta}_{\text{HAC}}$)** | **1.2529 (SE: 0.0458)** | **1.8228 (SE: 0.1270)** |
| **IC 95% Beta (HAC)** | **[1.1632 , 1.3427]** | **[1.5739 , 2.0717]** |
| **Bondad de Ajuste ($R^2$)** | **0.6641** | **0.2283** |
| **Retorno Observado Anual** | **+68.20%** | **-12.45%** |
| **Retorno CAPM Requerido** | **+46.75%** | **+18.12%** |
| **Volatilidad Anualizada** | **78.45%** | **94.22%** |
| **Ratio de Sharpe** | **0.818** | **-0.174** |
| **Ratio de Sortino** | **1.245** | **-0.241** |
| **Maximum Drawdown (MDD)** | **-75.45%** | **-63.55%** |
| **VaR 95% Diario** | **-6.85%** | **-8.12%** |
| **CVaR 95% Diario** | **-9.92%** | **-11.85%** |
| **% Retornos Cero** | **0.00%** | **6.75%** |
| **Iliquidez de Amihud** | $2.41 \times 10^{-10}$ | $1.28 \times 10^{-6}$ |
| **Beta Bajista ($\beta^-$)** | 1.3150 | 1.6420 |
| **Beta Dimson (Suma)** | 1.2810 | 2.0450 |

---

## 3. Síntesis Financiera y Empresarial

### 3.1. Kopin Corporation (KOPN)
* **Perfil:** Desarrollador micro-cap de micro-pantallas AR/VR y módulos ópticos para cascos de combate de la Fuerza Aérea de EE. UU. (ej. F-35) y visores quirúrgicos.
* **Diagnóstico de Negocio:** Aunque KOPN cuenta con propiedad intelectual sólida y contratos de defensa con Raytheon y Collins Aerospace, su baja escala ($< \text{USD } 1.00$ por acción) y dependencia del gasto federal provocan pérdidas operativas persistentes. La Beta de 1.82 debe interpretarse junto con su alta iliquidez de Amihud y su elevado porcentaje de días sin retorno (6.75%), indicando fragilidad ante shocks de liquidez.

### 3.2. Solana (SOL)
* **Perfil:** Blockchain Layer-1 de alta velocidad (PoH+PoS) con adopción masiva en finanzas descentralizadas (DeFi) y volúmenes de negociación DEX.
* **Diagnóstico de Negocio:** SOL funciona como una apuesta de alta beta sobre la adopción cripto global. Genera retornos superiores en fases alcistas ($\text{Sharpe} = 0.818$), pero exige tolerar una caída máxima de $-75.45\%$.

### 3.3. Explicación del Retorno Requerido del CAPM ($E(R_i)$)
* **Concepto:** El **Retorno Requerido por el CAPM** es la rentabilidad mínima exigida por los inversionistas para compensar únicamente el **riesgo sistemático** no diversificable.
* **Fórmula Matemática:**
  $$E(R_i) = R_f + \beta_i \cdot \left[ E(R_m) - R_f \right]$$
* **Desglose de Componentes:**
  - $R_f$: Tasa libre de riesgo ($4.35\%$ anual basada en T-Bills a 3 meses).
  - $\beta_i$: Sensibilidad del activo frente a su benchmark ($\hat{\beta}_{\text{HAC}} = 1.2529$ para SOL y $1.8228$ para KOPN).
  - $E(R_m) - R_f$: Prima de riesgo del mercado ($33.88\%$ en NCI y $7.55\%$ en XLK).
* **Cálculo de Resultados:**
  - **Solana (SOL):** $E(R_{\text{SOL}}) = 4.35\% + 1.2529 \times (33.88\%) = \mathbf{+46.75\%}$. Como su retorno observado fue de $+68.20\%$, genera un **Alpha de Jensen positivo ($\alpha = +21.45\%$)**.
  - **Kopin Corp (KOPN):** $E(R_{\text{KOPN}}) = 4.35\% + 1.8228 \times (7.55\%) = \mathbf{+18.12\%}$. Como su retorno observado fue de $-12.45\%$, genera un **Alpha de Jensen negativo ($\alpha = -18.32\%$)**.

---

## 4. Conclusión Econométrica: ¿Por qué usar Newey-West HAC?

Los datos de precios diarios presentan **agrupamiento de volatilidad** (*volatility clustering*) y **autocorrelación residual**. El estimador MCO (OLS) tradicional subestima los errores estándar en SOL (0.0400 vs 0.0458 en HAC), vendiendo una falsa sensación de precisión. Al utilizar **Newey-West HAC**, ajustamos la varianza con $L=5$ rezagos de Bartlett, garantizando intervalos de confianza científicamente válidos.

---

## 5. Recomendación Estructurada de Inversión

1. **Portafolio Conservador (Preservación):** $0\%$ asignación a KOPN y máximo $2\%$ a SOL. La volatilidad y drawdowns del $>60\%$ son incompatibles con la conservación de capital.
2. **Portafolio de Crecimiento:** Mantener SOL hasta un $5\%-8\%$ como activo de alta beta cripto. Excluir KOPN por contar con un Alpha negativo ($-18.32\%$).
3. **Portafolio Especulativo Acotado:** Limitar KOPN a un máximo de $1\%$ del portafolio como *call option* sobre la adjudicación de nuevos contratos de defensa, presupuestando stop-loss estricto.
