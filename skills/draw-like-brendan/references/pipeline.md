# Reference-first pipeline

This is visual reference conditioning, not weight training. Original drawings carry the style; learned rules protect the process around them.

1. Reduce the request to one sentence: what is the single relationship, joke, warning, portrait marker, or sequence the image must communicate?
2. Choose the smallest composition from `modes.md`. Split a complex workflow into 2–5 beats before adding density inside any beat.
3. Run `select_references.py`. Open the returned individual originals in order and state what each contributes.
4. Build a content lock: exact text, required objects, sequence, aspect ratio, and anything forbidden.
5. Run `build_prompt.py`. Attach only the paths in `visual_order`, in that order.
6. Render one candidate with GPT image generation.
7. Compare candidate and originals for composition, lettering, object construction, and color. Fix the largest mismatch only.
8. Re-open the originals before each revision. Stop after three attempts.

For a multidimensional composite, replace steps 1–6 with the cell-and-compositor workflow in `drawing-arrays.md`. Review each cell before assembly; do not use the finished composite as a style reference for later cells.

## Complex explainers

Do not solve complexity by making any one drawing denser. Use a loose strip for 2–5 beats or a drawing array for larger systems. Preserve a repeated visual token across cells only when it helps the viewer traverse dimensions. Keep explanatory prose outside the image when the image would otherwise become a wall of tiny lettering.

## Text-critical work

Use two passes when exact text is important: first establish the composition with blank or minimal label areas; then redraw lettering while the original lettering reference remains attached. Never accept a generic handwritten font because it is readable.

## Revision rule

Name one failed layer and one concrete change. Examples: “composition: collapse six boxes into one three-part metaphor”; “objects: replace clean database icons with the source's crude stacked-container logic”; “lettering: redraw only the title from L03 anatomy.”

## Learning loop

1. Record the user's verdict, failure tags, and exact note with `scripts/record_feedback.py`.
2. Keep repeated but unapproved patterns in `candidate-rules.md`; they do not affect rendering.
3. Promote a rule only after explicit user approval.
4. Add only original or explicitly approved Brendan artwork as style authority.
5. Store generated or reconstructed examples as structure-only with `style_authority: false`.
6. Re-run `scripts/verify_sources.py`, `scripts/validate_skill.py`, and `scripts/test_pipeline.py` after changing canonical materials.
