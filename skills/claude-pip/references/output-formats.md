# Output to user — confirmation templates

## After `CLAUDE PIP` or `LOCAL PIP`

```
✓ CLAUDE PIP — rule added to <path>
  id: <8-char-id>

  {rule}

This will fire deterministically on every future session. To remove,
invoke `OFF THE PIP <id>`.
```

## After `OFF THE PIP <id>`

```
✓ OFF THE PIP — rule removed from <path>
  id: <8-char-id>

  {removed rule}

The marker range was deleted in full. No orphan text remains.
```

## After `OFF THE PIP` with no argument (listing)

```
PIP rules currently active:

<id>  <file>                          <first line of rule body>
ab12cd34  .claude/CLAUDE-PIP.md        Write a failing test FIRST for any user-visible…
ef56gh78  ./CLAUDE.md                  Always lint before commit in this package
...

Which would you like to remove? (paste the id)
```

## After `PRUNE THE PIP` / `PROMOTE THE PIP`

Prune: markdown diff report grouped by verdict (`keep` / `refine` / `drop` / `move-elsewhere`), then post-apply rule count.
Promote: categorized rule table with destination column, then a per-destination diff for the rules the user named.
