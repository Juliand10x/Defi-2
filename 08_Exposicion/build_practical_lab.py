# -*- coding: utf-8 -*-
"""
Generador del Notebook de Laboratorio Práctico y Compilador a HTML Interactivo.
Tema: Opciones Reales (Árbol Binomial CRR, Plotly Interactivo, Sensibilidad)
Curso: Valoración de Activos (DEFI 2) - Universidad Externado de Colombia.
"""

import json
import os
import nbformat
from nbclient import NotebookClient

cells = []

def add_md(text):
    lines = [l + "\n" for l in text.strip().split("\n")]
    if lines:
        lines[-1] = lines[-1].rstrip("\n")
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": lines
    })

def add_code(text):
    lines = [l + "\n" for l in text.strip().split("\n")]
    if lines:
        lines[-1] = lines[-1].rstrip("\n")
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": lines
    })

# ==========================================
# CELL 0: PORTADA DEL LABORATORIO
# ==========================================
add_md(r"""# LABORATORIO COMPUTACIONAL PRÁCTICO: OPCIONES REALES
## Simulación Interactiva del Modelo Binomial (CRR) y Análisis de Sensibilidad
**Asignatura:** Valoración de Activos (DEFI 2) — Universidad Externado de Colombia  
**Estudiante expositor:** Julián Duarte  
**Tema:** Valuación Práctica de Opciones Reales Americanas  
**Referencia Oficial:** Francisco Venegas Martínez (2009), *Riesgos Financieros y Económicos*, 2.ª ed., Cap. 69, Sección 69.8 (págs. 811–813).

---

### 🎯 Objetivos de la Sesión Práctica en Aula
1. **Poner a prueba la teoría:** Replicar con exactitud el caso numérico resuelto por Francisco Venegas Martínez (opción americana de abandono sobre una empresa industrial).
2. **Interactividad visual:** Graficar el árbol binomial con **Plotly interactivo**, permitiendo al profesor y a los compañeros explorar cada nodo (pasando el cursor para ver el valor de flujos $S$, valor de la opción $c$ y la regla de decisión óptima).
3. **El Efecto Eureka:** Demostrar en vivo cómo la volatilidad ($\sigma$) ensancha el valor de la opción real y cómo la opcionalidad rescata proyectos que el VPN tradicional rechazaría.""")

# ==========================================
# CELL 1: CONFIGURACIÓN E IMPORTACIONES
# ==========================================
add_code(r"""# 1. Importación de librerías cuantitativas y de visualización interactiva
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de visualización de tablas en pandas
pd.set_option('display.float_format', lambda x: f'${x:,.2f}M')

print("✓ Librerías cuantitativas y motor gráfico interactivo (Plotly 6.x) cargados exitosamente.")
""")

# ==========================================
# CELL 2: EXPLICACIÓN DEL CASO NUMÉRICO
# ==========================================
add_md(r"""---
## Módulo 1: Parámetros del Caso Base (Venegas Martínez, págs. 811–813)

Imaginemos una empresa industrial que opera en un ambiente recesivo:
* **Flujos iniciales ($S_0$):** $\$90.00\text{M}$ (Valor presente de los flujos de efectivo esperados).
* **Inversión inicial requerida ($I_0$):** $\$90.00\text{M}$.
* **Valor de liquidación / rescate ($V$):** $\$60.00\text{M}$ (precio garantizado por venta de maquinaria o cierre).
* **Horizonte de evaluación ($T$):** $3$ años ($N = 3$ etapas anuales, $\Delta t = 1.0$).
* **Factores de salto:** $u = 2.0$, $d = 0.5 = 1/u$.
* **Tasa de interés libre de riesgo:** $e^r = 4/3 \implies r = \ln(4/3) \approx 28.77\% \implies e^{-r} = 0.75$ ($3/4$).
* **Probabilidad neutral al riesgo teórica:**
  $$q = \frac{e^{r\Delta t} - d}{u - d} = \frac{4/3 - 1/2}{2 - 1/2} = \frac{5/6}{3/2} = \frac{5}{9} \approx 0.5556$$""")

# ==========================================
# CELL 3: CÓDIGO DEL MOTOR BINOMIAL
# ==========================================
add_code(r"""# 2. Algoritmo General de Valuación de Opciones Reales Americanas
def motor_opciones_reales(S0=90.0, I0=90.0, V=60.0, u=2.0, d=0.5, r=np.log(4.0/3.0), T=3, N=3, tipo="abandono"):
    # Motor cuantitativo de inducción hacia atrás para opciones reales americanas (CRR).
    # Soporta:
    #   - 'abandono': Payoff terminal max(S_T, V) y regla intermedia max(Continuation, V)
    #   - 'expansion': Payoff terminal S_T + alpha * max(S_T - K/alpha, 0)
    dt = T / N
    df = np.exp(-r * dt)
    q = (np.exp(r * dt) - d) / (u - d)
    
    # Verificación de condiciones de no arbitraje
    assert d < np.exp(r * dt) < u, f"Condición de no arbitraje violada: d={d:.3f}, exp(r*dt)={np.exp(r*dt):.3f}, u={u:.3f}"
    
    # 1. Árbol del subyacente (Flujos de efectivo esperados S)
    arbol_S = {}
    for i in range(N + 1):
        arbol_S[i] = [S0 * (u ** (i - j)) * (d ** j) for j in range(i + 1)]
        
    # 2. Árbol de la opción real (C) y registro de decisiones
    arbol_C = {}
    arbol_decision = {}
    
    # Condiciones terminales en t = N
    arbol_C[N] = []
    arbol_decision[N] = []
    for val_S in arbol_S[N]:
        if tipo == "abandono":
            if V > val_S:
                arbol_C[N].append(V)
                arbol_decision[N].append("ABANDONO (Recupera V)")
            else:
                arbol_C[N].append(val_S)
                arbol_decision[N].append("CONTINUAR (Operación)")
        else:
            arbol_C[N].append(val_S)
            arbol_decision[N].append("CONTINUAR")
            
    # Inducción hacia atrás desde t = N-1 hasta t = 0
    for i in range(N - 1, -1, -1):
        arbol_C[i] = []
        arbol_decision[i] = []
        for j in range(i + 1):
            val_cont = df * (q * arbol_C[i + 1][j] + (1.0 - q) * arbol_C[i + 1][j + 1])
            if tipo == "abandono":
                if V > val_cont:
                    arbol_C[i].append(V)
                    arbol_decision[i].append("ABANDONO TEMPRANO (Ejercer V)")
                else:
                    arbol_C[i].append(val_cont)
                    arbol_decision[i].append("CONTINUAR (Esperar)")
            else:
                arbol_C[i].append(val_cont)
                arbol_decision[i].append("CONTINUAR")
                
    # Métricas ejecutivas
    vpn_estatico = S0 - I0
    vpn_modificado = arbol_C[0][0] - I0
    valor_opcion_pura = arbol_C[0][0] - S0
    
    return {
        "arbol_S": arbol_S,
        "arbol_C": arbol_C,
        "decision": arbol_decision,
        "q": q,
        "df": df,
        "vpn_estatico": vpn_estatico,
        "vpn_modificado": vpn_modificado,
        "valor_opcion": valor_opcion_pura,
        "S0": S0,
        "I0": I0,
        "V": V,
        "N": N
    }

# Ejecución del caso de Venegas Martínez
res = motor_opciones_reales()

print("="*75)
print("RESULTADOS EJECUTIVOS: CASO DE FRANCISCO VENEGAS MARTÍNEZ (2009, PÁG. 811)")
print("="*75)
print(f"• Probabilidad neutral al riesgo (q):    {res['q']:.4f}  (Fracción exacta: 5/9 = {5/9:.4f})")
print(f"• Factor de descuento temporal (df):    {res['df']:.4f} (Fracción exacta: 3/4 = 0.7500)")
print(f"• VPN Tradicional Estático (S0 - I0):  ${res['vpn_estatico']:>7.2f}M (Proyecto en punto de equilibrio neutro)")
print(f"• VALOR TOTAL DEL PROYECTO (c0):       ${res['arbol_C'][0][0]:>7.2f}M")
print(f"• Inversión requerida inicial (I0):    ${res['I0']:>7.2f}M")
print(f"• VPN MODIFICADO CON OPCIÓN REAL:       ${res['vpn_modificado']:>7.2f}M")
print(f"★ VALOR PURO DE LA OPCIÓN DE ABANDONO:  ${res['valor_opcion']:>7.2f}M")
print("="*75)
""")

# ==========================================
# CELL 4: VISUALIZACIÓN INTERACTIVA PLOTLY
# ==========================================
add_md(r"""---
## Módulo 2: Árbol Binomial Interactivo de Decisiones Gerenciales

En este gráfico interactivo:
* **Pasa el cursor sobre cualquier nodo:** Podrás ver en tiempo real el valor de los flujos del proyecto ($S$), el valor de la opción ($c$) y la decisión óptima de la junta directiva.
* **Nodos Azules:** La gerencia decide **CONTINUAR** operando porque el valor de continuar supera el valor de liquidación.
* **Nodos Rojos:** La gerencia ejerce activamente la opción de **ABANDONO**, frenando en seco las pérdidas y recibiendo los $\$60\text{M}$ garantizados.
* **Línea Punteada Roja:** El piso de seguridad del valor de rescate ($V = \$60\text{M}$).""")

# ==========================================
# CELL 5: CÓDIGO DEL GRÁFICO PLOTLY
# ==========================================
add_code(r"""# 3. Construcción del Árbol Interactivo en Plotly
def graficar_arbol_interactivo(res):
    arbol_S = res['arbol_S']
    arbol_C = res['arbol_C']
    dec = res['decision']
    N = res['N']
    V = res['V']
    
    fig = go.Figure()
    
    # 1. Dibujar ramas (aristas de conexión)
    edge_x = []
    edge_y = []
    for i in range(N):
        for j in range(i + 1):
            # Rama Arriba (Up)
            edge_x.extend([i, i + 1, None])
            edge_y.extend([arbol_S[i][j], arbol_S[i + 1][j], None])
            # Rama Abajo (Down)
            edge_x.extend([i, i + 1, None])
            edge_y.extend([arbol_S[i][j], arbol_S[i + 1][j + 1], None])
            
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(color='rgba(150, 150, 150, 0.5)', width=2, dash='dot'),
        hoverinfo='none',
        showlegend=False
    ))
    
    # 2. Dibujar nodos separados por decisión
    node_x_cont, node_y_cont, text_cont = [], [], []
    node_x_aban, node_y_aban, text_aban = [], [], []
    
    for i in range(N + 1):
        for j in range(i + 1):
            s_val = arbol_S[i][j]
            c_val = arbol_C[i][j]
            d_val = dec[i][j]
            
            tooltip = (f"<b>Año {i} (Nodo [{i},{j}])</b><br>"
                       f"• Flujos del Proyecto (S): ${s_val:.2f}M<br>"
                       f"• Valor con Opción (c):   ${c_val:.2f}M<br>"
                       f"• Valor de Rescate (V):   ${V:.2f}M<br>"
                       f"• Decisión Óptima:        <b>{d_val}</b>")
            
            if "ABANDONO" in d_val:
                node_x_aban.append(i)
                node_y_aban.append(s_val)
                text_aban.append(tooltip)
            else:
                node_x_cont.append(i)
                node_y_cont.append(s_val)
                text_cont.append(tooltip)
                
    # Nodos Continuación (Azul Corporativo)
    fig.add_trace(go.Scatter(
        x=node_x_cont, y=node_y_cont,
        mode='markers+text',
        marker=dict(size=26, color='#1f77b4', line=dict(color='white', width=2)),
        text=[f"${arbol_C[i][j]:.0f}M" for i, col in arbol_C.items() for j, v in enumerate(col) if "ABANDONO" not in dec[i][j]],
        textposition="top center",
        hovertext=text_cont,
        hoverinfo='text',
        name='Continuar Operación'
    ))
    
    # Nodos Abandono (Rojo Estratégico)
    fig.add_trace(go.Scatter(
        x=node_x_aban, y=node_y_aban,
        mode='markers+text',
        marker=dict(size=28, color='#d62728', symbol='diamond', line=dict(color='white', width=2)),
        text=[f"${arbol_C[i][j]:.0f}M" for i, col in arbol_C.items() for j, v in enumerate(col) if "ABANDONO" in dec[i][j]],
        textposition="bottom center",
        hovertext=text_aban,
        hoverinfo='text',
        name='Ejercer Abandono (Corta Pérdidas)'
    ))
    
    # Línea horizontal de valor de rescate V
    fig.add_hline(
        y=V, line_dash="dash", line_color="#d62728", line_width=2.5,
        annotation_text=f"Piso de Protección: Rescate V = ${V:.0f}M",
        annotation_position="bottom right",
        annotation_font=dict(color="#d62728", size=12, family="Arial")
    )
    
    fig.update_layout(
        title=dict(
            text="<b>Árbol Binomial de Opciones Reales: Decisión Óptima de Abandono</b><br><sup>Replicación interactiva del caso de Francisco Venegas Martínez (2009, págs. 811-813)</sup>",
            x=0.05, font=dict(size=18, family="Arial")
        ),
        xaxis=dict(
            title="Horizonte Temporal de Decisión (Años)",
            tickmode='array', tickvals=list(range(N + 1)),
            ticktext=[f"t = {t}<br>(Año {t})" for t in range(N + 1)],
            gridcolor='rgba(230,230,230,0.8)'
        ),
        yaxis=dict(
            title="Valor Presente de los Flujos de Efectivo (Millones)",
            gridcolor='rgba(230,230,230,0.8)'
        ),
        plot_bgcolor='white',
        legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.9)', bordercolor='gray', borderwidth=1),
        height=620,
        margin=dict(l=60, r=40, t=100, b=60)
    )
    
    return fig

fig_tree = graficar_arbol_interactivo(res)
from IPython.display import display, HTML
display(HTML(fig_tree.to_html(full_html=False, include_plotlyjs='cdn')))
""")

# ==========================================
# CELL 6: EXPERIMENTOS DE SENSIBILIDAD EN VIVO
# ==========================================
add_md(r"""---
## Módulo 3: El "Efecto Eureka" — Análisis de Sensibilidad Dinámico

En este módulo pondremos a prueba dos propiedades fundamentales de las Opciones Reales:
1. **Sensibilidad a la Volatilidad ($\sigma$):**  
   Demostración empírica de la asimetría del payoff: mientras que un mayor riesgo destruye valor en finanzas corporativas tradicionales por el aumento del WACC, **en opciones reales la incertidumbre ensancha el valor de la opción**.
2. **Sensibilidad al Valor de Rescate ($V$):**  
   ¿Cuánto valor debe tener la maquinaria o el contrato de venta secundaria para que la opción de abandono se vuelva financieramente crítica para la junta directiva?""")

# ==========================================
# CELL 7: CÓDIGO DE SENSIBILIDAD
# ==========================================
add_code(r"""# 4. Simulación de Curvas de Sensibilidad Dinámica
sigmas = np.linspace(0.15, 0.75, 30)
valores_con_opcion = []
valores_vpn_tradicional = []
valores_prima_opcion = []

S0_sim = 90.0
I0_sim = 90.0
V_sim = 60.0
r_sim = 0.08
T_sim = 3.0
N_sim = 3
dt_sim = T_sim / N_sim

for sig in sigmas:
    u_s = np.exp(sig * np.sqrt(dt_sim))
    d_s = 1.0 / u_s
    
    # Probabilidad neutral al riesgo
    df_s = np.exp(-r_sim * dt_sim)
    q_s = (np.exp(r_sim * dt_sim) - d_s) / (u_s - d_s)
    
    # Hojas terminales
    c_leaf = [max(S0_sim * (u_s ** (N_sim - j)) * (d_s ** j), V_sim) for j in range(N_sim + 1)]
    
    # Inducción hacia atrás
    for step in range(N_sim - 1, -1, -1):
        c_leaf = [max(df_s * (q_s * c_leaf[j] + (1 - q_s) * c_leaf[j + 1]), V_sim) for j in range(step + 1)]
        
    c0_s = c_leaf[0]
    valores_con_opcion.append(c0_s)
    valores_vpn_tradicional.append(S0_sim - I0_sim) # VPN plano en 0
    valores_prima_opcion.append(c0_s - S0_sim)

# Gráfico de dos paneles con Plotly
fig_sens = make_subplots(
    rows=1, cols=2,
    subplot_titles=(
        "<b>1. Valor del Proyecto vs. Volatilidad (σ)</b><br><sup>La incertidumbre aumenta el valor del activo con opción real</sup>",
        "<b>2. Prima Pura de la Opción de Abandono (c)</b><br><sup>Ganancia económica generada exclusivamente por la flexibilidad</sup>"
    )
)

# Panel 1: Valor total
fig_sens.add_trace(go.Scatter(
    x=sigmas * 100, y=valores_con_opcion,
    mode='lines+markers', line=dict(color='#1f77b4', width=3),
    marker=dict(size=6), name='Proyecto con Opción Real'
), row=1, col=1)

fig_sens.add_trace(go.Scatter(
    x=sigmas * 100, y=np.full_like(sigmas, S0_sim),
    mode='lines', line=dict(color='#d62728', width=2, dash='dash'),
    name='VPN Tradicional Plano ($90M)'
), row=1, col=1)

# Panel 2: Prima de opción pura
fig_sens.add_trace(go.Scatter(
    x=sigmas * 100, y=valores_prima_opcion,
    mode='lines+markers', line=dict(color='#2ca02c', width=3),
    fill='tozeroy', fillcolor='rgba(44, 160, 44, 0.15)',
    marker=dict(size=6), name='Valor de la Opción (c)'
), row=1, col=2)

fig_sens.update_layout(
    title=dict(text="<b>Análisis de Sensibilidad: El Poder de la Opcionalidad ante el Riesgo</b>", x=0.05, font=dict(size=18)),
    plot_bgcolor='white',
    height=480,
    margin=dict(l=60, r=40, t=90, b=60)
)
fig_sens.update_xaxes(title_text="Volatilidad Anual de los Flujos (σ en %)", gridcolor='rgba(230,230,230,0.8)')
fig_sens.update_yaxes(title_text="Valor en t=0 (Millones)", gridcolor='rgba(230,230,230,0.8)')

fig_sens.show()
""")

# ==========================================
# CELL 8: TABLA EJECUTIVA PARA PROYECTAR EN CLASE
# ==========================================
add_md(r"""---
## Módulo 4: Tabla Comparativa Ejecutiva para la Discusión en Clase

Esta tabla resume la comparación final para cerrar tu intervención práctica ante el auditorio:""")

# ==========================================
# CELL 9: CÓDIGO DE TABLA COMPARATIVA
# ==========================================
add_code(r"""# 5. Generación de Tabla Resumen Ejecutiva
resumen_data = {
    "Métrica de Evaluación": [
        "Flujos de Efectivo Descontados Pasivos (S0)",
        "Inversión Inicial Requerida (I0)",
        "Valor Presente Neto Convencional (VPN Estático)",
        "Valor del Proyecto Incorporando Opción de Abandono (c0)",
        "VPN Modificado / Ampliado (VPN Estático + Opción)",
        "VALOR PURO DE LA FLEXIBILIDAD DIRECTIVA (c)"
    ],
    "Criterio Tradicional": ["$90.00M", "$90.00M", "$0.00M", "No Aplica (Miopía)", "$0.00M", "$0.00M"],
    "Criterio de Opciones Reales": ["$90.00M", "$90.00M", "$0.00M", f"${res['arbol_C'][0][0]:.2f}M", f"${res['vpn_modificado']:.2f}M", f"${res['valor_opcion']:.2f}M"],
    "Decisión Gerencial": [
        "Incierta / Rechazo por Riesgo",
        "Obligatoria hoy",
        "Punto Neutro (Rechazar con riesgo de quiebra)",
        "Monitorear ejercicio nodo a nodo",
        "¡PROYECTO APROBADO Y VIABLE!",
        "Ganancia neta por diseñar contratos con rescate"
    ]
}

df_resumen = pd.DataFrame(resumen_data)
# Mostrar tabla formateada
from IPython.display import display, HTML
display(HTML(df_resumen.to_html(index=False, classes="table table-striped table-bordered")))
""")

# ==========================================
# CELL 10: CONCLUSIÓN PRÁCTICA
# ==========================================
add_md(r"""---
## 🏁 Conclusión del Laboratorio para el Cierre de tu Clase

> *"Como pudimos observar empíricamente en el simulador:  
> Si una empresa solo calcula el VPN estático, descarta proyectos porque teme a la caída. Pero si negocia activamente cláusulas de rescate, modularidad o liquidación, **la opción de abandono actúa como un seguro contra la catástrofe**.  
> Esto transforma la función de distribución de los rendimientos: recorta la cola izquierda de pérdidas severas y preserva intacto todo el potencial de captura al alza. Por eso, en el siglo XXI, **la flexibilidad directiva es un activo de capital con valor medible en el balance**."*""")

# ==========================================
# CONSTRUCCIÓN Y GUARDADO DEL NOTEBOOK
# ==========================================
notebook_json = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.12.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

nb_path = "08_Exposicion/laboratorio_practico_opciones_reales.ipynb"
with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(notebook_json, f, indent=2, ensure_ascii=False)

print(f"✓ Notebook de Laboratorio creado exitosamente en: {nb_path}")

# ==========================================
# EJECUCIÓN Y COMPILACIÓN A HTML INTERACTIVO
# ==========================================
print("Iniciando compilación a HTML interactivo...")
with open(nb_path, "r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

client = NotebookClient(nb, timeout=120, kernel_name="python3")
client.execute()

# Guardar notebook ejecutado
with open(nb_path, "w", encoding="utf-8") as f:
    nbformat.write(nb, f)

# Compilar a HTML
from nbconvert import HTMLExporter
html_exporter = HTMLExporter()
html_exporter.template_name = 'classic'
(body, resources) = html_exporter.from_notebook_node(nb)

html_path = "08_Exposicion/laboratorio_practico_opciones_reales.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(body)

print(f"✓ HTML Interactivo compilado exitosamente en: {html_path}")

