---
name: unvibe
description: >
  Code ownership session that turns AI-written code into understood code. The agent
  shortlists "vibe-y" pieces from recent changes, checks the user's confidence, then
  guides explain/reimplement/test exercises in a LeetCode-style format and captures
  distilled per-piece ownership notes — all without silently mutating the repo. Use
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

Silently find up to 3 pieces worth owning (1–3, never invent filler to reach 3): external API calls, core business logic, non-obvious patterns, error handling, anything the user may not be able to rewrite from memory. Skip trivial getters, boilerplate, self-evident code.

Present them as a numbered shortlist with a short "why this matters" note, then ask the user which one to drill and how confident they feel about it.

**Step 2 — Exercise loop** (repeat per selected piece)

*Phase 1: Explain* — ask one focused question about intent, not line-by-line. Evaluate: solid → Phase 2, partial → one follow-up → Phase 2, fuzzy → you explain (3–4 sentences) → they repeat back → Phase 2. See [REFERENCE.md](REFERENCE.md) for question forms and rubric.

*Phase 2: Reimplement (LeetCode-style)* — if the user approves file writes, create `.unvibe/exercises/<YYYY-MM-DD_HH-MM-SS>_<slug>/` containing:
- `README.md` — a LeetCode-style problem statement: **Difficulty** (easy/medium/hard, assigned from branch count, edge cases, and external deps), **Problem**, **2–3 curated Examples** (concrete Input→Output, happy path only), **Constraints**, and the **Signature**.
- an exercise file in the detected language — the signature plus a stub that fails clearly, no hints.
- a test file — behavioral tests acting as the hidden "judge". Edge and failure cases live ONLY here, not in the README. Every assertion carries a descriptive message (case label + expected vs actual) so a failure explains itself.
- `run.sh` — a language-aware runner (made executable). Verbose by default; `[-q]` for quiet; optional `[test_name]` to run a single test function. See [REFERENCE.md](REFERENCE.md) for templates.

If file writes are declined or native tests are not safe to generate, present a conceptual exercise spec in chat instead.

*Phase 3: Verify* — run the exercise's `run.sh`. If tests fail, give one conceptual nudge and let the user revise. If the agent cannot run tests, ask the user to paste the output before moving on.

*Phase 4: Capture* — draft a per-piece `notes.md` reflecting what actually happened, regardless of outcome: frontmatter with `status` set to `owned` / `partial` / `explained-only` / `abandoned` plus distilled body sections (what it does, the non-obvious "why", gotchas you missed, your reimplementation choice, what to re-check months from now). Show the draft to the user, accept edits, then write `.unvibe/exercises/<ts>_<slug>/notes.md` and update `.unvibe/INDEX.md` (one row per piece — update in place, don't duplicate, on re-drill). On re-drill of the same piece: append a new dated section to the existing `notes.md`; never overwrite earlier sections. See [REFERENCE.md](REFERENCE.md) for the notes template, status-specific body sections, and INDEX format.

**Step 3 — Session summary**

Briefly highlight what changed this session — pieces now owned, still partial, where the exercises live. `.unvibe/INDEX.md` is the authoritative log; the chat summary just calls out the deltas.

## Rules

- One phase at a time: never ask them to explain and reimplement in the same message.
- Never show the original code during Phase 2: they work from memory plus the problem statement and tests.
- Never reveal hidden edge/failure cases in the README — they surface only when a test goes red.
- Hints during Phase 2: one conceptual nudge only, never code.
- Keep generated tests behavioral. Do not assert private implementation details.
- `notes.md` is collaborative: agent drafts after each piece, user approves or edits, then it's written. Never save notes without showing the user the draft.
