# component-composer

Generator-critic loop for single-file HTML data graphics.

The composer drafts an artifact via an LLM drafter, renders it in Claude
Preview, validates with mechanical + LLM-judge checks at three viewports,
and iterates until every active-theme criterion passes. Themes own the
quality bar. Output is one self-contained HTML file with optional PNG +
PDF exports.

See `SKILL.md` for operating mode. See `references/` for protocol details.

Themes: `atomic-data-viz` (Tufte-style) and `bloomberg-dense` (terminal
aesthetic) ship as sibling skills.
