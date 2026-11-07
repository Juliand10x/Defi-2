"""Motor interactivo del Tour / Tutorial guiado de Kibo con foco spotlight, difuminado y oscurecimiento."""

import streamlit.components.v1 as components


def render_kibo_tour(current_step: int = 1):
    """
    Inyecta el motor de tutorial spotlight interactivo de Kibo.
    Crea un efecto de difuminado (blur) y oscurecimiento en toda la pantalla,
    centrando la atención exclusivamente en el botón u opción que se está explicando
    con un anillo de luz neón pulsante.
    """
    components.html(
        f"""
        <script>
        (() => {{
          const host = window.parent;
          const doc = host.document;
          const currentAppStep = {current_step};

          // Limpiar timers o instancias previas
          if (host.__kiboTimer) host.clearInterval(host.__kiboTimer);
          if (host.__kiboFastTimer) host.clearInterval(host.__kiboFastTimer);

          // Configuración de pasos del tutorial según la pantalla activa
          const tourConfigs = {{
            1: [
              {{
                target: '[data-testid="stNumberInput"]',
                title: '💰 ¿Cuánto dinero simulado evaluar?',
                text: 'Escribe aquí el capital que quieres analizar. Tranquilo: es 100% simulación educativa, no se arriesga ni un peso real.',
                hint: 'Paso 1 de 3 en esta pantalla'
              }},
              {{
                target: '[data-testid="stHorizontalBlock"]',
                title: '⚡ Botones Rápidos (Estilo Nequi / Nu)',
                text: 'Toca cualquiera de estos botones para ajustar el monto al instante con un solo toque.',
                hint: 'Paso 2 de 3 en esta pantalla'
              }},
              {{
                target: 'button[kind="primary"]',
                title: '🚀 Siguiente paso',
                text: 'Toca este botón para continuar a definir cómo te sientes frente al riesgo.',
                hint: 'Toca Continuar para avanzar',
                action: true
              }}
            ],
            2: [
              {{
                target: '[data-testid="stRadio"]',
                title: '🎯 Elige tu Perfil de Riesgo',
                text: 'Selecciona cómo quieres proteger tu dinero: Modo Escudo (Conservador), Modo Equilibrio (Moderado) o Modo Cohete (Agresivo).',
                hint: 'Paso 1 de 2 en esta pantalla'
              }},
              {{
                target: 'button[kind="primary"]',
                title: '✨ Continuar a Activos',
                text: 'Con tu perfil elegido, Kibo sabrá si blindar tu dinero ante caídas o buscar mayor crecimiento.',
                hint: 'Toca Continuar para avanzar',
                action: true
              }}
            ],
            3: [
              {{
                target: '[data-testid="stMultiSelect"]',
                title: '🧺 Canasta de Empresas',
                text: 'Elige las empresas que quieres analizar. Te dejamos una selección diversificada de 10 gigantes de Wall Street.',
                hint: 'Paso 1 de 3 en esta pantalla'
              }},
              {{
                target: '.diversification-gauge-card',
                title: '🛡️ Medidor de Diversificación',
                text: 'Regla de oro: No pongas todos los huevos en la misma canasta. Aquí Kibo vigila que cubras al menos 4 sectores económicos.',
                hint: 'Paso 2 de 3 en esta pantalla'
              }},
              {{
                target: 'button[kind="primary"]',
                title: '🧠 A los Modelos Matemáticos',
                text: 'Toca este botón para poner a competir a los 3 cerebros estocásticos de Kibo.',
                hint: 'Toca Continuar para avanzar',
                action: true
              }}
            ],
            4: [
              {{
                target: '.verdict-glass-card',
                title: '🏆 El Cerebro Ganador',
                text: 'Kibo analizó la historia real de la acción y determinó cuál de los 3 modelos predice mejor su comportamiento sin engañarte.',
                hint: 'Paso 1 de 3 en esta pantalla'
              }},
              {{
                target: '[data-testid="stPlotlyChart"]',
                title: '📈 Abanico de Probabilidades',
                text: 'Aquí ves las trayectorias posibles del precio hacia el futuro con percentiles de riesgo.',
                hint: 'Paso 2 de 3 en esta pantalla'
              }},
              {{
                target: 'button[kind="primary"]',
                title: '💼 Tu Portafolio Final',
                text: 'Toca aquí para ver la receta exacta de cuántas acciones comprar de cada empresa.',
                hint: 'Toca Continuar para avanzar',
                action: true
              }}
            ],
            5: [
              {{
                target: '.kpi-wallet-grid',
                title: '💼 Tu Billetera Inteligente',
                text: 'Resumen estilo Nu/Binance: capital total, riesgo máximo estimado (VaR 99%) y efectivo residual de reserva.',
                hint: 'Paso 1 de 3 en esta pantalla'
              }},
              {{
                target: '.stocks-plan-container',
                title: '🛒 Receta de Compra Exacta',
                text: 'Te decimos exactamente cuántas acciones enteras comprar de cada empresa para que tu riesgo sea el mínimo posible.',
                hint: 'Paso 2 de 3 en esta pantalla'
              }},
              {{
                target: '[data-testid="stDownloadButton"]',
                title: '📥 Descargar en Excel / CSV',
                text: 'Descarga tu plan de inversión completo para sustentarlo o guardarlo cuando quieras.',
                hint: '¡Tutorial completado con éxito!'
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
            /* Fondo oscurecido con difuminado (blur) */
            #kibo-backdrop {{
              position: fixed;
              inset: 0;
              width: 100vw;
              height: 100vh;
              background: rgba(6, 11, 25, 0.78);
              backdrop-filter: blur(8px);
              -webkit-backdrop-filter: blur(8px);
              z-index: 99990;
              opacity: 0;
              pointer-events: auto;
              transition: opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            }}
            #kibo-backdrop.visible {{
              opacity: 1;
            }}

            /* Anillo de Foco / Spotlight pulsante */
            #kibo-spotlight-box {{
              position: fixed;
              border: 3px solid #00d2ff;
              border-radius: 18px;
              /* Sombra infinita que oscurece el exterior y deja el interior transparente */
              box-shadow: 0 0 0 9999px rgba(6, 11, 25, 0.82),
                          0 0 30px rgba(0, 210, 255, 0.85),
                          inset 0 0 15px rgba(0, 210, 255, 0.25);
              z-index: 99995;
              pointer-events: none;
              opacity: 0;
              transition: all 0.32s cubic-bezier(0.2, 0.8, 0.2, 1);
              animation: kiboSpotlightPulse 2.4s infinite ease-in-out;
            }}
            #kibo-spotlight-box.visible {{
              opacity: 1;
            }}

            @keyframes kiboSpotlightPulse {{
              0%, 100% {{
                border-color: #00d2ff;
                box-shadow: 0 0 0 9999px rgba(6, 11, 25, 0.82),
                            0 0 25px rgba(0, 210, 255, 0.75),
                            inset 0 0 10px rgba(0, 210, 255, 0.2);
              }}
              50% {{
                border-color: #7952f5;
                box-shadow: 0 0 0 9999px rgba(6, 11, 25, 0.84),
                            0 0 45px rgba(121, 82, 245, 0.95),
                            inset 0 0 20px rgba(121, 82, 245, 0.35);
              }}
            }}

            /* Globo flotante de Kibo */
            #kibo-guide-card {{
              position: fixed;
              display: flex;
              align-items: flex-start;
              gap: 14px;
              max-width: 400px;
              width: calc(100vw - 32px);
              background: linear-gradient(145deg, #0e1526, #162038);
              border: 2px solid rgba(0, 210, 255, 0.5);
              border-radius: 22px;
              padding: 16px 18px 15px;
              color: #f1f5f9;
              box-shadow: 0 20px 50px rgba(0, 0, 0, 0.65), 0 0 25px rgba(0, 210, 255, 0.25);
              z-index: 100000;
              opacity: 0;
              transform: translateY(12px) scale(0.96);
              transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
              font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            #kibo-guide-card.visible {{
              opacity: 1;
              transform: translateY(0) scale(1);
            }}

            .kibo-card-avatar {{
              width: 52px;
              height: 52px;
              border-radius: 16px;
              background: linear-gradient(135deg, #00d2ff, #7952f5);
              display: flex;
              align-items: center;
              justify-content: center;
              font-size: 28px;
              flex-shrink: 0;
              box-shadow: 0 6px 18px rgba(0, 210, 255, 0.45);
              animation: kiboAvatarBounce 2.5s infinite ease-in-out;
            }}
            @keyframes kiboAvatarBounce {{
              0%, 100% {{ transform: translateY(0) rotate(0deg); }}
              50% {{ transform: translateY(-4px) rotate(2deg); }}
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
              color: #00d2ff;
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
              background: linear-gradient(135deg, #00d2ff, #0284c7);
              color: #061021;
              box-shadow: 0 4px 14px rgba(0, 210, 255, 0.4);
            }}
            .kibo-btn-primary:hover {{
              background: #38bdf8;
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
              <div class="kibo-card-avatar">🤖</div>
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
          const storageKey = `kibo-step-tour-${{currentAppStep}}`;
          let stepIndex = Number(host.localStorage.getItem(storageKey) || 0);
          let isTourActive = host.localStorage.getItem('kibo-tour-disabled') !== 'true';

          function findTarget(selector) {{
            if (!selector) return null;
            return doc.querySelector(selector);
          }}

          function hideTour() {{
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

          function finishTour() {{
            isTourActive = false;
            host.localStorage.setItem('kibo-tour-disabled', 'true');
            hideTour();
          }}

          function updateTour() {{
            if (!isTourActive || stepIndex >= steps.length) {{
              finishTour();
              return;
            }}

            const current = steps[stepIndex];
            const target = findTarget(current.target);

            if (!target) {{
              return;
            }}

            const rect = target.getBoundingClientRect();
            if (rect.width === 0 || rect.height === 0) return;

            // Scroll si no está en vista
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
              const guideWidth = Math.min(400, host.innerWidth - 32);
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
              finishTour();
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

          // Click en backdrop para cerrar o avanzar
          backdrop.onclick = (e) => {{
            // No cerrar accidentalmente, pero permitir cerrar si toca fuera
          }};

          // Listener de burbuja flotante para reabrir el tour cuando se desee
          if (!host.__kiboBubbleListenerAttached) {{
            doc.addEventListener('click', (e) => {{
              const bubble = e.target.closest('.kibo-bubble') || e.target.closest('#kibo-help-trigger');
              if (bubble) {{
                isTourActive = true;
                stepIndex = 0;
                host.localStorage.removeItem('kibo-tour-disabled');
                host.localStorage.setItem(storageKey, 0);
                updateTour();
              }}
            }}, true);
            host.__kiboBubbleListenerAttached = true;
          }}

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


# Compatibilidad
render_nori_tour = render_kibo_tour
