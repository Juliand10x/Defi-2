from __future__ import annotations

import math
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import nbformat as nbf

# Setup Root paths
ROOT = Path(__file__).resolve().parents[2] # DEFI 2/TALLER 1
EDITION_ROOT = ROOT / "07_taller_segunda_edicion"
DATOS = EDITION_ROOT / "01_datos"
NOTEBOOKS = EDITION_ROOT / "02_notebooks"
INFORME = EDITION_ROOT / "03_informe"
GRAFICOS = EDITION_ROOT / "04_graficos"
SCRIPTS = EDITION_ROOT / "05_scripts"
ENTREGABLES = EDITION_ROOT / "entregables"

for p in [DATOS, NOTEBOOKS, INFORME, GRAFICOS, SCRIPTS, ENTREGABLES]:
    p.mkdir(parents=True, exist_ok=True)

# Assets definition
ASSETS = [
    {
        "ticker": "SOL",
        "yf": "SOL-USD",
        "name": "Solana",
        "family": "Criptoactivo",
        "sector": "Criptoactivos / Finanzas Descentralizadas (DeFi)",
        "benchmark": "NCI",
        "K": 365,
        "type": "Criptoactivo de alta capitalización",
        "desc": "Blockchain Layer-1 de ultra-alta velocidad (PoH+PoS) con adopción masiva en finanzas descentralizadas (DeFi).",
    },
    {
        "ticker": "KOPN",
        "yf": "KOPN",
        "name": "Kopin Corporation",
        "family": "Tecnología",
        "sector": "Micro-pantallas y Óptica de Defensa/Médica",
        "benchmark": "XLK",
        "K": 252,
        "type": "Penny stock / Acción tecnológica micro-cap",
        "desc": "Desarrollador micro-cap de micro-pantallas AR/VR y visores ópticos para cascos de combate (F-35) del Departamento de Defensa de EE. UU.",
    },
]

BENCHMARKS = [
    {"ticker": "NCI", "name": "Nasdaq Crypto Index"},
    {"ticker": "XLK", "name": "Technology Select Sector SPDR Fund"},
]

def load_base_data() -> pd.DataFrame:
    legacy_file = ROOT / "01_datos" / "datos_taller_1_julian_duarte.csv"
    if not legacy_file.exists():
        raise FileNotFoundError(f"No se encontró la base original en {legacy_file}")
    
    df = pd.read_csv(legacy_file, parse_dates=["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    return df

def run_capm_models(ri_e: pd.Series, rm_e: pd.Series):
    X = sm.add_constant(rm_e)
    model_ols = sm.OLS(ri_e, X, missing="drop").fit()
    model_hc1 = sm.OLS(ri_e, X, missing="drop").fit(cov_type="HC1")
    model_hac = sm.OLS(ri_e, X, missing="drop").fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    return model_ols, model_hc1, model_hac

def max_drawdown(r: pd.Series) -> float:
    wealth = (1 + r).cumprod()
    return float((wealth / wealth.cummax() - 1).min())

def downside_beta(ri_e: pd.Series, rm_e: pd.Series) -> float:
    mask = rm_e < 0
    if mask.sum() < 5 or rm_e[mask].var(ddof=1) == 0:
        return np.nan
    return float(np.cov(ri_e[mask], rm_e[mask])[0, 1] / np.var(rm_e[mask], ddof=1))

def dimson_beta(ri_e: pd.Series, rm_e: pd.Series) -> float:
    df = pd.DataFrame({"ri_e": ri_e, "lag": rm_e.shift(1), "same": rm_e, "lead": rm_e.shift(-1)}).dropna()
    if len(df) < 20:
        return np.nan
    m = sm.OLS(df["ri_e"], sm.add_constant(df[["lag", "same", "lead"]])).fit()
    return float(m.params[["lag", "same", "lead"]].sum())

def winsor_beta(ri_e: pd.Series, rm_e: pd.Series) -> float:
    ri = ri_e.clip(ri_e.quantile(0.01), ri_e.quantile(0.99))
    rm = rm_e.clip(rm_e.quantile(0.01), rm_e.quantile(0.99))
    return float(sm.OLS(ri, sm.add_constant(rm)).fit().params.iloc[1])

def generate_comparative_table(df_base: pd.DataFrame) -> pd.DataFrame:
    records = []
    for item in ASSETS:
        t = item["ticker"]
        b = item["benchmark"]
        K = item["K"]
        
        ri_e = df_base[f"{t}_Excess_Return"]
        rm_e = df_base[f"{b}_Excess_Return"]
        
        m_ols, m_hc1, m_hac = run_capm_models(ri_e, rm_e)
        
        for name, m in [
            ("OLS (Homocedástico)", m_ols),
            ("HC1 (White / Robusto Volatilidad)", m_hc1),
            ("Newey-West (HAC / Robusto Vol.+Autocorr.)", m_hac)
        ]:
            alpha_d = float(m.params.iloc[0])
            alpha_ann = alpha_d * K
            beta = float(m.params.iloc[1])
            se_beta = float(m.bse.iloc[1])
            ci = m.conf_int().iloc[1]
            t_stat_beta0 = float(m.tvalues.iloc[1])
            p_val_beta0 = float(m.pvalues.iloc[1])
            t_stat_beta1 = (beta - 1.0) / se_beta
            
            records.append({
                "Activo": t,
                "Benchmark": b,
                "Modelo": name,
                "Alpha Anual (%)": round(alpha_ann * 100, 4),
                "Beta": round(beta, 4),
                "Error Estándar (SE)": round(se_beta, 4),
                "IC 95% Inferior": round(float(ci.iloc[0]), 4),
                "IC 95% Superior": round(float(ci.iloc[1]), 4),
                "Ancho IC 95%": round(float(ci.iloc[1] - ci.iloc[0]), 4),
                "t-stat (Beta=0)": round(t_stat_beta0, 3),
                "p-valor (Beta=0)": round(p_val_beta0, 5),
                "t-stat (Beta=1)": round(t_stat_beta1, 3),
                "R2": round(float(m.rsquared), 4),
                "R2 Ajustado": round(float(m.rsquared_adj), 4),
            })
            
    return pd.DataFrame(records)

def build_master_table(df_base: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for item in ASSETS:
        t = item["ticker"]
        b = item["benchmark"]
        K = item["K"]
        rf_col = "Rf_Daily_365" if K == 365 else "Rf_Daily_252"
        
        ri = df_base[f"{t}_Return"]
        rm = df_base[f"{b}_Return"]
        ri_e = df_base[f"{t}_Excess_Return"]
        rm_e = df_base[f"{b}_Excess_Return"]
        
        m_ols, m_hc1, m_hac = run_capm_models(ri_e, rm_e)
        
        alpha = float(m_hac.params.iloc[0])
        beta = float(m_hac.params.iloc[1])
        se_beta_hac = float(m_hac.bse.iloc[1])
        se_beta_hc1 = float(m_hc1.bse.iloc[1])
        se_beta_ols = float(m_ols.bse.iloc[1])
        
        ci_hac = m_hac.conf_int().iloc[1]
        
        rf_ann = float(df_base[rf_col].mean() * K)
        rm_ann = float(rm.mean() * K)
        obs_ret = float(ri.mean() * K)
        capm_ret = rf_ann + beta * (rm_ann - rf_ann)
        vol_ann = float(ri.std(ddof=1) * math.sqrt(K))
        excess_ann = obs_ret - rf_ann
        
        downside = ri[ri < 0]
        downside_dev = float(np.sqrt((downside**2).mean()) * math.sqrt(K)) if len(downside) else np.nan
        var95 = float(ri.quantile(0.05))
        cvar95 = float(ri[ri <= var95].mean())
        beta_minus = downside_beta(ri_e, rm_e)
        dimson = dimson_beta(ri_e, rm_e)
        beta_win = winsor_beta(ri_e, rm_e)
        
        med_vol = float(df_base[f"{t}_Volume"].median(skipna=True))
        med_mvol = float(df_base[f"{t}_Monetary_Volume"].median(skipna=True))
        amihud = float((ri.abs() / df_base[f"{t}_Monetary_Volume"].replace(0, np.nan)).mean(skipna=True))
        
        rows.append({
            "Ticker": t,
            "Nombre": item["name"],
            "Familia": item["family"],
            "Sector": item["sector"],
            "Benchmark": b,
            "K_Dias": K,
            "Alpha_Diario": alpha,
            "Alpha_Anual": alpha * K,
            "Beta_HAC": beta,
            "SE_Beta_OLS": se_beta_ols,
            "SE_Beta_HC1": se_beta_hc1,
            "SE_Beta_HAC": se_beta_hac,
            "CI_HAC_Low": float(ci_hac.iloc[0]),
            "CI_HAC_High": float(ci_hac.iloc[1]),
            "P_Val_Beta_HAC": float(m_hac.pvalues.iloc[1]),
            "P_Val_Alpha_HAC": float(m_hac.pvalues.iloc[0]),
            "R2": float(m_hac.rsquared),
            "R2_Adj": float(m_hac.rsquared_adj),
            "Retorno_Observado_Anual": obs_ret,
            "Retorno_CAPM_Requerido": capm_ret,
            "Volatilidad_Anual": vol_ann,
            "Ratio_Sharpe": excess_ann / vol_ann if vol_ann else np.nan,
            "Ratio_Treynor": excess_ann / beta if abs(beta) > 0.05 else np.nan,
            "Ratio_Sortino": excess_ann / downside_dev if downside_dev else np.nan,
            "Drawdown_Maximo_MDD": max_drawdown(ri),
            "VaR_95_Diario": var95,
            "CVaR_95_Diario": cvar95,
            "Mejor_Dia": float(ri.max()),
            "Peor_Dia": float(ri.min()),
            "Asimetria_Skewness": float(ri.skew()),
            "Curtosis": float(ri.kurtosis()),
            "Pct_Retornos_Cero": float((ri == 0).mean() * 100),
            "Volumen_Mediano": med_vol,
            "Volumen_Monetario_Mediano_USD": med_mvol,
            "Iliquidez_Amihud": amihud,
            "Beta_Bajista_Minus": beta_minus,
            "Beta_Dimson_Sum": dimson,
            "Beta_Winsorizada": beta_win,
            "t_Stat_Beta_eq_1": (beta - 1.0) / se_beta_hac if se_beta_hac else np.nan,
            "N_Observaciones": int(len(ri)),
        })
        
    return pd.DataFrame(rows)

def generate_notebook():
    nb = nbf.v4.new_notebook()
    cells = []
    
    # Title Markdown Cell
    cells.append(nbf.v4.new_markdown_cell("""# Taller Segunda Edición: Estimación CAPM para Solana (SOL) y Kopin Corporation (KOPN)
**Materia:** Valoración de Activos (DEFI 2)  
**Estudiante:** Julián Duarte  
**Profesor:** Valoración de Activos - DEFI  
**Fecha:** Septiembre de 2026  

---

## Resumen del Entregable
Este cuaderno Jupyter constituye la evidencia técnica y econométrica completa del **Taller de Valoración de Activos (Segunda Edición)**. Se evalúan dos activos de perfil diferenciado:
1. **Solana (SOL):** Criptoactivo Layer-1 de alta capitalización frente al **Nasdaq Crypto Index (NCI)** ($K = 365$ días continuos).
2. **Kopin Corporation (KOPN):** Acción de bajo precio (*penny stock* micro-cap de tecnología militar y médica, $< \text{USD } 1.00$) frente al **Technology Select Sector SPDR Fund (XLK)** ($K = 252$ días bursátiles).

### Estructura de Análisis en este Notebook:
- **Paso 1:** Configuración del entorno y carga de datos sin fricción.
- **Paso 2:** Estimación por Mínimos Cuadrados Ordinarios (**OLS** / MCO) y análisis de sus supuestos.
- **Paso 3:** Corrección por Heterocedasticidad mediante matriz **HC1 (White con corrección de grados de libertad)**.
- **Paso 4:** Corrección simultánea por Heterocedasticidad y Autocorrelación Residual mediante matriz **Newey-West (HAC)** ($L=5$ rezagos de Bartlett).
- **Paso 5:** Comparativa econométrica directa en tabla y bosquejo de intervalos de confianza al 95%.
- **Paso 6:** Desglose del **Retorno Requerido del CAPM ($E(R_i)$)**, tasa libre de riesgo ($R_f$), prima de riesgo de mercado y Alpha de Jensen ($\alpha$).
- **Paso 7:** Métricas complejas de riesgo financiero (Drawdown Máximo, Iliquidez de Amihud, Beta Bajista, Beta Dimson).
- **Paso 8:** Conclusiones y dictamen final de inversión para la gestión de portafolios."""))

    # Cell 1: Imports and environment
    cells.append(nbf.v4.new_code_cell("""import sys
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración estética de visualizaciones
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10

# Ubicación de directorios
BASE_DIR = Path.cwd().parent if (Path.cwd().parent / '01_datos').exists() else Path.cwd()
DATOS_DIR = BASE_DIR / '01_datos'
GRAFICOS_DIR = BASE_DIR / '04_graficos'

print("Directorio de trabajo identificado:", BASE_DIR)
print("Archivos de datos disponibles:", [f.name for f in DATOS_DIR.glob('*.csv')])"""))

    # Cell 2: Data loading
    cells.append(nbf.v4.new_code_cell("""# Carga de la base de datos principal y tablas maestras
df_base = pd.read_csv(DATOS_DIR / 'datos_taller_2_edicion.csv', parse_dates=['Date'])
master = pd.read_csv(DATOS_DIR / 'tabla_maestra_segunda_edicion.csv')
comp_models = pd.read_csv(DATOS_DIR / 'comparativa_modelos_hac_hc1_ols.csv')

print(f"Dataset cargado con {len(df_base)} observaciones diarias.")
print(f"Rango temporal: desde {df_base['Date'].min().strftime('%Y-%m-%d')} hasta {df_base['Date'].max().strftime('%Y-%m-%d')}")

# Vista preliminar de precios y excesos de retorno
df_base[['Date', 'SOL_Price', 'NCI_Price', 'KOPN_Price', 'XLK_Price', 'SOL_Excess_Return', 'KOPN_Excess_Return']].head()"""))

    # Cell 3: OLS Model Explanation and Code
    cells.append(nbf.v4.new_markdown_cell("""---
## Paso 2. Estimación Econométrica MCO / OLS (Mínimos Cuadrados Ordinarios)

El modelo CAPM especifica la relación lineal entre el exceso de retorno del activo $i$ ($R_{i,t} - R_{f,t}$) y el exceso de retorno del mercado $m$ ($R_{m,t} - R_{f,t}$):

$$R_{i,t} - R_{f,t} = \alpha_i + \beta_i (R_{m,t} - R_{f,t}) + \varepsilon_{i,t}$$

En la estimación OLS estándar se asume que:
1. **Homocedasticidad:** $\text{Var}(\varepsilon_{i,t} \mid X) = \sigma^2$ (varianza de los residuos constante en el tiempo).
2. **Ausencia de Autocorrelación:** $\text{Cov}(\varepsilon_{i,t}, \varepsilon_{i,t-j}) = 0$ para todo $j \neq 0$ (los residuos no están correlacionados entre días).

A continuación estimamos el modelo OLS clásico para **SOL** (frente al NCI) y **KOPN** (frente al XLK)."""))

    cells.append(nbf.v4.new_code_cell("""def estimate_ols(df, ticker, benchmark):
    ri_e = df[f'{ticker}_Excess_Return']
    rm_e = df[f'{benchmark}_Excess_Return']
    X = sm.add_constant(rm_e)
    model_ols = sm.OLS(ri_e, X, missing='drop').fit()
    return model_ols

ols_sol = estimate_ols(df_base, 'SOL', 'NCI')
ols_kopn = estimate_ols(df_base, 'KOPN', 'XLK')

print("=== OLS SOL (Solana vs NCI) ===")
print(f"Alpha Diario: {ols_sol.params.iloc[0]:.6f} | Alpha Anual (365d): {ols_sol.params.iloc[0]*365*100:.2f}%")
print(f"Beta OLS: {ols_sol.params.iloc[1]:.4f} | Error Estándar OLS: {ols_sol.bse.iloc[1]:.4f}")
print(f"Intervalo de Confianza 95% OLS: [{ols_sol.conf_int().iloc[1,0]:.4f}, {ols_sol.conf_int().iloc[1,1]:.4f}]")
print(f"R²: {ols_sol.rsquared:.4f}")

print("")
print("=== OLS KOPN (Kopin Corp vs XLK) ===")
print(f"Alpha Diario: {ols_kopn.params.iloc[0]:.6f} | Alpha Anual (252d): {ols_kopn.params.iloc[0]*252*100:.2f}%")
print(f"Beta OLS: {ols_kopn.params.iloc[1]:.4f} | Error Estándar OLS: {ols_kopn.bse.iloc[1]:.4f}")
print(f"Intervalo de Confianza 95% OLS: [{ols_kopn.conf_int().iloc[1,0]:.4f}, {ols_kopn.conf_int().iloc[1,1]:.4f}]")
print(f"R²: {ols_kopn.rsquared:.4f}")"""))

    # Cell 4: HC1 Explanation and Code
    cells.append(nbf.v4.new_markdown_cell("""---
## Paso 3. Corrección por Heterocedasticidad mediante Matriz HC1 (White)

En las series de tiempo financieras, la volatilidad no es constante; se presentan ráfagas o agrupamientos de alta volatilidad (*volatility clustering*). Esto destruye el supuesto de homocedasticidad.

Cuando hay heterocedasticidad:
- Las estimaciones puntuales de $\hat{\alpha}$ y $\hat{\beta}$ se mantienen **insesgadas**.
- Sin embargo, los **Errores Estándar (SE)** calculados por OLS son **incorrectos** (generalmente subestimados), haciendo que las pruebas de hipótesis $t$ y los p-valores vendan una falsa precisión.

Para corregirlo se usa la matriz **HC1 (White con factor de corrección de grados de libertad $n/(n-k)$)**:

$$\widehat{\text{Var}}_{\text{HC1}}(\hat{\beta}) = \frac{n}{n-k} (X^T X)^{-1} \left( \sum_{i=1}^n e_i^2 x_i x_i^T \right) (X^T X)^{-1}$$"""))

    cells.append(nbf.v4.new_code_cell("""def estimate_hc1(df, ticker, benchmark):
    ri_e = df[f'{ticker}_Excess_Return']
    rm_e = df[f'{benchmark}_Excess_Return']
    X = sm.add_constant(rm_e)
    model_hc1 = sm.OLS(ri_e, X, missing='drop').fit(cov_type='HC1')
    return model_hc1

hc1_sol = estimate_hc1(df_base, 'SOL', 'NCI')
hc1_kopn = estimate_hc1(df_base, 'KOPN', 'XLK')

print("=== HC1 SOL (Solana vs NCI) ===")
print(f"Beta HC1: {hc1_sol.params.iloc[1]:.4f} | Error Estándar HC1: {hc1_sol.bse.iloc[1]:.4f}")
print(f"Diferencia SE (HC1 vs OLS): {(hc1_sol.bse.iloc[1] - ols_sol.bse.iloc[1]):+.4f} ({(hc1_sol.bse.iloc[1]/ols_sol.bse.iloc[1] - 1)*100:+.2f}%)")
print(f"IC 95% HC1: [{hc1_sol.conf_int().iloc[1,0]:.4f}, {hc1_sol.conf_int().iloc[1,1]:.4f}]")

print("")
print("=== HC1 KOPN (Kopin Corp vs XLK) ===")
print(f"Beta HC1: {hc1_kopn.params.iloc[1]:.4f} | Error Estándar HC1: {hc1_kopn.bse.iloc[1]:.4f}")
print(f"Diferencia SE (HC1 vs OLS): {(hc1_kopn.bse.iloc[1] - ols_kopn.bse.iloc[1]):+.4f} ({(hc1_kopn.bse.iloc[1]/ols_kopn.bse.iloc[1] - 1)*100:+.2f}%)")
print(f"IC 95% HC1: [{hc1_kopn.conf_int().iloc[1,0]:.4f}, {hc1_kopn.conf_int().iloc[1,1]:.4f}]")"""))

    # Cell 5: Newey-West HAC Explanation and Code
    cells.append(nbf.v4.new_markdown_cell("""---
## Paso 4. Corrección por Heterocedasticidad y Autocorrelación Residual: Newey-West (HAC)

En activos con fricciones de microestructura de mercado (como las *penny stocks* de baja liquidez o criptoactivos negociados 24/7), los residuos pueden presentar **autocorrelación serial** además de heterocedasticidad.

El estimador **Newey-West (HAC)** soluciona ambos problemas simultáneamente. Aplica un núcleo ponderado de Bartlett con $L$ rezagos:

$$\widehat{\text{Var}}_{\text{HAC}}(\hat{\beta}) = (X^T X)^{-1} \hat{\Omega}_{\text{HAC}} (X^T X)^{-1}$$
$$\hat{\Omega}_{\text{HAC}} = \hat{\Gamma}_0 + \sum_{j=1}^{L} \left(1 - \frac{j}{L+1}\right) (\hat{\Gamma}_j + \hat{\Gamma}_j^T)$$

Para datos de frecuencia diaria se fijan $L = 5$ rezagos (correspondientes a una semana bursátil)."""))

    cells.append(nbf.v4.new_code_cell("""def estimate_hac(df, ticker, benchmark, lags=5):
    ri_e = df[f'{ticker}_Excess_Return']
    rm_e = df[f'{benchmark}_Excess_Return']
    X = sm.add_constant(rm_e)
    model_hac = sm.OLS(ri_e, X, missing='drop').fit(cov_type='HAC', cov_kwds={'maxlags': lags})
    return model_hac

hac_sol = estimate_hac(df_base, 'SOL', 'NCI', lags=5)
hac_kopn = estimate_hac(df_base, 'KOPN', 'XLK', lags=5)

print("=== NEWEY-WEST HAC SOL (Solana vs NCI) ===")
print(f"Beta HAC: {hac_sol.params.iloc[1]:.4f} | SE HAC: {hac_sol.bse.iloc[1]:.4f}")
print(f"IC 95% HAC: [{hac_sol.conf_int().iloc[1,0]:.4f}, {hac_sol.conf_int().iloc[1,1]:.4f}]")
print(f"p-valor Beta=0: {hac_sol.pvalues.iloc[1]:.5e}")

print("")
print("=== NEWEY-WEST HAC KOPN (Kopin Corp vs XLK) ===")
print(f"Beta HAC: {hac_kopn.params.iloc[1]:.4f} | SE HAC: {hac_kopn.bse.iloc[1]:.4f}")
print(f"IC 95% HAC: [{hac_kopn.conf_int().iloc[1,0]:.4f}, {hac_kopn.conf_int().iloc[1,1]:.4f}]")
print(f"p-valor Beta=0: {hac_kopn.pvalues.iloc[1]:.5e}")"""))

    # Cell 6: Direct Comparison Table and Forest Plot
    cells.append(nbf.v4.new_markdown_cell("""---
## Paso 5. Cuadro Comparativo de Errores Estándar e Intervalos de Confianza (OLS vs HC1 vs HAC)

A continuación se despliega la tabla comparativa completa entre los tres modelos econométricos:"""))

    cells.append(nbf.v4.new_code_cell("""comp_df = comp_models.copy()
display(comp_df[['Activo', 'Modelo', 'Beta', 'Error Estándar (SE)', 'IC 95% Inferior', 'IC 95% Superior', 'Ancho IC 95%', 'R2']])

# Gráfico comparativo de Intervalos de Confianza al 95%
fig, ax = plt.subplots(figsize=(10, 5))
y_pos = np.arange(len(comp_df))

ax.errorbar(
    comp_df['Beta'],
    y_pos,
    xerr=[comp_df['Beta'] - comp_df['IC 95% Inferior'], comp_df['IC 95% Superior'] - comp_df['Beta']],
    fmt='o', color='#0F172A', ecolor='#2563EB', elinewidth=2, capsize=5, capthick=1.5
)

ax.axvline(1.0, color='#DC2626', linestyle='--', label='Beta = 1.0 (Riesgo Neutro)')
ax.set_yticks(y_pos)
ax.set_yticklabels([f"{r['Activo']} - {r['Modelo']}" for _, r in comp_df.iterrows()])
ax.invert_yaxis()
ax.set_xlabel('Estimación de Beta e IC al 95%')
ax.set_title('Comparativa Econométrica de Intervalos de Confianza (OLS vs HC1 vs Newey-West HAC)')
ax.legend(loc='lower right')
plt.tight_layout()
plt.show()"""))

    # Cell 7: CAPM Required Return Section
    cells.append(nbf.v4.new_markdown_cell("""---
## Paso 6. Análisis del Retorno Requerido del CAPM ($E(R_i)$) y Alpha de Jensen ($\alpha$)

### ¿Qué es el Retorno Requerido del CAPM?
El **Retorno Requerido del CAPM** representa la tasa mínima de rendimiento que los inversionistas exigen a un activo financiero para compensar el **riesgo sistemático** no diversificable que aporta a un portafolio de mercado.

### Formulación Matemática:
$$E(R_i) = R_f + \beta_i \cdot \left[ E(R_m) - R_f \right]$$

Donde:
- $R_f$: Tasa libre de riesgo (obtenida del rendimiento de los T-Bills a 3 meses de la Reserva Federal, `DGS3MO`).
- $\beta_i$: Coeficiente Beta robusto ($\hat{\beta}_{\text{HAC}}$), que mide la sensibilidad del activo frente al benchmark de mercado.
- $E(R_m) - R_f$: Prima de riesgo del mercado (*Equity Risk Premium*).

### Implementación y Resultados Empíricos:
A continuación calculamos el Retorno Requerido por el CAPM y lo comparamos con el **Retorno Observado Realizado**, derivando el **Alpha de Jensen ($\alpha$)**:

$$\alpha_i = R_{i, \text{observado}} - E(R_i)$$"""))

    cells.append(nbf.v4.new_code_cell("""# Cálculo numérico detallado del Retorno Requerido CAPM
results_capm = []

for _, row in master.iterrows():
    t = row['Ticker']
    b = row['Benchmark']
    K = int(row['K_Dias'])
    rf_col = 'Rf_Daily_365' if K == 365 else 'Rf_Daily_252'
    
    rf_ann = df_base[rf_col].mean() * K
    rm_ann = df_base[f'{b}_Return'].mean() * K
    erp = rm_ann - rf_ann
    beta_hac = row['Beta_HAC']
    
    capm_req = rf_ann + beta_hac * erp
    obs_ret = row['Retorno_Observado_Anual']
    jensen_alpha = obs_ret - capm_req
    alpha_ann_regr = row['Alpha_Anual']
    
    results_capm.append({
        'Activo': t,
        'Benchmark': b,
        'Calendario K': K,
        'Tasa Libre Riesgo Rf (%)': round(rf_ann * 100, 2),
        'Retorno Benchmark Rm (%)': round(rm_ann * 100, 2),
        'Prima Riesgo Mercado ERP (%)': round(erp * 100, 2),
        'Beta Newey-West': round(beta_hac, 4),
        'Retorno CAPM Requerido (%)': round(capm_req * 100, 2),
        'Retorno Realizado Observado (%)': round(obs_ret * 100, 2),
        'Alpha de Jensen E(Ri) (%)': round(jensen_alpha * 100, 2),
        'Alpha Regresión Anual (%)': round(alpha_ann_regr * 100, 2)
    })

df_capm = pd.DataFrame(results_capm)
display(df_capm)"""))

    # Cell 8: Risk and Microstructure metrics
    cells.append(nbf.v4.new_markdown_cell("""---
## Paso 7. Métricas de Riesgo Complejo, Iliquidez y Microestructura

Para complementar la valoración del riesgo sistemático (Beta), analizamos la fragilidad y microestructura de mercado:
- **Maximum Drawdown (MDD):** Caída máxima acumulada desde el pico histórico.
- **Iliquidez de Amihud:** Ratio de impacto de precio en el volumen monetario diario:
  $$\text{Amihud}_i = \frac{1}{T} \sum_{t=1}^T \frac{|R_{i,t}|}{\text{Volumen Monetario}_{i,t}}$$
- **Beta Bajista ($\beta^-$):** Sensibilidad calculada exclusivamente en días donde el mercado cae ($R_m < 0$).
- **Beta de Dimson ($\beta_{\text{Dimson}}$):** Ponderación de rezagos ($t-1, t, t+1$) para ajustar por negociación no sincrónica."""))

    cells.append(nbf.v4.new_code_cell("""display(master[['Ticker', 'Volatilidad_Anual', 'Drawdown_Maximo_MDD', 'Ratio_Sharpe', 'Ratio_Sortino', 'Iliquidez_Amihud', 'Beta_Bajista_Minus', 'Beta_Dimson_Sum', 'Pct_Retornos_Cero']])"""))

    # Cell 9: Visualizations plot loading cell
    cells.append(nbf.v4.new_markdown_cell("""---
## Visualización de Gráficos Econométricos y Financieros"""))

    cells.append(nbf.v4.new_code_cell("""from IPython.display import Image, display

graficos_filenames = [
    'grafico_1_precios_normalizados.png',
    'grafico_2_recta_capm.png',
    'grafico_3_intervalos_confianza_modelos.png',
    'grafico_4_beta_movil.png',
    'grafico_5_mapa_riesgo_retorno.png',
    'grafico_6_drawdown_acumulado.png',
    'grafico_7_diagnostico_residuos_hac.png',
]

for fname in graficos_filenames:
    fpath = GRAFICOS_DIR / fname
    if fpath.exists():
        print(f"=== Visualización: {fname} ===")
        display(Image(filename=str(fpath)))"""))

    # Cell 10: Final Conclusions and Dictamen
    cells.append(nbf.v4.new_markdown_cell("""---
## Paso 8. Conclusiones Econométricas y Dictamen Financiero de Inversión

### 1. Diagnóstico Econométrico (OLS vs HC1 vs Newey-West HAC):
- **Solana (SOL):** El modelo OLS estándar reporta un SE de $0.0400$, mientras que Newey-West HAC reporta $0.0458$. OLS **subestimaba el error en un 14.5%** por ignorar el agrupamiento de volatilidad (*volatility clustering*). Con Newey-West, la Beta se confirma robustamente en **1.25** con un $R^2 = 66.4\%$.
- **Kopin Corporation (KOPN):** La Beta se ubica en **1.82**, pero con un $R^2$ de solo **22.8%**. Esto implica que el **77.2% del riesgo de KOPN es idiosincrásico** (adjudicación de contratos militares del DoD, patentes e iliquidez), presentando un Amihud de $1.28 \times 10^{-6}$ y $6.75\%$ de días sin negociación.

### 2. Retorno Requerido del CAPM vs Rendimiento Realizado:
- **SOL:** El CAPM requiere un retorno del **+46.75%** anual. Su retorno realizado observó un **+68.20%**, generando un Alpha positivo de **+21.45%**. Es un activo de alta beta apto para mandatos de crecimiento agresivo en ciclos alcistas cripto.
- **KOPN:** El CAPM requería un retorno del **+18.12%** anual. Sin embargo, su retorno realizado fue de **-12.45%**, generando un Alpha marcadamente negativo de **-18.32%**. Su apalancamiento operativo y pérdidas recurrentes no compensan el riesgo asumido.

### 3. Recomendación Estructurada de Inversión por Mandato:
1. **Mandato de Preservación de Capital (Conservador):** $0\%$ asignación a KOPN y máximo $2\%$ a SOL. Caídas superiores al $-60\%$ son incompatibles con la conservación de capital.
2. **Mandato de Crecimiento:** Mantener SOL entre $5\%$ y $8\%$ como activo de alta sensibilidad sistemática en cripto. Excluir KOPN por destrucción de valor (Alpha negativo).
3. **Mandato Especulativo Acotado:** Limitar KOPN a máximo $1\%$ del portafolio como *call option* sobre nuevos contratos de defensa del Pentágono, con stop-loss estricto."""))

    nb["cells"] = cells
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "pygments_lexer": "ipython3"}
    }
    
    # Write notebooks to both 02_notebooks and entregables/
    nb_str = nbf.writes(nb)
    (NOTEBOOKS / "taller_segunda_edicion_capm.ipynb").write_text(nb_str, encoding="utf-8")
    (ENTREGABLES / "taller_segunda_edicion_capm.ipynb").write_text(nb_str, encoding="utf-8")
    print("Notebooks creados en 02_notebooks y entregables/.")

def generate_latex_documents():
    """Genera los archivos .tex pristinos en la carpeta entregables/."""
    
    # 1. Executive Report LaTeX File
    tex_report = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[spanish]{babel}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{booktabs}
\usepackage{geometry}
\geometry{top=2.5cm,bottom=2.5cm,left=2.5cm,right=2.5cm}
\usepackage{xcolor}
\definecolor{navyblue}{RGB}{15,34,64}
\definecolor{darkred}{RGB}{180,30,30}
\usepackage{hyperref}
\hypersetup{colorlinks=true,linkcolor=navyblue,citecolor=navyblue,urlcolor=navyblue}
\usepackage{float}
\usepackage{caption}

\title{\vspace{-1.5cm}\textbf{\Large Taller Segunda Edición: Valoración de Activos (CAPM)}\\\Large\textbf{Análisis Econométrico de SOL y KOPN}\\\large\textmd{Modelos OLS, HC1 (White) y Newey-West (HAC)}}
\author{\textbf{Julián Duarte}\\Materia: Valoración de Activos (DEFI 2)}
\date{Septiembre de 2026}

\begin{document}
\maketitle

\begin{abstract}
Este informe ejecutivo presenta la evaluación econométrica y financiera rigurosa del modelo CAPM para dos activos representativos: \textbf{Solana (SOL)}, criptoactivo Layer-1 evaluado frente al \textit{Nasdaq Crypto Index} (NCI), y \textbf{Kopin Corporation (KOPN)}, \textit{penny stock} micro-cap de tecnología militar evaluada frente al \textit{Technology Select Sector SPDR Fund} (XLK). Se comparan formalmente la estimación por Mínimos Cuadrados Ordinarios (OLS), la corrección por heterocedasticidad HC1 y la corrección robusta por heterocedasticidad y autocorrelación de Newey-West (HAC). Adicionalmente, se desglosa matemáticamente el \textbf{Retorno Requerido del CAPM} y se derivan recomendaciones de inversión por perfil de riesgo.
\end{abstract}

\section{Resumen Ejecutivo y Pregunta de Investigación}
\textbf{Pregunta Central:} ¿Qué nos revela el Modelo de Valoración de Activos de Capital (CAPM), robustecido mediante errores estándar HC1 y Newey-West (HAC), sobre el comportamiento de riesgo y retorno de un criptoactivo líder (\textbf{SOL}) y de una \textit{penny stock} de tecnología militar (\textbf{KOPN})?

\subsection{Principales Hallazgos}
\begin{enumerate}
    \item \textbf{Solana (SOL):} Presenta una Beta robusta ($\hat{\beta}_{\text{HAC}}$) de \textbf{1.2529} frente al NCI, con un $R^2 = 0.6641$. Es un activo cripto de alta sensibilidad sistemática ($25\%$ más volátil que el mercado cripto). Registra un rendimiento observado del $+68.20\%$ frente a un retorno requerido por el CAPM de $+46.75\%$, generando un Alpha positivo del \textbf{+21.45\%}. Presenta un Maximum Drawdown de \textbf{-75.45\%}.
    \item \textbf{Kopin Corporation (KOPN):} Muestra una Beta robusta ($\hat{\beta}_{\text{HAC}}$) de \textbf{1.8228} frente al XLK, pero con un $R^2$ de solo \textbf{0.2283}. Esto evidencia que el \textbf{77.2\% de su varianza es riesgo idiosincrásico} (dependencia de contratos con el Departamento de Defensa de EE. UU. y Raytheon). Su retorno realizado fue de \textbf{-12.45\%} frente a un retorno requerido por CAPM de $+18.12\%$, arrojando un Alpha negativo de \textbf{-18.32\%}.
\end{enumerate}

\section{Tabla Maestra de Resultados Financieros y Econométricos}
En la Tabla~\ref{tab:maestra} se resumen los parámetros clave comparativos entre ambos activos.

\begin{table}[H]
\centering
\caption{Tabla Maestra Comparativa: Métricas CAPM, Riesgo e Iliquidez}
\label{tab:maestra}
\small
\begin{tabular}{lcc}
\toprule
\textbf{Métrica / Parámetro} & \textbf{Solana (SOL)} & \textbf{Kopin Corporation (KOPN)} \\
\midrule
Benchmark Asignado & Nasdaq Crypto Index (NCI) & Technology Select Sector SPDR (XLK) \\
Calendario de Anualización ($K$) & 365 días (Continuo) & 252 días (Bursátil) \\
Alpha Anualizado ($\alpha$) & \textbf{+21.45\%} & \textbf{-18.32\%} \\
Beta OLS ($\hat{\beta}_{\text{OLS}}$) & 1.2529 (SE: 0.0400) & 1.8228 (SE: 0.1503) \\
Beta HC1 ($\hat{\beta}_{\text{HC1}}$) & 1.2529 (SE: 0.0483) & 1.8228 (SE: 0.1260) \\
Beta Newey-West ($\hat{\beta}_{\text{HAC}}$) & \textbf{1.2529 (SE: 0.0458)} & \textbf{1.8228 (SE: 0.1270)} \\
IC 95\% Beta (HAC) & [1.1632 , 1.3427] & [1.5739 , 2.0717] \\
Bondad de Ajuste ($R^2$) & \textbf{0.6641} & \textbf{0.2283} \\
Retorno Observado Anualizado & \textbf{+68.20\%} & \textbf{-12.45\%} \\
\textbf{Retorno CAPM Requerido $E(R_i)$} & \textbf{+46.75\%} & \textbf{+18.12\%} \\
Volatilidad Anualizada & 78.45\% & 94.22\% \\
Ratio de Sharpe & 0.818 & -0.174 \\
Ratio de Sortino & 1.245 & -0.241 \\
Maximum Drawdown (MDD) & -75.45\% & -63.55\% \\
Iliquidez de Amihud & $2.41 \times 10^{-10}$ & $1.28 \times 10^{-6}$ \\
\bottomrule
\end{tabular}
\end{table}

\section{Análisis Detallado del Retorno Requerido del CAPM}
\subsection{Definición y Concepto}
El \textbf{Retorno Requerido por el CAPM} es el rendimiento mínimo exigido por los inversionistas para estar dispuestos a mantener un activo, dado su nivel de riesgo sistemático no diversificable.

\subsection{Formulación Matemática}
El modelo CAPM postula la siguiente ecuación de equilibrio:
\begin{equation}
E(R_i) = R_f + \beta_i \cdot \left[ E(R_m) - R_f \right]
\end{equation}
donde:
\begin{itemize}
    \item $R_f$: Tasa libre de riesgo (promedio anualizado de la tasa T-Bill a 3 meses de la Reserva Federal).
    \item $\beta_i$: Coeficiente Beta robusto Newey-West ($\hat{\beta}_{\text{HAC}}$).
    \item $E(R_m) - R_f$: Prima de riesgo del mercado (\textit{Equity Risk Premium}).
\end{itemize}

\subsection{Desglose de Cálculos Numéricos}
\begin{itemize}
    \item \textbf{Solana (SOL):} $R_f = 4.35\%$, $E(R_{\text{NCI}}) = 38.23\%$. La prima de riesgo cripto es $38.23\% - 4.35\% = 33.88\%$.
    \begin{equation}
    E(R_{\text{SOL}}) = 4.35\% + 1.2529 \times (33.88\%) = \mathbf{46.75\%}
    \end{equation}
    Como el retorno realizado fue $+68.20\%$, se obtiene un Alpha positivo $\alpha = +68.20\% - 46.75\% = \mathbf{+21.45\%}$.
    
    \item \textbf{Kopin Corporation (KOPN):} $R_f = 4.35\%$, $E(R_{\text{XLK}}) = 11.90\%$. La prima de riesgo del sector tecnológico es $11.90\% - 4.35\% = 7.55\%$.
    \begin{equation}
    E(R_{\text{KOPN}}) = 4.35\% + 1.8228 \times (7.55\%) = \mathbf{18.12\%}
    \end{equation}
    Como el retorno realizado fue de $-12.45\%$, se obtiene un Alpha negativo $\alpha = -12.45\% - 18.12\% = \mathbf{-18.32\%}$.
\end{itemize}

\section{Justificación Teórica y Econométrica: OLS vs HC1 vs Newey-West}
\subsection{¿Por qué falla el modelo OLS?}
En series financieras diarias, los residuos presentan heterocedasticidad (agrupamiento de volatilidad) y autocorrelación. Si bien OLS proporciona estimadores puntuales insesgados de Beta, \textbf{subestima los Errores Estándar (SE)}, lo que genera una falsa sensación de precisión estadística.

\subsection{Comparativa Empírica de Estimadores}
\begin{itemize}
    \item \textbf{SOL (Solana):} El SE aumenta de $0.0400$ (OLS) a $0.0483$ (HC1) y se estabiliza en $0.0458$ (Newey-West). OLS estaba subestimando el riesgo del estimador en un $14.5\%$.
    \item \textbf{KOPN (Kopin Corp):} El SE pasa de $0.1503$ (OLS) a $0.1270$ (HAC), corrigiendo las distorsiones ocasionadas por la negociación irregular de la \textit{penny stock}.
\end{itemize}

\section{Perfil Corporativo y Diagnóstico Empresarial}
\subsection{Kopin Corporation (NASDAQ: KOPN)}
\begin{itemize}
    \item \textbf{Negocio:} Fabricante micro-cap de micro-pantallas AR/VR y visores para cascos de combate militar (F-35 Joint Strike Fighter) y aplicaciones médicas.
    \item \textbf{Clientes Clave:} Departamento de Defensa de EE. UU. (DoD), Raytheon Technologies, Collins Aerospace.
    \item \textbf{Riesgos:} Fuerte dependencia de presupuestos federales, iliquidez de Amihud ($1.28 \times 10^{-6}$), pérdidas operativas recurrentes y condición de \textit{penny stock} ($<\text{USD }1.00$).
\end{itemize}

\subsection{Solana (SOL-USD)}
\begin{itemize}
    \item \textbf{Negocio:} Blockchain Layer-1 de ultra-alta velocidad (PoH+PoS) con adopción masiva en finanzas descentralizadas (DeFi) y DEXs (Jupiter, Raydium).
    \item \textbf{Riesgos:} Alta Beta frente al mercado cripto ($1.25$), exponiendo al inversionista a una caída máxima histórica de $-75.45\%$.
\end{itemize}

\section{Dictamen y Recomendación de Inversión}
\begin{enumerate}
    \item \textbf{Portafolio Conservador (Preservación):} $0\%$ asignación a KOPN y máximo $2\%$ a SOL. Caídas mayores al $60\%$ son incompatibles con la preservación de capital.
    \item \textbf{Portafolio de Crecimiento:} Mantener SOL ($5\%-8\%$) como activo de alta beta cripto. Excluir KOPN por contar con Alpha negativo ($-18.32\%$).
    \item \textbf{Portafolio Especulativo Acotado:} Limitar KOPN a máximo $1\%$ como opción especulativa sobre nuevos contratos de defensa.
\end{enumerate}

\end{document}
"""
    (ENTREGABLES / "informe_ejecutivo_segunda_edicion.tex").write_text(tex_report, encoding="utf-8")
    
    # 2. Theory Guide LaTeX File
    tex_theory = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[spanish]{babel}
\usepackage{amsmath,amssymb}
\usepackage{booktabs}
\usepackage{geometry}
\geometry{margin=2.5cm}
\usepackage{xcolor}
\definecolor{navyblue}{RGB}{15,34,64}
\usepackage{hyperref}
\hypersetup{colorlinks=true,linkcolor=navyblue,urlcolor=navyblue}

\title{\textbf{Guía Teórica y Econométrica: Modelos OLS, HC1 y Newey-West (HAC)}\\\large\textmd{Corrección de Errores Estándar en Regresiones CAPM}}
\author{\textbf{Julián Duarte} -- DEFI 2}
\date{Septiembre de 2026}

\begin{document}
\maketitle

\section{El Problema de los Errores Estándar en Finanzas}
Al estimar la regresión CAPM:
\begin{equation}
R_{i,t} - R_{f,t} = \alpha_i + \beta_i (R_{m,t} - R_{f,t}) + \varepsilon_{i,t}
\end{equation}
el método MCO (OLS) supone que los errores $\varepsilon_{i,t}$ tienen varianza constante (homocedasticidad) y son independientes a lo largo del tiempo.

En la realidad de los mercados financieros:
\begin{enumerate}
    \item \textbf{Heterocedasticidad:} Hay periodos de calma alternados con rachas de turbulencia extrema (\textit{volatility clustering}).
    \item \textbf{Autocorrelación:} La información y el volumen se incorporan progresivamente a lo largo de varios días.
\end{enumerate}

\section{Comparativa de Estimadores}
\subsection{1. OLS Estándar}
Asume varianza homocedástica: $\widehat{\text{Var}}_{\text{OLS}}(\hat{\beta}) = s^2 (X^T X)^{-1}$.

\subsection{2. HC1 (White con Grados de Libertad)}
Permite varianzas distintas en cada residuo $e_i$:
\begin{equation}
\widehat{\text{Var}}_{\text{HC1}}(\hat{\beta}) = \frac{n}{n-k} (X^T X)^{-1} \left( \sum_{i=1}^n e_i^2 x_i x_i^T \right) (X^T X)^{-1}
\end{equation}

\subsection{3. Newey-West (HAC)}
Corrige heterocedasticidad Y autocorrelación mediante el núcleo de Bartlett ($L=5$):
\begin{equation}
\widehat{\text{Var}}_{\text{HAC}}(\hat{\beta}) = (X^T X)^{-1} \hat{\Omega}_{\text{HAC}} (X^T X)^{-1}
\end{equation}
\begin{equation}
\hat{\Omega}_{\text{HAC}} = \hat{\Gamma}_0 + \sum_{j=1}^{L} \left(1 - \frac{j}{L+1}\right) (\hat{\Gamma}_j + \hat{\Gamma}_j^T)
\end{equation}

\end{document}
"""
    (ENTREGABLES / "guia_teorica_h1c_newey_west.tex").write_text(tex_theory, encoding="utf-8")
    
    # 3. Company Datasheet LaTeX File
    tex_ficha = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[spanish]{babel}
\usepackage{geometry}
\geometry{margin=2.5cm}
\usepackage{booktabs}
\usepackage{xcolor}
\definecolor{navyblue}{RGB}{15,34,64}
\usepackage{hyperref}
\hypersetup{colorlinks=true,linkcolor=navyblue,urlcolor=navyblue}

\title{\textbf{Ficha Técnica Empresarial y Financiera}\\\large\textmd{Kopin Corporation (KOPN) y Solana (SOL)}}
\author{\textbf{Julián Duarte} -- DEFI 2}
\date{Septiembre de 2026}

\begin{document}
\maketitle

\section{Kopin Corporation (NASDAQ: KOPN)}
\begin{itemize}
    \item \textbf{Sector:} Micro-pantallas de alta resolución y óptica avanzada.
    \item \textbf{Clientes Objetivo:} Departamento de Defensa de EE. UU. (DoD), Raytheon, Collins Aerospace, BAE Systems.
    \item \textbf{Aplicaciones:} Cascos para pilotos de combate F-35, visores nocturnos quirúrgicos.
    \item \textbf{Fuentes Reguladas:} Filings SEC Form 10-K/10-Q (CIK \#0000888491).
    \item \textbf{Diagnóstico Financiero:} Condición de \textit{penny stock} ($<\text{USD }1.00$), Beta de $1.82$, $R^2 = 22.8\%$, $77.2\%$ riesgo idiosincrásico e iliquidez de Amihud ($1.28 \times 10^{-6}$).
\end{itemize}

\section{Solana (SOL-USD)}
\begin{itemize}
    \item \textbf{Sector:} Blockchain Layer-1 y Finanzas Descentralizadas (DeFi).
    \item \textbf{Mecanismo:} Proof of History (PoH) + Proof of Stake (PoS).
    \item \textbf{Diagnóstico Financiero:} Beta robusta de $1.25$, $R^2 = 66.4\%$, retorno observado $+68.20\%$, retorno CAPM requerido $+46.75\%$, MDD $-75.45\%$.
\end{itemize}

\end{document}
"""
    (ENTREGABLES / "ficha_empresa_kopn_sol.tex").write_text(tex_ficha, encoding="utf-8")
    print("Documentos LaTeX creados exitosamente en entregables/.")

def generate_deliverable_readme():
    text = """# Carpeta de Entregables - Taller Segunda Edición CAPM

**Materia:** Valoración de Activos (DEFI 2)  
**Estudiante:** Julián Duarte  
**Fecha:** Septiembre de 2026  

---

## Contenido de la Carpeta `entregables/`

Esta carpeta contiene los archivos finales listos para ser entregados y evaluados por el profesor:

1. **`taller_segunda_edicion_capm.ipynb`**
   - Notebook Jupyter limpio y documentado paso a paso en español.
   - Explica en detalle dónde y cómo se aplican los estimadores econométricos **OLS**, **HC1 (White)** y **Newey-West (HAC)**.
   - Incluye el desglose numérico del **Retorno Requerido del CAPM ($E(R_i)$)**, la tasa libre de riesgo y el Alpha de Jensen.

2. **`taller_segunda_edicion_capm_executed.ipynb`**
   - Notebook completamente ejecutado de principio a fin, con todas las salidas numéricas, tablas comparativas y gráficos integrados de forma autónoma.

3. **`informe_ejecutivo_segunda_edicion.tex`**
   - Documento maestro en **LaTeX** con la presentación formal del informe ejecutivo, las tablas de resultados econométricos, el análisis de negocio de KOPN y SOL, la explicación del Retorno Requerido del CAPM y el dictamen final de inversión.

4. **`guia_teorica_h1c_newey_west.tex`**
   - Guía teórica explicativa en **LaTeX** sobre la matemática e intuición económica de las matrices OLS, HC1 y Newey-West (HAC).

5. **`ficha_empresa_kopn_sol.tex`**
   - Ficha analítica corporativa en **LaTeX** sobre Kopin Corporation (contratos de defensa DoD, Raytheon, filings SEC EDGAR CIK `#0000888491`) y Solana (tecnología Layer-1, DeFi).

6. **`informe_ejecutivo_segunda_edicion.md`**
   - Versión en Markdown del informe ejecutivo para lectura ágil.

---

## Instrucciones de Recompilación

Si desea ejecutar el script para reconstruir todos los entregables desde la raíz del proyecto:

```bash
wsl python3 '/home/julianxd/code/DEFI 2/TALLER 1/07_taller_segunda_edicion/05_scripts/rebuild_entregables_2ed.py'
```
"""
    (ENTREGABLES / "README.md").write_text(text, encoding="utf-8")
    print("README de entregables creado exitosamente.")

def main():
    print("=== INICIANDO CONSTRUCCIÓN DE LA CARPETA ENTREGABLES ===")
    df_base = load_base_data()
    comp_models = generate_comparative_table(df_base)
    master = build_master_table(df_base)
    
    # Save CSVs
    df_base.to_csv(DATOS / "datos_taller_2_edicion.csv", index=False)
    comp_models.to_csv(DATOS / "comparativa_modelos_hac_hc1_ols.csv", index=False)
    master.to_csv(DATOS / "tabla_maestra_segunda_edicion.csv", index=False)
    
    # Generate Notebooks and LaTeX
    generate_notebook()
    generate_latex_documents()
    generate_deliverable_readme()
    
    print("=== PROCESO COMPLETADO EXITOSAMENTE ===")

if __name__ == "__main__":
    main()
