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


def render_kibo_tour(current_step: int = 1):
    """
    Inyecta el motor de tutorial spotlight interactivo de Kibo con la imagen 3D de la mascota,
    efecto de difuminado (blur) y oscurecimiento en toda la pantalla,
    centrando la atención exclusivamente en el botón u opción que se está explicando.
    """
    kibo_img_b64 = get_kibo_image_base64()

    components.html(
        f"""
        <script>
        (() => {{
          const host = window.parent;
          const doc = host.document;
          const currentAppStep = {current_step};
          const kiboImg = "{kibo_img_b64}";

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
                hint: 'Paso 1 de 3 en esta pantalla'
              }},
              {{
                target: '[data-testid="stHorizontalBlock"]',
                title: '⚡ Montos Rápidos (Estilo Nequi / Nu)',
                text: 'Toca cualquiera de estos botones ($10K, $50K, $100K) para cambiar el monto con un solo toque y ver cómo reacciona tu estrategia.',
                hint: 'Paso 2 de 3 en esta pantalla'
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
                hint: 'Paso 1 de 2 en esta pantalla'
              }},
              {{
                target: 'button[kind="primary"]',
                title: '✨ Continuar a tus Acciones',
                text: 'Con tu perfil listo, pasaremos a seleccionar las empresas en las que invertirás.',
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
                text: 'Kibo analizó 3 años de historia real de cada acción con 3 teorías matemáticas (Browniano, Merton y Ornstein-Uhlenbeck) y te dice cuál modelo predice mejor su comportamiento sin engañarte.',
                hint: 'Paso 1 de 3 en esta pantalla'
              }},
              {{
                target: '[data-testid="stPlotlyChart"]',
                title: '📈 Abanico de Probabilidades',
                text: 'Este gráfico muestra las trayectorias futuras posibles del precio con percentiles de riesgo. Puedes tocarlo y hacer zoom.',
                hint: 'Paso 2 de 3 en esta pantalla'
              }},
              {{
                target: 'button[kind="primary"]',
                title: '💼 Ver Mi Portafolio Final',
                text: 'Pasemos a ver la receta exacta de cuántas acciones comprar de cada empresa.',
                hint: 'Toca el botón resaltado para avanzar',
                action: true
              }}
            ],
            5: [
              {{
                target: '.kpi-wallet-grid',
                title: '💼 Resumen de Billetera',
                text: 'Estilo Nu / Binance: ves tu capital asignado, el riesgo máximo estimado (VaR 99% a 10 días) y el efectivo de reserva por redondeo de acciones.',
                hint: 'Paso 1 de 3 en esta pantalla'
              }},
              {{
                target: '.stocks-plan-container',
                title: '🛒 Receta de Compra Exacta',
                text: 'Te indicamos el número entero exacto de acciones a comprar de cada empresa para minimizar tu riesgo matemático.',
                hint: 'Paso 2 de 3 en esta pantalla'
              }},
              {{
                target: '[data-testid="stDownloadButton"]',
                title: '📥 Descargar Reporte',
                text: 'Descarga tu portafolio en Excel / CSV para entregarlo, guardarlo o compartirlo.',
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
              background: rgba(5, 8, 15, 0.82);
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
          const splashSeen = host.sessionStorage.getItem('kibo-splash-seen');

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
              <div class="splash-brand-sub">Tu Copiloto Inteligente de Finanzas & Riesgo</div>
              <div class="splash-bar-track">
                <div class="splash-bar-fill"></div>
              </div>
            `;
            doc.body.appendChild(splash);

            // Permitir saltar al hacer clic
            splash.onclick = () => {{
              splash.classList.add('fade-out');
              host.sessionStorage.setItem('kibo-splash-seen', 'true');
              setTimeout(() => splash.remove(), 550);
            }};

            // Desvanecer automáticamente tras la animación
            host.setTimeout(() => {{
              splash.classList.add('fade-out');
              host.sessionStorage.setItem('kibo-splash-seen', 'true');
              host.setTimeout(() => {{
                if (splash && splash.parentNode) splash.remove();
              }}, 600);
            }}, 1800);
          }}
        }})();
        </script>
        """,
        height=0,
    )


# Compatibilidad
render_nori_tour = render_kibo_tour
