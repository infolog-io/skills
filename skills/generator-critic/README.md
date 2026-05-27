# generator-critic

Abstract pattern for iteratively refining LLM-produced artifacts against a declared quality bar.

A drafter LLM proposes; a hybrid critic (deterministic mechanical checks + LLM-as-judge) scores; the orchestrator loops feedback back to the drafter until the critic returns zero failures or detects a stuck state. Artifact-agnostic — works for HTML, code, schemas, prose, anything with declared validators.

Consumed by `component-composer` for production-grade HTML data graphics. Future composer-style skills declare this skill as their orchestration dependency.

## Install

```
/plugin install generator-critic@infolog-io
```

## When to use this skill

You're designing a `<thing>-composer` skill and need the refinement-loop machinery. Read `references/loop-protocol.md` first.

## When NOT to use

You want casual or one-off HTML. Use the `html-sketch` skill or just ask Claude directly — no validator loop needed for throwaway artifacts.
