# Throwaway Editor Pattern

A single HTML file, purpose-built for one piece of data. Not a product.
Not a reusable tool. The user opens it, manipulates the data, exports a
result (usually via the copy-as-prompt pattern), and discards the file.

Use when text-box prompting is too clumsy for the manipulation: drag,
drop, reorder, multi-select, bucket, annotate, tag, approve/reject.

## When this pattern fits

- **Reordering / triaging / bucketing** — Linear tickets across columns,
  test cases by priority, feedback by theme
- **Editing structured config** — feature flags with dependencies, env
  vars, JSON with constraints
- **Tuning prompts or templates** with live preview
- **Curating datasets** — approve/reject rows, tag examples, export the
  selection
- **Annotating documents, transcripts, diffs**
- **Picking values painful to express in text** — colors, easing curves,
  crop regions, cron schedules, regex

## When this pattern does NOT fit

- The artifact has long-term value and will be re-opened by others
- The data needs to be persisted to a backend
- Multiple users edit concurrently
- You want to track changes over time

Use a real tool for those cases. This pattern is intentionally
single-use.

## Skeleton

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Throwaway editor · <DOMAIN></title>
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 24px;
    font-family: system-ui, -apple-system, sans-serif;
    background: #fafaf7; color: #1a1a1a;
  }
  header { margin-bottom: 16px; }
  h1 { margin: 0; font-size: 1.4rem; }
  .lede { color: #555; margin-top: 4px; }

  /* Layout — adapt per task: columns for triage, grid for tagging, etc. */
  .columns { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
  .column { background: #f3f1ea; border-radius: 8px; padding: 12px; min-height: 200px; }
  .column h2 { margin: 0 0 8px; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; color: #555; }
  .item {
    background: white; border: 1px solid #d1cfc5; border-radius: 6px;
    padding: 8px; margin-bottom: 8px; cursor: grab; font-size: 0.9rem;
  }
  .item.dragging { opacity: 0.4; }
  .item:hover { border-color: #888; }

  /* Footer with copy-as-prompt button — see copy-as-prompt.md */
  footer { margin-top: 24px; display: flex; gap: 8px; }
  button {
    padding: 8px 16px; border: 1px solid #1a1a1a; background: white;
    cursor: pointer; font-family: inherit; font-size: 0.9rem;
    border-radius: 6px;
  }
  button:hover { background: #1a1a1a; color: white; }
  .copied { background: #2c5e6f !important; color: white !important; border-color: #2c5e6f !important; }
</style>
</head>
<body>

<header>
  <h1>Triage: 30 Linear tickets</h1>
  <p class="lede">Drag tickets across columns. Hit "copy as markdown" to export.</p>
</header>

<div class="columns">
  <div class="column" data-bucket="now"><h2>Now</h2></div>
  <div class="column" data-bucket="next"><h2>Next</h2></div>
  <div class="column" data-bucket="later"><h2>Later</h2></div>
  <div class="column" data-bucket="cut"><h2>Cut</h2></div>
</div>

<footer>
  <button id="copy">Copy as markdown</button>
  <span id="status"></span>
</footer>

<script>
  // Seed data — drafter pre-sorts based on best guess
  const TICKETS = [
    { id: "ENG-101", title: "Fix auth token refresh", bucket: "now" },
    { id: "ENG-102", title: "Migrate to Next 16", bucket: "next" },
    // ... 28 more
  ];

  // Render
  function render() {
    document.querySelectorAll('.column').forEach(col => {
      const bucket = col.dataset.bucket;
      const items = TICKETS.filter(t => t.bucket === bucket);
      col.innerHTML = '<h2>' + bucket.toUpperCase() + '</h2>' +
        items.map(t => `<div class="item" draggable="true" data-id="${t.id}"><strong>${t.id}</strong> · ${t.title}</div>`).join('');
    });
    wire();
  }

  // Drag/drop wiring
  function wire() {
    let dragging = null;
    document.querySelectorAll('.item').forEach(el => {
      el.addEventListener('dragstart', e => { dragging = el; el.classList.add('dragging'); });
      el.addEventListener('dragend', e => { el.classList.remove('dragging'); });
    });
    document.querySelectorAll('.column').forEach(col => {
      col.addEventListener('dragover', e => e.preventDefault());
      col.addEventListener('drop', e => {
        if (!dragging) return;
        const id = dragging.dataset.id;
        const ticket = TICKETS.find(t => t.id === id);
        ticket.bucket = col.dataset.bucket;
        render();
      });
    });
  }

  // Copy as markdown — see copy-as-prompt.md for the pattern
  document.getElementById('copy').addEventListener('click', async () => {
    const md = ['# Linear triage', ''];
    ['now','next','later','cut'].forEach(b => {
      md.push(`## ${b.toUpperCase()}`);
      TICKETS.filter(t => t.bucket === b).forEach(t => md.push(`- ${t.id} · ${t.title}`));
      md.push('');
    });
    await navigator.clipboard.writeText(md.join('\n'));
    const btn = document.getElementById('copy');
    btn.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(() => { btn.textContent = 'Copy as markdown'; btn.classList.remove('copied'); }, 1500);
  });

  render();
</script>

</body>
</html>
```

## Adaptation notes

- **Data is inlined.** No fetch, no API. The drafter bakes the input
  data into the `const TICKETS = [...]` array. This is what makes it
  throwaway.
- **Layout matches the manipulation.** Columns for triage, grid for
  tagging, list for ordering. Don't force a column metaphor on a
  reordering task.
- **One export button.** "Copy as markdown" or "copy as prompt" or
  "copy as JSON" — pick the format that fits how the user will paste
  the result back. See `copy-as-prompt.md`.
- **No backend, no state survival.** Refresh = data resets. That's
  intended — the user exports before closing.
- **Pre-sort intelligently.** The drafter should make a best-guess
  initial assignment, not leave all items in one bucket. Saves user
  effort.

## Example prompts

- "I need to reprioritize these 30 Linear tickets. Make me an HTML file
  with each ticket as a draggable card across Now / Next / Later / Cut
  columns. Pre-sort them by your best guess. Add a 'copy as markdown'
  button that exports the final ordering with a one-line rationale per
  bucket."
- "Here's our feature flag config. Build a form-based editor for it,
  group flags by area, show dependencies between them, warn me if I
  enable a flag whose prerequisite is off. Add a 'copy diff' button
  that gives me just the changed keys."
- "I'm tuning this system prompt. Make a side-by-side editor: editable
  prompt on the left with the variable slots highlighted, three sample
  inputs on the right that re-render the filled template live. Add a
  character/token counter and a copy button."
