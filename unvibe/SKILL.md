---
name: unvibe
description: >
  Code ownership session that turns AI-written code into understood code. The agent
  shortlists "vibe-y" pieces from recent changes, checks the user's confidence, then
  guides explain/reimplement/test exercises without silently mutating the repo. Use
  after an AI coding session, or on-demand when the user does not understand a
  specific API, function, or behavior the agent wrote.
---

# Unvibe

## Quick start

```
/unvibe                      # analyze recent git changes
/unvibe src/lib/auth.ts      # analyze a specific file or function
```

## Setup

1. Detect the language, build system, and test runner from repo files (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.).
2. Do not change files silently. Before creating `.unvibe/` or editing `.gitignore`, ask for explicit approval.
3. If the stack or runner is unclear, pause before Phase 2 and ask whether to make a runnable native exercise or a conceptual exercise.

## Mode detection

- **Post-session**: no args → inspect `git diff` and `git diff --staged`; if both are empty, inspect the last commit (`git show --stat --patch HEAD`).
- **On-demand**: file/function arg → read that specific code.
- **Unclear**: ask "Which file or function do you want to unvibe?"

## Workflow

**Step 1 — Identify candidates**

Silently find 3-5 pieces worth owning: external API calls, core business logic, non-obvious patterns, error handling, anything the user may not be able to rewrite from memory. Skip trivial getters, boilerplate, self-evident code.

Present them as a numbered shortlist with a short "why this matters" note, then ask the user which one to drill and how confident they feel about it.

**Step 2 — Exercise loop** (repeat per selected piece)

*Phase 1: Explain* — ask one focused question about intent, not line-by-line. Evaluate: solid → Phase 2, partial → one follow-up → Phase 2, fuzzy → you explain (3–4 sentences) → they repeat back → Phase 2. See [REFERENCE.md](REFERENCE.md) for question forms and rubric.

*Phase 2: Reimplement* — if the user approves file writes, create `.unvibe/exercises/<YYYY-MM-DD>_<slug>/` with a no-hints `README.md`, an exercise file in the detected language, and native tests when runner detection is confident. If file writes are declined or native tests are not safe to generate, present a conceptual exercise spec in chat instead. See [REFERENCE.md](REFERENCE.md) for templates.

*Phase 3: Verify* — run the detected test command when repo access allows it. If tests fail, give one conceptual nudge and let the user revise. If the agent cannot run tests, ask the user to paste the output before moving on.

**Step 3 — Session summary**

List what they now own, what is still partial, and the exercise location or command used.

## Rules

- One phase at a time: never ask them to explain and reimplement in the same message.
- Never show the original code during Phase 2: they work from memory plus tests/spec.
- Hints during Phase 2: one conceptual nudge only, never code.
- Keep generated tests behavioral. Do not assert private implementation details.
