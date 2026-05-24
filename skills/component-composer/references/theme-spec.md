# Theme Spec — Interface Contract

A skill conforms to the theme-spec interface by providing:

```
skills/<theme-name>/
  SKILL.md                    declares itself as a theme
  themespec.json              machine-readable manifest
  references/
    tokens.md                 CSS variable schema (which vars, what they mean)
    palette.md                concrete palette values
    criteria.md               validator rules
    patterns.md               preferred component patterns
    principles.md             (optional) foundational reference
```

## themespec.json schema

```json
{
  "name": "atomic-data-viz",
  "version": "1.0.0",
  "context": "data-graphics",
  "capabilities": ["chart", "table", "sparkline", "small-multiples"],
  "output_formats": ["html", "png", "pdf"],
  "style_anchor": "single-file-html"
}
```

Required fields: `name`, `version`, `context`, `output_formats`.

## tokens.md

Markdown with one section per token category. Each section declares which
CSS variables that theme uses and what role they play. Example:

```markdown
## Color

| Variable | Role |
|---|---|
| `--paper` | primary background |
| `--ink` | primary text/data |
| `--accent-warm` | single highlight (90% gray + 10% color rule) |
```

The composer reads tokens.md to know which variables the artifact must
declare on `:root`. The `token_compliance` mechanical check enforces it.

## palette.md

Concrete values. Example:

````markdown
## Color values

```css
:root {
  --paper: #fafaf7;
  --ink: #1a1a1a;
  --accent-warm: #c8553d;
}
```
````

## criteria.md

Each criterion has an id (markdown H2) and a check description (prose).
No severity, no priority. The composer concatenates all criteria into the
LLM-judge prompt; the mechanical layer dispatches by id.

```markdown
## text_collision

No text labels overlap each other or data marks.

## missing_range_frame

Axis terminates at data extent, not arbitrary round numbers.
```

## patterns.md

Preferred component patterns. The drafter reads these before composing.

```markdown
## Time-series → line, not bar

Lines preserve sequence; bars imply discreteness.

## Many-to-many comparison → small multiples

A single overloaded chart with N colors fails. N panels with identical
encoding succeeds.
```

## Theme discovery

The composer scans `skills/*/themespec.json` at session start. Themes are
keyed by `name`. The user names a theme; composer resolves and loads.
