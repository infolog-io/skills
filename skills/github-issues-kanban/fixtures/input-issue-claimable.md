# Fixture — a claimable issue

## Issue #42 — "Add a logout button to the user menu"

**Labels:**
- `status:claimable`
- `size:m`
- `complexity:medium`
- `priority:p2`
- `agent-output:pr`
- `claim-ttl:30m`

**Body:**

```markdown
## Context

The user menu (top-right of the header) currently has Profile and
Settings options but no way to log out. Users keep filing tickets
asking how to log out.

## Acceptance criteria

- [ ] Logout button appears in the user menu dropdown
- [ ] Clicking it calls `/api/auth/logout` and redirects to `/`
- [ ] After logout, protected routes redirect to `/login`
- [ ] Component tests cover the button rendering + click handler
- [ ] E2E test covers the full logout flow

## Out of scope

- Logout from mobile app (different codebase)
- Single sign-out across multiple tabs (deferred)
```

## What the audit reads

- `status:claimable` is present → eligible for dispatch
- `claimed-by:*` is absent → no current claim
- `claim-ttl:30m` → custom TTL on this issue (will set expires_at = now + 30 min)
- Acceptance criteria present (5 checkboxes) → conductor accepts the issue as ready
- `agent-output:pr` → the worker is expected to open a PR
- No `depends-on:*` labels → no dependencies; immediately claimable

## Expected claim outcome

A worker claiming this issue produces:

- Labels after claim:
  - `status:claimed`
  - `claimed-by:<worker-id>`
  - `claim-expires:<now + 30m>`
  - (size/complexity/priority/agent-output:pr retained)
- A `<!-- event: claimed -->` comment from the worker
