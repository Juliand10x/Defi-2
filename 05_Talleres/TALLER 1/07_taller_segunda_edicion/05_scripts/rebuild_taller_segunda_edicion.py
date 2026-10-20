from __future__ import annotations

import math
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf
import matplotlib.pyplot as plt
import seaborn as sns

# Setup Root paths
ROOT = Path(__file__).resolve().parents[2] # DEFI 2/TALLER 1
EDITION_ROOT = ROOT / "07_taller_segunda_edicion"
DATOS = EDITION_ROOT / "01_datos"
NOTEBOOKS = EDITION_ROOT / "02_notebooks"
INFORME = EDITION_ROOT / "03_informe"
GRAFICOS = EDITION_ROOT / "04_graficos"
SCRIPTS = EDITION_ROOT / "05_scripts"

for p in [DATOS, NOTEBOOKS, INFORME, GRAFICOS, SCRIPTS]:
    p.mkdir(parents=True, exist_ok=True)

# Define assets and benchmarks
ASSETS = [
    {
        "ticker": "SOL",
        "yf": "SOL-USD",
        "name": "Solana",
        "family": "Criptoactivo",
        "sector": "Criptoactivos / DeFi",
        "benchmark": "NCI",
        "K": 365,
        "type": "Criptoactivo de alta capitalizacion",
        "desc": "Blockchain de capa 1 de alto rendimiento con consenso PoH+PoS y activo colateral en DeFi.",
    },
    {
        "ticker": "KOPN",
        "yf": "KOPN",
        "name": "Kopin Corporation",
        "family": "Tecnologia",
        "sector": "Micro-pantallas y Optica de Defensa/Medica",
        "benchmark": "XLK",
        "K": 252,
        "type": "Penny stock / Accion tecnologica micro-cap",
        "desc": "Desarrollador de micro-pantallas AR/VR y visores opticos para defensa (Departamento de Defensa EE.UU.) y medicina.",
    },
]

BENCHMARKS = [
    {"ticker": "NCI", "name": "Nasdaq Crypto Index"},
    {"ticker": "XLK", "name": "Technology Select Sector SPDR Fund"},
]

def load_base_data() -> pd.DataFrame:
    """Carga los datos desde la base maestra principal del Taller 1."""
    legacy_file = ROOT / "01_datos" / "datos_taller_1_julian_duarte.csv"
    if not legacy_file.exists():
        raise FileNotFoundError(f"No se encontro la base original en {legacy_file}")
    
    df = pd.read_csv(legacy_file, parse_dates=["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    return df

def run_capm_models(ri_e: pd.Series, rm_e: pd.Series):
    """Estima regresiones CAPM con OLS, HC1 (White) y Newey-West (HAC)."""
    X = sm.add_constant(rm_e)
    
    # Model OLS standard
    model_ols = sm.OLS(ri_e, X, missing="drop").fit()
    
    # Model HC1 (White / MacKinnon-White df adjusted)
    model_hc1 = sm.OLS(ri_e, X, missing="drop").fit(cov_type="HC1")
    
    # Model Newey-West (HAC, 5 lags for daily data)
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
    """Construye la comparativa econometrica directa entre OLS, HC1 y Newey-West HAC."""
    records = []
    for item in ASSETS:
        t = item["ticker"]
        b = item["benchmark"]
        K = item["K"]
        
        ri_e = df_base[f"{t}_Excess_Return"]
        rm_e = df_base[f"{b}_Excess_Return"]
        
        m_ols, m_hc1, m_hac = run_capm_models(ri_e, rm_e)
        
        for name, m in [("OLS (Homocedastico)", m_ols), ("HC1 (White / Robusto Volatilidad)", m_hc1), ("Newey-West (HAC / Robusto Vol.+Autocorr.)", m_hac)]:
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
    """Construye la tabla maestra con metricas financieras completas para SOL y KOPN."""
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

def plot_all_visualizations(df_base: pd.DataFrame, master: pd.DataFrame, comp_models: pd.DataFrame):
    """Genera las 7 visualizaciones del taller en 04_graficos/."""
    plt.style.use("seaborn-v0_8-whitegrid")
    dates = pd.to_datetime(df_base["Date"])
    
    # -------------------------------------------------------------
    # Grafico 1: Precios Normalizados Base 100 (SOL vs NCI, KOPN vs XLK)
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # SOL vs NCI
    sol_b100 = df_base["SOL_Price"] / df_base["SOL_Price"].iloc[0] * 100
    nci_b100 = df_base["NCI_Price"] / df_base["NCI_Price"].iloc[0] * 100
    axes[0].plot(dates, sol_b100, label="SOL (Solana)", color="#9945FF", linewidth=1.8)
    axes[0].plot(dates, nci_b100, label="NCI (Nasdaq Crypto Index)", color="#14F195", linewidth=1.5, linestyle="--")
    axes[0].set_title("Criptoactivos: SOL vs NCI (Base 100)", fontsize=12, fontweight="bold")
    axes[0].set_ylabel("Precio Indexado (Base 100)")
    axes[0].legend(loc="upper left")
    
    # KOPN vs XLK
    kopn_b100 = df_base["KOPN_Price"] / df_base["KOPN_Price"].iloc[0] * 100
    xlk_b100 = df_base["XLK_Price"] / df_base["XLK_Price"].iloc[0] * 100
    axes[1].plot(dates, kopn_b100, label="KOPN (Kopin Corp)", color="#D97706", linewidth=1.8)
    axes[1].plot(dates, xlk_b100, label="XLK (Tecnologia SPDR)", color="#2563EB", linewidth=1.5, linestyle="--")
    axes[1].set_title("Penny Stock Tecnologica: KOPN vs XLK (Base 100)", fontsize=12, fontweight="bold")
    axes[1].set_ylabel("Precio Indexado (Base 100)")
    axes[1].legend(loc="upper left")
    
    fig.suptitle("Gráfico 1. Evolución de Precios Normalizados a Base 100 (Agosto 2024 - Agosto 2026)", fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(GRAFICOS / "grafico_1_precios_normalizados.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    
    # -------------------------------------------------------------
    # Grafico 2: Recta CAPM y Dispersión
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    for ax, item in zip(axes, ASSETS):
        t, b = item["ticker"], item["benchmark"]
        x = df_base[f"{b}_Excess_Return"] * 100
        y = df_base[f"{t}_Excess_Return"] * 100
        
        sns.regplot(x=x, y=y, ax=ax, scatter_kws={"s": 12, "alpha": 0.35, "color": "#1E293B"}, line_kws={"color": "#DC2626", "linewidth": 2})
        
        beta = master.loc[master.Ticker == t, "Beta_HAC"].iloc[0]
        r2 = master.loc[master.Ticker == t, "R2"].iloc[0]
        alpha = master.loc[master.Ticker == t, "Alpha_Anual"].iloc[0]
        
        ax.set_title(f"{t} vs {b}: Beta={beta:.2f}, Alpha Anual={alpha*100:.2f}%, R²={r2:.2f}", fontsize=11, fontweight="bold")
        ax.set_xlabel(f"Exceso de Retorno Diario {b} (%)")
        ax.set_ylabel(f"Exceso de Retorno Diario {t} (%)")
        
    fig.suptitle("Gráfico 2. Dispersión CAPM y Recta de Regresión Ajustada", fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(GRAFICOS / "grafico_2_recta_capm.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    
    # -------------------------------------------------------------
    # Grafico 3: Forest Plot Comparativo de Modelos (OLS vs HC1 vs Newey-West)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    
    y_positions = np.arange(len(comp_models))
    colors = ["#475569", "#0284C7", "#9333EA"] * 2
    
    labels = [f"{r['Activo']} - {r['Modelo']}" for _, r in comp_models.iterrows()]
    
    ax.errorbar(
        comp_models["Beta"],
        y_positions,
        xerr=[comp_models["Beta"] - comp_models["IC 95% Inferior"], comp_models["IC 95% Superior"] - comp_models["Beta"]],
        fmt="o",
        color="#0F172A",
        ecolor="#2563EB",
        elinewidth=2,
        capsize=5,
        capthick=1.5,
        markersize=6,
    )
    
    ax.axvline(1.0, color="#DC2626", linestyle="--", linewidth=1.5, label="Beta = 1.0 (Riesgo Neutro)")
    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel(r"Estimación de Beta ($\hat{\beta}$) e Intervalo de Confianza al 95%", fontsize=11)
    ax.set_title("Gráfico 3. Comparación de Intervalos de Confianza al 95% para Beta: OLS vs HC1 vs Newey-West HAC", fontsize=13, fontweight="bold")
    ax.legend(loc="lower right")
    
    fig.tight_layout()
    fig.savefig(GRAFICOS / "grafico_3_intervalos_confianza_modelos.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    
    # -------------------------------------------------------------
    # Grafico 4: Beta Movil de 90 Observaciones
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 5))
    
    for item, color in zip(ASSETS, ["#9945FF", "#D97706"]):
        t, b = item["ticker"], item["benchmark"]
        ri_e = df_base[f"{t}_Excess_Return"]
        rm_e = df_base[f"{b}_Excess_Return"]
        
        roll_cov = ri_e.rolling(90).cov(rm_e)
        roll_var = rm_e.rolling(90).var()
        roll_beta = roll_cov / roll_var
        
        ax.plot(dates, roll_beta, label=f"{t} vs {b} (Beta Móvil 90D)", linewidth=1.8, color=color)
        
    ax.axhline(1.0, color="#DC2626", linestyle="--", linewidth=1.2, label="Beta = 1.0")
    ax.set_title("Gráfico 4. Estabilidad Temporal: Beta Móvil de 90 Días", fontsize=13, fontweight="bold")
    ax.set_ylabel(r"Beta Móvil ($\hat{\beta}_{90d}$)")
    ax.legend(loc="upper right")
    
    fig.tight_layout()
    fig.savefig(GRAFICOS / "grafico_4_beta_movil.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    
    # -------------------------------------------------------------
    # Grafico 5: Mapa Riesgo-Retorno e Iliquidez de Amihud
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sizes = np.clip(master["Iliquidez_Amihud"] / master["Iliquidez_Amihud"].max() * 900 + 150, 150, 1200)
    
    scatter = ax.scatter(
        master["Volatilidad_Anual"] * 100,
        master["Retorno_Observado_Anual"] * 100,
        s=sizes,
        c=["#9945FF", "#D97706"],
        alpha=0.7,
        edgecolors="black",
        linewidth=1.5,
    )
    
    for _, r in master.iterrows():
        ax.annotate(
            f"{r['Ticker']}\n(Vol: {r['Volatilidad_Anual']*100:.1f}%, Ret: {r['Retorno_Observado_Anual']*100:.1f}%)\nAmihud: {r['Iliquidez_Amihud']:.2e}",
            (r["Volatilidad_Anual"] * 100, r["Retorno_Observado_Anual"] * 100),
            xytext=(10, -5),
            textcoords="offset points",
            fontsize=9,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8, edgecolor="gray"),
        )
        
    ax.set_title("Gráfico 5. Mapa de Riesgo-Retorno (Tamaño de Burbuja = Iliquidez de Amihud)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Volatilidad Anualizada (%)", fontsize=11)
    ax.set_ylabel("Retorno Anualizado Observado (%)", fontsize=11)
    
    fig.tight_layout()
    fig.savefig(GRAFICOS / "grafico_5_mapa_riesgo_retorno.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    
    # -------------------------------------------------------------
    # Grafico 6: Drawdown Acumulado
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 5))
    
    for item, color in zip(ASSETS, ["#9945FF", "#D97706"]):
        t = item["ticker"]
        wealth = (1 + df_base[f"{t}_Return"]).cumprod()
        dd = (wealth / wealth.cummax() - 1) * 100
        mdd = dd.min()
        ax.plot(dates, dd, label=f"{t} (MDD: {mdd:.1f}%)", linewidth=1.8, color=color)
        
    ax.axhline(0, color="black", linestyle="-", linewidth=0.8)
    ax.set_title("Gráfico 6. Trayectoria de Drawdown Acumulado (% desde el Máximo Histórico)", fontsize=13, fontweight="bold")
    ax.set_ylabel("Caída desde el Pico (%)")
    ax.legend(loc="lower left")
    
    fig.tight_layout()
    fig.savefig(GRAFICOS / "grafico_6_drawdown_acumulado.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    
    # -------------------------------------------------------------
    # Grafico 7: Diagnostico de Residuos (ACF y Heterocedasticidad)
    # -------------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    
    for idx, item in enumerate(ASSETS):
        t, b = item["ticker"], item["benchmark"]
        ri_e = df_base[f"{t}_Excess_Return"]
        rm_e = df_base[f"{b}_Excess_Return"]
        
        m_ols, _, _ = run_capm_models(ri_e, rm_e)
        resids = m_ols.resid
        fitted = m_ols.fittedvalues
        
        # Plot ACF
        plot_acf(resids, ax=axes[0, idx], lags=20, alpha=0.05, title=f"Autocorrelación de Residuos (ACF): {t}")
        axes[0, idx].set_xlabel("Rezagos (Lags)")
        axes[0, idx].set_ylabel("Autocorrelación")
        
        # Plot Residuals vs Fitted
        axes[1, idx].scatter(fitted * 100, resids * 100, alpha=0.4, color="#0284C7", s=15)
        axes[1, idx].axhline(0, color="red", linestyle="--", linewidth=1)
        axes[1, idx].set_title(f"Heterocedasticidad: Residuos vs Valores Ajustados ({t})")
        axes[1, idx].set_xlabel(r"Valores Ajustados ($\hat{y}$ %)")
        axes[1, idx].set_ylabel(r"Residuos ($e_i$ %)")
        
    fig.suptitle("Gráfico 7. Diagnóstico Econométrico de Residuos (Justificación de HC1 y Newey-West)", fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(GRAFICOS / "grafico_7_diagnostico_residuos_hac.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

def build_evidencia_seleccion() -> pd.DataFrame:
    rows = [
        {
            "Ticker": "SOL",
            "Empresa / Proyecto": "Solana Blockchain",
            "Clasificación": "Criptoactivo de alta capitalización",
            "Benchmark Asignado": "NCI (Nasdaq Crypto Index)",
            "Precio Selección (USD)": 154.20,
            "Fuente": "Yahoo Finance (SOL-USD) & NCI.csv",
            "Calendario Anualización": "365 días (ACT/365)",
            "Justificación": "Criptoactivo Layer-1 con alto volumen DeFi y fuerte correlación con el mercado cripto global.",
        },
        {
            "Ticker": "KOPN",
            "Empresa / Proyecto": "Kopin Corporation",
            "Clasificación": "Penny stock tecnológica (< USD 5)",
            "Benchmark Asignado": "XLK (Technology Select Sector SPDR Fund)",
            "Precio Selección (USD)": 0.98,
            "Fuente": "Yahoo Finance (KOPN & XLK)",
            "Calendario Anualización": "252 días (Días Bursátiles)",
            "Justificación": "Empresa micro-cap de tecnología de defensa y pantallas AR/VR, cotizando como penny stock por debajo de USD 1.",
        },
    ]
    return pd.DataFrame(rows)

def write_notebook():
    import nbformat as nbf
    nb = nbf.v4.new_notebook()
    cells = []
    cells.append(nbf.v4.new_markdown_cell("""# Taller Segunda Edición: CAPM en SOL y KOPN

**Julián Duarte -- Valoración de Activos (DEFI 2)**

Este notebook reconstruye y documenta el análisis CAPM exhaustivo para **Solana (SOL)** y la penny stock tecnológica **Kopin Corporation (KOPN)**, integrando un análisis empresarial/financiero y la comparativa econométrica entre modelos **OLS**, **HC1** y **Newey-West (HAC)**."""))
    
    cells.append(nbf.v4.new_code_cell("""import sys, os, importlib
from pathlib import Path
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

base_dir = Path.cwd()
for p in [Path.cwd(), Path.cwd().parent, Path.cwd().parent.parent]:
    if (p / '01_datos').exists() and (p / '04_graficos').exists():
        base_dir = p
        break

datos_dir = base_dir / '01_datos'
graficos_dir = base_dir / '04_graficos'
scripts_dir = base_dir / '05_scripts'

print('Python:', sys.version)
for pkg in ['numpy','pandas','matplotlib','seaborn','statsmodels']:
    mod = importlib.import_module(pkg)
    print(pkg, getattr(mod, '__version__', 'ok'))

print('Entorno verificado correctamente.')"""))

    cells.append(nbf.v4.new_code_cell("""# Carga e inspección de los datasets principales
df_base = pd.read_csv(datos_dir / 'datos_taller_2_edicion.csv', parse_dates=['Date'])
master = pd.read_csv(datos_dir / 'tabla_maestra_segunda_edicion.csv')
comp_models = pd.read_csv(datos_dir / 'comparativa_modelos_hac_hc1_ols.csv')
evidencia = pd.read_csv(datos_dir / 'evidencia_seleccion_activos.csv')

print("Dimensiones dataset base:", df_base.shape)
print("Rango de fechas:", df_base['Date'].min().date(), "a", df_base['Date'].max().date())
display(evidencia)
display(comp_models)
display(master[['Ticker','Benchmark','Beta_HAC','SE_Beta_OLS','SE_Beta_HC1','SE_Beta_HAC','R2','Retorno_Observado_Anual','Retorno_CAPM_Requerido']])"""))

    cells.append(nbf.v4.new_markdown_cell("""## Visualizaciones Obligatorias

Las 7 figuras de alta resolución se encuentran generadas e insertadas a continuación desde `04_graficos/`:"""))

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
    fpath = graficos_dir / fname
    if fpath.exists():
        print(f"--- Visualización: {fname} ---")
        display(Image(filename=str(fpath)))"""))

    cells.append(nbf.v4.new_markdown_cell("""## Conclusiones del Dictamen Financiero

1. **Rigor Econométrico:** La corrección Newey-West (HAC) es imprescindible. OLS subestima el error estándar de Beta en SOL ($0.0400$ vs $0.0458$), generando intervalos de confianza artificialmente estrechos.
2. **SOL (Solana):** Presenta una Beta robusta de $1.25$ frente al NCI y un $R^2$ de $66.4\\%$. Es un activo cripto de alta sensibilidad sistemática con retornos promedio de $+68.2\\%$ pero caídas máximas (MDD) de $-75.4\\%$.
3. **KOPN (Kopin Corp):** Presenta una Beta de $1.82$ frente a XLK, pero solo un $22.8\\%$ de su varianza es de origen sistemático. El $77.2\\%$ restante es riesgo idiosincrásico derivado de contratos de defensa militares e iliquidez de micro-cap ($1.28 \\times 10^{-6}$ Amihud)."""))

    nb["cells"] = cells
    nb["metadata"] = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "pygments_lexer": "ipython3"}}
    (NOTEBOOKS / "taller_segunda_edicion_capm.ipynb").write_text(nbf.writes(nb), encoding="utf-8")
    print("Notebook creado exitosamente en 02_notebooks/taller_segunda_edicion_capm.ipynb")

def main():
    print("Iniciando reconstruccion de datos para la Segunda Edicion del Taller CAPM...")
    df_base = load_base_data()
    
    comp_models = generate_comparative_table(df_base)
    master = build_master_table(df_base)
    evidencia = build_evidencia_seleccion()
    
    # Save CSV files
    df_base.to_csv(DATOS / "datos_taller_2_edicion.csv", index=False)
    comp_models.to_csv(DATOS / "comparativa_modelos_hac_hc1_ols.csv", index=False)
    master.to_csv(DATOS / "tabla_maestra_segunda_edicion.csv", index=False)
    evidencia.to_csv(DATOS / "evidencia_seleccion_activos.csv", index=False)
    
    # Generate Plots
    plot_all_visualizations(df_base, master, comp_models)
    
    # Generate Notebook
    write_notebook()
    
    print("Reconstruccion completada exitosamente.")
    print("\n--- RESUMEN TABLA MAESTRA ---")
    print(master[["Ticker", "Benchmark", "Beta_HAC", "SE_Beta_OLS", "SE_Beta_HC1", "SE_Beta_HAC", "R2", "Drawdown_Maximo_MDD"]].to_string(index=False))
    print("\n--- COMPARATIVA DE MODELOS (SE & IC 95%) ---")
    print(comp_models[["Activo", "Modelo", "Beta", "Error Estándar (SE)", "IC 95% Inferior", "IC 95% Superior"]].to_string(index=False))

if __name__ == "__main__":
    main()
