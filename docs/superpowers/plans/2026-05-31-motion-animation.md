# Motion & Animation §11 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (recommended for this single-file change) or superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add §11 Motion & Animation to the infolog.lib reference page: duration/easing tokens, all motion graduated onto those tokens, and reduced-motion honored by one override.

**Architecture:** One self-contained HTML file (`docs/superpowers/reference/infolog-lib-design-system.html`, untracked by convention). Edits land in three places: the `:root` token block, the `<style>` motion rules, and the section markup + one JS helper. Verification is a deterministic Python byte-read for structure and an agent-browser file:// check for behavior (light, dark, reduced-motion). No git commits for the HTML — it is untracked on purpose; the final step copies it to the two `/tmp` mirrors.

**Tech Stack:** Plain HTML/CSS/JS. CSS custom properties. Native `<dialog>`. agent-browser (Chromium) for preview. Spec: `docs/superpowers/specs/2026-05-31-motion-animation-design.md`.

**Canonical file (call it `$F`):** `docs/superpowers/reference/infolog-lib-design-system.html`

---

### Task 1: Add motion tokens to `:root`

**Files:**
- Modify: `$F` `:root` block (ends at line 37, after the z-index scale line 36)

- [ ] **Step 1: Insert the token block** immediately after the z-index scale line (`--z-base: 0; ...`), before the `:root` closing brace.

```css
    /* Motion — quiet & tight, honored by prefers-reduced-motion (locked 2026-05-31) */
    --dur-fast: 120ms;  --dur-base: 160ms;  --dur-slow: 240ms;
    --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);  /* in-place changes: accel then decel */
    --ease-out:      cubic-bezier(0, 0, 0.2, 1);     /* entrances: decelerate to rest */
```

- [ ] **Step 2: Verify (structure).**

Run: `python3 -c "s=open('$F').read(); print('--dur-fast' in s, '--ease-standard' in s, '--ease-out' in s)"`
Expected: `True True True`

---

### Task 2: Graduate the nine hardcoded motion values onto tokens

**Files:**
- Modify: `$F` lines 151, 367, 393, 399, 434 (transitions) and 467, 468, 474, 478 (animations)

- [ ] **Step 1: Edit each transition.** Replace the literal value with the token pair.

- `.btn` (line 151): `transition: opacity 0.15s;` → `transition: opacity var(--dur-fast) var(--ease-standard);`
- `.select` (line 367): `transition: border-color 0.12s, background 0.12s;` → `transition: border-color var(--dur-fast) var(--ease-standard), background var(--dur-fast) var(--ease-standard);`
- toggle bg (line 393): `transition: background 0.15s;` → `transition: background var(--dur-base) var(--ease-standard);`
- toggle knob (line 399): `transition: left 0.15s;` → `transition: left var(--dur-base) var(--ease-standard);`
- `.copy-btn` (line 434): `transition: opacity 0.15s;` → `transition: opacity var(--dur-fast) var(--ease-standard);`

- [ ] **Step 2: Edit each animation.**

- modal (line 467): `animation: modal-in 0.16s ease-out;` → `animation: modal-in var(--dur-base) var(--ease-out);`
- scrim (line 468): `animation: scrim-in 0.16s ease-out;` → `animation: scrim-in var(--dur-base) var(--ease-out);`
- toast-in (line 474): `animation: toast-in 0.18s ease-out;` → `animation: toast-in var(--dur-base) var(--ease-out);`
- toast-out (line 478): `animation: toast-out 0.18s ease-in forwards;` → `animation: toast-out var(--dur-base) var(--ease-standard) forwards;`

- [ ] **Step 3: Verify no hardcoded motion durations remain** in those rules.

Run: `python3 -c "import re; s=open('$F').read(); hits=re.findall(r'(transition|animation):[^;]*\b0\.\d+s\b[^;]*;', s); print(len(hits), hits)"`
Expected: `0 []` (every transition/animation now reads a `var(--dur-*)`).

---

### Task 3: Replace the reduced-motion block with the token override

**Files:**
- Modify: `$F` lines 482–484 (current `prefers-reduced-motion` block)

- [ ] **Step 1: Replace the block.**

From:
```css
  @media (prefers-reduced-motion: reduce) {
    dialog.modal[open], dialog.modal[open]::backdrop, .toast, .toast.toast-out { animation: none; }
  }
```
To:
```css
  @media (prefers-reduced-motion: reduce) {
    :root { --dur-fast: 0.01ms; --dur-base: 0.01ms; --dur-slow: 0.01ms; }
  }
```

- [ ] **Step 2: Verify.**

Run: `python3 -c "s=open('$F').read(); print('animation: none' not in s, '--dur-fast: 0.01ms' in s)"`
Expected: `True True`

---

### Task 4: Add the §11 demo CSS

**Files:**
- Modify: `$F` `<style>`, immediately after the toast-out keyframe (line 480), before the reduced-motion media query

- [ ] **Step 1: Insert the demo CSS.**

```css
  /* §11 motion demo */
  .motion-demo { display: flex; flex-direction: column; gap: var(--space-3); max-width: 64ch; margin-top: var(--space-2); }
  .motion-lane { position: relative; height: 32px; display: flex; align-items: center; border-bottom: 1px solid var(--gray-100); }
  .motion-tag { font-family: var(--mono); font-size: 0.72rem; color: var(--ink-soft); text-transform: uppercase; letter-spacing: var(--tracking-wide); }
  .motion-dot { position: absolute; left: 0; width: 14px; height: 14px; border-radius: 50%; background: var(--tonal-info-ink); }
  .motion-dot.standard { transition: left var(--dur-slow) var(--ease-standard); }
  .motion-dot.out      { transition: left var(--dur-slow) var(--ease-out); }
  .motion-demo.is-playing .motion-dot { left: calc(100% - 14px); }
```

- [ ] **Step 2: Verify.**

Run: `python3 -c "s=open('$F').read(); print('.motion-demo' in s, 'is-playing .motion-dot' in s)"`
Expected: `True True`

---

### Task 5: Add the §11 section markup

**Files:**
- Modify: `$F`, insert after the `toast-stack` div (line 1409), before the feedback coda comment (line 1411)

- [ ] **Step 1: Insert the section.**

```html
<!-- §11 Motion & animation ======================================== -->
<section id="motion" class="tight">
  <div class="grid">
    <header class="span-full lg-span-8">
      <p class="meta eyebrow">11 · Motion & animation</p>
      <h2>Three speeds, two curves — quiet by default.</h2>
      <p class="desc">Motion marks state changes and entrances. Nothing decorates. Every transition routes through duration and easing tokens. One media query flattens the whole system when the operating system requests reduced motion.</p>
    </header>

    <div class="span-full lg-span-6">
      <p class="form-block-label">Duration</p>
      <div class="z-scale">
        <div class="z-row"><span class="z-tok">--dur-fast</span><span class="z-val">120ms</span><span class="z-use">opacity, hover, micro-feedback</span></div>
        <div class="z-row"><span class="z-tok">--dur-base</span><span class="z-val">160ms</span><span class="z-use">toggles, modal &amp; toast entrance</span></div>
        <div class="z-row"><span class="z-tok">--dur-slow</span><span class="z-val">240ms</span><span class="z-use">larger travel — the demo below</span></div>
      </div>
    </div>

    <div class="span-full lg-span-6">
      <p class="form-block-label">Easing</p>
      <div class="z-scale">
        <div class="z-row"><span class="z-tok">--ease-standard</span><span class="z-val">.4,0,.2,1</span><span class="z-use">in-place changes</span></div>
        <div class="z-row"><span class="z-tok">--ease-out</span><span class="z-val">0,0,.2,1</span><span class="z-use">entrances — decelerate to rest</span></div>
      </div>
    </div>

    <div class="span-full">
      <p class="form-block-label">Live</p>
      <div class="motion-demo">
        <div class="motion-lane"><span class="motion-tag">--ease-standard</span><span class="motion-dot standard"></span></div>
        <div class="motion-lane"><span class="motion-tag">--ease-out</span><span class="motion-dot out"></span></div>
      </div>
      <div class="elev-actions">
        <button class="btn tonal info" type="button" onclick="replayMotion()">Replay</button>
        <span class="meta">at --dur-slow · flattens under reduced-motion</span>
      </div>
    </div>
  </div>
</section>
```

- [ ] **Step 2: Verify.**

Run: `python3 -c "s=open('$F').read(); print('id=\"motion\"' in s, '11 · Motion' in s, s.count('motion-dot')>=2)"`
Expected: `True True True`

---

### Task 6: Add the `replayMotion()` helper

**Files:**
- Modify: `$F` `<script>` (near `spawnToast`, around line 1660)

- [ ] **Step 1: Insert the function.**

```js
    function replayMotion(){ document.querySelector('.motion-demo').classList.toggle('is-playing'); }
```

- [ ] **Step 2: Verify.**

Run: `python3 -c "s=open('$F').read(); print('function replayMotion' in s)"`
Expected: `True`

---

### Task 7: Behavioral verification in agent-browser (file://)

**Files:** none — verification only. Use the absolute path to `$F`.

- [ ] **Step 1: Open + light screenshot.** `agent-browser open "file://<abs $F>"`, scroll `#motion` into view, screenshot. Expect the section: header, two scale tables, two lanes, Replay button. No console errors.

- [ ] **Step 2: Replay.** Click Replay (`document.querySelector('.motion-demo').classList` toggles `is-playing`). Confirm both dots move to the right edge; click again, they return. Screenshot mid/after.

- [ ] **Step 3: Regression — existing motion still works.** Click "Open dialog" (modal fades+scales in), close, "Show toast" (toast slides in, auto-dismisses), toggle a switch in §forms. No console errors.

- [ ] **Step 4: Dark.** `eval "document.documentElement.setAttribute('data-theme','dark')"`, scroll `#motion` into view, screenshot. Dot uses `--tonal-info-ink` (readable). Tables legible.

- [ ] **Step 5: Reduced-motion.** Emulate `prefers-reduced-motion: reduce` (agent-browser CDP `Emulation.setEmulatedMedia`, or devtools). Click Replay → dots jump instantly (no travel). Open dialog → appears with no fade. If emulation is unavailable, confirm by inspection that the override block is present and every motion rule reads `var(--dur-*)` (Task 2 Step 3 already proved the latter).

- [ ] **Step 6: Safari-parity sanity.** Inject the localStorage throw shim at top (`Object.defineProperty(window,'localStorage',{configurable:true,get(){throw new Error()}})`), reload, confirm the theme switch still toggles and no console errors (guards against any regression near the script edits). Memory: `file-url-localstorage-guard`.

---

### Task 8: Propagate to the mirrors

**Files:**
- Copy: `$F` → `/tmp/dslib.html` and `/tmp/composer-e2e/spraypixel-state.html`

- [ ] **Step 1: Copy.**

Run: `cp "$F" /tmp/dslib.html && cp "$F" /tmp/composer-e2e/spraypixel-state.html`

- [ ] **Step 2: Verify byte-identical.**

Run: `cmp "$F" /tmp/dslib.html && cmp "$F" /tmp/composer-e2e/spraypixel-state.html && echo OK`
Expected: `OK`

---

## Self-Review

**Spec coverage:** Tokens (Task 1) ✓. Reduced-motion override + bug fix (Task 3) ✓. Nine-value graduation map (Task 2, all nine listed) ✓. Section markup with duration + easing tables + live demo (Task 5) ✓. Demo CSS (Task 4) and ping-pong JS (Task 6) ✓. Propagation to mirrors (Task 8) ✓. Light/dark/reduced-motion + regression + Safari-parity verification (Task 7) ✓.

**Placeholder scan:** none — every CSS/HTML/JS step carries its literal content; every verify step carries an exact command and expected output.

**Type consistency:** the JS toggles `.is-playing` on `.motion-demo`; the CSS selector is `.motion-demo.is-playing .motion-dot`; the markup has `class="motion-demo"` with `.motion-dot.standard` / `.motion-dot.out`. Token names (`--dur-fast/base/slow`, `--ease-standard/out`) are identical across Tasks 1, 2, 4. Consistent.
