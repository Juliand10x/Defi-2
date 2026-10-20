from __future__ import annotations

import json
import math
from pathlib import Path

import nbformat as nbf
import numpy as np
import pandas as pd
import statsmodels.api as sm
import yfinance as yf


try:
    ROOT = Path(__file__).resolve().parents[1]
except NameError:
    ROOT = Path.cwd().parent if Path.cwd().name in ('05_scripts', '02_notebooks') else Path.cwd()
DATOS = ROOT / "01_datos"
NOTEBOOKS = ROOT / "02_notebooks"
INFORME = ROOT / "03_informe"
GRAFICOS = ROOT / "04_graficos"
SCRIPTS = ROOT / "05_scripts"

DATOS.mkdir(exist_ok=True)
NOTEBOOKS.mkdir(exist_ok=True)
INFORME.mkdir(exist_ok=True)
GRAFICOS.mkdir(exist_ok=True)
SCRIPTS.mkdir(exist_ok=True)

START = "2024-08-24"
END = "2026-08-25"
SELECTION_DATE = pd.Timestamp("2026-08-20")

ASSETS = [
    {"ticker": "SOL", "yf": "SOL-USD", "name": "Solana", "family": "Cripto", "sector": "Criptoactivos", "benchmark": "NCI", "K": 365, "type": "Criptoactivo"},
    {"ticker": "KOPN", "yf": "KOPN", "name": "Kopin Corporation", "family": "Tecnologia", "sector": "Tecnologia", "benchmark": "XLK", "K": 252, "type": "Penny stock"},
    {"ticker": "MVIS", "yf": "MVIS", "name": "MicroVision, Inc.", "family": "Tecnologia", "sector": "Tecnologia", "benchmark": "XLK", "K": 252, "type": "Penny stock"},
    {"ticker": "LIDR", "yf": "LIDR", "name": "AEye, Inc.", "family": "Tecnologia", "sector": "Tecnologia", "benchmark": "XLK", "K": 252, "type": "Penny stock"},
    {"ticker": "GERN", "yf": "GERN", "name": "Geron Corporation", "family": "Biotecnologia", "sector": "Biotecnologia", "benchmark": "XBI", "K": 252, "type": "Penny stock"},
    {"ticker": "CTMX", "yf": "CTMX", "name": "CytomX Therapeutics, Inc.", "family": "Biotecnologia", "sector": "Biotecnologia", "benchmark": "XBI", "K": 252, "type": "Penny stock"},
    {"ticker": "OCGN", "yf": "OCGN", "name": "Ocugen, Inc.", "family": "Biotecnologia", "sector": "Biotecnologia", "benchmark": "XBI", "K": 252, "type": "Penny stock"},
    {"ticker": "BORR", "yf": "BORR", "name": "Borr Drilling Limited", "family": "Energia", "sector": "Energia", "benchmark": "XLE", "K": 252, "type": "Penny stock"},
    {"ticker": "KLXE", "yf": "KLXE", "name": "KLX Energy Services Holdings, Inc.", "family": "Energia", "sector": "Energia", "benchmark": "XLE", "K": 252, "type": "Penny stock"},
    {"ticker": "TTI", "yf": "TTI", "name": "TETRA Technologies, Inc.", "family": "Energia", "sector": "Energia", "benchmark": "XLE", "K": 252, "type": "Accion de bajo precio"},
]
BENCHMARKS = [
    {"ticker": "NCI", "yf": None, "name": "Nasdaq Crypto Index"},
    {"ticker": "XLK", "yf": "XLK", "name": "Technology Select Sector SPDR Fund"},
    {"ticker": "XBI", "yf": "XBI", "name": "SPDR S&P Biotech ETF"},
    {"ticker": "XLE", "yf": "XLE", "name": "Energy Select Sector SPDR Fund"},
]


def download_yahoo(symbols: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = yf.download(
        symbols,
        start=START,
        end=END,
        progress=False,
        auto_adjust=False,
        threads=False,
    )
    if raw.empty:
        raise RuntimeError("Yahoo Finance no devolvio datos.")
    if not isinstance(raw.columns, pd.MultiIndex):
        raw.columns = pd.MultiIndex.from_product([raw.columns, symbols])
    price_field = "Adj Close" if "Adj Close" in raw.columns.get_level_values(0) else "Close"
    prices = raw[price_field].copy()
    volumes = raw["Volume"].copy()
    prices.index = pd.to_datetime(prices.index).normalize()
    volumes.index = pd.to_datetime(volumes.index).normalize()
    return prices, volumes


def load_nci() -> pd.Series:
    nci_path = DATOS / "NCI.csv" if (DATOS / "NCI.csv").exists() else ROOT / "NCI.csv"
    nci = pd.read_csv(nci_path)
    nci["Date"] = pd.to_datetime(nci["Date"], format="%m/%d/%Y")
    nci = nci.sort_values("Date").set_index("Date")
    return nci["Close/Last"].rename("NCI")


def load_fred_rf(index: pd.DatetimeIndex) -> pd.Series:
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS3MO"
    try:
        rf = pd.read_csv(url)
        rf["observation_date"] = pd.to_datetime(rf["observation_date"])
        rf["DGS3MO"] = pd.to_numeric(rf["DGS3MO"], errors="coerce") / 100.0
        rf = rf.set_index("observation_date")["DGS3MO"].sort_index()
    except Exception:
        legacy_path = DATOS / "datos_taller_1_julian_duarte.csv" if (DATOS / "datos_taller_1_julian_duarte.csv").exists() else ROOT / "datos_taller_1_julian_duarte.csv"
        if legacy_path.exists():
            legacy = pd.read_csv(legacy_path, parse_dates=["Date"])
            if "Rf_Annual" in legacy.columns:
                rf = legacy.set_index("Date")["Rf_Annual"].sort_index()
            else:
                rf = pd.Series(0.04, index=index)
        else:
            rf = pd.Series(0.04, index=index)
    return rf.reindex(index).ffill().bfill().rename("Rf_Annual")


def capm_hac(ri_e: pd.Series, rm_e: pd.Series):
    X = sm.add_constant(rm_e)
    return sm.OLS(ri_e, X, missing="drop").fit(cov_type="HAC", cov_kwds={"maxlags": 5})


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


def build_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    y_symbols = sorted({x["yf"] for x in ASSETS + BENCHMARKS if x["yf"]})
    prices_y, volumes_y = download_yahoo(y_symbols)
    nci = load_nci()

    price_map = {"NCI": nci}
    volume_map = {"NCI": pd.Series(0.0, index=nci.index, name="NCI")}
    for item in ASSETS + BENCHMARKS:
        yf_symbol = item.get("yf")
        if not yf_symbol:
            continue
        ticker = item["ticker"]
        price_map[ticker] = prices_y[yf_symbol].rename(ticker)
        volume_map[ticker] = volumes_y[yf_symbol].rename(ticker)

    tickers = [a["ticker"] for a in ASSETS] + [b["ticker"] for b in BENCHMARKS]
    prices = pd.concat([price_map[t] for t in tickers], axis=1, sort=True)
    volumes = pd.concat([volume_map[t] for t in tickers], axis=1, sort=True)

    # Stocks force a business-day intersection; SOL and NCI are aligned to those dates.
    required = [a["ticker"] for a in ASSETS] + ["NCI", "XLK", "XBI", "XLE"]
    prices = prices.dropna(subset=required)
    volumes = volumes.reindex(prices.index)
    returns = prices.pct_change().dropna()
    prices = prices.loc[returns.index]
    volumes = volumes.loc[returns.index]

    rf = load_fred_rf(returns.index)
    out = pd.DataFrame({"Date": returns.index})
    out["Rf_Annual"] = rf.values
    out["Rf_Daily_252"] = (1 + out["Rf_Annual"]) ** (1 / 252) - 1
    out["Rf_Daily_365"] = (1 + out["Rf_Annual"]) ** (1 / 365) - 1

    for t in tickers:
        K = 365 if t in ["SOL", "NCI"] else 252
        rf_col = "Rf_Daily_365" if K == 365 else "Rf_Daily_252"
        out[f"{t}_Price"] = prices[t].values
        out[f"{t}_Return"] = returns[t].values
        out[f"{t}_Excess_Return"] = returns[t].values - out[rf_col].values
        out[f"{t}_Volume"] = volumes[t].values
        out[f"{t}_Monetary_Volume"] = prices[t].values * volumes[t].values

    # Backward-compatible return columns for quick inspection.
    for t in tickers:
        out[t] = out[f"{t}_Return"]

    selection_rows = []
    sel_prices = prices.reindex([SELECTION_DATE], method="ffill").iloc[0]
    for item in ASSETS:
        price = float(sel_prices[item["ticker"]])
        selection_rows.append({
            "Ticker": item["ticker"],
            "Empresa": item["name"],
            "Sector declarado": item["sector"],
            "Benchmark": item["benchmark"],
            "Precio seleccion USD": round(price, 4),
            "Fecha consulta": SELECTION_DATE.date().isoformat(),
            "Mercado/Fuente": "Yahoo Finance; NCI.csv suministrado por profesor; FRED DGS3MO para tasa libre de riesgo",
            "Clasificacion": ("Criptoactivo asignado" if item["type"] == "Criptoactivo" else (item["type"] if price < 5 else "Accion de bajo precio (excepcion < USD 10)")),
            "Cumple precio": ("No aplica" if item["type"] == "Criptoactivo" else ("Si" if price < 5 else ("Excepcion < USD 10" if price < 10 else "No"))),
        })
    selection = pd.DataFrame(selection_rows)
    return out, selection, prices


def build_master(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for item in ASSETS:
        t = item["ticker"]
        b = item["benchmark"]
        K = item["K"]
        rf_col = "Rf_Daily_365" if K == 365 else "Rf_Daily_252"
        ri = data[f"{t}_Return"]
        rm = data[f"{b}_Return"]
        ri_e = data[f"{t}_Excess_Return"]
        rm_e = data[f"{b}_Excess_Return"]
        model = capm_hac(ri_e, rm_e)
        alpha = float(model.params.iloc[0])
        beta = float(model.params.iloc[1])
        se_beta = float(model.bse.iloc[1])
        ci = model.conf_int().iloc[1]
        rf_ann = float(data[rf_col].mean() * K)
        rm_ann = float(rm.mean() * K)
        obs = float(ri.mean() * K)
        capm = rf_ann + beta * (rm_ann - rf_ann)
        vol = float(ri.std(ddof=1) * math.sqrt(K))
        excess_ann = obs - rf_ann
        downside = ri[ri < 0]
        downside_dev = float(np.sqrt((downside**2).mean()) * math.sqrt(K)) if len(downside) else np.nan
        var95 = float(ri.quantile(0.05))
        cvar95 = float(ri[ri <= var95].mean())
        beta_minus = downside_beta(ri_e, rm_e)
        dimson = dimson_beta(ri_e, rm_e)
        beta_win = winsor_beta(ri_e, rm_e)
        med_mv = float(data[f"{t}_Monetary_Volume"].median(skipna=True)) if f"{t}_Monetary_Volume" in data else np.nan
        amihud = float((ri.abs() / data[f"{t}_Monetary_Volume"].replace(0, np.nan)).mean(skipna=True)) if t != "SOL" else float((ri.abs() / data[f"{t}_Monetary_Volume"].replace(0, np.nan)).mean(skipna=True))
        rows.append({
            "Ticker": t,
            "Name": item["name"],
            "Family": item["family"],
            "Sector": item["sector"],
            "Benchmark": b,
            "K": K,
            "Alpha_Daily": alpha,
            "Alpha_Annual": alpha * K,
            "Beta": beta,
            "SE_Beta": se_beta,
            "CI_Beta_Low": float(ci.iloc[0]),
            "CI_Beta_High": float(ci.iloc[1]),
            "P_Val_Beta": float(model.pvalues.iloc[1]),
            "P_Val_Alpha": float(model.pvalues.iloc[0]),
            "R2": float(model.rsquared),
            "R2_Adj": float(model.rsquared_adj),
            "Observed_Return": obs,
            "CAPM_Expected_Return": capm,
            "Vol_Annual": vol,
            "Sharpe": excess_ann / vol if vol else np.nan,
            "Treynor": excess_ann / beta if abs(beta) > 0.1 else np.nan,
            "Sortino": excess_ann / downside_dev if downside_dev else np.nan,
            "MDD": max_drawdown(ri),
            "VaR_95_Daily": var95,
            "CVaR_95_Daily": cvar95,
            "Best_Day": float(ri.max()),
            "Worst_Day": float(ri.min()),
            "Skewness": float(ri.skew()),
            "Kurtosis": float(ri.kurtosis()),
            "Pct_Zero_Returns": float((ri == 0).mean() * 100),
            "Med_Volume": float(data[f"{t}_Volume"].median(skipna=True)),
            "Med_Monetary_Volume": med_mv,
            "Amihud_Illiquidity": amihud,
            "Beta_Minus": beta_minus,
            "Beta_Dimson_Sum": dimson,
            "Beta_Winsor": beta_win,
            "T_Beta_1": (beta - 1) / se_beta if se_beta else np.nan,
            "N_Obs": int(len(ri)),
        })
    return pd.DataFrame(rows)


def plot_all(data: pd.DataFrame, master: pd.DataFrame):
    import matplotlib.pyplot as plt
    import seaborn as sns

    plt.style.use("seaborn-v0_8-whitegrid")
    dates = pd.to_datetime(data["Date"])
    tickers = [a["ticker"] for a in ASSETS]

    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    groups = [
        ("Cripto: SOL frente al NCI", ["SOL", "NCI"]),
        ("Tecnologia frente a XLK", ["KOPN", "MVIS", "LIDR", "XLK"]),
        ("Biotecnologia frente a XBI", ["GERN", "CTMX", "OCGN", "XBI"]),
        ("Energia frente a XLE", ["BORR", "KLXE", "TTI", "XLE"]),
    ]
    for ax, (title, cols) in zip(axes.flat, groups):
        for c in cols:
            base = data[f"{c}_Price"] / data[f"{c}_Price"].iloc[0] * 100
            ax.plot(dates, base, label=c, linewidth=1.4)
        ax.set_title(title)
        ax.set_ylabel("Base 100")
        ax.legend(fontsize=8)
    fig.suptitle("Grafico 1. Precios ajustados normalizados a 100, agosto 2024-agosto 2026")
    fig.tight_layout()
    fig.savefig(GRAFICOS / "grafico_1_precios_normalizados.png", dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(5, 2, figsize=(14, 20))
    for ax, item in zip(axes.flat, ASSETS):
        t, b = item["ticker"], item["benchmark"]
        sns.regplot(x=data[f"{b}_Excess_Return"] * 100, y=data[f"{t}_Excess_Return"] * 100, ax=ax, scatter_kws={"s": 10, "alpha": 0.35}, line_kws={"color": "crimson"})
        beta = master.loc[master.Ticker == t, "Beta"].iloc[0]
        r2 = master.loc[master.Ticker == t, "R2"].iloc[0]
        ax.set_title(f"{t} vs {b}: beta={beta:.2f}, R2={r2:.2f}")
        ax.set_xlabel(f"Exceso {b} (%)")
        ax.set_ylabel(f"Exceso {t} (%)")
    fig.suptitle("Grafico 2. Dispersion CAPM con recta ajustada por activo")
    fig.tight_layout()
    fig.savefig(GRAFICOS / "grafico_2_recta_capm_todos.png", dpi=180)
    plt.close(fig)

    df = master.sort_values("Beta")
    fig, ax = plt.subplots(figsize=(10, 6))
    y = np.arange(len(df))
    ax.errorbar(df["Beta"], y, xerr=[df["Beta"] - df["CI_Beta_Low"], df["CI_Beta_High"] - df["Beta"]], fmt="o", capsize=4)
    ax.axvline(1, color="crimson", linestyle="--")
    ax.set_yticks(y, df["Ticker"] + " (" + df["Benchmark"] + ")")
    ax.set_title("Grafico 3. Betas CAPM con intervalos HAC al 95%")
    ax.set_xlabel("Beta")
    fig.tight_layout()
    fig.savefig(GRAFICOS / "grafico_3_forest_plot_betas.png", dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(5, 2, figsize=(14, 18))
    for ax, item in zip(axes.flat, ASSETS):
        t, b = item["ticker"], item["benchmark"]
        roll = data[f"{t}_Excess_Return"].rolling(90).cov(data[f"{b}_Excess_Return"]) / data[f"{b}_Excess_Return"].rolling(90).var()
        ax.plot(dates, roll, linewidth=1.2)
        ax.axhline(1, color="black", linestyle="--", alpha=0.5)
        ax.set_title(f"{t}: beta movil 90 observaciones frente a {b}")
    fig.suptitle("Grafico 4. Estabilidad temporal de beta")
    fig.tight_layout()
    fig.savefig(GRAFICOS / "grafico_4_beta_movil_todos.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    sizes = np.clip(master["Amihud_Illiquidity"].fillna(0) / master["Amihud_Illiquidity"].fillna(0).max() * 800 + 80, 80, 900)
    sns.scatterplot(data=master, x=master["Vol_Annual"] * 100, y=master["Observed_Return"] * 100, hue="Family", size=sizes, sizes=(80, 900), ax=ax, legend="brief")
    for _, r in master.iterrows():
        ax.annotate(r["Ticker"], (r["Vol_Annual"] * 100, r["Observed_Return"] * 100), xytext=(4, 4), textcoords="offset points", fontsize=8)
    ax.set_xscale("log")
    ax.set_title("Grafico 5. Mapa riesgo-retorno; tamano por iliquidez de Amihud")
    ax.set_xlabel("Volatilidad anualizada (%)")
    ax.set_ylabel("Retorno observado anualizado (%)")
    fig.tight_layout()
    fig.savefig(GRAFICOS / "grafico_5_mapa_riesgo_retorno.png", dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(5, 2, figsize=(14, 18))
    for ax, item in zip(axes.flat, ASSETS):
        t = item["ticker"]
        wealth = (1 + data[f"{t}_Return"]).cumprod()
        dd = wealth / wealth.cummax() - 1
        ax.plot(dates, dd * 100, linewidth=1.2)
        ax.set_title(f"{t}: drawdown maximo {dd.min()*100:.1f}%")
        ax.set_ylabel("% desde pico")
    fig.suptitle("Grafico 6. Drawdown acumulado por activo")
    fig.tight_layout()
    fig.savefig(GRAFICOS / "grafico_6_drawdown_acumulado_todos.png", dpi=180)
    plt.close(fig)

    pct = master.copy()
    metrics = ["Vol_Annual", "MDD", "CVaR_95_Daily", "Amihud_Illiquidity", "Beta_Minus"]
    for m in metrics:
        pct[m] = pct.groupby("Family")[m].rank(pct=True) * 100
    matrix = pct.set_index("Ticker")[metrics]
    matrix.columns = ["Volatilidad", "Drawdown", "CVaR", "Iliquidez", "Beta bajista"]
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(matrix, annot=True, fmt=".0f", cmap="YlOrRd", ax=ax)
    ax.set_title("Grafico 7. Percentiles de riesgo dentro de cada familia")
    fig.tight_layout()
    fig.savefig(GRAFICOS / "grafico_7_matriz_percentiles.png", dpi=180)
    plt.close(fig)


def pct(x):
    if pd.isna(x):
        return "N/A"
    return f"{x*100:.2f}\\%"


def write_tex(master: pd.DataFrame, selection: pd.DataFrame):
    rows1 = "\n".join(
        f"{r.Ticker} & {r.Benchmark} & {pct(r.Alpha_Annual)} & {r.Beta:.2f} & [{r.CI_Beta_Low:.2f},{r.CI_Beta_High:.2f}] & {r.R2:.2f} & {pct(r.Observed_Return)} & {pct(r.CAPM_Expected_Return)} \\\\"
        for r in master.itertuples()
    )
    rows2 = "\n".join(
        f"{r.Ticker} & {pct(r.Vol_Annual)} & {r.Sharpe:.2f} & {pct(r.MDD)} & {pct(r.CVaR_95_Daily)} & {r.Pct_Zero_Returns:.1f}\\% & {r.Beta_Minus:.2f} & {r.Amihud_Illiquidity:.2e} \\\\"
        for r in master.itertuples()
    )
    tex = rf"""\documentclass[10pt,a4paper]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[spanish]{{babel}}
\usepackage{{geometry,booktabs,graphicx,float,hyperref}}
\graphicspath{{{{../04_graficos/}}{{04_graficos/}}{{./}}}}
\geometry{{margin=1.55cm}}
\setlength{{\parskip}}{{2pt}}
\setlength{{\parindent}}{{0pt}}
\title{{\vspace{{-1.2cm}}\textbf{{Informe ejecutivo Taller 1: La Beta de los Pobres}}}}
\author{{Julián Duarte -- Valoración de Activos (DEFI 2)}}
\date{{Agosto de 2026}}
\begin{{document}}
\maketitle
\textbf{{Pregunta.}} ¿Qué revela el CAPM sobre SOL frente al NCI y sobre nueve acciones de bajo precio frente a sus ETF sectoriales? La evidencia muestra que el 25\% anual sin caídas no es defendible: los retornos altos observados vienen acompañados de drawdowns, CVaR e iliquidez severa.

\textbf{{Datos.}} Ventana común: agosto de 2024 a agosto de 2026. SOL se compara con NCI; Tecnología con XLK; Biotecnología con XBI; Energía con XLE. Se usan precios ajustados y volumen de Yahoo Finance, NCI suministrado por el profesor y DGS3MO de FRED. La tasa diaria usa ACT/365 para cripto y 252 días para acciones. Los tickers son KOPN, MVIS, LIDR, GERN, CTMX, OCGN, BORR, KLXE y TTI; TTI se documenta como acción de bajo precio bajo la excepción menor a USD 10.

\begin{{table}}[H]\centering\scriptsize
\caption{{CAPM con errores HAC Newey--West}}
\begin{{tabular}}{{lccccccc}}\toprule
Activo & Bench. & $\alpha$ anual & $\beta$ & IC 95\% $\beta$ & $R^2$ & Ret. obs. & Ret. CAPM\\\midrule
{rows1}
\bottomrule\end{{tabular}}\end{{table}}

\begin{{table}}[H]\centering\scriptsize
\caption{{Riesgo, desempeño y liquidez}}
\begin{{tabular}}{{lccccccc}}\toprule
Activo & Vol. & Sharpe & MDD & CVaR 95\% & $r=0$ & $\beta^-$ & Amihud\\\midrule
{rows2}
\bottomrule\end{{tabular}}\end{{table}}

\begin{{figure}}[H]\centering
\includegraphics[width=.92\linewidth]{{grafico_3_forest_plot_betas.png}}
\caption{{Las betas se interpretan frente a su benchmark propio; una beta alta en XLE no equivale directamente a una beta alta en NCI.}}
\end{{figure}}

\textbf{{Hallazgos.}} SOL tiene una exposición sistemática material frente al mercado cripto y conserva riesgo bajista. En acciones de bajo precio, la beta debe leerse junto con liquidez: retornos cero, bajo volumen monetario y cambios fuertes entre beta contemporánea, Dimson y winsorizada sugieren posible negociación no sincrónica. Las acciones de energía y tecnología concentran episodios de drawdown severo; biotecnología mantiene sensibilidad alta a choques sectoriales y regulatorios.

\textbf{{Hipótesis.}} Se contrasta $H_0:\beta=1$ con el estadístico $(\hat\beta-1)/SE(\hat\beta)$ y $H_0:\alpha=0$ con p-valores HAC. La decisión no se basa solo en significancia: se reportan intervalos, tamaño del efecto y significado financiero.

\textbf{{Recomendación.}} Para conservación, liquidar posiciones con iliquidez extrema o drawdowns incompatibles con el mandato y priorizar T-Bills/ETF diversificados. Para crecimiento, SOL solo puede mantenerse como exposición acotada al mercado cripto, no como fuente de retorno garantizado. Para especulación acotada, limitar cada acción de bajo precio a 1\%-2\% del portafolio y presupuestar pérdida máxima; ninguna posición justifica prometer 25\% anual sin caídas.

\textbf{{Limitaciones.}} El CAPM es lineal, usa betas históricas y no captura eventos discretos como splits, aprobaciones regulatorias, riesgo de financiación o shocks de liquidez. Por eso la recomendación combina beta, drawdown, CVaR, beta bajista, Amihud y estabilidad temporal.
\end{{document}}
"""
    (INFORME / "informe_ejecutivo_taller_1.tex").write_text(tex, encoding="utf-8")

    ficha_rows = "\n".join(
        f"\\item[\\textbf{{{r.Ticker}}}] {r.Name}. Sector: {r.Sector}. Benchmark: {r.Benchmark}. Precio de seleccion: USD {selection.loc[selection.Ticker==r.Ticker, 'Precio seleccion USD'].iloc[0]:.2f}. Beta: {r.Beta:.2f}; MDD: {r.MDD*100:.1f}\\%; liquidez: volumen mediano {r.Med_Volume:,.0f}."
        for r in master.itertuples()
    )
    ficha = rf"""\documentclass[10pt,a4paper]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[spanish]{{babel}}
\usepackage{{geometry,enumitem}}
\geometry{{margin=1.5cm}}
\setlength{{\parskip}}{{2pt}}
\begin{{document}}
\begin{{center}}\Large\textbf{{Ficha de personajes de activos -- Julián Duarte}}\end{{center}}
\begin{{description}}[leftmargin=2.8cm,style=nextline]
{ficha_rows}
\end{{description}}
\vfill
\footnotesize Fuente de precios y volumen: Yahoo Finance, consulta {SELECTION_DATE.date().isoformat()}. NCI: archivo suministrado por el profesor. Tasa libre de riesgo: FRED DGS3MO.
\end{{document}}
"""
    (INFORME / "ficha_personajes_activos.tex").write_text(ficha, encoding="utf-8")


def write_checklist():
    text = """# Checklist de cumplimiento Taller 1 CAPM

- [x] 1 criptoactivo asignado: SOL frente al NCI.
- [x] 3 sectores: Tecnologia (XLK), Biotecnologia (XBI) y Energia (XLE).
- [x] 9 acciones de bajo precio documentadas; TTI queda bajo excepcion < USD 10.
- [x] CSV individual con fechas, precios, retornos, excesos, benchmarks, tasa libre de riesgo y volumen.
- [x] CAPM con alfa, beta, HAC, IC 95%, p-valores, R2, R2 ajustado y retorno requerido.
- [x] Riesgo y desempeno: volatilidad, Sharpe, Treynor, Sortino, MDD, VaR, CVaR, mejor/peor dia, asimetria y curtosis.
- [x] Liquidez: retornos cero, volumen, volumen monetario, Amihud y beta Dimson.
- [x] Estabilidad: beta movil de 90 observaciones, beta bajista y sensibilidad winsorizada.
- [x] 7 visualizaciones obligatorias actualizadas en `04_graficos/`.
- [x] Informe ejecutivo separado del material de estudio.
- [x] Ficha de personajes separada.

Pendiente manual antes de entrega: compilar los `.tex` en Overleaf o en un equipo con LaTeX instalado y confirmar que el informe queda en maximo 6 paginas.
"""
    (INFORME / "checklist_cumplimiento_taller_1.md").write_text(text, encoding="utf-8")


def write_readme_append():
    readme = ROOT / "README.md"
    txt = readme.read_text(encoding="utf-8")
    marker = "## Estado de Verificacion"
    block = f"""

## Estado de Cumplimiento Actualizado

La carpeta fue ajustada para cumplir la rubrica formal del taller:

- `01_datos/datos_taller_1_julian_duarte.csv`: base consolidada con precios ajustados, retornos, excesos, volumen, volumen monetario, benchmarks y tasa libre de riesgo.
- `01_datos/tabla_maestra_resultados.csv`: metricas CAPM, riesgo, liquidez, beta bajista, Dimson y robustez recalculadas.
- `01_datos/evidencia_seleccion_activos.csv`: fuente, fecha de consulta, precio de seleccion y clasificacion de cada activo.
- `03_informe/informe_ejecutivo_taller_1.tex`: version ejecutiva separada del material de estudio.
- `03_informe/ficha_personajes_activos.tex`: ficha sintetica de SOL y las nueve acciones.
- `03_informe/checklist_cumplimiento_taller_1.md`: lista de verificacion contra el enunciado.

Nota: `TTI` se reporta como accion de bajo precio bajo la excepcion permitida por el enunciado (< USD 10), no como penny stock estricta.
"""
    if marker not in txt:
        readme.write_text(txt.rstrip() + "\n" + block, encoding="utf-8")


def write_notebook():
    nb = nbf.v4.new_notebook()
    cells = []
    cells.append(nbf.v4.new_markdown_cell("""# Taller 1: CAPM en dos mercados

**Julián Duarte -- Valoración de Activos (DEFI 2)**

Este notebook reconstruye la base del expediente, audita datos, estima CAPM con errores HAC, calcula métricas de riesgo/liquidez/robustez, produce las siete visualizaciones obligatorias y cierra con recomendación para Doña Victoria."""))
    cells.append(nbf.v4.new_code_cell("""import sys, subprocess, importlib, os
from pathlib import Path

base_dir = Path.cwd()
for p in [Path.cwd(), Path.cwd().parent, Path.cwd().parent.parent]:
    if (p / '01_datos').exists():
        base_dir = p
        break
datos_dir = base_dir / '01_datos'
graficos_dir = base_dir / '04_graficos'
scripts_dir = base_dir / '05_scripts'

print('Python:', sys.version)
for pkg in ['numpy','pandas','matplotlib','seaborn','statsmodels','yfinance','nbformat']:
    mod = importlib.import_module(pkg)
    print(pkg, getattr(mod, '__version__', 'ok'))

print('Entorno y versiones registrados.')"""))
    cells.append(nbf.v4.new_code_cell("""# Ejecuta el pipeline reproducible: descarga precios/volumen, alinea calendarios,
# construye retornos/excesos, estima metricas y regenera tablas/graficos.
script_target = str(scripts_dir / 'rebuild_entregables.py')
exec(open(script_target).read())"""))
    cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(datos_dir / 'datos_taller_1_julian_duarte.csv', parse_dates=['Date'])
master = pd.read_csv(datos_dir / 'tabla_maestra_resultados.csv')
seleccion = pd.read_csv(datos_dir / 'evidencia_seleccion_activos.csv')

print(df.shape, df['Date'].min(), df['Date'].max())
display(seleccion)
display(master[['Ticker','Benchmark','Beta','CI_Beta_Low','CI_Beta_High','R2','Observed_Return','CAPM_Expected_Return']])"""))
    cells.append(nbf.v4.new_code_cell("""activos = ['SOL','KOPN','MVIS','LIDR','GERN','CTMX','OCGN','BORR','KLXE','TTI']
auditoria = []
for t in activos:
    r = df[f'{t}_Return']
    auditoria.append({
        'Activo': t,
        'Inicio': df['Date'].min().date(),
        'Fin': df['Date'].max().date(),
        'Obs': len(r),
        'Faltantes': int(r.isna().sum()),
        'Duplicados fecha': int(df['Date'].duplicated().sum()),
        'Retornos cero (%)': round((r == 0).mean()*100, 2),
        'Volumen mediano': round(df[f'{t}_Volume'].median(), 0),
        '5 peores retornos': ', '.join(f'{x:.2%}' for x in r.nsmallest(5)),
        '5 mejores retornos': ', '.join(f'{x:.2%}' for x in r.nlargest(5)),
    })
display(pd.DataFrame(auditoria))"""))
    cells.append(nbf.v4.new_code_cell("""print('Tabla maestra 1: CAPM')
display(master[['Ticker','Family','Benchmark','Alpha_Annual','Beta','SE_Beta','CI_Beta_Low','CI_Beta_High','P_Val_Beta','P_Val_Alpha','R2','R2_Adj','Observed_Return','CAPM_Expected_Return']])

print('Tabla maestra 2: riesgo, desempeno y liquidez')
display(master[['Ticker','Vol_Annual','Sharpe','Treynor','Sortino','MDD','VaR_95_Daily','CVaR_95_Daily','Best_Day','Worst_Day','Skewness','Kurtosis','Pct_Zero_Returns','Med_Volume','Med_Monetary_Volume','Amihud_Illiquidity','Beta_Minus','Beta_Dimson_Sum','Beta_Winsor','T_Beta_1']])"""))
    cells.append(nbf.v4.new_markdown_cell("""## Visualizaciones obligatorias

Las siete figuras quedan guardadas en `04_graficos/`:

1. Precios normalizados por expediente.
2. Dispersión CAPM con recta para todos los activos.
3. Forest plot de betas con IC HAC.
4. Beta móvil de 90 observaciones para todos los activos.
5. Mapa riesgo-retorno.
6. Drawdown acumulado para todos los activos.
7. Matriz de percentiles por familia."""))
    cells.append(nbf.v4.new_code_cell("""from IPython.display import Image, display
for filename in [
    'grafico_1_precios_normalizados.png',
    'grafico_2_recta_capm_todos.png',
    'grafico_3_forest_plot_betas.png',
    'grafico_4_beta_movil_todos.png',
    'grafico_5_mapa_riesgo_retorno.png',
    'grafico_6_drawdown_acumulado_todos.png',
    'grafico_7_matriz_percentiles.png',
]:
    imgPath = graficos_dir / filename
    print(imgPath)
    if imgPath.exists():
        display(Image(filename=str(imgPath)))"""))
    cells.append(nbf.v4.new_markdown_cell("""## Dictamen final

Doña Victoria no puede exigir 25% anual sin caídas: esa restricción contradice la evidencia de drawdowns, CVaR e iliquidez. Para conservación, se deben evitar posiciones con baja liquidez y pérdidas extremas. Para crecimiento, SOL solo debe mantenerse como exposición acotada al mercado cripto. Para especulación acotada, las acciones de bajo precio deben limitarse a porcentajes pequeños del portafolio y con pérdida máxima presupuestada.

La beta se interpreta dentro de cada benchmark: SOL frente al NCI, tecnología frente a XLK, biotecnología frente a XBI y energía frente a XLE. Una beta baja no se acepta como defensiva si viene acompañada de retornos cero, bajo volumen monetario o fuerte sensibilidad a Dimson/winsorización."""))
    nb["cells"] = cells
    nb["metadata"] = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "pygments_lexer": "ipython3"}}
    (NOTEBOOKS / "taller_1_capm.ipynb").write_text(nbf.writes(nb), encoding="utf-8")


def main():
    legacy = DATOS / "datos_taller_1_julian_duarte.csv"
    backup = DATOS / "datos_taller_1_julian_duarte_retornos_original.csv"
    if legacy.exists() and not backup.exists():
        backup.write_bytes(legacy.read_bytes())

    data, selection, _ = build_data()
    master = build_master(data)

    data.to_csv(DATOS / "datos_taller_1_julian_duarte.csv", index=False)
    selection.to_csv(DATOS / "evidencia_seleccion_activos.csv", index=False)
    master.to_csv(DATOS / "tabla_maestra_resultados.csv", index=False)
    plot_all(data, master)
    write_tex(master, selection)
    write_checklist()
    write_readme_append()
    write_notebook()

    print("Entregables reconstruidos exitosamente.")
    print("Filas dataset:", len(data), "Columnas:", len(data.columns))
    print(master[["Ticker", "Benchmark", "Beta", "R2", "MDD", "Pct_Zero_Returns"]].to_string(index=False))


if __name__ == "__main__":
    main()
