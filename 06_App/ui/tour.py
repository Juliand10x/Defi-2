"""
Motor interactivo del Tour / Tutorial guiado de Kibo con foco spotlight, difuminado y mascota 3D.
Paleta de autor: Obsidiana, Esmeralda Financiero y Oro Champaña.
"""

import os
import sys

try:
    import streamlit.components.v1 as components
except Exception:
    import streamlit as st
    components = getattr(st, "components", None)
    if components:
        components = getattr(components, "v1", components)

try:
    from ui.kibo_avatar import get_kibo_image_base64
except Exception:
    try:
        from kibo_avatar import get_kibo_image_base64
    except Exception:
        def get_kibo_image_base64():
            return ""


def render_kibo_tour(current_step: int = 1, force_trigger: bool = False):
    """
    Inyecta el motor de tutorial spotlight interactivo de Kibo con la imagen 3D de la mascota,
    efecto de difuminado (blur) y oscurecimiento en toda la pantalla,
    centrando la atención exclusivamente en el botón u opción que se está explicando.
    """
    kibo_img_b64 = get_kibo_image_base64()
    force_js = "true" if force_trigger else "false"

    components.html(
        f"""
        <script>
        (() => {{
          const host = window.parent;
          const doc = host.document;
          const currentAppStep = {current_step};
          const kiboImg = "{kibo_img_b64}";
          const forceTrigger = {force_js};

          // Limpiar timers o instancias previas
          if (host.__kiboTimer) host.clearInterval(host.__kiboTimer);
          if (host.__kiboFastTimer) host.clearInterval(host.__kiboFastTimer);

          // Configuración de pasos del tutorial según la pantalla activa
          const tourConfigs = {{
            1: [
              {{
                target: '[data-testid="stNumberInput"]',
                title: '💰 Tu Capital Simulado',
                text: 'Escribe aquí cuánto dinero pondremos a prueba. No te preocupes: es un simulador educativo 100% seguro con cotizaciones reales de Wall Street sin arriesgar ni un solo centavo.',
                hint: 'Paso 1 de 4 en esta pantalla'
              }},
              {{
                target: '[data-testid="stHorizontalBlock"]',
                title: '⚡ Montos Rápidos',
                text: 'Toca cualquiera de estos botones ($10K, $50K, $100K) para cambiar el monto con un solo toque y ver cómo reacciona tu estrategia.',
                hint: 'Paso 2 de 4 en esta pantalla'
              }},
              {{
                target: '[data-testid="stExpander"]',
                title: '⚙️ Presupuesto de riesgo',
                text: 'Si quieres afinar la simulación, aquí puedes definir el límite de riesgo de tu estrategia.',
                hint: 'Paso 3 de 4 en esta pantalla'
              }},
              {{
                target: 'button[kind="primary"]',
                title: '🚀 Siguiente: Tu Perfil',
                text: 'Toca aquí para definir cómo quieres que Kibo cuide tu dinero frente a los altibajos del mercado.',
                hint: 'Toca el botón resaltado para avanzar',
                action: true
              }}
            ],
            2: [
              {{
                target: '[data-testid="stRadio"]',
                title: '🎯 Elige cómo cuidar tu dinero',
                text: 'Elige tu modo: Escudo (Conservador: máxima protección), Equilibrio (Moderado: balance) o Cohete (Agresivo: mayor rentabilidad asumiendo vaivenes). Kibo adaptará las matemáticas a tu estilo.',
                hint: 'Paso 1 de 3 en esta pantalla'
              }},
              {{
                target: '[data-testid="stExpander"]',
                title: '⚙️ Opciones Avanzadas',
                text: 'Para personas más interesadas o avanzadas: aquí puedes personalizar el horizonte de días a proyectar y el nivel de confianza para medir el riesgo (95% o 99%). Si eres principiante, puedes continuar con los valores sugeridos.',
                hint: 'Paso 2 de 3 en esta pantalla'
              }},
              {{
                target: 'button[kind="primary"]',
                title: '✨ Continuar a tus Acciones',
                text: 'Con tu perfil y parámetros listos, pasaremos a seleccionar las empresas en las que invertirás.',
                hint: 'Toca el botón resaltado para avanzar',
                action: true
              }}
            ],
            3: [
              {{
                target: '[data-testid="stMultiSelect"]',
                title: '🧺 Tu Canasta de Acciones',
                text: 'Aquí eliges las empresas que te interesan. Te dejamos 10 líderes mundiales (Apple, Microsoft, Nvidia, etc.) listas para evaluar.',
                hint: 'Paso 1 de 3 en esta pantalla'
              }},
              {{
                target: '.diversification-gauge-card',
                title: '🛡️ Medidor de Diversificación',
                text: 'Regla de oro: No pongas todos los huevos en la misma canasta. Kibo vigila que cubras al menos 4 sectores diferentes (tecnología, salud, energía, etc.) para que una crisis en un sector no hunda tu dinero.',
                hint: 'Paso 2 de 3 en esta pantalla'
              }},
              {{
                target: 'button[kind="primary"]',
                title: '🧠 A los Modelos Matemáticos',
                text: 'Toca aquí para que Kibo ponga a competir a los 3 cerebros estocásticos.',
                hint: 'Toca el botón resaltado para avanzar',
                action: true
              }}
            ],
            4: [
              {{
                target: '.verdict-glass-card',
                title: '🏆 El Cerebro Ganador',
                text: 'Kibo analizó 3 años de cotizaciones con 4 teorías matemáticas avanzadas (Browniano, Merton, Ornstein-Uhlenbeck y Browniano Fraccionario con memoria de Hurst) y te explica cuál modelo describe mejor cada acción.',
                hint: 'Paso 1 de 4 en esta pantalla'
              }},
              {{
                target: '[data-testid="stPlotlyChart"]',
                title: '📈 Modelos y Backtesting Rolling',
                text: 'Explora las pestañas: puedes ver las proyecciones estocásticas y la pestaña 5 de Evaluación Predictiva Rolling (RMSE y MAPE) frente a la caminata aleatoria.',
                hint: 'Paso 2 de 4 en esta pantalla'
              }},
              {{
                target: '[data-testid="stExpander"]',
                title: '⚙️ Opciones avanzadas',
                text: 'Aquí puedes consultar los parámetros calibrados y comparar los modelos con AIC y BIC.',
                hint: 'Paso 3 de 4 en esta pantalla'
              }},
              {{
                target: 'button[kind="primary"]',
                title: '⚡ Explorar Opciones',
                text: 'Toca aquí para comparar contratos reales, precios de mercado y una valoración teórica.',
                hint: 'Toca el botón resaltado para avanzar',
                action: true
              }}
            ],
            5: [
              {{
                target: '[data-testid="stSelectbox"]',
                title: '🔎 Elige el activo subyacente',
                text: 'Selecciona una acción para proyectar precios y consultar contratos disponibles.',
                hint: 'Paso 1 de 3 en esta pantalla'
              }},
              {{
                target: 'text:Buscar Seguros',
                title: '📋 Consulta contratos listados',
                text: 'Consulta vencimientos, strikes, bid, ask, volumen e interés abierto.',
                hint: 'Pulsa el botón y luego continúa con la guía'
              }},
              {{
                target: 'text:Ver Mi Portafolio Final',
                title: '💼 Ver Mi Portafolio Final',
                text: 'Pasemos a la asignación óptima de capital y receta de compra.',
                hint: 'Toca el botón resaltado para avanzar',
                action: true
              }}
            ],
            6: [
              {{
                target: '.kpi-wallet-grid',
                title: '💼 Resumen de Billetera',
                text: 'Aquí encuentras tu resumen ejecutivo: capital asignado, riesgo máximo estimado (VaR), efectivo de reserva por redondeo y el estatus de la optimización cuadrática.',
                hint: 'Paso 1 de 4 en esta pantalla'
              }},
              {{
                target: '[data-testid="stTabs"]',
                title: '🛡️ Plan, 3 Métodos de VaR y Estrés',
                text: 'Navega por las 3 pestañas: revisa tu lista de compra en Wall Street, compara los 3 métodos de VaR (Paramétrico, Histórico y Monte Carlo 20.000 sims) y somete tu cartera a las 3 Pruebas de Estrés.',
                hint: 'Paso 2 de 4 en esta pantalla'
              }},
              {{
                target: '[data-testid="stExpander"]',
                title: '⚙️ Opciones avanzadas',
                text: 'Si quieres ajustar los costos y revisar algunos detalles de la optimización, puedes hacerlo aquí.',
                hint: 'Paso 3 de 4 en esta pantalla'
              }},
              {{
                target: '[data-testid="stDownloadButton"]',
                title: '📥 Descargar Reporte CSV',
                text: 'Descarga tu plan de inversión con acciones enteras y montos exactos en CSV para guardarlo.',
                hint: 'Paso 4 de 4 en esta pantalla'
              }}
            ]
          }};

          const steps = tourConfigs[currentAppStep] || tourConfigs[1];

          // Inyectar o actualizar estilos CSS del Tour
          let style = doc.getElementById('kibo-tour-styles');
          if (!style) {{
            style = doc.createElement('style');
            style.id = 'kibo-tour-styles';
            doc.head.appendChild(style);
          }}
          
          style.textContent = `
            /* Fondo oscurecido nítido sin difuminar el elemento enfocado */
            #kibo-backdrop {{
              position: fixed;
              inset: 0;
              width: 100vw;
              height: 100vh;
              background: rgba(4, 7, 14, 0.70);
              z-index: 99990;
              opacity: 0;
              pointer-events: auto;
              transition: opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            }}
            #kibo-backdrop.visible {{
              opacity: 1;
            }}

            /* Resaltado del elemento objetivo: 100% nítido, sin blur ni oscurecimiento */
            .kibo-tour-target-active {{
              position: relative !important;
              z-index: 99998 !important;
              pointer-events: auto !important;
              filter: none !important;
              -webkit-filter: none !important;
              border-radius: 12px;
            }}

            /* Anillo de Foco / Spotlight pulsante (Esmeralda & Oro) */
            #kibo-spotlight-box {{
              position: fixed;
              border: 2.5px solid #10b981;
              border-radius: 18px;
              box-shadow: 0 0 0 9999px rgba(5, 8, 15, 0.84),
                          0 0 25px rgba(16, 185, 129, 0.65),
                          inset 0 0 12px rgba(16, 185, 129, 0.25);
              z-index: 99995;
              pointer-events: none;
              opacity: 0;
              transition: all 0.32s cubic-bezier(0.2, 0.8, 0.2, 1);
              animation: kiboSpotlightPulse 2.8s infinite ease-in-out;
            }}
            #kibo-spotlight-box.visible {{
              opacity: 1;
            }}

            @keyframes kiboSpotlightPulse {{
              0%, 100% {{
                border-color: #10b981;
                box-shadow: 0 0 0 9999px rgba(5, 8, 15, 0.84),
                            0 0 22px rgba(16, 185, 129, 0.6),
                            inset 0 0 10px rgba(16, 185, 129, 0.2);
              }}
              50% {{
                border-color: #f59e0b;
                box-shadow: 0 0 0 9999px rgba(5, 8, 15, 0.86),
                            0 0 35px rgba(245, 158, 11, 0.75),
                            inset 0 0 16px rgba(245, 158, 11, 0.3);
              }}
            }}

            /* Globo flotante de Kibo con la Mascota 3D Real */
            #kibo-guide-card {{
              position: fixed;
              display: flex;
              align-items: flex-start;
              gap: 15px;
              max-width: 410px;
              width: calc(100vw - 32px);
              background: linear-gradient(145deg, #0d131f, #141c2c);
              border: 1.5px solid rgba(16, 185, 129, 0.4);
              border-radius: 22px;
              padding: 16px 18px 15px;
              color: #f1f5f9;
              box-shadow: 0 22px 55px rgba(0, 0, 0, 0.7), 0 0 25px rgba(16, 185, 129, 0.2);
              z-index: 100000;
              opacity: 0;
              transform: translateY(12px) scale(0.96);
              transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
              font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            #kibo-guide-card.visible {{
              opacity: 1;
              transform: translateY(0) scale(1);
            }}

            .kibo-card-avatar {{
              width: 58px;
              height: 58px;
              border-radius: 18px;
              overflow: hidden;
              border: 2px solid #10b981;
              background: #111827;
              display: flex;
              align-items: center;
              justify-content: center;
              flex-shrink: 0;
              box-shadow: 0 8px 20px rgba(16, 185, 129, 0.35);
              animation: kiboAvatarBounce 2.5s infinite ease-in-out;
            }}
            @keyframes kiboAvatarBounce {{
              0%, 100% {{ transform: translateY(0) rotate(0deg); }}
              50% {{ transform: translateY(-4px) rotate(2deg); }}
            }}
            .kibo-tour-img {{
              width: 100%;
              height: 100%;
              object-fit: cover;
            }}

            .kibo-card-body {{
              flex: 1;
              min-width: 0;
            }}
            .kibo-card-badge {{
              display: inline-block;
              font-size: 11px;
              font-weight: 800;
              text-transform: uppercase;
              letter-spacing: 0.08em;
              color: #10b981;
              margin-bottom: 4px;
            }}
            .kibo-card-title {{
              font-size: 15px;
              font-weight: 800;
              color: #ffffff;
              margin: 0 0 6px 0;
              line-height: 1.25;
            }}
            .kibo-card-text {{
              font-size: 13px;
              line-height: 1.45;
              color: #cbd5e1;
              margin: 0 0 10px 0;
            }}
            .kibo-card-hint {{
              font-size: 11px;
              font-weight: 700;
              color: #94a3b8;
              margin-bottom: 12px;
            }}

            .kibo-card-actions {{
              display: flex;
              gap: 8px;
              justify-content: flex-end;
              align-items: center;
            }}
            .kibo-btn {{
              padding: 7px 14px;
              border-radius: 10px;
              font-size: 12px;
              font-weight: 750;
              cursor: pointer;
              transition: all 0.15s ease;
              border: none;
            }}
            .kibo-btn-primary {{
              background: linear-gradient(135deg, #10b981, #047857);
              color: #ffffff;
              box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4);
            }}
            .kibo-btn-primary:hover {{
              background: #059669;
              transform: translateY(-1px);
            }}
            .kibo-btn-secondary {{
              background: rgba(255, 255, 255, 0.08);
              color: #cbd5e1;
              border: 1px solid rgba(255, 255, 255, 0.15);
            }}
            .kibo-btn-secondary:hover {{
              background: rgba(255, 255, 255, 0.15);
              color: #ffffff;
            }}
            .kibo-btn-close {{
              position: absolute;
              top: 10px;
              right: 12px;
              background: transparent;
              border: none;
              color: #94a3b8;
              font-size: 20px;
              cursor: pointer;
              line-height: 1;
              padding: 2px;
            }}
            .kibo-btn-close:hover {{
              color: #ffffff;
            }}
          `;

          // Elementos del DOM
          let backdrop = doc.getElementById('kibo-backdrop');
          if (!backdrop) {{
            backdrop = doc.createElement('div');
            backdrop.id = 'kibo-backdrop';
            doc.body.appendChild(backdrop);
          }}

          let spotlight = doc.getElementById('kibo-spotlight-box');
          if (!spotlight) {{
            spotlight = doc.createElement('div');
            spotlight.id = 'kibo-spotlight-box';
            doc.body.appendChild(spotlight);
          }}

          let guide = doc.getElementById('kibo-guide-card');
          if (!guide) {{
            guide = doc.createElement('div');
            guide.id = 'kibo-guide-card';
            guide.innerHTML = `
              <button class="kibo-btn-close" id="kibo-tour-close" title="Cerrar guía">×</button>
              <div class="kibo-card-avatar">
                <img src="${{kiboImg}}" class="kibo-tour-img" alt="Kibo Mascot" />
              </div>
              <div class="kibo-card-body">
                <span class="kibo-card-badge">KIBO COPILOTO · GUÍA EN VIVO</span>
                <div class="kibo-card-title"></div>
                <div class="kibo-card-text"></div>
                <div class="kibo-card-hint"></div>
                <div class="kibo-card-actions">
                  <button class="kibo-btn kibo-btn-secondary" id="kibo-tour-prev">Anterior</button>
                  <button class="kibo-btn kibo-btn-primary" id="kibo-tour-next">Siguiente ➔</button>
                </div>
              </div>
            `;
            doc.body.appendChild(guide);
          }}

          const dom = {{
            title: guide.querySelector('.kibo-card-title'),
            text: guide.querySelector('.kibo-card-text'),
            hint: guide.querySelector('.kibo-card-hint'),
            prev: guide.querySelector('#kibo-tour-prev'),
            next: guide.querySelector('#kibo-tour-next'),
            close: guide.querySelector('#kibo-tour-close')
          }};

          // Estado del paso actual
          const storageKey = `kibo-step-tour-v2-${{currentAppStep}}`;
          if (forceTrigger) {{
            host.sessionStorage.removeItem('kibo-tour-completed');
            host.sessionStorage.setItem('kibo-tour-enabled', 'true');
            host.localStorage.removeItem('kibo-tour-disabled');
            host.localStorage.setItem(storageKey, 0);
          }}
          const savedStepIndex = Number(host.localStorage.getItem(storageKey) || 0);
          let stepIndex = forceTrigger ? 0 : (Number.isInteger(savedStepIndex) && savedStepIndex >= 0 && savedStepIndex < steps.length ? savedStepIndex : 0);
          const tourCompleted = host.sessionStorage.getItem('kibo-tour-completed') === 'true';
          const tourEnabled = host.sessionStorage.getItem('kibo-tour-enabled') === 'true';
          let isTourActive = forceTrigger || (tourEnabled && !tourCompleted);

          function findTarget(selector) {{
            if (!selector) return null;
            if (selector.startsWith('text:')) {{
              const label = selector.slice(5).toLocaleLowerCase();
              return Array.from(doc.querySelectorAll('button')).find(
                button => button.textContent.trim().toLocaleLowerCase().includes(label)
              ) || null;
            }}
            let el = doc.querySelector(selector);
            if (!el && selector === '[data-testid="stExpander"]') {{
              el = doc.querySelector('.stExpander') || doc.querySelector('details') || doc.querySelector('[data-testid="stExpanderDetails"]');
            }}
            return el;
          }}

          function clearActiveTargets() {{
            try {{
              doc.querySelectorAll('.kibo-tour-target-active').forEach(el => {{
                el.classList.remove('kibo-tour-target-active');
              }});
            }} catch(e) {{}}
          }}

          function hideTour() {{
            clearActiveTargets();
            backdrop.classList.remove('visible');
            spotlight.classList.remove('visible');
            guide.classList.remove('visible');
            setTimeout(() => {{
              if (!isTourActive) {{
                backdrop.style.display = 'none';
                spotlight.style.display = 'none';
                guide.style.display = 'none';
              }}
            }}, 300);
          }}

          function pauseTour() {{
            isTourActive = false;
            hideTour();
          }}

          function finishTour() {{
            isTourActive = false;
            host.sessionStorage.setItem('kibo-tour-completed', 'true');
            host.sessionStorage.setItem('kibo-tour-enabled', 'false');
            host.localStorage.setItem('kibo-tour-disabled', 'true');
            hideTour();
          }}

          function updateTour() {{
            if (!isTourActive) {{ hideTour(); return; }}
            if (stepIndex >= steps.length) {{
              finishTour();
              return;
            }}

            const current = steps[stepIndex];
            const target = findTarget(current.target);

            if (!target) {{
              return;
            }}

            // Desmarcar targets anteriores y elevar el actual para nitidez absoluta (sin blur)
            clearActiveTargets();
            target.classList.add('kibo-tour-target-active');

            const rect = target.getBoundingClientRect();
            if (rect.width === 0 || rect.height === 0) return;

            // Scroll suave si no está en vista
            if (rect.top < 40 || rect.bottom > host.innerHeight - 40) {{
              target.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
            }}

            const pad = 10;
            const top = Math.max(0, rect.top - pad);
            const left = Math.max(0, rect.left - pad);
            const width = rect.width + pad * 2;
            const height = rect.height + pad * 2;

            backdrop.style.display = 'block';
            spotlight.style.display = 'block';
            guide.style.display = 'flex';

            // Activar difuminado y foco
            requestAnimationFrame(() => {{
              backdrop.classList.add('visible');
              spotlight.classList.add('visible');
              guide.classList.add('visible');

              Object.assign(spotlight.style, {{
                top: `${{top}}px`,
                left: `${{left}}px`,
                width: `${{width}}px`,
                height: `${{height}}px`
              }});

              dom.title.textContent = current.title;
              dom.text.textContent = current.text;
              dom.hint.textContent = current.hint || '';
              dom.prev.style.display = stepIndex === 0 ? 'none' : 'inline-block';
              dom.next.textContent = stepIndex === steps.length - 1 ? '¡Listo! Entendido ✨' : 'Siguiente ➔';

              // Posicionar globo guía Kibo
              const guideWidth = Math.min(410, host.innerWidth - 32);
              let guideTop = top + height + 16;
              if (guideTop + 180 > host.innerHeight) {{
                guideTop = Math.max(16, top - 200);
              }}
              let guideLeft = Math.max(16, Math.min(left, host.innerWidth - guideWidth - 16));

              Object.assign(guide.style, {{
                top: `${{guideTop}}px`,
                left: `${{guideLeft}}px`
              }});
            }});
          }}

          dom.next.onclick = (e) => {{
            e.stopPropagation();
            if (stepIndex >= steps.length - 1) {{
              if (currentAppStep === 6) finishTour(); else pauseTour();
            }} else {{
              stepIndex++;
              host.localStorage.setItem(storageKey, stepIndex);
              updateTour();
            }}
          }};

          dom.prev.onclick = (e) => {{
            e.stopPropagation();
            if (stepIndex > 0) {{
              stepIndex--;
              host.localStorage.setItem(storageKey, stepIndex);
              updateTour();
            }}
          }};

          dom.close.onclick = (e) => {{
            e.stopPropagation();
            finishTour();
          }};

          // Menú flotante de Kibo: tutorial, diccionario financiero y FAQ
          let menu = doc.getElementById('kibo-help-menu');
          if (!menu) {{
            menu = doc.createElement('div');
            menu.id = 'kibo-help-menu';
            doc.body.appendChild(menu);
          }}
          menu.style.cssText = 'display:none;position:fixed;right:20px;bottom:82px;z-index:100005;width:min(340px,calc(100vw - 32px));max-height:80vh;overflow-y:auto;border-radius:18px;background:#0d131f;border:1.5px solid #10b981;color:#e2e8f0;box-shadow:0 20px 50px rgba(0,0,0,.75),0 0 25px rgba(16,185,129,.25);padding:16px;font-family:Inter,-apple-system,sans-serif;';
          menu.innerHTML = `
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
              <div style="display:flex;align-items:center;gap:8px;">
                <span style="font-size:18px;">🤖</span>
                <strong style="font-size:15px;color:#fff;">Copiloto Kibo</strong>
              </div>
              <button id="kibo-menu-close" style="background:transparent;border:0;color:#94a3b8;font-size:22px;cursor:pointer;line-height:1;padding:0 4px;" title="Cerrar">×</button>
            </div>
            <p style="font-size:12px;color:#94a3b8;margin:0 0 10px 0;line-height:1.4;">¿Qué necesitas hacer ahora?</p>
            <button id="kibo-menu-tour" style="width:100%;padding:10px 12px;margin-bottom:6px;border:0;border-radius:10px;background:linear-gradient(135deg,#10b981,#047857);color:#fff;font-weight:700;font-size:13px;cursor:pointer;text-align:left;">🚀 Iniciar tutorial de este paso</button>
            <button id="kibo-menu-dict" style="width:100%;padding:10px 12px;margin-bottom:6px;border:1px solid #334155;border-radius:10px;background:#172033;color:#fff;font-weight:700;font-size:13px;cursor:pointer;text-align:left;">📖 Diccionario (Traductor a cristiano)</button>
            <div id="kibo-dict-content" style="display:none;margin:8px 0 12px 0;padding:10px;background:#111827;border-radius:10px;border-left:3px solid #10b981;font-size:12px;line-height:1.45;max-height:220px;overflow-y:auto;">
              <div style="font-weight:750;color:#34d399;margin-bottom:4px;">💡 Jerga traducida por Kibo:</div>
              <p style="margin:4px 0;"><b>• VaR (Riesgo normal):</b> Lo máximo que perderías en el 99% de los días habituales.</p>
              <p style="margin:4px 0;"><b>• CVaR (Desastre extremo):</b> Cuánto perderías en promedio si ocurre el peor 1% de catástrofes.</p>
              <p style="margin:4px 0;"><b>• GBM (Browniano):</b> Simula precios flotando suavemente con tendencia y olas.</p>
              <p style="margin:4px 0;"><b>• Merton (Saltos):</b> Contempla noticias bomba o caídas repentinas de susto.</p>
              <p style="margin:4px 0;"><b>• O-U (Imán):</b> El precio tiende a regresar a su costo histórico promedio.</p>
              <p style="margin:4px 0;"><b>• fBm (Hurst):</b> Mide si la acción tiene memoria de tendencia (H > 0.5).</p>
              <p style="margin:4px 0;"><b>• Manada (CCK):</b> Detecta si la gente entra en pánico y corre en estampida junta.</p>
              <p style="margin:4px 0;"><b>• Opción Put (Seguro):</b> Póliza que te salva el dinero si la acción se desploma.</p>
              <p style="margin:4px 0;"><b>• Strike (K):</b> El precio garantizado pactado en el contrato de seguro.</p>
              <p style="margin:4px 0;"><b>• Prima:</b> El costo que pagas hoy para comprar la protección.</p>
              <p style="margin:4px 0;"><b>• SLSQP:</b> Algoritmo chef que reparte tus acciones sin superar el 35% por sector.</p>
            </div>
            <button id="kibo-menu-faq" style="width:100%;padding:10px 12px;margin-bottom:4px;border:1px solid #334155;border-radius:10px;background:#172033;color:#fff;font-weight:700;font-size:13px;cursor:pointer;text-align:left;">❓ Preguntas frecuentes (FAQ)</button>
            <div id="kibo-faq-content" style="display:none;margin:8px 0 6px 0;padding:10px;background:#111827;border-radius:10px;border-left:3px solid #f59e0b;font-size:12px;line-height:1.45;max-height:200px;overflow-y:auto;">
              <p style="margin:4px 0;"><b>¿Cómo avanzo o regreso?</b><br>Usa los botones 'Continuar' o 'Volver' al final de la pantalla.</p>
              <p style="margin:6px 0 4px;"><b>¿Estoy invirtiendo dinero real?</b><br>No. Todo es un simulador pedagógico seguro con cotizaciones reales de Wall Street.</p>
              <p style="margin:6px 0 4px;"><b>¿Cómo leo los gráficos de abanico?</b><br>La línea verde central es la trayectoria mediana. Las bandas verdes son los escenarios más probables (10%-90%).</p>
            </div>
          `;

          const toggleHelpMenu = (show) => {{
            if (show === undefined) {{
              menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
            }} else {{
              menu.style.display = show ? 'block' : 'none';
            }}
          }};

          if (!host.__kiboBubbleListenerAttached) {{
            const handleEvent = (e) => {{
              if (e.target.closest('#kibo-help-trigger')) {{
                e.preventDefault();
                e.stopPropagation();
                toggleHelpMenu();
                return;
              }}
              if (e.target.closest('#kibo-menu-close')) {{
                e.preventDefault();
                toggleHelpMenu(false);
                return;
              }}
              if (e.target.closest('#kibo-menu-tour')) {{
                toggleHelpMenu(false);
                if (host.__kiboTriggerTour) host.__kiboTriggerTour();
                return;
              }}
              if (e.target.closest('#kibo-menu-dict')) {{
                const dictEl = doc.getElementById('kibo-dict-content');
                if (dictEl) dictEl.style.display = dictEl.style.display === 'none' ? 'block' : 'none';
                return;
              }}
              if (e.target.closest('#kibo-menu-faq')) {{
                const faqEl = doc.getElementById('kibo-faq-content');
                if (faqEl) faqEl.style.display = faqEl.style.display === 'none' ? 'block' : 'none';
                return;
              }}
              if (!e.target.closest('#kibo-help-menu')) {{
                toggleHelpMenu(false);
              }}
            }};

            doc.addEventListener('click', handleEvent, true);
            doc.addEventListener('touchend', handleEvent, true);
            host.__kiboBubbleListenerAttached = true;
          }}

          // Función global para disparar el tour desde el splash o el reinicio
          host.__kiboTriggerTour = () => {{
            isTourActive = true;
            stepIndex = 0;
            host.sessionStorage.removeItem('kibo-tour-completed');
            host.sessionStorage.setItem('kibo-tour-enabled', 'true');
            host.localStorage.removeItem('kibo-tour-disabled');
            host.localStorage.setItem(storageKey, 0);
            updateTour();
          }};

          // Listener de resize
          host.addEventListener('resize', updateTour);

          // Intentos de actualización rápida tras el render de Streamlit
          let attempts = 0;
          host.__kiboFastTimer = host.setInterval(() => {{
            attempts++;
            updateTour();
            if (attempts > 30 || findTarget(steps[stepIndex]?.target)) {{
              host.clearInterval(host.__kiboFastTimer);
            }}
          }}, 50);

          host.__kiboTimer = host.setInterval(updateTour, 400);
          updateTour();
        }})();
        </script>
        """,
        height=0,
    )


def render_intro_splash_animation():
    """
    Inyecta una pantalla de bienvenida / intro splash screen cinematográfica
    que revela el nombre de Kibo, la mascota 3D y el propósito de la app.
    Solo se muestra una vez por sesión (o al hacer clic en el logo).
    """
    kibo_img_b64 = get_kibo_image_base64()

    components.html(
        f"""
        <script>
        (() => {{
          const host = window.parent;
          const doc = host.document;
          const splashSeen = host.sessionStorage.getItem('kibo-splash-seen-v2');

          if (splashSeen) return;

          let splash = doc.getElementById('kibo-splash-screen');
          if (!splash) {{
            splash = doc.createElement('div');
            splash.id = 'kibo-splash-screen';
            splash.innerHTML = `
              <div class="splash-glow-halo">
                <img src="{kibo_img_b64}" class="splash-avatar-img" alt="Kibo Mascot" />
              </div>
              <div class="splash-brand-title">KIBO</div>
              <div class="splash-brand-sub">Copiloto Inteligente de Finanzas & Riesgo</div>
              <div class="splash-context-card">
                <div class="splash-context-title">¿Es tu primera vez usando Kibo?</div>
                <div class="splash-context-text">
                  ¡Hola! Soy tu asistente cuantitativo 🚀 Podemos hacer un recorrido interactivo guiado para explicarte cada botón, modelo estocástico y gráfico paso a paso, o puedes comenzar a usar la plataforma directamente si ya la conoces.
                </div>
                <div class="splash-btn-row">
                  <button class="splash-cta-btn splash-cta-tour" id="kibo-splash-start-tour">
                    🚀 Sí, iniciar tutorial guiado
                  </button>
                  <button class="splash-cta-btn splash-cta-skip" id="kibo-splash-skip-tour">
                    ⚡ Ya la conozco, omitir guía
                  </button>
                </div>
              </div>
              <div class="splash-bar-track">
                <div class="splash-bar-fill"></div>
              </div>
            `;
            doc.body.appendChild(splash);

            const startTourAction = () => {{
              splash.classList.add('fade-out');
              host.sessionStorage.setItem('kibo-splash-seen-v2', 'true');
              host.sessionStorage.removeItem('kibo-tour-completed');
            host.sessionStorage.setItem('kibo-tour-enabled', 'true');
              host.localStorage.removeItem('kibo-tour-disabled');
              setTimeout(() => {{
                if (splash && splash.parentNode) splash.remove();
                if (typeof host.__kiboTriggerTour === 'function') host.__kiboTriggerTour();
              }}, 450);
            }};

            const skipTourAction = () => {{
              splash.classList.add('fade-out');
              host.sessionStorage.setItem('kibo-splash-seen-v2', 'true');
              host.sessionStorage.setItem('kibo-tour-completed', 'true');
              host.sessionStorage.setItem('kibo-tour-enabled', 'false');
              host.localStorage.setItem('kibo-tour-disabled', 'true');
              setTimeout(() => {{
                if (splash && splash.parentNode) splash.remove();
              }}, 450);
            }};

            const btnTour = splash.querySelector('#kibo-splash-start-tour');
            if (btnTour) btnTour.onclick = (e) => {{
              e.stopPropagation();
              startTourAction();
            }};

            const btnSkip = splash.querySelector('#kibo-splash-skip-tour');
            if (btnSkip) btnSkip.onclick = (e) => {{
              e.stopPropagation();
              skipTourAction();
            }};
          }}
        }})();
        </script>
        """,
        height=0,
    )


# Compatibilidad
render_nori_tour = render_kibo_tour
