/* ── WVCAC Accessibility Widget ───────────────────────────────────────────── */
(function () {
  'use strict';

  const STORAGE_KEY = 'wvcac_a11y';
  const defaults = {
    contrast:       false,
    highlightLinks: false,
    biggerText:     false,
    textSpacing:    false,
    pauseAnim:      false,
    hideImages:     false,
    dyslexia:       false,
    bigCursor:      false,
    lineHeight:     false,
    textAlign:      false,
    saturation:     false,
    oversized:      false,
  };

  let state = Object.assign({}, defaults);
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
    if (saved) state = Object.assign({}, defaults, saved);
  } catch (_) {}

  function apply() {
    const html = document.documentElement;
    Object.keys(defaults).forEach(k => html.classList.toggle('a11y-' + k, !!state[k]));

    document.querySelectorAll('[data-a11y]').forEach(btn => {
      const k = btn.dataset.a11y;
      btn.setAttribute('aria-pressed', String(!!state[k]));
      btn.classList.toggle('a11y-btn--on', !!state[k]);
    });

    const panel = document.getElementById('a11y-panel');
    if (panel) panel.classList.toggle('a11y-panel--wide', !!state.oversized);
    const ovToggle = document.getElementById('a11y-oversized-toggle');
    if (ovToggle) {
      ovToggle.setAttribute('aria-pressed', String(!!state.oversized));
      ovToggle.classList.toggle('a11y-toggle--on', !!state.oversized);
    }

    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }

  function buildWidget() {

    // ── CSS ──────────────────────────────────────────────────────────────────
    const style = document.createElement('style');
    style.textContent = `
      #a11y-widget {
        position: fixed; bottom: 1.5rem; right: 1.5rem; z-index: 9900;
        font-family: 'Segoe UI', system-ui, sans-serif;
      }
      #a11y-trigger {
        width: 54px; height: 54px; border-radius: 50%;
        background: #9b1c1c; color: #fff; border: 3px solid #fff;
        box-shadow: 0 4px 16px rgba(0,0,0,.4);
        cursor: pointer; display: flex; align-items: center; justify-content: center;
        transition: background .2s, transform .2s;
      }
      #a11y-trigger:hover { background: #7f1d1d; transform: scale(1.08); }
      #a11y-trigger:focus-visible { outline: 3px solid #f59e0b; outline-offset: 3px; }

      #a11y-panel {
        position: absolute; bottom: 64px; right: 0;
        width: 340px; background: #fff;
        border-radius: 14px;
        box-shadow: 0 12px 40px rgba(0,0,0,.28);
        overflow: hidden; border: 1px solid #e5e7eb;
      }
      #a11y-panel.a11y-panel--wide { width: 430px; }

      .a11y-header {
        background: #9b1c1c; color: #fff;
        display: flex; align-items: center; justify-content: space-between;
        padding: .75rem 1rem; font-size: 1rem; font-weight: 700;
      }
      .a11y-header-title { display: flex; align-items: center; gap: .5rem; }
      #a11y-close {
        background: rgba(255,255,255,.18); border: none; color: #fff;
        width: 34px; height: 34px; border-radius: 50%; font-size: 1.1rem;
        cursor: pointer; display: flex; align-items: center; justify-content: center;
        transition: background .15s;
      }
      #a11y-close:hover { background: rgba(255,255,255,.35); }
      #a11y-close:focus-visible { outline: 3px solid #f59e0b; }

      .a11y-oversized-row {
        display: flex; align-items: center; justify-content: space-between;
        padding: .7rem 1rem; border-bottom: 1px solid #e5e7eb;
        font-size: 1rem; color: #374151; font-weight: 500;
      }
      .a11y-toggle {
        width: 46px; height: 28px; border-radius: 999px;
        background: #d1d5db; border: none; cursor: pointer;
        position: relative; transition: background .2s; flex-shrink: 0;
      }
      .a11y-toggle::after {
        content: ''; position: absolute; top: 4px; left: 4px;
        width: 20px; height: 20px; border-radius: 50%;
        background: #fff; transition: transform .2s;
        box-shadow: 0 1px 4px rgba(0,0,0,.25);
      }
      .a11y-toggle--on { background: #9b1c1c; }
      .a11y-toggle--on::after { transform: translateX(18px); }

      .a11y-grid {
        display: grid; grid-template-columns: 1fr 1fr;
        gap: .6rem; padding: .75rem;
      }
      .a11y-btn {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        gap: .45rem; padding: .9rem .5rem;
        background: #f9fafb; border: 1.5px solid #e5e7eb; border-radius: 10px;
        cursor: pointer; font-size: .9rem; font-weight: 600; color: #374151;
        min-height: 85px; transition: background .15s, border-color .15s, color .15s;
        font-family: inherit; text-align: center; line-height: 1.2;
      }
      .a11y-btn:hover  { background: #f3f4f6; border-color: #9b1c1c; color: #9b1c1c; }
      .a11y-btn:focus-visible { outline: 3px solid #f59e0b; outline-offset: 2px; }
      .a11y-btn--on   { background: #fef2f2; border-color: #9b1c1c; color: #9b1c1c; }

      .a11y-reset-row { padding: .4rem .75rem .75rem; }
      #a11y-reset {
        width: 100%; min-height: 48px;
        background: #9b1c1c; color: #fff; border: none; border-radius: 8px;
        cursor: pointer; font-size: 1rem; font-weight: 700;
        display: flex; align-items: center; justify-content: center; gap: .5rem;
        font-family: inherit; transition: background .2s;
      }
      #a11y-reset:hover { background: #7f1d1d; }
      #a11y-reset:focus-visible { outline: 3px solid #f59e0b; }

      .a11y-move-row {
        padding: .55rem 1rem .7rem; font-size: .95rem; color: #6b7280;
        display: flex; align-items: center; gap: .4rem;
        border-top: 1px solid #e5e7eb; cursor: pointer; user-select: none;
      }
      .a11y-move-row:hover { color: #111; }
      .a11y-move-row:focus-visible { outline: 3px solid #f59e0b; }

      /* ── Modes ── */
      .a11y-contrast      { filter: contrast(160%) brightness(1.05) !important; }
      .a11y-saturation    { filter: saturate(0) !important; }
      .a11y-contrast.a11y-saturation { filter: saturate(0) contrast(160%) !important; }
      .a11y-highlightLinks a { background: #ffff00 !important; color: #000 !important; text-decoration: underline !important; padding: 0 2px !important; border-radius: 2px; }
      .a11y-biggerText    { font-size: 120% !important; }
      .a11y-textSpacing * { letter-spacing: .1em !important; word-spacing: .15em !important; }
      .a11y-pauseAnim *, .a11y-pauseAnim *::before, .a11y-pauseAnim *::after { animation-duration:.001ms !important; transition-duration:.001ms !important; }
      .a11y-hideImages img, .a11y-hideImages video { visibility: hidden !important; }
      .a11y-dyslexia, .a11y-dyslexia * { font-family: Arial, Helvetica, sans-serif !important; letter-spacing: .05em !important; word-spacing: .12em !important; }
      .a11y-bigCursor, .a11y-bigCursor * { cursor: zoom-in !important; }
      .a11y-lineHeight *  { line-height: 2.2 !important; }
      .a11y-textAlign p, .a11y-textAlign li, .a11y-textAlign td, .a11y-textAlign h1, .a11y-textAlign h2, .a11y-textAlign h3 { text-align: left !important; }
    `;
    document.head.appendChild(style);

    // ── HTML ─────────────────────────────────────────────────────────────────
    const wrap = document.createElement('div');
    wrap.id = 'a11y-widget';
    wrap.setAttribute('role', 'region');
    wrap.setAttribute('aria-label', 'Accessibility options');

    const items = [
      { key: 'contrast',       label: 'Contrast +',        icon: `<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 0 1 0 20Z" fill="currentColor" stroke="none"/></svg>` },
      { key: 'highlightLinks', label: 'Highlight Links',   icon: `<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>` },
      { key: 'biggerText',     label: 'Bigger Text',       icon: `<svg width="30" height="30" viewBox="0 0 24 24" fill="none" aria-hidden="true"><text x="1" y="19" font-size="15" font-weight="bold" fill="currentColor">TT</text></svg>` },
      { key: 'textSpacing',    label: 'Text Spacing',      icon: `<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M3 12h18M8 7l-5 5 5 5M16 7l5 5-5 5"/></svg>` },
      { key: 'pauseAnim',      label: 'Pause Animations',  icon: `<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="10" y1="15" x2="10" y2="9"/><line x1="14" y1="15" x2="14" y2="9"/></svg>` },
      { key: 'hideImages',     label: 'Hide Images',       icon: `<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/><line x1="2" y1="2" x2="22" y2="22"/></svg>` },
      { key: 'dyslexia',       label: 'Dyslexia Friendly', icon: `<svg width="30" height="30" viewBox="0 0 24 24" fill="none" aria-hidden="true"><text x="1" y="19" font-size="14" font-weight="bold" fill="currentColor">Df</text></svg>` },
      { key: 'bigCursor',      label: 'Cursor',            icon: `<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 3l14 9-7 1-4 7z"/></svg>` },
      { key: 'lineHeight',     label: 'Line Height',       icon: `<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><line x1="9" y1="6" x2="21" y2="6"/><line x1="9" y1="12" x2="21" y2="12"/><line x1="9" y1="18" x2="21" y2="18"/><polyline points="3 8 3 4 3 4"/><path d="M3 4v16M1.5 18l1.5 2 1.5-2M1.5 6 3 4l1.5 2"/></svg>` },
      { key: 'textAlign',      label: 'Text Align',        icon: `<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="15" y2="12"/><line x1="3" y1="18" x2="18" y2="18"/></svg>` },
      { key: 'saturation',     label: 'Saturation',        icon: `<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M12 2v20M2 12h20" opacity=".25"/><circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 1 0 18Z" fill="currentColor" stroke="none"/></svg>` },
    ];

    const gridHTML = items.map(i => `
      <button class="a11y-btn" data-a11y="${i.key}" aria-pressed="false" aria-label="${i.label}">
        ${i.icon}
        ${i.label}
      </button>`).join('');

    wrap.innerHTML = `
      <button id="a11y-trigger" aria-expanded="false" aria-controls="a11y-panel"
              aria-label="Open accessibility menu (Ctrl+U)" title="Accessibility Menu (Ctrl+U)">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <circle cx="12" cy="4.5" r="1.8"/>
          <path d="M15.5 8.5H8.5l-2 3.5h3l-1.5 7 2.5-1.5L12 14l1.5 3.5 2.5 1.5-1.5-7h3z"/>
        </svg>
      </button>

      <div id="a11y-panel" role="dialog" aria-label="Accessibility Menu" hidden>
        <div class="a11y-header">
          <span class="a11y-header-title">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><circle cx="12" cy="4.5" r="1.8"/><path d="M15.5 8.5H8.5l-2 3.5h3l-1.5 7 2.5-1.5L12 14l1.5 3.5 2.5 1.5-1.5-7h3z"/></svg>
            Accessibility Menu (CTRL+U)
          </span>
          <button id="a11y-close" aria-label="Close accessibility menu">✕</button>
        </div>

        <div class="a11y-oversized-row">
          <span>Oversized Widget</span>
          <button class="a11y-toggle" id="a11y-oversized-toggle"
                  aria-pressed="false" aria-label="Toggle oversized widget"></button>
        </div>

        <div class="a11y-grid">${gridHTML}</div>

        <div class="a11y-reset-row">
          <button id="a11y-reset" aria-label="Reset all accessibility settings">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
            Reset All Accessibility Settings
          </button>
        </div>

        <div class="a11y-move-row" id="a11y-move" role="button" tabindex="0" aria-label="Move widget to next corner">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/></svg>
          Move/Hide Widget ›
        </div>
      </div>`;

    document.body.appendChild(wrap);

    // ── Wire events ──────────────────────────────────────────────────────────
    const trigger  = document.getElementById('a11y-trigger');
    const panel    = document.getElementById('a11y-panel');
    const closeBtn = document.getElementById('a11y-close');
    const resetBtn = document.getElementById('a11y-reset');
    const ovToggle = document.getElementById('a11y-oversized-toggle');
    const moveBtn  = document.getElementById('a11y-move');

    const openPanel  = () => { panel.hidden = false; trigger.setAttribute('aria-expanded','true');  closeBtn.focus(); };
    const closePanel = () => { panel.hidden = true;  trigger.setAttribute('aria-expanded','false'); trigger.focus(); };

    trigger.addEventListener('click', () => panel.hidden ? openPanel() : closePanel());
    closeBtn.addEventListener('click', closePanel);

    document.addEventListener('keydown', e => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'u') { e.preventDefault(); panel.hidden ? openPanel() : closePanel(); }
      if (e.key === 'Escape' && !panel.hidden) closePanel();
    });

    document.querySelectorAll('[data-a11y]').forEach(btn => {
      btn.addEventListener('click', () => { state[btn.dataset.a11y] = !state[btn.dataset.a11y]; apply(); });
    });

    ovToggle.addEventListener('click', () => { state.oversized = !state.oversized; apply(); });

    resetBtn.addEventListener('click', () => { state = Object.assign({}, defaults); apply(); });

    // Move widget around corners
    const corners = [
      { bottom:'1.5rem', right:'1.5rem', top:'auto', left:'auto' },
      { bottom:'1.5rem', right:'auto',  top:'auto', left:'1.5rem' },
      { bottom:'auto',   right:'1.5rem', top:'1.5rem', left:'auto' },
      { bottom:'auto',   right:'auto',  top:'1.5rem', left:'1.5rem' },
    ];
    let cornerIdx = 0;
    moveBtn.addEventListener('click', () => {
      cornerIdx = (cornerIdx + 1) % corners.length;
      const c = corners[cornerIdx];
      const w = document.getElementById('a11y-widget');
      w.style.bottom = c.bottom; w.style.right  = c.right;
      w.style.top    = c.top;    w.style.left   = c.left;
      panel.style.bottom = c.bottom !== 'auto' ? '64px' : 'auto';
      panel.style.top    = c.top    !== 'auto' ? '64px' : 'auto';
    });
    moveBtn.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); moveBtn.click(); } });

    apply();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', buildWidget);
  } else {
    buildWidget();
  }
})();
