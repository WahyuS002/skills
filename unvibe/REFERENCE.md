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

## Phase 2: File Templates

### README.md
```
# Exercise: <function-name>

**Source:** `<file-path>` → `<function-name>`

**What it should do:** [plain English, no code, no hints]

**Run tests:** npx vitest run exercises/<date>_<name>
```

### exercise.ts
```typescript
// No hints beyond the signature and types
export function functionName(param: Type): ReturnType {
  throw new Error("Not implemented")
}
```

### exercise.test.ts
```typescript
import { describe, it, expect } from "vitest"
import { functionName } from "./exercise"

describe("functionName", () => {
  it("handles the happy path", () => { ... })
  it("handles an edge case", () => { ... })
  it("throws or rejects on bad input", () => { ... })
})
```

Tests must be the spec — the user should be able to derive the implementation from them alone. Test behavior, not implementation details.

## Candidate Identification Priorities

1. External API calls or library methods the user may have never typed themselves
2. Core business logic (the "why" behind the code, not just the "what")
3. Patterns that look simple but have non-obvious behavior
4. Error handling or edge cases Claude added without discussion
5. Any function the user would struggle to rewrite from memory

Skip: trivial getters/setters, boilerplate, code self-evident from its name.
