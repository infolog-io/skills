# html-sketch

Casual HTML artifacts in Thariq Shihipar's [Unreasonable Effectiveness of HTML](https://www.anthropic.com/engineering/claude-code-html) style — throwaway editors, side-by-side variant comparisons, interactive tuning with sliders, single-page reports.

No validator loop. No themes. No industrial QA. You ask, the drafter makes, you use it once, you move on. Includes the **copy-as-prompt** footer pattern so you can round-trip tuned output back into a Claude prompt.

If you want consistency across many artifacts, use `component-composer` instead.

## Install

```
/plugin install html-sketch@infolog-io
```

## Patterns

| Pattern | When |
|---|---|
| Throwaway editor | Triage tickets, edit config, tune a prompt — one data set, one UI, then discard |
| Compare variants | "Show me 6 options side by side" — explore design space at a glance |
| Interactive tuning | Sliders + knobs + a "copy params" button to bring tuned values back to Claude |
| Single-page report | Long-scroll explainer with TOC, anchors, inline SVG diagrams |
