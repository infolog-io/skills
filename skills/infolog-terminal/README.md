# infolog-terminal

Terminal aesthetic theme for `component-composer`. Green-on-black, monospace
everywhere, maximum data density. Looks like a Bloomberg terminal or a 1995
Unix top display.

No serifs. No drop-shadows. No gradients. Every pixel carries data.

This theme exists to prove the multi-theme architecture. The same data that
renders as a quiet Tufte chart under `infolog-io` renders as a dense monospace
table under `infolog-terminal`. Both themes share the same component-composer
loop; only the tokens, palette, and criteria change.

## When to use

Use `infolog-terminal` when the audience expects dense tabular output —
trading dashboards, ops runbooks, CLI-embedded reports, or any surface where
the Bloomberg aesthetic fits the context.

## When not to use

For Tufte-quiet, light-background data graphics, use `infolog-io` instead.
For casual one-off HTML, use `html-sketch` or ask Claude directly.

## Install

```
/plugin install generator-critic@infolog-io
/plugin install component-composer@infolog-io
/plugin install infolog-terminal@infolog-io
```

## Invoke

```
compose with infolog-terminal showing my GitHub usage data
```

`component-composer` resolves the theme, drafts in terminal aesthetic, and
validates against density-first criteria until the artifact is clean.
