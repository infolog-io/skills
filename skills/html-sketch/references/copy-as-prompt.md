# Copy-as-Prompt Pattern

The round-trip footer that turns whatever the user did in a sketch HTML
file back into a paste-ready string for Claude. From Thariq:

> "The trick is always to end with an export: a 'copy as JSON' or 'copy
> as prompt' button that turns whatever I did in the UI back into
> something I can paste into Claude Code."

This is what makes a sketch *useful* instead of just decorative. The
user opens it, manipulates the data, hits copy, and the result is in
the clipboard ready to paste back into Claude.

## When to include it

- The user is editing, tuning, or curating something the drafter
  produced
- The output will be acted on by Claude (next prompt, next file
  generation, next refactor)
- The manipulation is too clumsy to express in text directly (drags,
  sliders, multi-select)

## When to skip it

- The HTML is purely a *report* or *explainer* — the user reads, doesn't
  carry data forward
- The output goes somewhere other than Claude (e.g., a clipboard paste
  into a spreadsheet)

## Three export shapes

Pick the one that fits how the user will use the result:

### 1. Copy as prompt (natural language)

For tuning UI parameters, design decisions, prose choices. The pasted
text reads like instructions to Claude.

```js
const lines = [
  'Use these tuned button parameters:',
  '',
  `- duration: ${$('duration').value}ms`,
  `- easing: ${$('ease').value}`,
  `- color: ${$('color').value}`,
];
await navigator.clipboard.writeText(lines.join('\n'));
```

Output:
```
Use these tuned button parameters:

- duration: 240ms
- easing: cubic-bezier(0.34, 1.56, 0.64, 1)
- color: #6b46c1
```

### 2. Copy as JSON

For structured data Claude will re-parse: feature-flag configs,
prioritized lists, schemas, configuration.

```js
const data = {
  triage: {
    now: TICKETS.filter(t => t.bucket === 'now').map(t => t.id),
    next: TICKETS.filter(t => t.bucket === 'next').map(t => t.id),
    later: TICKETS.filter(t => t.bucket === 'later').map(t => t.id),
    cut: TICKETS.filter(t => t.bucket === 'cut').map(t => t.id),
  }
};
await navigator.clipboard.writeText(JSON.stringify(data, null, 2));
```

Output:
```json
{
  "triage": {
    "now": ["ENG-101", "ENG-103", "ENG-110"],
    "next": ["ENG-102", "ENG-104"],
    ...
  }
}
```

### 3. Copy as markdown

For results that go into docs, PRs, status updates. Human- AND
Claude-readable.

```js
const md = ['# Triage'];
['now','next','later','cut'].forEach(b => {
  md.push(`\n## ${b.toUpperCase()}`);
  TICKETS.filter(t => t.bucket === b).forEach(t => {
    md.push(`- ${t.id} — ${t.title}`);
  });
});
await navigator.clipboard.writeText(md.join('\n'));
```

## The UX

Two visible states for the copy button: idle and copied. The "copied"
state lasts ~1.5 seconds, then reverts. No toast, no notification, no
modal — the button itself confirms.

```js
const btn = document.getElementById('copy');
btn.addEventListener('click', async () => {
  await navigator.clipboard.writeText(buildExport());
  btn.textContent = 'Copied!';
  btn.classList.add('copied');
  setTimeout(() => {
    btn.textContent = 'Copy as prompt';
    btn.classList.remove('copied');
  }, 1500);
});
```

With matching CSS:

```css
button { padding: 8px 16px; border: 1px solid #1a1a1a;
         background: white; cursor: pointer; border-radius: 6px; }
button:hover { background: #1a1a1a; color: white; }
button.copied { background: #2c5e6f; color: white; border-color: #2c5e6f; }
```

## Multiple export options

If the user might want different formats, offer two or three buttons,
not a dropdown. Lower friction.

```html
<footer>
  <button id="copy-prompt">Copy as prompt</button>
  <button id="copy-json">Copy as JSON</button>
  <button id="copy-md">Copy as markdown</button>
</footer>
```

## Don't

- Don't use `prompt()` or a textarea for the user to see the result
  first — the user wants to *paste*, not *read-and-paste*. Skip the
  intermediate display unless debugging.
- Don't make them download a file. Clipboard is the round-trip path.
- Don't add a "save to disk" feature. That's a different pattern; this
  is throwaway.
- Don't include long explanations in the pasted text. The user is going
  to paste this *into a Claude prompt* — they'll add context inline.
  Keep the export terse and structured.

## Test

Open the sketch in a browser, click copy, paste into Claude. Does the
pasted text make sense as the *opening line* of a new prompt or as the
*continuation* of an existing one? If yes, the export shape is right.
If you have to edit before pasting, the format is wrong — fix the
exporter.
