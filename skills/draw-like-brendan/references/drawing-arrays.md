# Drawing arrays

A drawing array is a large composite made from independently rendered Brendan drawings. Treat it like a multidimensional array:

- columns encode stages, time, or alternatives;
- rows encode actors, system layers, questions, or perspectives;
- optional layers encode scenarios, versions, or another dimension.

The array can be complex. A cell cannot. Each cell carries one visual proposition and at most three major objects.

## Workflow

1. Write an array spec using `array-schema.json`.
2. Run `scripts/new_array.py SPEC --root PROJECT`. It creates one brief, prompt, and shared reference packet per cell.
3. Render every cell separately. Attach the same paths from each cell's `selected_references.json`. Save the accepted image as that cell's `final.png`.
4. Review every cell against the shared originals before assembly.
5. Run `scripts/compose_array.py ARRAY_JSON --out COMPOSITE.png`.
6. Review the composite for traversal, axis meaning, repeated-token continuity, and accidental card-grid drift.

Do not render the whole array in one image-generation call. Do not run an AI polish pass over the assembled composite. The compositor preserves accepted cell pixels.

## Example spec

```json
{
  "title": "RAG FROM THREE ANGLES",
  "concept": "How material becomes an answer",
  "rows": [
    {"id": "material", "label": "MATERIAL"},
    {"id": "question", "label": "QUESTION"}
  ],
  "columns": [
    {"id": "before", "label": "BEFORE"},
    {"id": "during", "label": "DURING"},
    {"id": "after", "label": "AFTER"}
  ],
  "layers": [
    {"id": "happy", "label": "WORKING"},
    {"id": "broken", "label": "BROKEN"}
  ],
  "cells": [
    {
      "layer": "happy",
      "row": "material",
      "column": "before",
      "concept": "A crude heap of useful notes waiting to be stored",
      "exact_text": ["PUT IT IN"]
    }
  ],
  "allow_empty_cells": true,
  "cell_size": [1024, 1024],
  "gutter": 96,
  "jitter": 24,
  "composite_background": "white"
}
```

Use `allow_empty_cells: false` for a complete matrix. Empty cells are valid when absence is meaningful.

## Titles and axis labels

Do not typeset labels during composition. Make a title, row label, or column label as its own Brendan drawing cell when it must be visible. Otherwise explain axes outside the image. This avoids a clean typographic shell around source-locked drawings.

## Cohesion without cloning

- Lock the same 2–4 original references across every cell.
- Reuse one object, color, or path token across a sequence when it carries meaning.
- Vary scale and placement inside cells; do not clone one template.
- Assemble with open space and small deterministic jitter; do not add rounded cards or equal borders.
