# bloomberg-dense · Validator criteria

Inherits the structural mechanical checks (text_collision, overflow, etc.)
from the composer's built-in registry. Adds these subjective criteria
(LLM-judge):

## insufficient_density

This theme demands maximum information per pixel. A chart with more
than 40% empty space below the fold is too sparse. Subjective judgment.

## missing_monospace_alignment

Every numeric column is right-aligned and uses `font-variant-numeric:
tabular-nums`. Subjective check on rendered output.

## non_monospace_font

Any text rendered in a non-monospace font violates the aesthetic.
Subjective.

## color_outside_palette

The artifact uses any color outside the declared palette
(`--paper`, `--ink`, `--accent-*`, `--gray-*`). Verified by the
mechanical `token_compliance` check; LLM-judge confirms aesthetic.
