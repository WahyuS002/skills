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

## Phase 2: Exercise Templates

Create exercises under `.unvibe/exercises/<YYYY-MM-DD>_<slug>/` only after the user approves file writes.

### README.md
```
# Exercise: <behavior-or-function-name>

**Source:** `<file-path>` -> `<symbol-or-behavior>`

**Goal:** [plain English behavior, no implementation hints]

**Your task:** Recreate the behavior from memory using the exercise file and tests/spec.

**Verify:** [native test command, or "Share your result/output here"]
```

### Runnable Native Exercise

Use this when the language and test runner are confidently detected. Match the repo's conventions for filenames, imports, package/module layout, and test command.

Exercise file:
```
[same public signature or smallest useful interface]

[minimal stub that fails clearly, without hints]
```

Test file:
```
[native test framework setup]

[happy path behavior]
[edge case behavior]
[bad input or failure behavior]
```

Tests must be the spec: enough to derive correct behavior, but not so detailed that they reveal the original implementation. Test observable behavior, not private structure.

### Conceptual Exercise

Use this when runner detection is unclear, file writes are declined, or runnable tests would require unsafe scaffolding.

```
# Conceptual Exercise: <behavior-or-function-name>

Reimplement this behavior in the project style:

1. Happy path: [observable input/output or state change]
2. Edge case: [boundary behavior]
3. Failure case: [error, rejection, or fallback behavior]

When done, explain the implementation choices and share test output if available.
```

### JS/TS Example

Only use this shape when `package.json` and the repo test setup make it safe.

```typescript
// exercise.ts
export function functionName(param: Type): ReturnType {
  throw new Error("Not implemented")
}
```

```typescript
// exercise.test.ts
import { describe, it, expect } from "vitest"
import { functionName } from "./exercise"

describe("functionName", () => {
  it("handles the happy path", () => { /* behavior assertion */ })
  it("handles an edge case", () => { /* behavior assertion */ })
  it("throws or rejects on bad input", () => { /* behavior assertion */ })
})
```

Run with the repo's detected command, such as `npm test -- .unvibe/exercises/<date>_<slug>` or `npx vitest run .unvibe/exercises/<date>_<slug>`.

## Candidate Identification Priorities

1. External API calls or library methods the user may have never typed themselves
2. Core business logic (the "why" behind the code, not just the "what")
3. Patterns that look simple but have non-obvious behavior
4. Error handling or edge cases the agent added without discussion
5. Any function the user would struggle to rewrite from memory

Skip: trivial getters/setters, boilerplate, code self-evident from its name.

## Verification

- Prefer running the detected test command yourself when you have repo access.
- If tests fail, explain the failing behavior in plain language and give one conceptual nudge, not code.
- If you cannot run tests, ask the user to paste the command output before marking the exercise complete.
