// hud.js — injected into the rendered artifact during iteration.
// Reads from window.__composer_state for user commands.

(function () {
  const HUD_ID = '__composer_hud';
  if (document.getElementById(HUD_ID)) return; // already injected

  window.__composer_state = window.__composer_state || {
    command: null,
    guidance: ''
  };

  const hud = document.createElement('div');
  hud.id = HUD_ID;
  hud.style.cssText = [
    'position:fixed', 'top:8px', 'right:8px',
    'z-index:99999',
    'background:rgba(20,20,18,0.92)', 'color:#fff',
    'padding:10px 12px', 'border-radius:8px',
    'font-family:ui-monospace,SF Mono,Menlo,monospace',
    'font-size:11px', 'line-height:1.5',
    'max-width:300px', 'box-shadow:0 4px 16px rgba(0,0,0,0.3)'
  ].join(';');

  hud.innerHTML = `
    <div style="font-weight:600;margin-bottom:6px">composer · iter <span id="${HUD_ID}_iter">1</span></div>
    <div id="${HUD_ID}_status" style="margin-bottom:8px;color:#aaa">drafting…</div>
    <div id="${HUD_ID}_failures" style="margin-bottom:8px;font-size:10px"></div>
    <div style="display:flex;gap:4px;margin-bottom:6px">
      <button data-cmd="continue" style="flex:1;background:#2c5e6f;color:#fff;border:none;padding:4px 8px;border-radius:4px;font-size:10px;cursor:pointer">continue</button>
      <button data-cmd="abort" style="flex:1;background:#c8553d;color:#fff;border:none;padding:4px 8px;border-radius:4px;font-size:10px;cursor:pointer">abort</button>
    </div>
    <textarea id="${HUD_ID}_guidance" placeholder="optional: nudge the drafter…" style="width:100%;background:#000;color:#fff;border:1px solid #444;border-radius:4px;padding:4px;font-size:10px;font-family:inherit;resize:vertical;min-height:32px"></textarea>
    <button data-cmd="guidance" style="width:100%;margin-top:4px;background:#3d3d3a;color:#fff;border:none;padding:4px 8px;border-radius:4px;font-size:10px;cursor:pointer">apply guidance</button>
  `;

  document.body.appendChild(hud);

  hud.addEventListener('click', (e) => {
    const cmd = e.target?.dataset?.cmd;
    if (!cmd) return;
    if (cmd === 'guidance') {
      window.__composer_state.guidance = document.getElementById(HUD_ID + '_guidance').value;
    }
    window.__composer_state.command = cmd;
  });

  window.__composer_update = function ({ iteration, failures, stuck }) {
    document.getElementById(HUD_ID + '_iter').textContent = String(iteration);
    const statusEl = document.getElementById(HUD_ID + '_status');
    const failsEl = document.getElementById(HUD_ID + '_failures');
    if (stuck) {
      statusEl.textContent = 'STUCK — same failures 2x';
      statusEl.style.color = '#c8553d';
    } else if (failures.length === 0) {
      statusEl.textContent = 'all clear';
      statusEl.style.color = '#8aa67c';
    } else {
      statusEl.textContent = `${failures.length} failing`;
      statusEl.style.color = '#d6a544';
    }
    failsEl.innerHTML = failures.slice(0, 5).map(f =>
      `<div style="color:#aaa">· ${f.id} @${f.viewport}</div>`
    ).join('');
  };
})();
