---
name: draw-like-brendan
description: Create, redraw, compose, or critique raster artwork in Brendan Hand's source-locked drawing language using bundled original art, learned rules, and a reference-first workflow. Use for Brendan-like posters, signs, portraits, diagrams, visual jokes, technical explainers, hand lettering, composite drawing arrays, multidimensional matrices of small drawings, or when a user says an image should look like Brendan drew it. Ground every rendered cell in Brendan's originals and reject generic hand-drawn infographic drift.
---
# Draw Like Brendan

## What this skill does

Translate a new idea through Brendan's original drawings. Do not define the style as “rough infographic.” The originals are usually blunt and economical: one visual thought, one odd object or relationship, handmade lettering, flat hard-edged color, and a lot of unembarrassed empty space.

The bundle provides 37 source-locked drawings, lettering studies, contact sheets, reference-selection tools, JSON schemas, deterministic brief and array scripts, grading gates, learned rules, and an inspectable feedback record. It uses visual reference conditioning and project memory; it does not train model weights.

## Start here

1. Read `references/source-of-truth.md`, `references/learned-rules.md`, `references/pipeline.md`, and `references/modes.md`.
2. Read `references/typography.md` when visible text matters.
3. Read project-local `.Brendan-Drawing-Style-Skill/learned-rules.md` when present; it may tighten, but not silently contradict, the bundled rules.
4. Create a run with `scripts/new_run.py` and lint its brief with `scripts/lint_brief.py`.
5. Build the render prompt and ordered reference list with `scripts/build_prompt.py`.
6. For composite arrays or matrices, read `references/drawing-arrays.md` and use `scripts/new_array.py` plus `scripts/compose_array.py`.

## Core process

1. Reduce the request to one visual proposition or a short sequence.
2. Choose the smallest viable mode and lock exact text, required objects, aspect ratio, and exclusions.
3. Select 2–4 original drawings by compositional analogy and inspect them individually.
4. Assign each original one role: composition, object construction, lettering, or palette.
5. Build a short render prompt and attach only the ordered originals.
6. Render one candidate with GPT image generation.
7. Compare the candidate with the same originals for composition, lettering, objects, and color.
8. Fix only the worst mismatch, re-open the originals, and stop after three failed attempts.
9. Record explicit user feedback in project state; promote only user-approved rules or original source art.

## Source lock

- Attach 2–4 individual original/user-supplied drawings. Each must have a declared role: composition, object construction, lettering, or palette.
- Prefer the closest compositional analogy, not a giant contact sheet or a general mood board.
- Keep any generated or agent-made image out of the style-reference set. It may be a structure target only.
- Look at the selected originals before deciding the layout. The originals control composition as well as line and color.

## Composition law

Choose the smallest format that can carry the idea:

- **One sign/poster:** one claim, one central visual mechanism, usually 1–2 supporting marks.
- **Small diagram:** one relationship, up to 3 major objects, direct labels or arrows.
- **Complex workflow:** 2–5 separate Brendan-like drawings or a loose strip. Each frame carries one beat. Do not turn complexity into a dashboard of cards.
- **Drawing array:** many independent one-idea drawings assembled into rows, columns, and optional layers. Render cells separately with shared originals, then composite their pixels deterministically.
- **Portrait:** one simplified figure plus only the few motifs that identify the person.

Dense systems boards are not the default style. Use one only when Brendan supplies that exact composition as a current-task reference.

Never ask the image model to render a large drawing array in one pass. Complexity belongs in the array plan and compositor; simplicity belongs inside each cell.

## Render and review

Use GPT image generation with the ordered individual references attached. Keep the prompt short and positive. Describe the visual idea and the reference roles; do not ask the renderer to simulate imperfection with a long list of anti-rules.

Review against the same originals in this order:

1. **Composition:** same economy, scale relationships, and use of empty space?
2. **Lettering:** drawn glyphs with Brendan-like anatomy, not a font or generic marker hand?
3. **Objects:** naive, specific construction copied from the references' logic, not polished icons?
4. **Color:** flat, decisive, and source-derived rather than a polite design-system palette?

Fix only the worst mismatch. Re-anchor on the originals for every revision. Stop after three failed attempts and ask Brendan which candidate has the closest bones.

## Training and provenance

- Treat `assets/source-art/` plus `assets/source-manifest.json` as the bundled style authority.
- Treat `references/learned-rules.md` as approved process memory.
- Treat `assets/training/feedback.jsonl` and `assets/training/candidate-rules.md` as audit history, not automatic instructions.
- Treat `assets/training/structure-references/` as composition-only material. It has `style_authority: false` and must never define drawing, lettering, or color.
- Follow `references/learning-policy.md` when adding sources or promoting feedback.
- Never promote generated outputs, reconstructed examples, contact sheets, or previous candidates into style authority.

## Hard failures

- A generated-looking explainer board, UI card grid, or icon library wearing wobbly outlines.
- More modules, captions, symbols, or decoration than the idea needs.
- Treating “hand-drawn” as a texture filter instead of copying source composition and object logic.
- Smooth vector geometry, tasteful gradients, shading, or evenly balanced palette systems.
- Generated/reference-board artwork used as style authority.
- A composite array rendered as one AI infographic instead of assembled from independently reviewed cells.
- A pass justified by legibility alone.

## Output

Return the final image path, the originals used and their roles, and the single strongest reason it passes. If it does not pass, say which of the four review layers remains wrong.
