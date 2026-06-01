/* ── WVCAC Accessibility Widget ───────────────────────────────────────────── */
(function () {
  'use strict';

  const STORAGE_KEY = 'wvcac_a11y';
  const defaults = {
    fontSize:    0,       // steps: -2 to +4
    contrast:    false,
    grayscale:   false,
    underline:   false,
    dyslexia:    false,
    pauseAnim:   false,
  };

  let state = Object.assign({}, defaults);

  /* ── Restore saved state ── */
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
    if (saved) state = Object.assign({}, defaults, saved);
  } catch (_) {}

  /* ── Apply state to <html> ── */
  function apply() {
    const root = document.documentElement;

    // Font size
    root.style.fontSize = state.fontSize === 0 ? '' : (100 + state.fontSize * 10) + '%';

    // Toggles via class
    root.classList.toggle('a11y-contrast',   state.contrast);
    root.classList.toggle('a11y-grayscale',  state.grayscale);
    root.classList.toggle('a11y-underline',  state.underline);
    root.classList.toggle('a11y-dyslexia',   state.dyslexia);
    root.classList.toggle('a11y-pauseAnim',  state.pauseAnim);

    // Sync button states
    document.querySelectorAll('[data-a11y]').forEach(btn => {
      const key = btn.dataset.a11y;
      if (typeof state[key] === 'boolean') {
        btn.setAttribute('aria-pressed', state[key]);
        btn.classList.toggle('a11y-btn--on', state[key]);
      }
    });

    // Font size counter
    const counter = document.getElementById('a11y-size-val');
    if (counter) counter.textContent = (state.fontSize >= 0 ? '+' : '') + state.fontSize;

    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }

  /* ── Build the widget HTML ── */
  function buildWidget() {
    const widget = document.createElement('div');
    widget.id = 'a11y-widget';
    widget.setAttribute('role', 'region');
    widget.setAttribute('aria-label', 'Accessibility options');
    widget.innerHTML = `
      <button id="a11y-trigger" aria-expanded="false" aria-controls="a11y-panel"
              aria-label="Open accessibility menu" title="Accessibility">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor"
             stroke-width="2" aria-hidden="true">
          <circle cx="12" cy="4" r="1.5"/>
          <path d="M12 7v5l3 3M9 10l-3 1M15 10l3 1M12 12v5"/>
          <circle cx="12" cy="12" r="10" stroke-width="1.5"/>
        </svg>
      </button>

      <div id="a11y-panel" role="dialog" aria-label="Accessibility settings" hidden>
        <div class="a11y-header">
          <span>Accessibility</span>
          <button id="a11y-close" aria-label="Close accessibility menu">✕</button>
        </div>

        <div class="a11y-section-label">Text Size</div>
        <div class="a11y-row">
          <button class="a11y-btn" id="a11y-dec" aria-label="Decrease text size">A−</button>
          <span id="a11y-size-val" aria-live="polite" aria-atomic="true">+0</span>
          <button class="a11y-btn" id="a11y-inc" aria-label="Increase text size">A+</button>
        </div>

        <div class="a11y-section-label">Display</div>
        <button class="a11y-btn a11y-btn--full" data-a11y="contrast"  aria-pressed="false">⬛ High Contrast</button>
        <button class="a11y-btn a11y-btn--full" data-a11y="grayscale" aria-pressed="false">◑ Grayscale</button>
        <button class="a11y-btn a11y-btn--full" data-a11y="underline" aria-pressed="false">U̲ Underline Links</button>
        <button class="a11y-btn a11y-btn--full" data-a11y="dyslexia"  aria-pressed="false">Aa Readable Font</button>
        <button class="a11y-btn a11y-btn--full" data-a11y="pauseAnim" aria-pressed="false">⏸ Pause Animations</button>

        <button id="a11y-reset" class="a11y-btn a11y-btn--full a11y-btn--reset">↺ Reset All</button>
      </div>`;
    document.body.appendChild(widget);

    /* ── Trigger ── */
    const trigger = document.getElementById('a11y-trigger');
    const panel   = document.getElementById('a11y-panel');
    const close   = document.getElementById('a11y-close');

    function openPanel() {
      panel.hidden = false;
      trigger.setAttribute('aria-expanded', 'true');
      close.focus();
    }
    function closePanel() {
      panel.hidden = true;
      trigger.setAttribute('aria-expanded', 'false');
      trigger.focus();
    }

    trigger.addEventListener('click', () => panel.hidden ? openPanel() : closePanel());
    close.addEventListener('click', closePanel);
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && !panel.hidden) closePanel();
    });

    /* ── Font size ── */
    document.getElementById('a11y-inc').addEventListener('click', () => {
      if (state.fontSize < 4) { state.fontSize++; apply(); }
    });
    document.getElementById('a11y-dec').addEventListener('click', () => {
      if (state.fontSize > -2) { state.fontSize--; apply(); }
    });

    /* ── Toggle buttons ── */
    document.querySelectorAll('[data-a11y]').forEach(btn => {
      btn.addEventListener('click', () => {
        const key = btn.dataset.a11y;
        state[key] = !state[key];
        apply();
      });
    });

    /* ── Reset ── */
    document.getElementById('a11y-reset').addEventListener('click', () => {
      state = Object.assign({}, defaults);
      apply();
    });

    apply(); // initial render
  }

  /* ── CSS ── */
  const css = `
    /* Accessibility widget */
    #a11y-widget { position: fixed; bottom: 1.5rem; right: 1.5rem; z-index: 9000; font-family: 'Segoe UI', system-ui, sans-serif; }

    #a11y-trigger {
      width: 54px; height: 54px; border-radius: 50%;
      background: #1a4f8a; color: #fff; border: 3px solid #fff;
      box-shadow: 0 4px 16px rgba(0,0,0,.35);
      cursor: pointer; display: flex; align-items: center; justify-content: center;
      transition: background .2s, transform .2s;
    }
    #a11y-trigger:hover, #a11y-trigger:focus-visible { background: #133a66; transform: scale(1.08); }
    #a11y-trigger:focus-visible { outline: 3px solid #f59e0b; outline-offset: 3px; }

    #a11y-panel {
      position: absolute; bottom: 64px; right: 0;
      width: 240px; background: #fff;
      border: 2px solid #1a4f8a; border-radius: 12px;
      box-shadow: 0 8px 32px rgba(0,0,0,.2);
      padding: 0; overflow: hidden;
    }

    .a11y-header {
      background: #1a4f8a; color: #fff;
      display: flex; justify-content: space-between; align-items: center;
      padding: .7rem 1rem; font-size: 1rem; font-weight: 700;
    }
    #a11y-close {
      background: none; border: none; color: #fff;
      font-size: 1.1rem; cursor: pointer; line-height: 1;
      width: 32px; height: 32px; border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
    }
    #a11y-close:hover { background: rgba(255,255,255,.2); }
    #a11y-close:focus-visible { outline: 3px solid #f59e0b; }

    .a11y-section-label {
      font-size: .75rem; font-weight: 700; text-transform: uppercase;
      letter-spacing: .08em; color: #6b7280;
      padding: .6rem 1rem .2rem;
    }

    .a11y-row {
      display: flex; align-items: center; justify-content: center;
      gap: .75rem; padding: .4rem 1rem .6rem;
    }
    #a11y-size-val {
      font-size: 1rem; font-weight: 700; color: #1a4f8a;
      min-width: 32px; text-align: center;
    }

    .a11y-btn {
      background: #f3f4f6; border: 2px solid #d1d5db;
      border-radius: 6px; color: #1a1a2e;
      font-size: 1rem; font-weight: 600;
      cursor: pointer; padding: .45rem .9rem;
      min-height: 44px; min-width: 44px;
      transition: background .15s, border-color .15s;
      font-family: inherit;
    }
    .a11y-btn:hover { background: #e8f0fb; border-color: #1a4f8a; }
    .a11y-btn:focus-visible { outline: 3px solid #f59e0b; outline-offset: 2px; }
    .a11y-btn--full {
      display: block; width: calc(100% - 2rem);
      margin: .3rem 1rem 0; text-align: left;
    }
    .a11y-btn--on { background: #1a4f8a; color: #fff; border-color: #1a4f8a; }
    .a11y-btn--on:hover { background: #133a66; }
    .a11y-btn--reset {
      margin-top: .6rem; margin-bottom: .75rem;
      background: #fef2f2; border-color: #fca5a5; color: #b91c1c;
    }
    .a11y-btn--reset:hover { background: #fee2e2; }

    /* ── Accessibility modes ── */
    .a11y-contrast { filter: contrast(150%) brightness(1.1); }
    .a11y-grayscale { filter: grayscale(100%); }
    .a11y-contrast.a11y-grayscale { filter: grayscale(100%) contrast(150%); }
    .a11y-underline a { text-decoration: underline !important; }
    .a11y-dyslexia, .a11y-dyslexia * { font-family: Arial, Helvetica, sans-serif !important; letter-spacing: .05em !important; word-spacing: .1em !important; line-height: 1.8 !important; }
    .a11y-pauseAnim *, .a11y-pauseAnim *::before, .a11y-pauseAnim *::after { animation-duration: 0.001ms !important; transition-duration: 0.001ms !important; }
  `;

  const style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', buildWidget);
  } else {
    buildWidget();
  }
})();
