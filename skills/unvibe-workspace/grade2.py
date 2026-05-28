#!/usr/bin/env python3
import json
from pathlib import Path

IT = Path(__file__).parent / "iteration-2"

GRADES = {
    ("python-video-strategy", "new_skill"): {
        "g": [
            (True,  "Shortlist had 2 candidates (choose_strategy, process_video chunking); skill correctly refused to pad to 3."),
            (True,  "Dir '2026-05-28_10-20-03_choose-strategy' matches YYYY-MM-DD_HH-MM-SS_<slug>."),
            (True,  "README has '[MEDIUM]' difficulty, 3 Input->Output Examples, Constraints, and Python Signature."),
            (True,  "Examples are 3 success outcomes (caption/asr_primary/asr); Constraints alludes to defensive input but no failure mapping shown in Examples."),
            (True,  "run.sh executable; verbose 'pytest -s -v' default, '-q' toggles quiet, optional ::TEST argument for one function."),
            (True,  "pytest assertions use rich f-string messages with case label + expected-vs-got."),
        ],
        "notes": {},
    },
    ("python-video-strategy", "old_skill"): {
        "g": [
            (True,  "Shortlist had 2 candidates; iter-1-new skill already enforced the no-pad rule."),
            (True,  "Dir '2026-05-28_10-19-58_choose-strategy' matches YYYY-MM-DD_HH-MM-SS_<slug> (iter-1-new already had seconds)."),
            (True,  "README has '[MEDIUM]', 3 Examples, Constraints, Signature."),
            (True,  "Examples show only success outcomes; Constraints alludes to bad-input handling without spelling out the Output."),
            (True,  "run.sh template same as new (Python template unchanged across iter-1->iter-2)."),
            (True,  "pytest assertions use descriptive messages."),
        ],
        "notes": {},
    },
    ("go-ratelimiter-refill", "new_skill"): {
        "g": [
            (True,  "Shortlist had 2 candidates (AllowN refill math, TokenBucket thread-safety model); no padding."),
            (True,  "Dir '2026-05-28_10-20-10_token-bucket-allown' matches YYYY-MM-DD_HH-MM-SS_<slug>."),
            (True,  "README upgraded to '[HARD]' under the new rubric (concurrency + state + non-trivial math), with Problem, 3 Input->Output Examples, Constraints, Signature."),
            (True,  "All 3 Examples are success outcomes; refill/cap/denial semantics live only in hidden tests."),
            (True,  "run.sh uses the new bash-3.2-safe explicit if/else branches. Agent confirmed all three modes work: './run.sh', './run.sh -q', './run.sh TestName'. Iter-1's unbound-variable bug is FIXED."),
            (True,  "Go tests use rich t.Fatalf messages with case label + expected-vs-actual; added a recoverPanic helper for clean failure output on the unimplemented stub."),
        ],
        "notes": {},
    },
    ("go-ratelimiter-refill", "old_skill"): {
        "g": [
            (True,  "Shortlist had 1 candidate (AllowN refill math); legitimately just one substantive piece, no padding."),
            (True,  "Dir '2026-05-28_10-20-21_token-bucket-allown' matches YYYY-MM-DD_HH-MM-SS_<slug>."),
            (True,  "README has '[MEDIUM]', Problem, 3 Examples, Constraints, Signature."),
            (True,  "Examples show success outcomes (and a denied AllowN, which is a normal operational return for a rate limiter, not an error)."),
            (False, "run.sh generated from the buggy iter-1-new template: empty 'ARGS=()' + 'set -u' + \"${ARGS[@]}\" aborts under macOS bash 3.2. The eval agent had to patch it in place (with '${ARGS[@]+...}') to run the tests — the skill's emitted run.sh would not have worked default/-q."),
            (True,  "Go tests use descriptive t.Fatalf messages with expected-vs-actual."),
        ],
        "notes": {"workarounds": ["Iter-1-new (=this run's baseline) Go run.sh template still crashes on macOS bash 3.2; agent patched run.sh in-place after generation. This is exactly the bug iter-2 fixed."]},
    },
    ("ts-jwt-verify", "new_skill"): {
        "g": [
            (True,  "Shortlist had 3 candidates (verifyAuth flow, error-collapsing, Bearer parsing)."),
            (True,  "Dir '2026-05-28_10-20-35_verify-auth-bearer' matches YYYY-MM-DD_HH-MM-SS_<slug>."),
            (True,  "README upgraded to '[HARD]' under the new rubric (security-sensitive error collapsing + external API), with Problem, 2 success Examples, Constraints, Signature."),
            (True,  "Examples are 2 success outcomes; the missing-header / wrong-scheme / bad-signature / expired / malformed cases are all kept out of Examples and live in hidden tests. Iter-1's missing-header 401 leak is FIXED."),
            (True,  "run.sh executable; '--reporter verbose' default, '-q' toggles quiet, optional '-t' single-test arg."),
            (True,  "vitest assertions use 2nd-arg messages with case label + expected-vs-got."),
        ],
        "notes": {},
    },
    ("ts-jwt-verify", "old_skill"): {
        "g": [
            (True,  "Shortlist had 2 candidates (verifyAuth flow + uniform-401 policy); no padding."),
            (True,  "Dir '2026-05-28_10-20-32_verify-auth' matches YYYY-MM-DD_HH-MM-SS_<slug>."),
            (True,  "README has '[MEDIUM]', Examples, Constraints, Signature."),
            (True,  "This run, Examples are happy-path only with an explicit comment '(Happy paths only. The tests cover the rest.)'. Iter-1 had a 401 leak on this same skill — that was variance under the old looser wording; this run was lucky."),
            (True,  "run.sh TS template (unchanged across iter-1->iter-2); works."),
            (True,  "vitest tests use descriptive messages with case + expected vs actual."),
        ],
        "notes": {"uncertainties": ["This run happened NOT to leak a failure case into README Examples, even though iter-1 did with the same skill. The improvement is probabilistic under the old wording; iter-2's tightened guidance makes it structural."]},
    },
}


def main():
    for ev in sorted(IT.glob("eval-*")):
        meta = json.loads((ev / "eval_metadata.json").read_text())
        assertions = meta["assertions"]
        name = meta["eval_name"]
        for cfg in ["new_skill", "old_skill"]:
            entry = GRADES[(name, cfg)]
            exps = []
            for text, (passed, evidence) in zip(assertions, entry["g"]):
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
            (ev / cfg / "run-1" / "grading.json").write_text(json.dumps(grading, indent=2))
            print(f"{name:24s} {cfg:10s} -> {passed}/{total}  ({grading['summary']['pass_rate']})")


if __name__ == "__main__":
    main()
