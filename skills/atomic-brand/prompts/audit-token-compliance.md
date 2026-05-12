# Prompt — Audit token compliance

**Purpose:** Score the token-compliance dimension. Walk every component file
and count literal values vs. token references.

## Input contract

- A parsed token map: `{ color: {...}, spacing: {...}, type: {...}, ... }`
- A list of component file paths
- Optional: a `tokens-exceptions.md` file declaring intentional literals

## Output contract

```json
{
  "score": 1-5,
  "total_values_counted": N,
  "token_references": M,
  "hardcoded_with_token_equivalent": K,
  "compliance_pct": K_pct,
  "findings": [
    {
      "tag": "token_violation",
      "file": "src/components/atoms/button.tsx",
      "line": 12,
      "found": "color: #FF6600",
      "expected": "color: var(--color-primary)",
      "confidence": "high"
    }
  ]
}
```

## Procedure

### 1. Parse the token map

Index tokens by their literal value for fast lookup:

```
value_to_token_map = {
  "#FF6600": "--color-primary",
  "8px": "--space-2",
  "16px": "--space-3",
  "300ms": "--duration-normal",
  ...
}
```

When multiple tokens share a value, prefer the most semantic name
(`--color-primary` over `--color-brand-orange-default`).

### 2. Walk component files

For each file:

1. Read the file
2. Extract every literal value from style declarations (CSS rules,
   inline styles, CSS-in-JS, style props)
3. For each literal, check the value_to_token_map

### 3. Classify each value

| Classification | Definition |
|---|---|
| Token reference | The value is `var(--token)` or equivalent | counted as compliant |
| Hardcoded with token equivalent | The literal value matches a token in the map | violation |
| Hardcoded without token equivalent | The literal value is not in the map | exception candidate |
| Computed / derived | `100% - var(--space-2)`, calculated grid columns, etc. | counted as compliant |
| Listed in exceptions | The value matches an entry in `tokens-exceptions.md` | skipped |

### 4. Score per the rubric

| Compliance % | Score |
|---|---|
| ≥95% | 5 |
| 85-94% | 4 |
| 70-84% | 3 |
| 50-69% | 2 |
| <50% | 1 |

### 5. Emit findings

For each "Hardcoded with token equivalent" classification, emit a
finding with the file, line, found value, expected token reference, and
confidence (high for exact matches; medium when the value is close but
not identical).

## Worked example

### Input

Token map:
```css
--color-primary: #FF6600;
--space-2: 8px;
--space-3: 12px;
--radius-md: 6px;
--duration-normal: 300ms;
```

Component:
```css
/* src/components/atoms/button.css */
.button {
  background: #FF6600;
  padding: 8px 12px;
  border-radius: 6px;
  transition: background 300ms;
  color: white;
}

.button:hover {
  background: #FF7711;
  border: 1px solid rgba(0, 0, 0, 0.1);
}
```

### Output

```json
{
  "score": 2,
  "total_values_counted": 9,
  "token_references": 0,
  "hardcoded_with_token_equivalent": 5,
  "compliance_pct": 0,
  "findings": [
    {
      "tag": "token_violation",
      "file": "src/components/atoms/button.css",
      "line": 3,
      "found": "background: #FF6600",
      "expected": "background: var(--color-primary)",
      "confidence": "high"
    },
    {
      "tag": "token_violation",
      "file": "src/components/atoms/button.css",
      "line": 4,
      "found": "padding: 8px 12px",
      "expected": "padding: var(--space-2) var(--space-3)",
      "confidence": "high"
    },
    {
      "tag": "token_violation",
      "file": "src/components/atoms/button.css",
      "line": 5,
      "found": "border-radius: 6px",
      "expected": "border-radius: var(--radius-md)",
      "confidence": "high"
    },
    {
      "tag": "token_violation",
      "file": "src/components/atoms/button.css",
      "line": 6,
      "found": "transition: background 300ms",
      "expected": "transition: background var(--duration-normal)",
      "confidence": "high"
    },
    {
      "tag": "brand_drift",
      "file": "src/components/atoms/button.css",
      "line": 11,
      "found": "background: #FF7711 (hover state)",
      "expected": "Use --color-primary-hover token if hover variants exist; otherwise document",
      "confidence": "medium"
    }
  ]
}
```

The score is 2 because compliance is 0% — but the values match tokens
1:1, so the fix is mechanical replacement. After fix, score becomes 5.

## Negative example

### Input

A file where every value is a token reference already:

```css
.button {
  background: var(--color-primary);
  padding: var(--space-2) var(--space-3);
  color: var(--color-text-on-primary);
}
```

### Output

```json
{
  "score": 5,
  "total_values_counted": 4,
  "token_references": 4,
  "hardcoded_with_token_equivalent": 0,
  "compliance_pct": 100,
  "findings": []
}
```

## Edge cases

| Pattern | Handling |
|---|---|
| Tailwind class names that imply tokens (`bg-primary`, `p-2`) | Resolve to the underlying token; treat as token reference |
| CSS-in-JS template literal: `` `${tokens.color.primary}` `` | Token reference |
| Style prop with object literal: `style={{ color: theme.colors.primary }}` | Token reference |
| `border: 1px solid rgba(0,0,0,0.1)` with no equivalent token | Hardcoded without equivalent — possible exception |
| Generated grid widths from container | Computed; skip |
| Animation @keyframes with literal values | Skip if motion tokens don't cover keyframe steps; document otherwise |

## Verification before returning output

- Every counted value classified into one of five categories
- Findings cite the exact file and line
- Score follows the rubric strictly
- Exceptions consulted if `tokens-exceptions.md` exists
