import streamlit.components.v1 as components


def render_nori_tour():
    components.html(
        """
        <script>
        (() => {
          const host = window.parent;
          const doc = host.document;
          if (host.__noriTour) { host.__noriTour.refresh(); return; }

          const steps = [
            { target: '[data-testid="stNumberInput"]', title: 'Define el monto', text: 'Escribe el capital que quieres analizar. Es una simulación: aquí no se invierte dinero real.' },
            { target: '[data-testid="stRadio"]', title: 'Elige tu perfil', text: 'Toca Conservador, Moderado o Agresivo. Esta elección guiará las explicaciones de riesgo.' },
            { target: 'button[kind="primary"]', title: 'Avanza cuando estés listo', text: 'Pulsa Continuar. Voy contigo a la selección de acciones.', action: true },
            { target: '[data-testid="stMultiSelect"]', title: 'Selecciona tus acciones', text: 'Toca el campo, escribe un ticker y selecciónalo. Puedes retirar una acción con la x junto a su nombre.' },
            { target: 'button[kind="primary"]', title: 'Revisa tu lista', text: 'Cuando termines, pulsa Revisar selección. No necesitas completar diez activos para avanzar.', action: true },
            { target: '[data-testid="stDataFrame"]', title: 'Comprueba lo esencial', text: 'Aquí ves cada ticker y su sector. Esta será la base para validar diversificación y calidad de datos.' },
            { target: 'button[kind="primary"]', title: 'Confirma la decisión', text: 'Pulsa Ver mi resumen para dejar la configuración lista. Después siempre podrás modificarla.', action: true },
            { target: '[data-testid="stMetric"]', title: 'Consulta tu resumen', text: 'El resumen mantiene visibles el capital, perfil y número de activos. Los resultados cuantitativos aparecerán aquí en la siguiente fase.' },
            { target: '.nori-bubble', title: 'Aquí me encuentras', text: 'Me quedaré a tu lado. Pronto podrás preguntarme sobre los resultados; por ahora, al tocarme puedes repetir esta guía.' }
          ];

          const style = doc.createElement('style');
          style.textContent = `
            .nori-shade{background:rgba(12,18,30,.58);position:fixed;z-index:10000;pointer-events:auto;transition:all .25s ease}
            #nori-ring{border:2px solid #f3b44b;border-radius:12px;box-shadow:0 0 0 5px rgba(243,180,75,.25);pointer-events:none;position:fixed;transition:all .42s cubic-bezier(.2,.8,.2,1);z-index:10002}
            #nori-guide{align-items:flex-end;display:flex;gap:10px;max-width:370px;position:fixed;transition:all .45s cubic-bezier(.2,.8,.2,1);z-index:10003}
            #nori-robot{align-items:center;animation:noriFloat 1.8s ease-in-out infinite;background:#172033;border:3px solid #f3b44b;border-radius:20px 20px 16px 16px;box-shadow:0 10px 20px rgba(0,0,0,.25);color:white;display:flex;font-size:30px;height:58px;justify-content:center;min-width:58px}
            #nori-speech{background:#fffdf7;border-radius:18px 18px 18px 4px;box-shadow:0 14px 34px rgba(0,0,0,.24);color:#172033;font-family:system-ui,-apple-system,sans-serif;padding:14px 15px 12px}
            #nori-speech h3{font-size:15px;margin:0 24px 5px 0}.nori-copy{font-size:13px;line-height:1.45;margin:0}.nori-hint{color:#667085;font-size:11px;margin:9px 0 0}
            #nori-close{background:transparent;border:0;color:#667085;cursor:pointer;font-size:20px;position:absolute;right:8px;top:5px}.nori-controls{display:flex;gap:7px;justify-content:flex-end;margin-top:10px}.nori-controls button{background:#174a7e;border:0;border-radius:7px;color:white;cursor:pointer;font-size:12px;font-weight:700;padding:7px 10px}.nori-controls button.secondary{background:transparent;color:#174a7e}
            @keyframes noriFloat{0%,100%{transform:translateY(0) rotate(-2deg)}50%{transform:translateY(-7px) rotate(2deg)}}
            @media(max-width:640px){#nori-guide{max-width:calc(100vw - 28px)}#nori-robot{font-size:24px;height:47px;min-width:47px}#nori-speech{padding:12px}#nori-speech h3{font-size:14px}.nori-copy{font-size:12px}}
          `;
          doc.head.appendChild(style);

          const shade = ['top', 'left', 'right', 'bottom'].map(name => {
            const item = doc.createElement('div'); item.id = `nori-shade-${name}`; item.className = 'nori-shade'; doc.body.appendChild(item); return item;
          });
          const ring = doc.createElement('div'); ring.id = 'nori-ring'; doc.body.appendChild(ring);
          const guide = doc.createElement('div'); guide.id = 'nori-guide'; guide.innerHTML = `<div id="nori-robot">🤖</div><div id="nori-speech"><button id="nori-close" aria-label="Cerrar guía">×</button><h3></h3><p class="nori-copy"></p><p class="nori-hint"></p><div class="nori-controls"><button class="secondary" id="nori-back">Atrás</button><button id="nori-next">Siguiente</button></div></div>`; doc.body.appendChild(guide);
          const elements = { title: guide.querySelector('h3'), text: guide.querySelector('.nori-copy'), hint: guide.querySelector('.nori-hint'), back: guide.querySelector('#nori-back'), next: guide.querySelector('#nori-next') };
          let index = Number(host.localStorage.getItem('nori-tour-step') || 0);
          let visible = host.localStorage.getItem('nori-tour-complete') !== 'true';

          function targetFor(step) { return doc.querySelector(step.target); }
          function clear() { [...shade, ring, guide].forEach(item => item.style.display = 'none'); }
          function finish() { visible = false; host.localStorage.setItem('nori-tour-complete', 'true'); clear(); }
          function show() {
            if (!visible) return clear();
            const step = steps[index]; const target = targetFor(step);
            if (!target) { clear(); return; }
            const rect = target.getBoundingClientRect(); const pad = 8;
            const top = Math.max(0, rect.top - pad), left = Math.max(0, rect.left - pad), right = Math.min(host.innerWidth, rect.right + pad), bottom = Math.min(host.innerHeight, rect.bottom + pad);
            const assignments = [[0,0,host.innerWidth,top],[left,top,Math.max(0,host.innerWidth-right),bottom-top],[0,bottom,host.innerWidth,Math.max(0,host.innerHeight-bottom)],[0,top,left,bottom-top]];
            shade.forEach((item, position) => { const [x,y,w,h] = assignments[position]; Object.assign(item.style,{display:'block',left:x+'px',top:y+'px',width:w+'px',height:h+'px'}); });
            Object.assign(ring.style,{display:'block',left:left+'px',top:top+'px',width:(right-left)+'px',height:(bottom-top)+'px'});
            elements.title.textContent = step.title; elements.text.textContent = step.text; elements.hint.textContent = step.action ? 'Haz clic en el control destacado para continuar.' : `Paso ${index + 1} de ${steps.length}`;
            elements.back.style.visibility = index === 0 ? 'hidden' : 'visible'; elements.next.textContent = index === steps.length - 1 ? 'Terminar' : step.action ? 'Entendido' : 'Siguiente';
            const guideWidth = Math.min(370, host.innerWidth - 28); const guideTop = bottom + 16 + 142 < host.innerHeight ? bottom + 16 : Math.max(12, top - 150); const guideLeft = Math.max(14, Math.min(left, host.innerWidth - guideWidth - 14));
            Object.assign(guide.style,{display:'flex',left:guideLeft+'px',top:guideTop+'px'});
          }
          function next() { if (index >= steps.length - 1) return finish(); index += 1; host.localStorage.setItem('nori-tour-step', index); show(); }
          function previous() { index = Math.max(0,index - 1); host.localStorage.setItem('nori-tour-step', index); show(); }
          elements.next.onclick = next; elements.back.onclick = previous; guide.querySelector('#nori-close').onclick = finish;
          doc.addEventListener('click', event => {
            const step = steps[index]; const target = targetFor(step);
            if (visible && step?.action && target && target.contains(event.target)) { index = Math.min(index + 1, steps.length - 1); host.localStorage.setItem('nori-tour-step', index); }
            if (event.target.closest('.nori-bubble')) { visible = true; index = 0; host.localStorage.removeItem('nori-tour-complete'); host.localStorage.setItem('nori-tour-step', index); setTimeout(show, 50); }
          }, true);
          host.addEventListener('resize', show); host.setInterval(show, 700);
          host.__noriTour = { refresh: show }; show();
        })();
        </script>
        """,
        height=0,
    )
