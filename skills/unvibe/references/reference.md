# Unvibe — Reference

This file holds **guidance** (rubrics, priorities, format adaptations) that does not change per-exercise. Per-exercise **templates** live under `assets/`, and **executable helpers** under `scripts/`. SKILL.md tells the agent when to reach for each.

## Contents

- [Phase 1: Question forms](#phase-1-question-forms)
- [Phase 1: Evaluation rubric](#phase-1-evaluation-rubric)
- [Phase 2: Exercise layout + asset map](#phase-2-exercise-layout--asset-map)
- [Phase 2: Difficulty rubric](#phase-2-difficulty-rubric)
- [Phase 2: Examples rule (happy-path only)](#phase-2-examples-rule-happy-path-only)
- [Phase 2: Conceptual exercise fallback](#phase-2-conceptual-exercise-fallback)
- [Phase 4: Notes body adaptations per status](#phase-4-notes-body-adaptations-per-status)
- [Phase 4: Re-drill append pattern](#phase-4-re-drill-append-pattern)
- [Candidate identification priorities](#candidate-identification-priorities)
- [Verification](#verification)

## Phase 1: Question forms

- "Explain what `X` does — not line by line, but what problem it solves and how."
- "Walk me through what happens when `X` is called with a bad input."
- "Why does this use `Y` instead of just doing `Z`?"
- "What would break if you removed this line?"

## Phase 1: Evaluation rubric

- **Solid** (✅): Got the intent and mechanism → move to Phase 2.
- **Partial** (⚠️): Understands what but not why (or vice versa) → one follow-up → Phase 2.
- **Fuzzy** (❓): Guessing → explain yourself in 3–4 sentences → ask them to repeat back → Phase 2.

## Phase 2: Exercise layout + asset map

Each exercise dir under `.unvibe/exercises/<YYYY-MM-DD_HH-MM-SS>_<slug>/` should end up with:

```
README.md          <- copy of assets/templates/readme.md, placeholders filled
exercise.<ext>     <- signature + failing stub, written inline by the agent
test_exercise.<ext><- copy of the matching assets/templates/test_<lang>.<ext>,
                     placeholders filled, hidden cases added
run.sh             <- copy of assets/runners/<lang>.sh, chmod +x
```

Templates use `<TOKENS>` (e.g. `<DIFFICULTY>`, `<PIECE_NAME>`) that the agent substitutes. Workflow:

1. `Read` the template from `assets/`.
2. Apply substitutions in memory.
3. `Write` the substituted file to the exercise dir.

After all four files are in place, run `bash scripts/quick_validate.sh <exercise-dir>` as a shape-check before handing off to Phase 3.

## Phase 2: Difficulty rubric

The `<DIFFICULTY>` placeholder in `assets/templates/readme.md` is one of `EASY` / `MEDIUM` / `HARD`. Apply this rubric so labels stay comparable across exercises:

- **EASY** — pure transformation, single branch or simple guard, no state, no concurrency, no external API.
- **MEDIUM** — multi-way branching driven by a small invariant set (e.g. whitelist + normalization + edge guard), OR a single external library call whose decoded payload needs non-trivial handling.
- **HARD** — at least two of: concurrency / thread-safety, mutable state shared across calls, non-trivial algorithm (timing math, data structure), security-sensitive error collapsing, external API with retry / expiry semantics.

## Phase 2: Examples rule (happy-path only)

Every entry under `## Examples` in the generated README must be a **successful outcome**. Failure cases — including the most basic missing-input / 401 / 4xx / validation error — MUST NOT appear in Examples. If an Example's Output is an error, status code, or `{ok:false, ...}`, delete it and move that case to the hidden tests.

Examples prove the function is *reachable*; tests prove it's *correct*. This rule is enforced as much by `quick_validate.sh` as by your judgment — but the script can't tell semantic happy-path from semantic failure, so the human-judgement part stays with you.

## Phase 2: Conceptual exercise fallback

Use when runner detection is unclear, file writes are declined, or runnable tests would require unsafe scaffolding. Keep the same Problem / Examples / Constraints / Signature structure as the README template, but the user reports results in chat instead of running `run.sh`. No `assets/runners/*.sh` is needed; no `quick_validate.sh` check is required.

## Phase 4: Notes body adaptations per status

`scripts/render_notes.py` picks the body sections based on `status`:

- **`owned`** — five sections: *What it does* / *The non-obvious part* / *Gotchas I missed at first* / *My reimplementation choice* / *What to re-check in 3 months*.
- **`partial`** — same five, plus *What I'm still stuck on* at the bottom.
- **`explained-only`** — *What it does* / *The non-obvious part* / *Gotchas I missed at first* / *Why I didn't drill further*. Drop *My reimplementation choice* (no Phase 2 happened).
- **`abandoned`** — minimal: *What it does* (whatever was reached) plus *Why I stopped*.

The render script is the source of truth. If you find yourself wanting to add or remove a section, edit `scripts/render_notes.py`'s `SECTIONS_BY_STATUS`, then update this list.

## Phase 4: Re-drill append pattern

When the same piece is drilled again later, **append** a dated section above the prior content and update the frontmatter `date`, `re_drills`, and (if changed) `status` / `confidence_after`. Never overwrite earlier sections.

```
---
date: 2026-08-15            # latest
first_drilled: 2026-05-28
re_drills: 1
status: owned
...
---

# choose_strategy — owned 2026-08-15

## 2026-08-15 re-drill (still owned)

### What I forgot since last time
- [the gotcha that returned]

### Refresher (delta from original)
[only the points needed to re-anchor; not a full rewrite]

---

## 2026-05-28 original
[original notes preserved verbatim]
```

After appending, run `python scripts/update_index.py --notes <path>` so the workspace INDEX reflects the latest state.

## Candidate identification priorities

When choosing the shortlist (Step 1), prioritise:

1. External API calls or library methods the user may have never typed themselves.
2. Core business logic (the "why" behind the code, not just the "what").
3. Patterns that look simple but have non-obvious behavior.
4. Error handling or edge cases the agent added without discussion.
5. Any function the user would struggle to rewrite from memory.

Shortlist up to 3 (1–3). Skip trivial getters / setters, boilerplate, code self-evident from its name. Never pad the list with weak candidates to reach 3.

## Verification

- Prefer running the exercise's `run.sh` yourself when you have repo access.
- If tests fail, explain the failing behavior in plain language and give one conceptual nudge, not code.
- If you cannot run tests, ask the user to paste the `run.sh` output before marking the exercise complete.
- Independent of Phase 3, run `bash scripts/quick_validate.sh <exercise-dir>` to confirm the exercise dir itself is well-formed (correct dir-name format, README has a difficulty tag, run.sh is executable, test + stub files present). This catches shape problems regardless of whether the test toolchain is available.
