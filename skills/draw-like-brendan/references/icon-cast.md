# Icon Cast and Motif Control

## Principle

Choose an icon because it explains the concept. Do not choose it merely because it appeared in another Brendan-Drawing-Style-Skill drawing.

But do not start from a clean semantic icon. Start from the source drawings' morphology first: stubby proportions, blunt cut ends, uneven contour rhythm, awkward spacing, flat marker construction, and odd simplification. Then adapt that source-like shape to the concept. A pictogram with a rough outline filter fails.

## Cast

- people, faces, hands, request cards, speech bubbles
- doors, portals, gates, checkpoints, pipes
- conveyors, waiting blocks, snakes, dotted paths
- dice, batteries, plugs, outlets, keys, locks
- knives, wrenches, tools, magic wands, flags
- notebooks, receipts, books, drawers, cabinets, server stacks
- warning triangles, skull-ish marks, tombstones, low batteries
- cacti, leaves, mushrooms, flowers, simple animals
- aliens and odd helpers
- stars, asterisks, bursts, flames, waves
- maps, arrows, loops, ladders, odd containers
- eyes only when seeing, monitoring, evaluation, surveillance, or perspective is the actual concept

## Technical mapping

Use these mappings as semantic intent, not as literal icon-pack nouns. For each object, write or draw it as a source-derived sign/container/tool/odd mark first.

- user/request -> person, hand, card, face, speech bubble
- API/gateway -> door, gate, portal, checkpoint
- queue -> conveyor, waiting blocks, snake, line
- agent/worker -> helper, alien, tool-user, simple machine
- tool call -> wrench, key, plug, wand, knife-like implement
- memory -> notebook, drawer, cards, archive box
- database/vector store -> cabinet, server stack, odd storage vessel
- logs -> receipt roll, notebook, tally sheet
- monitoring -> gauge, tower, magnifier; eye only when justified
- error/retry -> warning sign, low battery, tombstone, loop, spill
- success/response -> flag, star, open door, output card

## Diversity gate

For a dense diagram, use at least four motif families. No decorative motif should repeat more than three times. Arrows and structural boxes are exempt, but boxes must not resemble polished UI cards.

## User Reference Drift Gate

When the user supplies closer style references, reject symbols that are merely clean, useful diagram icons. The drawing must inherit the supplied reference's roughness: flat marker construction, chunky uneven outlines, simple shapes, raw spacing, and hand-authored oddness. Require source-like drawing quirks and avoid AI slop. If an object looks like it came from an icon pack with a rough outline filter, it fails even when the label is correct.

Default to flat drawings. A little dimensionality is allowed only when it feels naive and hand-built, like a simple cube or box. Avoid polished perspective, app-diagram machinery, and clean 3D objects.

When a requested technical object is not visibly present in the sources, transform it through the nearest source family instead of drawing the canonical icon. For example: a database can become an awkward source-like box, receipt stack, drawer, or labeled container; retrieval can become a dotted path, hand, key-like odd tool, or sign; evaluation can become a warning mark, tally, or crude badge.
