import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAFICAS_DIR = ROOT / "06_presentacion" / "graficas"
OUT_HTML = ROOT / "06_presentacion" / "presentacion_taller1_capm_standalone.html"

# Load images into base64 mapping
b64_images = {}
for img_path in GRAFICAS_DIR.glob("*.png"):
    with open(img_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
        b64_images[img_path.name] = f"data:image/png;base64,{encoded}"

print(f"Loaded {len(b64_images)} images into Base64 dictionary.")

html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informe CAPM: La Beta de los Pobres - 10 Expedientes</title>
    
    <!-- Google Fonts: Playfair Display, Cinzel, Plus Jakarta Sans -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    
    <style>
        :root {{
            --bg-base: #090d16;
            --bg-card: rgba(19, 27, 44, 0.85);
            --bg-card-hover: rgba(30, 42, 68, 0.95);
            
            --gold-primary: #f59e0b;
            --gold-light: #fef3c7;
            --gold-glow: rgba(245, 158, 11, 0.25);
            
            --emerald-accent: #10b981;
            --emerald-bg: rgba(16, 185, 129, 0.12);
            
            --crimson-accent: #ef4444;
            --crimson-bg: rgba(239, 68, 68, 0.12);
            
            --sky-accent: #38bdf8;
            --sky-bg: rgba(56, 189, 248, 0.12);
            
            --text-heading: #f8fafc;
            --text-body: #cbd5e1;
            --text-muted: #64748b;
            --border-color: rgba(245, 158, 11, 0.2);
            --border-subtle: rgba(255, 255, 255, 0.08);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-base);
            background-image: 
                radial-gradient(ellipse at 10% 0%, rgba(245, 158, 11, 0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 90% 100%, rgba(56, 189, 248, 0.06) 0%, transparent 50%);
            color: var(--text-body);
            width: 100vw;
            min-height: 100vh;
            padding: 18px 24px;
            display: flex;
            flex-direction: column;
            gap: 14px;
            overflow-x: hidden;
        }}

        /* Header Editorial Styling */
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: linear-gradient(135deg, rgba(20, 29, 47, 0.95), rgba(11, 16, 26, 0.95));
            border-radius: 16px;
            padding: 14px 24px;
            border: 1px solid var(--border-color);
            box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.6);
            position: relative;
        }}

        header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 5%;
            width: 90%;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--gold-primary), transparent);
        }}

        .header-brand {{
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}

        .institution-tag {{
            font-family: 'Cinzel', serif;
            font-size: 11px;
            letter-spacing: 2px;
            color: var(--gold-primary);
            font-weight: 700;
            text-transform: uppercase;
        }}

        .main-title {{
            font-family: 'Playfair Display', serif;
            font-size: 22px;
            font-weight: 700;
            color: var(--text-heading);
            letter-spacing: -0.3px;
        }}

        .sub-title {{
            font-size: 11px;
            color: var(--text-muted);
        }}

        .meta-pills {{
            display: flex;
            gap: 10px;
            align-items: center;
        }}

        .pill-gold {{
            background: rgba(245, 158, 11, 0.12);
            border: 1px solid rgba(245, 158, 11, 0.35);
            color: var(--gold-light);
            padding: 6px 14px;
            border-radius: 30px;
            font-size: 11px;
            font-weight: 600;
        }}

        .pill-dark {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-subtle);
            color: var(--text-body);
            padding: 6px 14px;
            border-radius: 30px;
            font-size: 11px;
        }}

        /* Key Metrics / Highlights Bar */
        .kpi-row {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
        }}

        .kpi-box {{
            background: var(--bg-card);
            border-radius: 14px;
            padding: 12px 16px;
            border: 1px solid var(--border-subtle);
            display: flex;
            flex-direction: column;
            gap: 3px;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }}

        .kpi-box:hover {{
            transform: translateY(-2px);
            border-color: var(--gold-primary);
            box-shadow: 0 8px 20px -4px var(--gold-glow);
        }}

        .kpi-box::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 3px;
            height: 100%;
        }}

        .kpi-box.gold::after {{ background: var(--gold-primary); }}
        .kpi-box.emerald::after {{ background: var(--emerald-accent); }}
        .kpi-box.crimson::after {{ background: var(--crimson-accent); }}
        .kpi-box.sky::after {{ background: var(--sky-accent); }}

        .kpi-lbl {{
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
        }}

        .kpi-num {{
            font-family: 'Playfair Display', serif;
            font-size: 22px;
            font-weight: 700;
            color: var(--text-heading);
        }}

        .kpi-desc {{
            font-size: 11px;
            color: var(--text-muted);
        }}

        /* Main Workspace Grid */
        .workspace-grid {{
            display: grid;
            grid-template-columns: 320px 1fr 320px;
            gap: 14px;
            flex: 1;
        }}

        .panel-card {{
            background: var(--bg-card);
            border-radius: 16px;
            border: 1px solid var(--border-subtle);
            padding: 14px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
        }}

        .panel-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border-subtle);
        }}

        .panel-title {{
            font-family: 'Cinzel', serif;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 1px;
            color: var(--gold-primary);
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        /* Left Panel: 10 Expedientes List */
        .expedientes-scroll {{
            display: flex;
            flex-direction: column;
            gap: 6px;
            overflow-y: auto;
            max-height: calc(100vh - 275px);
            padding-right: 4px;
        }}

        .expedientes-scroll::-webkit-scrollbar {{
            width: 4px;
        }}
        .expedientes-scroll::-webkit-scrollbar-thumb {{
            background: rgba(245, 158, 11, 0.3);
            border-radius: 4px;
        }}

        .group-label {{
            font-size: 9.5px;
            font-weight: 800;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            color: var(--gold-primary);
            margin-top: 4px;
            margin-bottom: 1px;
        }}

        .asset-item {{
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 7px 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .asset-item:hover, .asset-item.active {{
            background: rgba(245, 158, 11, 0.1);
            border-color: var(--gold-primary);
            transform: translateX(2px);
        }}

        .asset-name {{
            font-family: 'Playfair Display', serif;
            font-weight: 700;
            font-size: 13px;
            color: var(--text-heading);
            width: 45px;
        }}

        .asset-sub {{
            font-size: 9.5px;
            color: var(--text-muted);
            background: rgba(255, 255, 255, 0.05);
            padding: 2px 5px;
            border-radius: 4px;
        }}

        .badge-pos {{
            color: var(--emerald-accent);
            font-weight: 700;
            font-size: 10.5px;
        }}

        .badge-neg {{
            color: var(--crimson-accent);
            font-weight: 700;
            font-size: 10.5px;
        }}

        /* Center Viewer */
        .tabs-row {{
            display: flex;
            gap: 6px;
        }}

        .tab-btn {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-subtle);
            color: var(--text-body);
            padding: 5px 10px;
            border-radius: 7px;
            font-size: 10.5px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .tab-btn:hover, .tab-btn.active {{
            background: var(--gold-primary);
            color: #000;
            font-weight: 700;
            border-color: var(--gold-primary);
            box-shadow: 0 0 10px var(--gold-glow);
        }}

        .image-container {{
            flex: 1;
            background: #ffffff;
            border-radius: 12px;
            padding: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.1);
        }}

        .image-container img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            border-radius: 8px;
            transition: opacity 0.3s ease;
        }}

        .caption-box {{
            background: rgba(11, 16, 26, 0.85);
            border-left: 3px solid var(--gold-primary);
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 11px;
            line-height: 1.4;
            color: var(--text-body);
        }}

        /* Right Panel: Decisiones Doña Victoria */
        .verdict-card {{
            border-radius: 10px;
            padding: 10px 12px;
            border-left: 4px solid;
            background: rgba(255, 255, 255, 0.02);
            display: flex;
            flex-direction: column;
            gap: 3px;
        }}

        .verdict-card.red {{
            border-color: var(--crimson-accent);
            background: var(--crimson-bg);
        }}
        .verdict-card.amber {{
            border-color: var(--gold-primary);
            background: var(--gold-glow);
        }}
        .verdict-card.green {{
            border-color: var(--emerald-accent);
            background: var(--emerald-bg);
        }}

        .v-title {{
            font-family: 'Cinzel', serif;
            font-size: 10.5px;
            font-weight: 800;
            display: flex;
            justify-content: space-between;
        }}

        .red .v-title {{ color: var(--crimson-accent); }}
        .amber .v-title {{ color: var(--gold-primary); }}
        .green .v-title {{ color: var(--emerald-accent); }}

        .v-desc {{
            font-size: 10.5px;
            color: var(--text-body);
            line-height: 1.35;
        }}

        .export-btn {{
            background: linear-gradient(135deg, var(--gold-primary), #d97706);
            color: #000;
            font-weight: 800;
            font-size: 10.5px;
            border: none;
            padding: 9px;
            border-radius: 8px;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 4px 15px var(--gold-glow);
            transition: all 0.2s ease;
            text-align: center;
            margin-top: auto;
        }}

        .export-btn:hover {{
            transform: translateY(-1px);
            filter: brightness(1.1);
        }}

        /* Footer */
        footer {{
            background: linear-gradient(90deg, rgba(20, 29, 47, 0.9), rgba(11, 16, 26, 0.9));
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 8px 18px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .footer-quote {{
            font-family: 'Playfair Display', serif;
            font-size: 12px;
            font-style: italic;
            color: var(--gold-light);
        }}

        .footer-sub {{
            font-size: 10.5px;
            color: var(--text-muted);
        }}
    </style>
</head>
<body>

    <!-- Header -->
    <header>
        <div class="header-brand">
            <span class="institution-tag">Universidad Externado de Colombia | Valoración de Activos</span>
            <h1 class="main-title">EVALUACIÓN CAPM INTEGRADA: 10 EXPEDIENTES</h1>
            <span class="sub-title">"La Beta de los Pobres" (SOL vs NCI) y Acciones de Bajo Precio frente a ETF Sectoriales</span>
        </div>

        <div class="meta-pills">
            <div class="pill-gold">🏛️ Caso Doña Victoria</div>
            <div class="pill-dark">👤 Julián Duarte</div>
            <div class="pill-dark">⏱️ 7 Minutos</div>
        </div>
    </header>

    <!-- Top KPI Highlights -->
    <div class="kpi-row">
        <div class="kpi-box gold">
            <span class="kpi-lbl">Promesa vs Realidad</span>
            <span class="kpi-num">25% Sin Riesgo</span>
            <span class="kpi-desc">Técnicamente IMPOSIBLE en los datos</span>
        </div>
        <div class="kpi-box crimson">
            <span class="kpi-lbl">Peor Caída de Capital</span>
            <span class="kpi-num">-93.9% <small style="font-size: 13px;">(MVIS)</small></span>
            <span class="kpi-desc">El promedio oculta ruinas extremas</span>
        </div>
        <div class="kpi-box sky">
            <span class="kpi-lbl">Máxima Beta del Estudio</span>
            <span class="kpi-num">1.94 <small style="font-size: 13px;">(KLXE)</small></span>
            <span class="kpi-desc">Sensibilidad destructiva sin alfa</span>
        </div>
        <div class="kpi-box emerald">
            <span class="kpi-lbl">Retorno > Exigido CAPM</span>
            <span class="kpi-num">4 de 10 Activos</span>
            <span class="kpi-desc">Solo KOPN, LIDR, CTMX y TTI pagaron alfa</span>
        </div>
    </div>

    <!-- Main Workspace Grid -->
    <div class="workspace-grid">

        <!-- Left Panel: 10 Expedientes -->
        <div class="panel-card">
            <div class="panel-header">
                <span class="panel-title">📂 Los 10 Expedientes</span>
                <span style="font-size: 9.5px; color: var(--text-muted);">Clic para enfocar</span>
            </div>

            <div class="expedientes-scroll">
                
                <div class="group-label">🪙 Criptoactivo (vs NCI)</div>
                <div class="asset-item active" onclick="highlight('SOL', '1.25', '-75.4%', '-17.2 pp', 'Criptoactivo asignado. Rinde +21.6% en bruto, pero CAPM exigia +38.8% por su beta de 1.25. Brecha negativa de -17.2 pp.')">
                    <span class="asset-name" style="color: var(--sky-accent);">SOL</span>
                    <span class="asset-sub">NCI</span>
                    <span class="badge-neg">β 1.25 | -17.2pp</span>
                </div>

                <div class="group-label">💻 Tecnología (vs XLK)</div>
                <div class="asset-item" onclick="highlight('KOPN', '1.82', '-82.1%', '+38.7 pp', 'Mayor generador de alfa del estudio (+38.7 pp frente a CAPM), pero exige tolerar una beta de 1.82 y caer -82.1%.')">
                    <span class="asset-name">KOPN</span>
                    <span class="asset-sub">XLK</span>
                    <span class="badge-pos">β 1.82 | +38.7pp</span>
                </div>

                <div class="asset-item" onclick="highlight('MVIS', '1.61', '-93.9%', '-29.1 pp', 'Destruccion extrema de valor. Peor Max Drawdown del estudio (-93.9%) y alfa altamente negativo (-29.1 pp).')">
                    <span class="asset-name">MVIS</span>
                    <span class="asset-sub">XLK</span>
                    <span class="badge-neg">β 1.61 | -29.1pp</span>
                </div>

                <div class="asset-item" onclick="highlight('LIDR', '1.43', '-88.5%', '+20.5 pp', 'Genera alfa positivo (+20.5 pp), pero sufre de fragilidad extrema de iliquidez (picos severos en indice Amihud).')">
                    <span class="asset-name">LIDR</span>
                    <span class="asset-sub">XLK</span>
                    <span class="badge-pos">β 1.43 | +20.5pp</span>
                </div>

                <div class="group-label">🧬 Biotecnología (vs XBI)</div>
                <div class="asset-item" onclick="highlight('GERN', '0.75', '-68.4%', '-12.8 pp', 'Unica beta defensiva (< 1.00), pero su retorno observado no logro cubrir el retorno requerido por CAPM.')">
                    <span class="asset-name">GERN</span>
                    <span class="asset-sub">XBI</span>
                    <span class="badge-neg">β 0.75 | -12.8pp</span>
                </div>

                <div class="asset-item" onclick="highlight('CTMX', '1.11', '-74.2%', '+8.3 pp', 'Alfa positivo moderado (+8.3 pp) con comportamiento de volatilidad biotecnologica estandar.')">
                    <span class="asset-name">CTMX</span>
                    <span class="asset-sub">XBI</span>
                    <span class="badge-pos">β 1.11 | +8.3pp</span>
                </div>

                <div class="asset-item" onclick="highlight('OCGN', '1.35', '-85.0%', '-5.4 pp', 'Sensibilidad elevada (1.35) con destruccion de valor moderada. Brecha negativa de -5.4 pp.')">
                    <span class="asset-name">OCGN</span>
                    <span class="asset-sub">XBI</span>
                    <span class="badge-neg">β 1.35 | -5.4pp</span>
                </div>

                <div class="group-label">⚡ Energía (vs XLE)</div>
                <div class="asset-item" onclick="highlight('BORR', '1.12', '-64.1%', '-14.6 pp', 'No compensa el riesgo del sector energetico. Brecha negativa de -14.6 pp frente al retorno exigido por CAPM.')">
                    <span class="asset-name">BORR</span>
                    <span class="asset-sub">XLE</span>
                    <span class="badge-neg">β 1.12 | -14.6pp</span>
                </div>

                <div class="asset-item" onclick="highlight('KLXE', '1.94', '-72.1%', '-27.0 pp', 'Maxima beta del estudio (1.94). Sensibilidad extrema al sector que no pago retorno, destruyendo capital.')">
                    <span class="asset-name">KLXE</span>
                    <span class="asset-sub">XLE</span>
                    <span class="badge-neg">β 1.94 | -27.0pp</span>
                </div>

                <div class="asset-item" onclick="highlight('TTI', '1.18', '-59.8%', '+3.2 pp', 'Accion bajo excepcion permitida (< USD 10). Genera alfa positivo (+3.2 pp) y presenta la menor caida del grupo (-59.8%).')">
                    <span class="asset-name">TTI</span>
                    <span class="asset-sub">XLE</span>
                    <span class="badge-pos">β 1.18 | +3.2pp</span>
                </div>

            </div>
        </div>

        <!-- Center Panel: Interactive Viewer with Embedded Base64 Images -->
        <div class="panel-card">
            <div class="panel-header">
                <span class="panel-title">📈 Evidencia en Vivo</span>
                <div class="tabs-row">
                    <button class="tab-btn active" onclick="showGraphic('09_mapa_beta_drawdown.png', 'Mapa Beta vs Max Drawdown: Los activos abajo y a la derecha (MVIS -93.9%, SOL -75.4%, KLXE -72.1%) demuestran que la beta viene acompañada de caidas severas.', this)">🗺️ Beta vs MDD</button>
                    <button class="tab-btn" onclick="showGraphic('07_brecha_retorno_capm.png', 'Brecha Retorno vs CAPM: Barras verdes superan lo exigido por el modelo (KOPN, LIDR, CTMX, TTI). Barras rojas no remuneraron el riesgo.', this)">📊 Brecha CAPM</button>
                    <button class="tab-btn" onclick="showGraphic('06_matriz_percentiles.png', 'Matriz de Percentiles: Sintesis multicriterio que evalua volatilidad, alfa, iliquidez y drawdown en un solo mapa.', this)">🏆 Percentiles</button>
                    <button class="tab-btn" onclick="showGraphic('10_liquidez_retornos_cero.png', 'Liquidez e Iliquidez de Amihud: Dias sin retorno y costo de salida. KLXE y LIDR muestran fragilidad operativa.', this)">💧 Liquidez</button>
                </div>
            </div>

            <div class="image-container">
                <img id="main-img" src="{b64_images.get('09_mapa_beta_drawdown.png', '')}" alt="Grafica CAPM">
            </div>

            <div class="caption-box" id="caption">
                💡 <strong>Mapa Beta vs Max Drawdown:</strong> Muestra la relación directa entre sensibilidad de mercado y profundidad de caída. Los activos de mayor beta combinan altas caídas acumuladas.
            </div>
        </div>

        <!-- Right Panel: Mandatos Doña Victoria -->
        <div class="panel-card">
            <div class="panel-header">
                <span class="panel-title">⚖️ Decisión Doña Victoria</span>
            </div>

            <div class="verdict-card red">
                <div class="v-title">
                    <span>🛡️ CONSERVACIÓN</span>
                    <span>RECHAZAR TODO</span>
                </div>
                <div class="v-desc">
                    Rechazar los 10 expedientes. Su extrema volatilidad e iliquidez destruyen el patrimonio. Asignar 100% a <strong>T-Bills 3M (DGS3MO)</strong>.
                </div>
            </div>

            <div class="verdict-card amber">
                <div class="v-title">
                    <span>📈 CRECIMIENTO</span>
                    <span>ETF BENCHMARK</span>
                </div>
                <div class="v-desc">
                    Evitar la selección individual de penny stocks. Indexarse a los ETF de mercado <strong>XLK, XLE y XBI</strong>.
                </div>
            </div>

            <div class="verdict-card green">
                <div class="v-title">
                    <span>⚡ ESPECULACIÓN</span>
                    <span>MÁXIMO 1% - 2%</span>
                </div>
                <div class="v-desc">
                    Permitir un cupo acotado en <strong>SOL</strong> o <strong>KOPN/TTI</strong> (con alfa) asignando stop-loss presupuestado del 15%.
                </div>
            </div>

            <button class="export-btn" onclick="window.print()">🖨️ Imprimir / Guardar en PDF</button>
        </div>

    </div>

    <!-- Footer -->
    <footer>
        <div class="footer-quote">
            "El 25% anual sin caídas es un espejismo financiero. El CAPM mide la factura real de la volatilidad y la iliquidez."
        </div>
        <div class="footer-sub">
            Entregable Oficial Taller 1 CAPM | Universidad Externado de Colombia
        </div>
    </footer>

    <!-- Embedded Base64 Data Dictionary & JavaScript -->
    <script>
        const imagesData = {json.dumps(b64_images)};

        function showGraphic(imgName, desc, btn) {{
            const img = document.getElementById('main-img');
            const caption = document.getElementById('caption');
            
            img.style.opacity = 0.2;
            setTimeout(() => {{
                img.src = imagesData[imgName] || '';
                img.style.opacity = 1;
                caption.innerHTML = '💡 <strong>' + desc.split(':')[0] + ':</strong>' + desc.split(':')[1];
            }}, 150);

            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        }}

        function highlight(ticker, beta, mdd, brecha, desc) {{
            document.querySelectorAll('.asset-item').forEach(i => i.classList.remove('active'));
            event.currentTarget.classList.add('active');

            const caption = document.getElementById('caption');
            caption.innerHTML = `📌 <strong>Enfoque en ${{ticker}}:</strong> Beta ${{beta}} | Max Drawdown ${{mdd}} | Brecha CAPM ${{brecha}}.<br>${{desc}}`;
        }}
    </script>
</body>
</html>
"""

# Write HTML file locally in project
with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Standalone HTML generated successfully at: {OUT_HTML}")
