---
name: unvibe
description: >
  Code ownership session that turns AI-written code into understood code. Claude extracts
  "vibe-y" pieces from recent changes, you explain them in your own words, then reimplement
  them from scratch with tests verifying correctness. Use after a coding session, or on-demand
  when you don't understand a specific API or function Claude wrote.
---

# Unvibe

## Quick start

```
/unvibe                      # analyze recent git changes
/unvibe src/lib/auth.ts      # analyze a specific file or function
```

## Setup (silent)

1. Detect test runner from `package.json` (`vitest` → `vitest run`, `jest` → `jest`). If none found, **stop and tell the user** — Phase 2 cannot run without one.
2. Ensure `exercises/` is in `.gitignore`. If missing, add it silently.

## Mode detection

- **Post-session**: no args → read `git diff HEAD~1` or `git diff --staged`
- **On-demand**: file/function arg → read that specific code
- **Unclear**: ask "Which file or function do you want to unvibe?"

## Workflow

**Step 1 — Identify candidates**

Silently find 3–5 pieces worth owning: external API calls, core business logic, non-obvious patterns, error handling, anything the user couldn't rewrite from memory. Skip trivial getters, boilerplate, self-evident code.

Present as a numbered list, ask which to work on.

**Step 2 — Exercise loop** (repeat per selected piece)

*Phase 1: Explain* — ask one focused question about intent, not line-by-line. Evaluate: solid → Phase 2, partial → one follow-up → Phase 2, fuzzy → you explain (3–4 sentences) → they repeat back → Phase 2. See [REFERENCE.md](REFERENCE.md) for question forms and rubric.

*Phase 2: Reimplement* — create `exercises/<YYYY-MM-DD>_<function-name>/` with `README.md` (context, no hints), `exercise.ts` (signature + `throw new Error("Not implemented")`), and `exercise.test.ts` (≥3 tests: happy path, edge case, error case). See [REFERENCE.md](REFERENCE.md) for file templates. Wait for user to confirm tests pass before moving on.

**Step 3 — Session summary**

List what they now own (✅), what's partial (⚠️), and exercise file location.

## Rules

- One phase at a time — never ask them to explain AND reimplement in the same message
- Never show the original code during Phase 2 — they work from memory + tests
- Hints during Phase 2: one conceptual nudge only, never code
