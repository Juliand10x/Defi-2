import streamlit.components.v1 as components


def render_kibo_tour():
    components.html(
        """
        <script>
        (() => {
          const host = window.parent;
          const doc = host.document;

          // Limpiar instancias previas para evitar duplicados
          if (host.__kiboTimer) { host.clearInterval(host.__kiboTimer); }
          if (host.__kiboFastTimer) { host.clearInterval(host.__kiboFastTimer); }

          const steps = [
            { target: '[data-testid="stNumberInput"]', title: '🚀 ¡Hola, soy Kibo!', text: 'Escribe aquí cuánto capital simulado quieres analizar. Es 100% un simulador seguro: ¡cero dinero real en juego!' },
            { target: '[data-testid="stRadio"]', title: '🛡️ ¿Cómo duermes mejor?', text: 'Elige tu perfil: Conservador (modo escudo), Moderado (equilibrio) o Agresivo (impulso). Adaptaremos las matemáticas a ti.' },
            { target: 'button[kind="primary"]', title: '✨ Siguiente paso', text: 'Toca Continuar. Te acompaño a elegir los activos de tu portafolio.', action: true },
            { target: '[data-testid="stMultiSelect"]', title: '🧺 No pongas los huevos en la misma canasta', text: 'Elige tus acciones favoritas. Te recomendamos combinar varios sectores (tecnología, salud, energía) para mayor seguridad.' },
            { target: 'button[kind="primary"]', title: '🎯 Revisa tu tripulación', text: 'Cuando tengas tus acciones listas, presiona Revisar selección.', action: true },
            { target: '[data-testid="stDataFrame"]', title: '📊 Tus activos elegidos', text: 'Aquí ves cada empresa y su sector. Kibo auditará 3 años de datos reales para ti.' },
            { target: 'button[kind="primary"]', title: '🚀 Confirmación final', text: 'Presiona Ver mi resumen para activar tu estrategia.', action: true },
            { target: '[data-testid="stMetric"]', title: '🌟 Tu resumen inteligente', text: '¡Excelente! Aquí ves tus métricas clave. Kibo calculará las probabilidades exactas para proteger tu inversión.' },
            { target: '.kibo-bubble, .nori-bubble', title: '🤖 Siempre a tu lado', text: 'Estaré flotando aquí abajo. Tócame en cualquier momento si quieres que te recuerde cómo funciona cada paso.' }
          ];

          let style = doc.getElementById('kibo-tour-styles');
          if (!style) {
            style = doc.createElement('style');
            style.id = 'kibo-tour-styles';
            style.textContent = `
              .kibo-shade{background:rgba(8,15,30,.55);position:fixed;z-index:10000;pointer-events:auto;transition:all .18s ease}
              #kibo-ring{border:2.5px solid #38bdf8;border-radius:14px;box-shadow:0 0 0 5px rgba(56,189,248,.35), 0 0 25px rgba(56,189,248,.4);pointer-events:none;position:fixed;transition:all .25s cubic-bezier(.2,.8,.2,1);z-index:10002}
              #kibo-guide{align-items:flex-end;display:flex;gap:12px;max-width:380px;position:fixed;transition:all .25s cubic-bezier(.2,.8,.2,1);z-index:10003;animation:kiboPop .22s ease-out}
              #kibo-robot{align-items:center;animation:kiboFloat 2s ease-in-out infinite;background:linear-gradient(135deg,#0f172a,#1e293b);border:2.5px solid #38bdf8;border-radius:24px;box-shadow:0 12px 28px rgba(0,0,0,.45),0 0 20px rgba(56,189,248,.4);color:white;display:flex;font-size:32px;height:62px;justify-content:center;min-width:62px}
              #kibo-speech{background:#ffffff;border:1.5px solid #e0f2fe;border-radius:20px 20px 20px 6px;box-shadow:0 16px 40px rgba(15,23,42,.32);color:#0f172a;font-family:system-ui,-apple-system,sans-serif;padding:15px 18px 14px}
              #kibo-speech h3{font-size:15.5px;font-weight:800;color:#0f172a;margin:0 24px 6px 0;letter-spacing:-0.01em}
              .kibo-copy{font-size:13.2px;line-height:1.5;color:#334155;margin:0}
              .kibo-hint{color:#0284c7;font-size:11.5px;font-weight:700;margin:10px 0 0}
              #kibo-close{background:transparent;border:0;color:#94a3b8;cursor:pointer;font-size:22px;line-height:1;position:absolute;right:12px;top:10px;padding:2px}
              #kibo-close:hover{color:#0f172a}
              .kibo-controls{display:flex;gap:8px;justify-content:flex-end;margin-top:12px}
              .kibo-controls button{background:linear-gradient(135deg,#0284c7,#2563eb);border:0;border-radius:9px;color:white;cursor:pointer;font-size:12.5px;font-weight:750;padding:7px 14px;box-shadow:0 4px 12px rgba(2,132,199,.35);transition:all .15s}
              .kibo-controls button:hover{background:#0369a1;transform:translateY(-1px)}
              .kibo-controls button.secondary{background:#f1f5f9;color:#0f172a;border:1px solid #cbd5e1;box-shadow:none}
              .kibo-controls button.secondary:hover{background:#e2e8f0}
              @keyframes kiboFloat{0%,100%{transform:translateY(0) rotate(-2deg)}50%{transform:translateY(-7px) rotate(2deg)}}
              @keyframes kiboPop{0%{opacity:0;transform:scale(0.92)}100%{opacity:1;transform:scale(1)}}
              @media(max-width:640px){#kibo-guide{max-width:calc(100vw - 28px)}#kibo-robot{font-size:26px;height:50px;min-width:50px}#kibo-speech{padding:12px}}
            `;
            doc.head.appendChild(style);
          }

          let shade = ['top', 'left', 'right', 'bottom'].map(name => {
            let item = doc.getElementById(`kibo-shade-${name}`);
            if (!item) {
              item = doc.createElement('div');
              item.id = `kibo-shade-${name}`;
              item.className = 'kibo-shade';
              doc.body.appendChild(item);
            }
            return item;
          });

          let ring = doc.getElementById('kibo-ring');
          if (!ring) {
            ring = doc.createElement('div');
            ring.id = 'kibo-ring';
            doc.body.appendChild(ring);
          }

          let guide = doc.getElementById('kibo-guide');
          if (!guide) {
            guide = doc.createElement('div');
            guide.id = 'kibo-guide';
            guide.innerHTML = `<div id="kibo-robot">🤖</div><div id="kibo-speech"><button id="kibo-close" aria-label="Cerrar guía">×</button><h3></h3><p class="kibo-copy"></p><p class="kibo-hint"></p><div class="kibo-controls"><button class="secondary" id="kibo-back">Atrás</button><button id="kibo-next">Siguiente</button></div></div>`;
            doc.body.appendChild(guide);
          }

          const elements = {
            title: guide.querySelector('h3'),
            text: guide.querySelector('.kibo-copy'),
            hint: guide.querySelector('.kibo-hint'),
            back: guide.querySelector('#kibo-back'),
            next: guide.querySelector('#kibo-next')
          };

          let index = Number(host.localStorage.getItem('kibo-tour-step') || 0);
          let visible = host.localStorage.getItem('kibo-tour-complete') !== 'true';

          function targetFor(step) { return doc.querySelector(step.target); }
          function clear() { [...shade, ring, guide].forEach(item => item.style.display = 'none'); }
          function finish() { visible = false; host.localStorage.setItem('kibo-tour-complete', 'true'); clear(); }

          function show() {
            if (!visible) { clear(); return; }
            const step = steps[index];
            const target = targetFor(step);
            if (!target) { return; }

            const rect = target.getBoundingClientRect();
            if (rect.width === 0 && rect.height === 0) return;

            const pad = 8;
            const top = Math.max(0, rect.top - pad);
            const left = Math.max(0, rect.left - pad);
            const right = Math.min(host.innerWidth, rect.right + pad);
            const bottom = Math.min(host.innerHeight, rect.bottom + pad);

            const assignments = [
              [0, 0, host.innerWidth, top],
              [left, top, Math.max(0, host.innerWidth - right), bottom - top],
              [0, bottom, host.innerWidth, Math.max(0, host.innerHeight - bottom)],
              [0, top, left, bottom - top]
            ];

            shade.forEach((item, pos) => {
              const [x, y, w, h] = assignments[pos];
              Object.assign(item.style, { display: 'block', left: x + 'px', top: y + 'px', width: w + 'px', height: h + 'px' });
            });

            Object.assign(ring.style, { display: 'block', left: left + 'px', top: top + 'px', width: (right - left) + 'px', height: (bottom - top) + 'px' });

            elements.title.textContent = step.title;
            elements.text.textContent = step.text;
            elements.hint.textContent = step.action ? 'Toca el botón resaltado para continuar.' : `Paso ${index + 1} de ${steps.length}`;
            elements.back.style.visibility = index === 0 ? 'hidden' : 'visible';
            elements.next.textContent = index === steps.length - 1 ? '¡Empezar a Invertir!' : step.action ? 'Entendido' : 'Siguiente';

            const guideWidth = Math.min(380, host.innerWidth - 28);
            const guideTop = bottom + 16 + 142 < host.innerHeight ? bottom + 16 : Math.max(12, top - 150);
            const guideLeft = Math.max(14, Math.min(left, host.innerWidth - guideWidth - 14));
            Object.assign(guide.style, { display: 'flex', left: guideLeft + 'px', top: guideTop + 'px' });
          }

          function next() {
            if (index >= steps.length - 1) return finish();
            index += 1;
            host.localStorage.setItem('kibo-tour-step', index);
            show();
          }

          function previous() {
            index = Math.max(0, index - 1);
            host.localStorage.setItem('kibo-tour-step', index);
            show();
          }

          elements.next.onclick = next;
          elements.back.onclick = previous;
          guide.querySelector('#kibo-close').onclick = finish;

          if (!host.__kiboEventsAttached) {
            doc.addEventListener('click', event => {
              const step = steps[index];
              const target = targetFor(step);
              if (visible && step?.action && target && target.contains(event.target)) {
                index = Math.min(index + 1, steps.length - 1);
                host.localStorage.setItem('kibo-tour-step', index);
                setTimeout(show, 30);
              }
              if (event.target.closest('.kibo-bubble') || event.target.closest('.nori-bubble')) {
                visible = true;
                index = 0;
                host.localStorage.removeItem('kibo-tour-complete');
                host.localStorage.setItem('kibo-tour-step', index);
                show();
              }
            }, true);
            host.addEventListener('resize', show);
            host.__kiboEventsAttached = true;
          }

          let fastAttempts = 0;
          host.__kiboFastTimer = host.setInterval(() => {
            fastAttempts++;
            show();
            if (fastAttempts > 45 || targetFor(steps[index])) {
              host.clearInterval(host.__kiboFastTimer);
            }
          }, 35);

          host.__kiboTimer = host.setInterval(show, 400);
          show();
        })();
        </script>
        """,
        height=0,
    )


# Alias para retrocompatibilidad
render_nori_tour = render_kibo_tour
