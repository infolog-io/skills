# Atomic Brand Audit — {{project_name}}

> **Brand source:** {{explicit-tokens | image-parsed | url-scraped}} · **Confidence:** {{high | medium | low}} · **Audited:** {{date}}

## Verdict

**{{system-healthy | drifting | broken}}**

{{one-sentence summary of the verdict and the next action}}

## Scores

| Dimension | Score | Reason |
|---|---|---|
| Token compliance | {{1-5}} | {{cite N hardcoded values; cite % using tokens}} |
| Atomic discipline | {{1-5}} | {{cite hierarchy state and misclassifications}} |
| Naming integrity | {{1-5}} | {{cite worst names}} |
| Brand coherence | {{1-5}} | {{cite outlier elements}} |
| Scale discipline | {{1-5}} | {{cite off-scale values}} |
| Composition health | {{1-5}} | {{cite reaches and inversions}} |
| Duplication | {{1-5}} | {{cite duplicate sets by component}} |
| Variant clarity | {{1-5}} | {{cite implicit variants}} |

## Findings

### Token violations ({{count}})

| File | Line | Found | Expected | Confidence |
|---|---|---|---|---|
| {{path}} | {{n}} | `{{snippet}}` | `var(--{{token}})` | {{high|medium|low}} |

### Atomic violations ({{count}})

| File | Current level | Should be | Reason |
|---|---|---|---|
| {{path}} | {{level}} | {{correct-level}} | {{rationale}} |

### Naming violations ({{count}})

| File | Current name | Suggested name | Reason |
|---|---|---|---|
| {{path}} | `{{current}}` | `{{suggested}}` | {{appearance | page | version | generic}} |

### Brand drift ({{count}})

| File | Found | Expected | Notes |
|---|---|---|---|
| {{path}} | {{value}} | {{brand value}} | {{notes}} |

### Composition violations ({{count}})

| Importer | Imported | Reason |
|---|---|---|
| {{atom-or-molecule}} | {{higher-level}} | {{which rule was violated}} |

### Scale violations ({{count}})

| File | Found value | Scale | Nearest step |
|---|---|---|---|
| {{path}} | `{{value}}` | {{scale name}} | `{{nearest}}` |

### Duplications ({{count}})

| Duplicate set | Canonical replacement |
|---|---|
| {{file-a}}, {{file-b}}, {{file-c}} | {{canonical-file}} with variants `{{v1, v2, v3}}` |

### Variant clarity issues ({{count}})

| File | Implicit variant | Declared form |
|---|---|---|
| {{path}} | `{{className override}}` | `intent="{{value}}"` |

## Recommended next change

{{single highest-leverage fix — the one thing that, if done, moves the verdict up one level}}

## Build-out plan

(emitted only when verdict is `broken`. See companion `build-out-plan.md`.)

## Refactor plan

(emitted only when verdict is `drifting`. See companion `refactor-plan.md`.)

## Adjacent passes

| Pass | When to run |
|---|---|
| Chart-audit pass | Run on any chart/dashboard surfaces |
| Typography-audit pass | Generate or audit the type scale referenced in tokens |
| Need-validation pass | If a redesign is being scoped, validate the underlying customer job |
| Sizing pass | Size the refactor or build-out tasks against your sizing rubric |
| Code-organization pass | Apply to design-system code organization itself |

## Confidence rationale

{{Why is confidence at this level? What would raise it?}}
