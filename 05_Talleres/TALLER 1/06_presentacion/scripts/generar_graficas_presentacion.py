from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "01_datos" / "tabla_maestra_resultados.csv"
OUT = ROOT / "06_presentacion" / "graficas"

COLORS = {
    "Cripto": "#2563EB",
    "Tecnologia": "#7C3AED",
    "Biotecnologia": "#059669",
    "Energia": "#EA580C",
}


def pct(x):
    return x * 100


def style_ax(ax, title, subtitle=None):
    ax.set_title(title, loc="left", fontsize=16, fontweight="bold", pad=24)
    if subtitle:
        ax.text(
            0,
            1.03,
            subtitle,
            transform=ax.transAxes,
            ha="left",
            va="bottom",
            fontsize=10.5,
            color="#475569",
        )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#CBD5E1")
    ax.spines["bottom"].set_color("#CBD5E1")
    ax.grid(axis="x", color="#E2E8F0", linewidth=0.8)
    ax.tick_params(colors="#334155")


def add_footer(fig):
    fig.text(
        0.02,
        0.015,
        "Fuente: tabla_maestra_resultados.csv | CAPM con errores HAC Newey-West",
        fontsize=8,
        color="#64748B",
    )


def plot_brecha(df):
    d = df.copy()
    d["Brecha"] = d["Observed_Return"] - d["CAPM_Expected_Return"]
    d = d.sort_values("Brecha")
    fig, ax = plt.subplots(figsize=(13.33, 7.5), dpi=180)
    colors = np.where(d["Brecha"] >= 0, "#059669", "#DC2626")
    ax.barh(d["Ticker"], pct(d["Brecha"]), color=colors)
    ax.axvline(0, color="#0F172A", linewidth=1)
    for y, value in enumerate(d["Brecha"]):
        ax.text(
            pct(value) + (2 if value >= 0 else -2),
            y,
            f"{pct(value):+.1f} pp",
            va="center",
            ha="left" if value >= 0 else "right",
            fontsize=10,
            color="#0F172A",
        )
    style_ax(
        ax,
        "Brecha entre retorno observado y retorno requerido por CAPM",
        "Valores positivos: el activo supero lo que CAPM exigia para su beta.",
    )
    ax.set_xlabel("Puntos porcentuales")
    add_footer(fig)
    fig.tight_layout(rect=[0.01, 0.04, 0.99, 0.88])
    fig.savefig(OUT / "07_brecha_retorno_capm.png", transparent=False, facecolor="white")
    plt.close(fig)


def plot_drawdown_cvar(df):
    d = df.sort_values("MDD")
    y = np.arange(len(d))
    fig, ax = plt.subplots(figsize=(13.33, 7.5), dpi=180)
    ax.scatter(pct(d["MDD"]), y, s=140, color="#DC2626", label="Max drawdown")
    ax.scatter(pct(d["CVaR_95_Daily"]), y, s=90, color="#F97316", label="CVaR 95% diario")
    for yi, row in zip(y, d.itertuples()):
        ax.plot([pct(row.MDD), pct(row.CVaR_95_Daily)], [yi, yi], color="#CBD5E1", linewidth=2)
        ax.text(pct(row.MDD) - 1, yi, f"{pct(row.MDD):.1f}%", ha="right", va="center", fontsize=9)
    ax.set_yticks(y)
    ax.set_yticklabels(d["Ticker"])
    style_ax(
        ax,
        "Perdida extrema: drawdown vs CVaR",
        "El drawdown muestra el golpe acumulado; el CVaR resume los peores dias.",
    )
    ax.set_xlabel("Retorno / perdida")
    ax.legend(frameon=False, loc="lower right")
    add_footer(fig)
    fig.tight_layout(rect=[0.01, 0.04, 0.99, 0.88])
    fig.savefig(OUT / "08_ranking_drawdown_cvar.png", transparent=False, facecolor="white")
    plt.close(fig)


def plot_beta_drawdown(df):
    fig, ax = plt.subplots(figsize=(13.33, 7.5), dpi=180)
    for family, group in df.groupby("Family"):
        ax.scatter(
            group["Beta"],
            pct(group["MDD"]),
            s=group["Vol_Annual"] * 260,
            color=COLORS.get(family, "#64748B"),
            alpha=0.82,
            edgecolor="white",
            linewidth=1,
            label=family,
        )
        for row in group.itertuples():
            ax.text(row.Beta + 0.02, pct(row.MDD) + 1, row.Ticker, fontsize=9, color="#0F172A")
    ax.axvline(1, color="#334155", linestyle="--", linewidth=1)
    ax.axhline(-70, color="#DC2626", linestyle="--", linewidth=1)
    style_ax(
        ax,
        "Mapa de alerta: beta vs max drawdown",
        "Tamano de burbuja = volatilidad anual. Abajo y a la derecha implica sensibilidad y caidas severas.",
    )
    ax.set_xlabel("Beta CAPM")
    ax.set_ylabel("Max drawdown")
    ax.yaxis.set_major_formatter(lambda x, pos: f"{x:.0f}%")
    ax.legend(frameon=False, loc="lower left")
    add_footer(fig)
    fig.tight_layout(rect=[0.01, 0.04, 0.99, 0.88])
    fig.savefig(OUT / "09_mapa_beta_drawdown.png", transparent=False, facecolor="white")
    plt.close(fig)


def plot_liquidez(df):
    d = df.copy()
    d["Log_Amihud"] = np.log10(d["Amihud_Illiquidity"].replace(0, np.nan))
    fig, ax = plt.subplots(figsize=(13.33, 7.5), dpi=180)
    for family, group in d.groupby("Family"):
        ax.scatter(
            pct(group["Pct_Zero_Returns"]),
            group["Log_Amihud"],
            s=np.clip(260 - np.log10(group["Med_Monetary_Volume"]) * 20, 80, 260),
            color=COLORS.get(family, "#64748B"),
            alpha=0.84,
            edgecolor="white",
            linewidth=1,
            label=family,
        )
        for row in group.itertuples():
            ax.text(
                pct(row.Pct_Zero_Returns) + 0.25,
                row.Log_Amihud + 0.05,
                row.Ticker,
                fontsize=9,
                color="#0F172A",
            )
    style_ax(
        ax,
        "Liquidez: dias sin retorno y Amihud",
        "Mas arriba implica mayor iliquidez; mas a la derecha implica mas retornos exactamente cero.",
    )
    ax.set_xlabel("% de dias con retorno cero")
    ax.set_ylabel("log10(Amihud)")
    ax.legend(frameon=False, loc="lower right")
    add_footer(fig)
    fig.tight_layout(rect=[0.01, 0.04, 0.99, 0.88])
    fig.savefig(OUT / "10_liquidez_retornos_cero.png", transparent=False, facecolor="white")
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA)
    plot_brecha(df)
    plot_drawdown_cvar(df)
    plot_beta_drawdown(df)
    plot_liquidez(df)


if __name__ == "__main__":
    main()
