# infolog-terminal · Patterns

## Default form is a dense table

Most output is a table with many rows, tabular numerics, monospace.

## Sparklines belong inline with numbers

Pair every numeric column with a sparkline of its trend.

## Charts only when comparison is the point

A chart wins only if a table can't show the comparison directly.

## ASCII-art divider lines

Use unicode box-drawing characters for separators between sections:
`────────`, `═══════`, `┄┄┄┄┄┄`.

## Header rows in uppercase

Section labels in caps and letter-spaced for the terminal feel.

## Status indicators inline

Use abbreviations directly in cells: `OK`, `WARN`, `ERR`, `--`. No
icons; no badges; no emoji.
