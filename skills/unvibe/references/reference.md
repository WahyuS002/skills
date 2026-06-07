# Unvibe — Reference

This file holds **guidance** (rubrics, priorities, format adaptations) that does not change per-exercise. Per-exercise **templates** live under `assets/`, and **executable helpers** under `scripts/`. SKILL.md tells the agent when to reach for each.

## Contents

- [Phase 1: Question forms](#phase-1-question-forms)
- [Phase 1: Evaluation rubric](#phase-1-evaluation-rubric)
- [Phase 2: Exercise layout + asset map](#phase-2-exercise-layout--asset-map)
- [Phase 2: Right-sizing — slice large pieces into a progression](#phase-2-right-sizing--slice-large-pieces-into-a-progression)
- [Phase 2: Difficulty rubric](#phase-2-difficulty-rubric)
- [Phase 2: Examples rule (happy-path only)](#phase-2-examples-rule-happy-path-only)
- [Reference grounding (external-surface facts)](#reference-grounding-external-surface-facts)
- [Phase 2: Conceptual exercise fallback](#phase-2-conceptual-exercise-fallback)
- [Phase 2 / 3: run.sh contract](#phase-2--3-runsh-contract)
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

## Phase 2: Right-sizing — slice large pieces into a progression

Before generating, decide whether the piece fits a single stub or needs to be **sliced**. One oversized stub is the most common way an exercise stops being a *learning* tool and becomes a wall the user bounces off — they don't know where to start, so they paste the original or give up.

**Slice when any of these hold:**

- The piece has more than one responsibility (e.g. computes layout *and* writes cells *and* wires validation).
- The user rated confidence low (fuzzy, or 1–2 of 5) in Phase 1.
- A faithful one-shot stub would be HARD, or more than ~25–30 lines to reimplement from memory.

Keep it a **single** exercise when the piece is one cohesive idea (a pure transform, one guarded branch, one API call). Don't slice for slicing's sake — 2 steps is the floor; if you can't find at least two genuinely separable sub-skills, it isn't a slice candidate.

**Layout.** The timestamped dir becomes a *container*; each step is its own leaf exercise in a subdir:

```
<YYYY-MM-DD_HH-MM-SS>_<slug>/
  README.md                 <- progression map (skeleton below); first line carries the OVERALL difficulty tag
  step1_<slug>/             <- leaf: exercise.<ext> + test_exercise.<ext> + run.sh (chmod +x)
  step2_<slug>/
  ...
  stepN_<slug>/             <- final step = COMPOSE the earlier pieces into the whole
  notes.md                  <- Phase 4, written once for the whole piece (container level)
```

Each `stepN_<slug>/` is a normal leaf exercise (same four files, same `run.sh` contract). The user does them in order: `cd step1_<slug> && ./run.sh`.

**Ordering — easy → hard, concrete → orchestration:**

1. **Pure functions first** — the small, side-effect-free helpers (mappings, calculations, guards). Usually EASY; they build momentum and confidence.
2. **Stateful / library-touching steps next** — functions that mutate state, call the framework/library, or return the value a later step depends on (the "bridge" value).
3. **The final step is always composition** — the real top-level function, reassembled from the steps just owned. By now it reads as a few lines of orchestration; *that realization is the payoff* ("the scary function was just glue").

**Give earlier solutions forward.** From step 2 on, paste the reference solution of every earlier helper into the step's stub file under a clearly marked block:

```python
# --- GIVEN (solved in earlier steps — do not edit) ---
def helper_from_step1(...): ...
# --- TODO: implement this step ---
def new_function(...):
    raise NotImplementedError(...)
```

This lets the user implement only the new function, see how the pieces connect, and compare the given solution against the answer they wrote earlier. The final compose-step provides *all* helpers as GIVEN; the user writes only the orchestration.

**Per-step difficulty.** Each step carries its own EASY/MEDIUM/HARD rating in the parent README's progression table (apply the difficulty rubric per step). The parent README's first-line tag is the *overall* difficulty — normally the hardest step.

**Parent README skeleton** (this is the container README; it replaces the single-exercise `assets/templates/readme.md` for sliced pieces — the leaf step READMEs are optional, keep the per-step problem statement in the step's `exercise.<ext>` docstring/comment if you skip them):

```
# [<OVERALL_DIFFICULTY>] <piece> — sliced into <N> steps

**Source:** `<source-path>` -> `<symbol>`

Why sliced: <one line>. Do the steps in order; each is its own folder with its own run.sh.

| Step | Folder | What you own | Level |
|-----:|--------|--------------|-------|
| 1 | `step1_<slug>/` | <pure helper …> | EASY |
| … |
| N | `stepN_<slug>/` | compose into `<piece>` | MEDIUM |

How to run each step: `cd step1_<slug> && ./run.sh`   (full contract: ./run.sh --help)
```

Embed the relevant doc links (see "Reference grounding") next to the calls each step uses — a per-step convenience that matters most when the user has no editor autocomplete.

**Validation & later phases.** `quick_validate.sh <container-dir>` auto-detects the sliced layout (presence of `stepN_*/` subdirs) and validates each step as a leaf (executable `run.sh` + a test file + an exercise stub) plus the container README's difficulty tag. Run **Phase 3 per step, in order**. Capture **Phase 4 notes once** for the whole piece, at the container level, after the final compose-step is green — the gotchas from individual steps become the bullets in *Gotchas I missed at first*.

## Phase 2: Difficulty rubric

The `<DIFFICULTY>` placeholder in `assets/templates/readme.md` is one of `EASY` / `MEDIUM` / `HARD`. Apply this rubric so labels stay comparable across exercises:

- **EASY** — pure transformation, single branch or simple guard, no state, no concurrency, no external API.
- **MEDIUM** — multi-way branching driven by a small invariant set (e.g. whitelist + normalization + edge guard), OR a single external library call whose decoded payload needs non-trivial handling.
- **HARD** — at least two of: concurrency / thread-safety, mutable state shared across calls, non-trivial algorithm (timing math, data structure), security-sensitive error collapsing, external API with retry / expiry semantics.

## Phase 2: Examples rule (happy-path only)

Every entry under `## Examples` in the generated README must be a **successful outcome**. Failure cases — including the most basic missing-input / 401 / 4xx / validation error — MUST NOT appear in Examples. If an Example's Output is an error, status code, or `{ok:false, ...}`, delete it and move that case to the hidden tests.

Examples prove the function is *reachable*; tests prove it's *correct*. This rule is enforced as much by `quick_validate.sh` as by your judgment — but the script can't tell semantic happy-path from semantic failure, so the human-judgement part stays with you.

## Reference grounding (external-surface facts)

When you author an exercise (or explain a fuzzy piece in Phase 1), you will state facts. Some you authored; some belong to the platform. **Ground the platform ones against a real source before asserting them, and surface the vetted links in the Phase 4 notes** — never in the Phase 2 README.

**The author-vs-platform test.** Ask of each load-bearing claim: *did I author this fact, or did the platform/spec?*

- **Authored** — claims about *this* code's behavior ("the handler routes `ArrowRight` to `next()`", "the refill rounds down"). No external source exists; never ground these.
- **External-surface** — behavior of a platform, standard library, framework, language spec, third-party API, or protocol that you did **not** write: DOM semantics (`tagName` is uppercase for HTML elements), stdlib contracts, framework lifecycle, HTTP status meanings, a library method's documented behavior. These are exactly candidate-priority #1 ("API calls or library methods the user may have never typed themselves"). **Ground every external-surface fact you assert.**

**How to ground (during authoring / explanation).**

1. Before writing an external-surface fact as an *absolute* ("X is always Y", "you can rely on this"), verify it with `WebSearch` / `WebFetch` against the canonical doc (MDN, language/stdlib docs, the library's own reference).
2. If verified → you may assert it, and record the link for the Phase 4 trail (see entry format below).
3. If you **cannot** verify it (web unavailable, page not found, uncertain) → **downgrade the wording from an absolute to a hedge** ("assume uppercase for this exercise; verify for your environment") and make sure the hidden tests do **not** silently bake in the unverified fact. Do not block exercise generation over this.

**The one non-negotiable: never emit a citation URL you did not actually fetch.** A plausible-looking-but-fabricated link is strictly worse than no link — it launders a hallucination as authority. No web access this session ⇒ no links in the trail, and hedge the prose.

**Trail entry format (Phase 4 notes, `Further reading` section).** One verified link, one line on the exact fact it grounds:

```
- [Element.tagName — MDN](https://developer.mozilla.org/en-US/docs/Web/API/Element/tagName) — confirms tagName is uppercase for HTML elements (the INPUT/TEXTAREA guard)
```

The `Further reading` section is rendered by `scripts/render_notes.py` for `owned` / `partial` / `explained-only` only, and only when non-empty. `abandoned` never carries it; a session that asserted no external-surface facts gets no section at all.

## Phase 2: Conceptual exercise fallback

Use when runner detection is unclear, file writes are declined, or runnable tests would require unsafe scaffolding. Keep the same Problem / Examples / Constraints / Signature structure as the README template, but the user reports results in chat instead of running `run.sh`. No `assets/runners/*.sh` is needed; no `quick_validate.sh` check is required.

## Phase 2 / 3: run.sh contract

Every `assets/runners/*.sh` template exposes the same five-mode CLI so the user gets a consistent experience across languages. The README template advertises this contract under "How to run"; the `run.sh` itself prints the full contract via `./run.sh --help`.

| Command | Behaviour | Notes |
|---|---|---|
| `./run.sh` | Run all tests, verbose | `-s -v` (pytest), `-v` (go test), `--reporter verbose` (vitest) |
| `./run.sh -q` | Run all tests, quiet | Default reporter / no `-v` / `-q` (pytest) |
| `./run.sh --list` *(ts/go only)* | List every test with index numbers | pytest is skipped here — its `::name` is already exact |
| `./run.sh <N>` *(ts/go only)* | Run test #N from `--list` (exact) | Numeric index resolves to anchored regex (`^Name$` for go) or to the resolved vitest name |
| `./run.sh <name>` | Run by name pattern | pytest `::name` (exact), vitest `-t` (substring), go test `-run` (regex) |
| `./run.sh -h` / `--help` | Print runner usage + language notes, then exit | Each runner ships an inline header comment AND a `cat <<EOF` help block |

**Why the index mode exists.** vitest `-t` and `go test -run` are substring/regex matches against free-form descriptions (or against identifiers prone to prefix collisions, like `TestFoo` matching `TestFooBar`). The numeric index sidesteps the matching semantics entirely — it resolves to a stable test name and either passes it verbatim (vitest) or wraps it in `^…$` anchors (go test). Use this whenever the user says "run exactly that one".

**Why python doesn't get `--list`.** pytest's `::` separator already provides an exact, identifier-based selector; layering an index would be ceremony with no upside. The python runner still ships `--help` for consistency.

**Multi-word name patterns must be quoted.** Without quotes the shell splits the description into separate `argv` entries, and only `$1` reaches the runner — a footgun that historically caused over-matched runs. The `--help` text explicitly warns about this.

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
