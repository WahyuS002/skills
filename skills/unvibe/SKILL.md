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

## Bundled resources

- `references/reference.md` — rubrics, priorities, and format adaptations. Consult this when you need the Phase 1 question forms, the difficulty rubric, the Examples-happy-path rule, or the per-status notes-body layout.
- `assets/templates/` — `readme.md`, `index.md`, `test_python.py`, `test_go.go`, `test_ts.ts`. Read the relevant file, fill the `<TOKENS>`, then `Write` the substituted file to the exercise dir.
- `assets/runners/python.sh`, `assets/runners/go.sh`, `assets/runners/ts.sh` — copy the matching one to the exercise dir as `run.sh`, `chmod +x`. For other stacks, follow the same `[-q] [test_name]` interface.
- `scripts/render_notes.py` — render `notes.md` with status-conditional body sections. Use this in Phase 4 instead of hand-writing the file.
- `scripts/update_index.py` — update `.unvibe/INDEX.md` in place from a `notes.md` frontmatter. Use this after every `notes.md` write (including re-drills).
- `scripts/quick_validate.sh` — self-check that a generated exercise dir is well-formed (dir name, README difficulty tag, executable run.sh, test + stub files). Run at the end of Phase 2.

## Workflow

**Step 1 — Identify candidates**

Silently find up to 3 pieces worth owning (1–3, never invent filler to reach 3); see `references/reference.md` → "Candidate identification priorities" for the selection criteria.

Present them as a numbered shortlist with a short "why this matters" note, then ask the user which one to drill and how confident they feel about it.

**Step 2 — Exercise loop** (repeat per selected piece)

*Phase 1: Explain* — ask one focused question about intent, not line-by-line. Evaluate solid → Phase 2, partial → one follow-up → Phase 2, fuzzy → you explain (3–4 sentences) → they repeat back → Phase 2. See `references/reference.md` → "Phase 1: Evaluation rubric".

*Phase 2: Reimplement (LeetCode-style)* — if the user approves file writes, create `.unvibe/exercises/<YYYY-MM-DD_HH-MM-SS>_<slug>/` containing:

1. `README.md` — Read `assets/templates/readme.md`, fill the `<TOKENS>` (`<DIFFICULTY>` per the rubric, `<PIECE_NAME>`, `<SOURCE_PATH>`, `<PROBLEM_DESCRIPTION>`, `<EXAMPLES_BLOCK>` *happy-path only*, `<CONSTRAINTS_LIST>`, `<LANG>`, `<SIGNATURE_BLOCK>`), `Write` to the exercise dir.
2. `exercise.<ext>` — write the public signature plus a stub that fails clearly (e.g. `raise NotImplementedError`, `panic("not implemented")`, `throw new Error("not implemented")`). No hints.
3. `test_exercise.<ext>` — Read the matching `assets/templates/test_<lang>.<ext>`, fill `<PIECE_NAME>` and add the hidden edge / failure cases. Every assertion must carry a descriptive message; edge and failure cases live ONLY in this file, never in the README.
4. `run.sh` — copy the matching `assets/runners/<lang>.sh` to the exercise dir, `chmod +x`. Verbose by default; `[-q]` for quiet; `--list` + numeric index for *exact* test selection (TS / Go); `<test_name>` for pattern match; `--help` prints the full contract. See `references/reference.md` → "Phase 2 / 3: run.sh contract".

After all four files exist, run `bash scripts/quick_validate.sh <exercise-dir>` and address any failure before moving on. If file writes are declined or native tests are not safe to generate, present a conceptual exercise spec in chat instead (see `references/reference.md` → "Phase 2: Conceptual exercise fallback").

*Phase 3: Verify* — run the exercise's `run.sh`. If tests fail, give one conceptual nudge and let the user revise. If the agent cannot run tests, ask the user to paste the output before moving on.

*Phase 4: Capture* — draft per-piece notes that reflect what actually happened, regardless of outcome:

1. Compose a config dict (date, first_drilled, piece, source, confidence_before/after, status one of `owned` / `partial` / `explained-only` / `abandoned`, time_minutes, difficulty, tags, re_drills, and the body `sections`). Save to a temp JSON file.
2. Render: `python scripts/render_notes.py --config <tmp.json> > <exercise-dir>/notes.md`. The script handles status-conditional body layout.
3. Show the rendered draft to the user. Accept their edits (overwrite the file if they request changes). Never persist notes without approval.
4. After the file is written, update the workspace index: `python scripts/update_index.py --notes <exercise-dir>/notes.md`.
5. On re-drill of the same piece: append a new dated section to the existing `notes.md` (do not overwrite earlier sections), bump `re_drills`, then re-run `update_index.py`. See `references/reference.md` → "Phase 4: Re-drill append pattern".

**Step 3 — Session summary**

Briefly highlight what changed this session — pieces now owned, still partial, where the exercises live. `.unvibe/INDEX.md` is the authoritative log; the chat summary just calls out the deltas.

## Rules

- One phase at a time: never ask them to explain and reimplement in the same message.
- Never show the original code during Phase 2: they work from memory plus the problem statement and tests.
- Never reveal hidden edge/failure cases in the README — they surface only when a test goes red.
- Hints during Phase 2: one conceptual nudge only, never code.
- Keep generated tests behavioral. Do not assert private implementation details.
- `notes.md` is collaborative: agent drafts after each piece, user approves or edits, then it's written. Never save notes without showing the user the draft.
