# infolog-terminal · Token schema

Same structural tokens as infolog-io. Different values.

Required `:root` variables:

| Variable | Role |
|---|---|
| `--paper`, `--paper-soft` | Surfaces (very dark) |
| `--ink`, `--ink-soft` | Primary + secondary text (bright green) |
| `--accent-warm`, `--accent-cool`, `--accent-quiet` | Highlights (amber, cyan, dim-green) |
| `--gray-100`..`--gray-900` | Grays (cool, near-black to off-white) |
| `--serif`, `--sans`, `--mono` | All resolve to the same monospace stack |
| `--font-size-h1`, `--font-size-h2`, `--font-size-body`, `--font-size-caption` | Type scale (tighter than infolog-io) |
| `--space-1`..`--space-12` | Spacing scale (tighter than infolog-io — values divided by 1.25) |
| `--radius-panel`, `--border` | Structural (radius 0; borders 1px solid green) |
