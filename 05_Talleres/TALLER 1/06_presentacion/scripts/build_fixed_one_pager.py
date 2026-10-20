import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAFICAS_DIR = ROOT / "06_presentacion" / "graficas"
OUT_HTML = ROOT / "06_presentacion" / "one_pager_dashboard.html"

# Encode all 10 graphics into base64
b64_images = {}
for img_path in GRAFICAS_DIR.glob("*.png"):
    with open(img_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
        b64_images[img_path.name] = f"data:image/png;base64,{encoded}"

print(f"Base64 encoded {len(b64_images)} graphics.")

html_code = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tablero CAPM: Realidad vs Promesa - 10 Expedientes</title>
    <!-- Google Fonts: Outfit & Inter -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@500;600;700;800;900&display=swap" rel="stylesheet">
    
    <style>
        :root {{
            --bg-dark: #0b0f19;
            --card-bg: rgba(18, 26, 43, 0.88);
            --card-hover: rgba(30, 43, 70, 0.95);
            --border-color: rgba(255, 255, 255, 0.1);
            --border-glow: rgba(56, 189, 248, 0.4);
            
            --neon-blue: #38bdf8;
            --neon-purple: #c084fc;
            --neon-green: #4ade80;
            --neon-red: #f87171;
            --neon-amber: #fbbf24;
            
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
        }}

        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-dark);
            background-image: 
                radial-gradient(circle at 10% 10%, rgba(56, 189, 248, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 90%, rgba(192, 132, 252, 0.08) 0%, transparent 40%);
            color: var(--text-primary);
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            padding: 14px 20px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        /* Header Bar */
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(15, 23, 42, 0.9);
            backdrop-filter: blur(16px);
            padding: 12px 22px;
            border-radius: 14px;
            border: 1px solid var(--border-color);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
            flex-shrink: 0;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .brand-logo {{
            width: 42px;
            height: 42px;
            background: linear-gradient(135deg, var(--neon-blue), var(--neon-purple));
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Outfit', sans-serif;
            font-weight: 900;
            color: #000;
            font-size: 20px;
            box-shadow: 0 0 18px rgba(56, 189, 248, 0.45);
        }}

        .brand-text h1 {{
            font-family: 'Outfit', sans-serif;
            font-size: 22px;
            font-weight: 800;
            letter-spacing: -0.3px;
            background: linear-gradient(90deg, #ffffff, var(--neon-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .brand-text p {{
            font-size: 12.5px;
            color: var(--text-secondary);
            font-weight: 500;
        }}

        .tags-container {{
            display: flex;
            gap: 10px;
        }}

        .tag {{
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 11.5px;
            font-weight: 700;
            letter-spacing: 0.3px;
            text-transform: uppercase;
            border: 1px solid rgba(255, 255, 255, 0.12);
            background: rgba(255, 255, 255, 0.05);
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .tag-danger {{
            background: rgba(248, 113, 113, 0.18);
            border-color: rgba(248, 113, 113, 0.5);
            color: var(--neon-red);
            animation: pulse-red 2s infinite;
        }}

        @keyframes pulse-red {{
            0%, 100% {{ box-shadow: 0 0 0 0 rgba(248, 113, 113, 0.4); }}
            50% {{ box-shadow: 0 0 12px 2px rgba(248, 113, 113, 0.6); }}
        }}

        .tag-glow {{
            background: rgba(56, 189, 248, 0.15);
            border-color: rgba(56, 189, 248, 0.5);
            color: var(--neon-blue);
        }}

        /* KPI Row */
        .kpi-row {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            flex-shrink: 0;
        }}

        .kpi-card {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 12px 18px;
            border: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            gap: 3px;
            position: relative;
            overflow: hidden;
            transition: all 0.25s ease;
        }}

        .kpi-card:hover {{
            transform: translateY(-2px);
            border-color: var(--neon-blue);
            box-shadow: 0 6px 20px rgba(56, 189, 248, 0.25);
        }}

        .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
        }}

        .kpi-card.blue::before {{ background: var(--neon-blue); }}
        .kpi-card.purple::before {{ background: var(--neon-purple); }}
        .kpi-card.red::before {{ background: var(--neon-red); }}
        .kpi-card.green::before {{ background: var(--neon-green); }}

        .kpi-label {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: var(--text-secondary);
            font-weight: 700;
        }}

        .kpi-val {{
            font-family: 'Outfit', sans-serif;
            font-size: 24px;
            font-weight: 800;
            color: var(--text-primary);
        }}

        .kpi-sub {{
            font-size: 11.5px;
            color: var(--text-muted);
        }}

        /* Main Workspace Grid */
        .dashboard-grid {{
            display: grid;
            grid-template-columns: 330px 1fr 340px;
            gap: 14px;
            flex: 1;
            min-height: 0;
        }}

        .panel {{
            background: var(--card-bg);
            backdrop-filter: blur(14px);
            border-radius: 14px;
            border: 1px solid var(--border-color);
            padding: 14px 16px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            min-height: 0;
            position: relative;
        }}

        .panel-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-shrink: 0;
            padding-bottom: 8px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }}

        .panel-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 14px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        /* Left Panel: 10 Expedientes List */
        .expedientes-list {{
            display: flex;
            flex-direction: column;
            gap: 6px;
            overflow-y: auto;
            flex: 1;
            padding-right: 4px;
        }}

        .expedientes-list::-webkit-scrollbar {{
            width: 4px;
        }}
        .expedientes-list::-webkit-scrollbar-thumb {{
            background: rgba(56, 189, 248, 0.35);
            border-radius: 4px;
        }}

        .sector-group-title {{
            font-size: 10.5px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--neon-blue);
            margin-top: 4px;
            margin-bottom: 2px;
        }}

        .asset-card {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 9px;
            padding: 8px 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .asset-card:hover, .asset-card.active {{
            background: rgba(56, 189, 248, 0.15);
            border-color: var(--neon-blue);
            transform: translateX(3px);
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.25);
        }}

        .asset-info {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .asset-ticker {{
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 14.5px;
            color: #fff;
            width: 46px;
        }}

        .asset-bench {{
            font-size: 10.5px;
            color: var(--text-muted);
            background: rgba(255, 255, 255, 0.08);
            padding: 2px 6px;
            border-radius: 4px;
        }}

        .asset-metrics {{
            display: flex;
            gap: 10px;
            font-size: 12px;
            font-weight: 600;
        }}

        .badge-alpha-pos {{ color: var(--neon-green); font-weight: 800; }}
        .badge-alpha-neg {{ color: var(--neon-red); font-weight: 800; }}

        /* Center Panel: Image Viewer */
        .viewer-controls {{
            display: flex;
            gap: 6px;
        }}

        .btn-tab {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-secondary);
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 11.5px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .btn-tab:hover, .btn-tab.active {{
            background: var(--neon-blue);
            color: #000;
            font-weight: 800;
            border-color: var(--neon-blue);
            box-shadow: 0 0 14px rgba(56, 189, 248, 0.45);
        }}

        .img-display-area {{
            flex: 1;
            min-height: 0;
            background: #ffffff;
            border-radius: 12px;
            padding: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            position: relative;
            box-shadow: inset 0 0 12px rgba(0,0,0,0.15);
        }}

        .img-display-area img {{
            max-width: 100%;
            max-height: 100%;
            width: auto;
            height: auto;
            object-fit: contain;
            border-radius: 6px;
            transition: opacity 0.2s ease;
        }}

        .graphic-caption {{
            flex-shrink: 0;
            font-size: 12.5px;
            color: var(--text-primary);
            background: rgba(15, 23, 42, 0.95);
            padding: 10px 14px;
            border-radius: 10px;
            border-left: 4px solid var(--neon-purple);
            line-height: 1.45;
        }}

        /* Right Panel: Decision Cards */
        .decision-cards {{
            display: flex;
            flex-direction: column;
            gap: 10px;
            flex: 1;
            min-height: 0;
        }}

        .decision-card {{
            flex: 1;
            border-radius: 12px;
            padding: 14px 16px;
            border-left: 5px solid;
            background: rgba(255, 255, 255, 0.03);
            transition: transform 0.2s ease, background-color 0.2s ease;
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 6px;
        }}

        .decision-card:hover {{
            transform: translateY(-2px);
            background: rgba(255, 255, 255, 0.05);
        }}

        .decision-card.red {{
            border-color: var(--neon-red);
            background: rgba(248, 113, 113, 0.12);
        }}
        .decision-card.amber {{
            border-color: var(--neon-amber);
            background: rgba(251, 191, 36, 0.12);
        }}
        .decision-card.green {{
            border-color: var(--neon-green);
            background: rgba(74, 222, 128, 0.12);
        }}

        .d-head {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 13px;
            font-weight: 800;
            font-family: 'Outfit', sans-serif;
            letter-spacing: 0.5px;
        }}

        .red .d-head {{ color: var(--neon-red); }}
        .amber .d-head {{ color: var(--neon-amber); }}
        .green .d-head {{ color: var(--neon-green); }}

        .d-body {{
            font-size: 12px;
            color: var(--text-secondary);
            line-height: 1.45;
        }}

        .d-bullets {{
            font-size: 11.5px;
            color: var(--text-primary);
            margin-top: 4px;
            padding-left: 14px;
            display: flex;
            flex-direction: column;
            gap: 3px;
        }}

        .d-bullets li {{
            list-style-type: square;
        }}

        .d-highlight {{
            font-weight: 700;
            color: #fff;
        }}

        /* Footer Banner */
        footer {{
            background: rgba(15, 23, 42, 0.9);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-shrink: 0;
        }}

        .footer-quote {{
            font-size: 12.5px;
            font-weight: 700;
            color: var(--text-primary);
        }}

        .footer-sub {{
            font-size: 11.5px;
            color: var(--text-muted);
        }}
    </style>
</head>
<body>

    <!-- Header -->
    <header>
        <div class="brand">
            <div class="brand-logo">C</div>
            <div class="brand-text">
                <h1>CAPM: REALIDAD vs. PROMESA</h1>
                <p>10 Expedientes bajo la lupa | Julián Duarte (Ciencia de Datos) | Valoración de Activos</p>
            </div>
        </div>

        <div class="tags-container">
            <div class="tag tag-glow">💡 10 Expedientes Conectados</div>
            <div class="tag tag-danger">🚨 Promesa 25%: IMPOSIBLE SIN RIESGO</div>
            <div class="tag" style="color: var(--neon-purple); border-color: rgba(192, 132, 252, 0.3);">🏛️ Cliente: Doña Victoria</div>
        </div>
    </header>

    <!-- Top KPI Row -->
    <div class="kpi-row">
        <div class="kpi-card blue">
            <span class="kpi-label">Universo Analizado</span>
            <span class="kpi-val">10 Activos</span>
            <span class="kpi-sub">1 Cripto (SOL) + 9 Acciones en 3 Sectores</span>
        </div>
        <div class="kpi-card purple">
            <span class="kpi-label">Máxima Beta CAPM</span>
            <span class="kpi-val">1.94 <small style="font-size: 14px; font-weight: normal;">(KLXE)</small></span>
            <span class="kpi-sub">Sensibilidad extrema no remunerada</span>
        </div>
        <div class="kpi-card red">
            <span class="kpi-label">Peor Max Drawdown</span>
            <span class="kpi-val">-93.9% <small style="font-size: 14px; font-weight: normal;">(MVIS)</small></span>
            <span class="kpi-sub">Destrucción severa de capital acumulado</span>
        </div>
        <div class="kpi-card green">
            <span class="kpi-label">Exceso Retorno > CAPM</span>
            <span class="kpi-val">4 / 10 Activos</span>
            <span class="kpi-sub">KOPN (+38.7pp), LIDR (+20.5pp), CTMX, TTI</span>
        </div>
    </div>

    <!-- Main Grid -->
    <div class="dashboard-grid">

        <!-- Left Panel: 10 Expedientes Interactive Cards -->
        <div class="panel">
            <div class="panel-header">
                <span class="panel-title">📦 10 Expedientes</span>
                <span style="font-size: 10.5px; color: var(--text-muted);">Clic para enfocar</span>
            </div>

            <div class="expedientes-list">
                
                <div class="sector-group-title">🪙 Criptoactivo (vs NCI)</div>
                <div class="asset-card active" onclick="highlightAsset('SOL', 'Cripto', '1.25', '-75.4%', '-17.2 pp', 'Rinde +21.6% en bruto, pero CAPM exigia +38.8% dada su beta (1.25). Brecha negativa de -17.2 pp.')">
                    <div class="asset-info">
                        <span class="asset-ticker" style="color: var(--neon-blue);">SOL</span>
                        <span class="asset-bench">NCI</span>
                    </div>
                    <div class="asset-metrics">
                        <span>β 1.25</span>
                        <span class="badge-alpha-neg">-17.2 pp</span>
                    </div>
                </div>

                <div class="sector-group-title">💻 Tecnología (vs XLK)</div>
                <div class="asset-card" onclick="highlightAsset('KOPN', 'Tecnología', '1.82', '-82.1%', '+38.7 pp', 'Mayor generador de alfa ex-post (+38.7 pp), pero exige soportar alta beta (1.82).')">
                    <div class="asset-info">
                        <span class="asset-ticker">KOPN</span>
                        <span class="asset-bench">XLK</span>
                    </div>
                    <div class="asset-metrics">
                        <span>β 1.82</span>
                        <span class="badge-alpha-pos">+38.7 pp</span>
                    </div>
                </div>

                <div class="asset-card" onclick="highlightAsset('MVIS', 'Tecnología', '1.61', '-93.9%', '-29.1 pp', 'Destrucción extrema de valor. Peor Max Drawdown (-93.9%) y alfa altamente negativo.')">
                    <div class="asset-info">
                        <span class="asset-ticker">MVIS</span>
                        <span class="asset-bench">XLK</span>
                    </div>
                    <div class="asset-metrics">
                        <span>β 1.61</span>
                        <span class="badge-alpha-neg">-29.1 pp</span>
                    </div>
                </div>

                <div class="asset-card" onclick="highlightAsset('LIDR', 'Tecnología', '1.43', '-88.5%', '+20.5 pp', 'Genera alfa positivo (+20.5 pp), pero sufre de fragilidad extrema de iliquidez (Amihud alto).')">
                    <div class="asset-info">
                        <span class="asset-ticker">LIDR</span>
                        <span class="asset-bench">XLK</span>
                    </div>
                    <div class="asset-metrics">
                        <span>β 1.43</span>
                        <span class="badge-alpha-pos">+20.5 pp</span>
                    </div>
                </div>

                <div class="sector-group-title">🧬 Biotecnología (vs XBI)</div>
                <div class="asset-card" onclick="highlightAsset('GERN', 'Biotecnología', '0.75', '-68.4%', '-12.8 pp', 'Beta defensiva (0.75), pero retorno insuficiente frente al exigido por CAPM.')">
                    <div class="asset-info">
                        <span class="asset-ticker">GERN</span>
                        <span class="asset-bench">XBI</span>
                    </div>
                    <div class="asset-metrics">
                        <span>β 0.75</span>
                        <span class="badge-alpha-neg">-12.8 pp</span>
                    </div>
                </div>

                <div class="asset-card" onclick="highlightAsset('CTMX', 'Biotecnología', '1.11', '-74.2%', '+8.3 pp', 'Alfa positivo moderado (+8.3 pp) con comportamiento de volatilidad biotech estándar.')">
                    <div class="asset-info">
                        <span class="asset-ticker">CTMX</span>
                        <span class="asset-bench">XBI</span>
                    </div>
                    <div class="asset-metrics">
                        <span>β 1.11</span>
                        <span class="badge-alpha-pos">+8.3 pp</span>
                    </div>
                </div>

                <div class="asset-card" onclick="highlightAsset('OCGN', 'Biotecnología', '1.35', '-85.0%', '-5.4 pp', 'Sensibilidad elevada (1.35) con retorno observado incapaz de cubrir el costo CAPM.')">
                    <div class="asset-info">
                        <span class="asset-ticker">OCGN</span>
                        <span class="asset-bench">XBI</span>
                    </div>
                    <div class="asset-metrics">
                        <span>β 1.35</span>
                        <span class="badge-alpha-neg">-5.4 pp</span>
                    </div>
                </div>

                <div class="sector-group-title">⚡ Energía (vs XLE)</div>
                <div class="asset-card" onclick="highlightAsset('BORR', 'Energía', '1.12', '-64.1%', '-14.6 pp', 'No paga el riesgo del sector energético. Brecha de -14.6 pp frente a CAPM.')">
                    <div class="asset-info">
                        <span class="asset-ticker">BORR</span>
                        <span class="asset-bench">XLE</span>
                    </div>
                    <div class="asset-metrics">
                        <span>β 1.12</span>
                        <span class="badge-alpha-neg">-14.6 pp</span>
                    </div>
                </div>

                <div class="asset-card" onclick="highlightAsset('KLXE', 'Energía', '1.94', '-72.1%', '-27.0 pp', 'Máxima beta de todo el estudio (1.94). Sensibilidad extrema sin compensación de alfa.')">
                    <div class="asset-info">
                        <span class="asset-ticker">KLXE</span>
                        <span class="asset-bench">XLE</span>
                    </div>
                    <div class="asset-metrics">
                        <span>β 1.94</span>
                        <span class="badge-alpha-neg">-27.0 pp</span>
                    </div>
                </div>

                <div class="asset-card" onclick="highlightAsset('TTI', 'Energía', '1.18', '-59.8%', '+3.2 pp', 'Acción bajo excepción (< USD 10). Alfa positivo liviano (+3.2 pp) y menor MDD del grupo.')">
                    <div class="asset-info">
                        <span class="asset-ticker">TTI</span>
                        <span class="asset-bench">XLE</span>
                    </div>
                    <div class="asset-metrics">
                        <span>β 1.18</span>
                        <span class="badge-alpha-pos">+3.2 pp</span>
                    </div>
                </div>

            </div>
        </div>

        <!-- Center Panel: Image Viewer -->
        <div class="panel">
            <div class="panel-header">
                <span class="panel-title">📊 Evidencia Conectora</span>
                <div class="viewer-controls">
                    <button class="btn-tab active" onclick="switchGraphic('09_mapa_beta_drawdown.png', 'Mapa Beta vs Max Drawdown: Los activos abajo y a la derecha (MVIS -93.9%, SOL -75.4%, KLXE -72.1%) combinan alta sensibilidad con ruina acumulada.', this)">🗺️ Beta vs MDD</button>
                    <button class="btn-tab" onclick="switchGraphic('07_brecha_retorno_capm.png', 'Brecha CAPM: Barras verdes superan lo exigido por el modelo (KOPN, LIDR, CTMX, TTI). Barras rojas destruyen valor.', this)">📈 Brecha CAPM</button>
                    <button class="btn-tab" onclick="showPercentiles(this)">🏆 Percentiles</button>
                    <button class="btn-tab" onclick="switchGraphic('10_liquidez_retornos_cero.png', 'Liquidez e Iliquidez de Amihud: Días de retorno cero y fragilidad operativa en KLXE y LIDR.', this)">💧 Liquidez</button>
                </div>
            </div>

            <div class="img-display-area">
                <img id="main-graphic" src="{b64_images.get('09_mapa_beta_drawdown.png', '')}" alt="Grafica CAPM">
            </div>

            <div class="graphic-caption" id="caption-text">
                💡 <strong>Mapa Beta vs Max Drawdown:</strong> Muestra cómo activos de alta beta como MVIS (-93.9%), SOL (-75.4%) y KLXE (-72.1%) demuestran que la trayectoria oculta caídas destructivas.
            </div>
        </div>

        <!-- Right Panel: Decision Matrix -->
        <div class="panel">
            <div class="panel-header">
                <span class="panel-title">⚖️ Decisión Doña Victoria</span>
            </div>

            <div class="decision-cards">

                <div class="decision-card red">
                    <div class="d-head">
                        <span>🛡️ MANDATO CONSERVACIÓN</span>
                        <span>RECHAZAR TODO</span>
                    </div>
                    <div class="d-body">
                        Evitar el 100% de los 10 expedientes. Su extrema volatilidad e iliquidez destruyen el patrimonio.
                    </div>
                    <ul class="d-bullets">
                        <li>Asignar 100% en <span class="d-highlight">T-Bills 3M (DGS3MO)</span>.</li>
                        <li>Cero exposición a penny stocks o cripto.</li>
                    </ul>
                </div>

                <div class="decision-card amber">
                    <div class="d-head">
                        <span>📈 MANDATO CRECIMIENTO</span>
                        <span>SOLO ETF BENCHMARK</span>
                    </div>
                    <div class="d-body">
                        No usar selección individual de penny stocks por fragilidad operativa y spread.
                    </div>
                    <ul class="d-bullets">
                        <li>Indexarse a los ETF <span class="d-highlight">XLK, XLE y XBI</span>.</li>
                        <li>Exposición sistemática diversificada.</li>
                    </ul>
                </div>

                <div class="decision-card green">
                    <div class="d-head">
                        <span>⚡ ESPECULACIÓN ACOTADA</span>
                        <span>MÁXIMO 1% - 2%</span>
                    </div>
                    <div class="d-body">
                        Permitir cupo mínimo especulativo en activos con alfa o catalizador sistemático.
                    </div>
                    <ul class="d-bullets">
                        <li>Asignar 1%-2% en <span class="d-highlight">SOL</span> o <span class="d-highlight">KOPN / TTI</span>.</li>
                        <li>Stop-loss presupuestado del 15% máximo.</li>
                    </ul>
                </div>

            </div>
        </div>

    </div>

    <!-- Footer Banner -->
    <footer>
        <div class="footer-quote">📣 Veredicto Final: "El 25% anual sin caídas es un espejismo financiero."</div>
        <div style="font-size: 11.5px; font-weight: 700; color: #c084fc;">
            Universidad Externado de Colombia | DEFI 2
        </div>
    </footer>

    <!-- Embedded Base64 Data Dictionary & JavaScript -->
    <script>
        const imagesData = {json.dumps(b64_images)};

        function switchGraphic(imgName, text, btn) {{
            const img = document.getElementById('main-graphic');
            const caption = document.getElementById('caption-text');
            
            img.style.opacity = 0.2;
            setTimeout(() => {{
                if (imagesData[imgName]) {{
                    img.src = imagesData[imgName];
                }}
                img.style.opacity = 1;
                caption.innerHTML = '💡 <strong>' + text.split(':')[0] + ':</strong>' + text.split(':')[1];
            }}, 150);

            document.querySelectorAll('.btn-tab').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        }}

        function showPercentiles(btn) {{
            switchGraphic('06_matriz_percentiles.png', 'Matriz de Percentiles: Sintesis multicriterio que evalua volatilidad, alfa, iliquidez y drawdown en un solo mapa.', btn);
        }}

        function highlightAsset(ticker, sector, beta, mdd, brecha, desc) {{
            document.querySelectorAll('.asset-card').forEach(c => c.classList.remove('active'));
            event.currentTarget.classList.add('active');
            
            const caption = document.getElementById('caption-text');
            caption.innerHTML = `📌 <strong>Enfoque en ${{ticker}} (${{sector}}):</strong> Beta ${{beta}} | MDD ${{mdd}} | Brecha CAPM ${{brecha}}.<br>${{desc}}`;
        }}
    </script>
</body>
</html>
"""

# Write HTML file locally in project
with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_code)

print(f"Updated HTML dashboard built at: {OUT_HTML}")
