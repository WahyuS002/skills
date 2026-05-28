#!/usr/bin/env python3
import json
from pathlib import Path

IT = Path(__file__).parent / "iteration-1"

# Grades per (eval_name, config): list of (passed, evidence) in assertion order (6).
# Plus optional notes (workarounds/uncertainties).
GRADES = {
    ("python-video-strategy", "new_skill"): {
        "g": [
            (True,  "Shortlist had exactly 3 candidates (choose_strategy, CAPTION_RELIABLE/asr_primary path, process_video chunking)."),
            (True,  "Dir name '2026-05-27_14-48-22_choose-strategy' matches YYYY-MM-DD_HH-MM-SS_<slug> (seconds present, no colon)."),
            (True,  "README has '[MEDIUM]' difficulty, Examples with Input->Output, Constraints, and a Python Signature block."),
            (True,  "Examples show only the 3 normal outcomes (caption/asr_primary/asr); the empty-lang ValueError is hidden in tests, not the README."),
            (True,  "run.sh executable; default branch 'pytest -s -v' (verbose), -q toggles quiet, optional arg appends ::TEST for a single function."),
            (True,  "pytest assertions carry messages like f\"en+caption should be 'caption', got '{got}'\" (expected-vs-actual)."),
        ],
        "notes": {},
    },
    ("python-video-strategy", "old_skill"): {
        "g": [
            (True,  "Shortlist had 3 candidates (within the old 3-5 range)."),
            (False, "Dir name '2026-05-27_choose-strategy' has date only, no HH-MM-SS."),
            (False, "README is Goal/Your task/Verify prose; no Difficulty, no Input->Output Examples, no Constraints section, no Signature block."),
            (False, "README spells out edge/failure behavior in prose ('required language input must be present', 'case-insensitive') rather than hiding it in tests."),
            (False, "run.sh hardcodes 'python -m pytest -q' (quiet only) with no verbose default, no -q toggle, and no single-test argument."),
            (False, "Tests use bare asserts (e.g. assert choose_strategy('en',True)=='caption') with no failure messages."),
        ],
        "notes": {},
    },
    ("go-ratelimiter-refill", "new_skill"): {
        "g": [
            (True,  "Shortlist had exactly 3 candidates (AllowN refill math, NewTokenBucket init, lazy-refill pattern)."),
            (True,  "Dir name '2026-05-27_14-48-48_allown-refill' matches YYYY-MM-DD_HH-MM-SS_<slug>."),
            (True,  "README has '[MEDIUM]' difficulty, Problem, Examples with Input->Output, Constraints, and a Go Signature block."),
            (True,  "Examples show only normal allow/deny behavior; concurrency and zero-request edge cases are hidden in the tests."),
            (False, "run.sh has the right interface (verbose -v default, -q, -run TEST) BUT crashes on the default and -q paths under macOS bash 3.2: 'ARGS=()' + 'set -u' + \"${ARGS[@]}\" => 'ARGS[@]: unbound variable'. Default invocation is broken."),
            (True,  "Go tests use rich t.Errorf/t.Fatalf messages reporting case + expected-vs-actual."),
        ],
        "notes": {"workarounds": ["Go run.sh template fails under bash 3.2 (macOS default) on empty ARGS array with set -u; only works when a test name is passed."]},
    },
    ("go-ratelimiter-refill", "old_skill"): {
        "g": [
            (False, "Shortlist had 4 candidates (exceeds the <=3 target; allowed under the old 3-5 rule)."),
            (False, "Dir name '2026-05-27_allown-refill' has date only, no HH-MM-SS."),
            (False, "README is Goal/Your task/Verify prose; no Difficulty, Examples, Constraints, or Signature block."),
            (False, "README describes edge behavior (all-or-nothing, capacity cap) in prose rather than hiding it in tests."),
            (False, "run.sh hardcodes 'go test ... -v' with no -q toggle and no single-test argument."),
            (False, "Go tests use t.Fatal with intent-only messages (e.g. 'should deny once empty'); they do not report expected-vs-actual values."),
        ],
        "notes": {},
    },
    ("ts-jwt-verify", "new_skill"): {
        "g": [
            (True,  "Shortlist had exactly 3 candidates (verifyAuth+jwt.verify, Bearer parsing, error-collapsing decision)."),
            (True,  "Dir name '2026-05-27_14-49-05_verify-auth' matches YYYY-MM-DD_HH-MM-SS_<slug>."),
            (True,  "README has '[MEDIUM]' difficulty, Problem, Examples with Input->Output, Constraints, and a TS Signature block."),
            (False, "README Examples leak a failure case: it shows req={headers:{}} -> {ok:false,401,'missing bearer token'}. Non-success cases should stay in the hidden tests; only this most-basic guard leaked (wrong-scheme/bad-sig/expired/malformed are correctly hidden)."),
            (True,  "run.sh executable; default '--reporter verbose', -q toggles quiet, optional arg maps to vitest -t. ARGS initialized non-empty so no unbound-var bug."),
            (True,  "vitest assertions use descriptive 2nd-arg messages with case + expected-vs-got (e.g. 'bad signature: expected {...}, got ...')."),
        ],
        "notes": {"uncertainties": ["README Examples included one failure mapping (missing-header 401); minor leak of the easiest hidden case."]},
    },
    ("ts-jwt-verify", "old_skill"): {
        "g": [
            (False, "Shortlist had 4 candidates (exceeds <=3 target)."),
            (False, "Dir name '2026-05-27_verify-auth' has date only, no HH-MM-SS."),
            (False, "README is Goal/Your task/Verify prose; no Difficulty, Examples, Constraints, or Signature block."),
            (False, "README describes failure behavior in prose ('report unauthorized without leaking why', expired-vs-malformed) instead of hiding it in tests."),
            (False, "run.sh hardcodes 'npx vitest run <dir>' with no verbose flag, no -q toggle, and no single-test argument."),
            (False, "vitest assertions are bare expect().toBe()/.toEqual() with no descriptive messages; rely on default terse output."),
        ],
        "notes": {},
    },
}


def main():
    for ev in sorted(IT.glob("eval-*")):
        meta = json.loads((ev / "eval_metadata.json").read_text())
        assertions = meta["assertions"]
        name = meta["eval_name"]
        for cfg in ["new_skill", "old_skill"]:
            entry = GRADES[(name, cfg)]
            grades = entry["g"]
            exps = []
            for text, (passed, evidence) in zip(assertions, grades):
                exps.append({"text": text, "passed": passed, "evidence": evidence})
            passed = sum(1 for e in exps if e["passed"])
            total = len(exps)
            grading = {
                "expectations": exps,
                "summary": {
                    "passed": passed,
                    "failed": total - passed,
                    "total": total,
                    "pass_rate": round(passed / total, 4),
                },
                "execution_metrics": {"errors_encountered": 0},
            }
            notes = entry.get("notes") or {}
            if notes:
                grading["user_notes_summary"] = {
                    "uncertainties": notes.get("uncertainties", []),
                    "needs_review": notes.get("needs_review", []),
                    "workarounds": notes.get("workarounds", []),
                }
            rd = ev / cfg / "run-1"
            (rd / "grading.json").write_text(json.dumps(grading, indent=2))
            print(f"{name:24s} {cfg:10s} -> {passed}/{total}  ({grading['summary']['pass_rate']})")


if __name__ == "__main__":
    main()
