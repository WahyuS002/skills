# Unvibe — Reference

## Phase 1: Question Forms

- "Explain what `X` does — not line by line, but what problem it solves and how."
- "Walk me through what happens when `X` is called with a bad input."
- "Why does this use `Y` instead of just doing `Z`?"
- "What would break if you removed this line?"

## Phase 1: Evaluation Rubric

- **Solid** (✅): Got the intent and mechanism → move to Phase 2
- **Partial** (⚠️): Understands what but not why (or vice versa) → one follow-up → Phase 2
- **Fuzzy** (❌): Guessing → explain yourself in 3–4 sentences → ask them to repeat back → Phase 2

## Phase 2: Exercise Layout

Create exercises under `.unvibe/exercises/<YYYY-MM-DD_HH-MM-SS>_<slug>/` only after the user approves file writes. The timestamp uses dashes and underscores only (no colon) so the path is safe on every OS and shell.

```
.unvibe/exercises/2026-05-27_14-30-05_choose-strategy/
  README.md          # LeetCode-style problem statement
  exercise.<ext>     # signature + failing stub, no hints
  test_exercise.<ext># behavioral tests = the hidden judge
  run.sh             # language-aware runner (chmod +x)
```

### README.md — LeetCode-style problem

```
# [MEDIUM] <behavior-or-function-name>

**Source:** `<file-path>` -> `<symbol-or-behavior>`

## Problem
[plain-English description of what to build]

## Examples
[2–3 concrete happy-path Input→Output pairs only]
Input:  <args>
Output: <result>

## Constraints
- [input domain, invariants, required fallbacks]

## Signature
<exact public signature in the detected language>
```

- **Difficulty** (`EASY`/`MEDIUM`/`HARD`) is assigned with this rubric, so labels stay comparable across exercises:
  - `EASY` — pure transformation, single branch or simple guard, no state, no concurrency, no external API.
  - `MEDIUM` — multi-way branching driven by a small invariant set (e.g. whitelist + normalization + edge guard), OR a single external library call whose decoded payload needs non-trivial handling.
  - `HARD` — at least two of: concurrency / thread-safety, mutable state shared across calls, non-trivial algorithm (timing math, data structure), security-sensitive error collapsing, external API with retry / expiry semantics.
- **Examples are happy-path only.** Every entry under `## Examples` must be a successful outcome. Failure cases — including the most basic missing-input / 401 / 4xx / validation error — MUST NOT appear in Examples. If an Example's Output is an error, status code, or `{ok:false, ...}`, delete it and move that case to the hidden tests. Examples prove the function is *reachable*; tests prove it's *correct*.

### Test file — the hidden judge

Tests are the spec: enough to derive correct behavior, not so detailed they reveal the original implementation. Test observable behavior, not private structure. Every assertion carries a descriptive message (case label + expected vs actual) so a failure explains itself without `-s`/print. Do NOT print expected values on success — that leaks hidden cases.

```python
# test_exercise.py (pytest)
from exercise import choose_strategy

def test_indonesian_with_caption_uses_asr_primary():
    got = choose_strategy("id", True)
    assert got == "asr_primary", f"id+caption harus 'asr_primary', dapat '{got}'"

def test_unknown_lang_falls_back():  # hidden edge case
    got = choose_strategy("xx", True)
    assert got == "asr", f"unknown lang harus fallback 'asr', dapat '{got}'"

def test_empty_lang_raises():        # hidden failure case
    import pytest
    with pytest.raises(ValueError):
        choose_strategy("", True)
```

### Conceptual Exercise (fallback)

Use when runner detection is unclear, file writes are declined, or runnable tests would require unsafe scaffolding. Keep the same problem/examples/constraints structure, but the user reports results in chat instead of running `run.sh`.

## Phase 2: run.sh

One self-contained runner per exercise. Make it executable (`chmod +x run.sh`). Interface for every language:

```
./run.sh                     # all tests, verbose (shows logs)
./run.sh <test_name>         # one test function, verbose
./run.sh -q                  # all tests, quiet summary
./run.sh -q <test_name>      # one test function, quiet
```

The script resolves its own directory, so it works from anywhere. Pick the body that matches the detected language.

### Python (pytest)

```bash
#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
QUIET=0; [ "${1:-}" = "-q" ] && { QUIET=1; shift; }
TEST="${1:-}"
SEL="$DIR/test_exercise.py"
[ -n "$TEST" ] && SEL="$SEL::$TEST"
if [ "$QUIET" = 1 ]; then
  exec python3 -m pytest "$SEL" -q
else
  exec python3 -m pytest "$SEL" -s -v   # -s shows print/log
fi
```

### Go (go test)

```bash
#!/usr/bin/env bash
# Branches written out explicitly so the script stays safe under macOS
# bash 3.2 + `set -u` (an empty array + "${ARGS[@]}" would error there).
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"; cd "$DIR"
QUIET=0; [ "${1:-}" = "-q" ] && { QUIET=1; shift; }
TEST="${1:-}"
if [ "$QUIET" = 1 ]; then
  if [ -n "$TEST" ]; then exec go test -run "$TEST" ./...
  else                    exec go test ./...; fi
else
  if [ -n "$TEST" ]; then exec go test -v -run "$TEST" ./...   # -v streams t.Log output
  else                    exec go test -v ./...; fi
fi
```

### JS/TS (vitest)

```bash
#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
QUIET=0; [ "${1:-}" = "-q" ] && { QUIET=1; shift; }
TEST="${1:-}"
ARGS=(run "$DIR/exercise.test.ts"); [ -n "$TEST" ] && ARGS+=(-t "$TEST")
if [ "$QUIET" = 1 ]; then
  exec npx vitest "${ARGS[@]}"
else
  exec npx vitest "${ARGS[@]}" --reporter verbose
fi
```

For other stacks, keep the same `[-q] [test_name]` interface and map verbose to the runner's "show logs + per-test names" flags, quiet to its summary mode.

## Phase 4: Capture (notes.md + INDEX.md)

Persist what was learned (or where it got stuck) so future-them can pick the piece up cold months later. The agent **drafts**, the user **approves or edits**, then the file is written. Notes are written regardless of outcome — the `status` field reflects reality, not just successes.

### notes.md — per-piece

`.unvibe/exercises/<ts>_<slug>/notes.md`. One file per piece. On a re-drill of the same piece, append a new dated section to the bottom and update the frontmatter to the latest state; never overwrite earlier sections.

```
---
date: <YYYY-MM-DD>            # latest drill
first_drilled: <YYYY-MM-DD>   # set on first write, preserved on re-drill
piece: <symbol-or-behavior>
source: <file-path>
confidence_before: <fuzzy | partial | solid>
confidence_after:  <fuzzy | partial | solid>
status: <owned | partial | explained-only | abandoned>
time_minutes: <int>
difficulty: <EASY | MEDIUM | HARD>   # mirrors the README label
tags: [<short>, <free-form>, <list>]
re_drills: <int>              # 0 on first write
---

# <piece> — <status> <date>

## What it does (in 2 lines)
[plain-English behavior, not line-by-line]

## The non-obvious part (the "why")
[the design decision that wasn't obvious from reading the code]

## Gotchas I missed at first
- [specific case the user got wrong or didn't see in Phase 1]
- [edge case surfaced by a hidden test going red]

## My reimplementation choice
[what shape the user used in Phase 2 and why — short]

## What to re-check in 3 months
[the question future-them should be able to answer; the trap to avoid]
```

Body sections adapt to `status`:

- **`owned`** — all five sections above.
- **`partial`** — keep "Gotchas" and "Reimpl choice" if Phase 2/3 ran far enough to produce them, and add a final **`## What I'm still stuck on`**.
- **`explained-only`** — drop "Reimpl choice"; add **`## Why I didn't drill further`** (often: "Phase 1 was solid, didn't need the reimplementation").
- **`abandoned`** — minimal: "What it does" (whatever was reached) plus **`## Why I stopped`**.

### Re-drill: append, don't overwrite

When the same piece is drilled again later, append a dated section above the prior content and update the frontmatter. Future-them benefits from seeing the trajectory ("I forgot this exact gotcha 3 months ago too").

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

### INDEX.md — workspace-level

`.unvibe/INDEX.md`. A single table, **one row per piece** (not per drill). On re-drill, update the existing row's `Date`, `Status`, and `Conf.` in place; do not append a duplicate row. Add a `(×N)` suffix to `Status` to mark re-drill count.

```
# Unvibe ownership log

| Date       | Piece            | Source             | Status       | Conf. |
|------------|------------------|--------------------|--------------|-------|
| 2026-05-28 | choose_strategy  | process_video.py   | owned        | ✅    |
| 2026-05-28 | process_video    | process_video.py   | partial      | ⚠️    |
| 2026-08-15 | choose_strategy  | process_video.py   | owned (×2)   | ✅    |
```

Conf. icons: `✅` solid, `⚠️` partial, `❓` fuzzy. The INDEX is the authoritative log; the session-end summary in chat just calls out the deltas.

## Candidate Identification Priorities

1. External API calls or library methods the user may have never typed themselves
2. Core business logic (the "why" behind the code, not just the "what")
3. Patterns that look simple but have non-obvious behavior
4. Error handling or edge cases the agent added without discussion
5. Any function the user would struggle to rewrite from memory

Shortlist up to 3 (1–3). Skip trivial getters/setters, boilerplate, code self-evident from its name. Never pad the list with weak candidates to reach 3.

## Verification

- Prefer running the exercise's `run.sh` yourself when you have repo access.
- If tests fail, explain the failing behavior in plain language and give one conceptual nudge, not code.
- If you cannot run tests, ask the user to paste the `run.sh` output before marking the exercise complete.
