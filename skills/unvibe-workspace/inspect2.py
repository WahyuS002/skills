#!/usr/bin/env python3
"""Capture timing + dump key iter-2 artifacts for grading."""
import json, re, stat
from pathlib import Path

IT = Path(__file__).parent / "iteration-2"

TIMING = {
    ("python-video-strategy", "new_skill"): (32116, 146194),
    ("python-video-strategy", "old_skill"): (29374, 121289),
    ("go-ratelimiter-refill", "new_skill"): (38108, 201590),
    ("go-ratelimiter-refill", "old_skill"): (35688, 197994),
    ("ts-jwt-verify",         "new_skill"): (33458, 187338),
    ("ts-jwt-verify",         "old_skill"): (31575, 158505),
}

def write_timing():
    for (ev, cfg), (tok, ms) in TIMING.items():
        rd = IT / f"eval-{ev}" / cfg / "run-1"
        (rd / "timing.json").write_text(json.dumps({
            "total_tokens": tok, "duration_ms": ms,
            "total_duration_seconds": round(ms/1000, 1)
        }, indent=2))

def exdir(work):
    base = work / ".unvibe" / "exercises"
    if not base.is_dir(): return None
    subs = [d for d in base.iterdir() if d.is_dir()]
    return subs[0] if subs else None

def isx(p): return bool(p.stat().st_mode & stat.S_IXUSR)

def dump():
    for ev in sorted(IT.glob("eval-*")):
        for cfg in ["new_skill", "old_skill"]:
            rd = ev / cfg / "run-1"
            work = rd / "work"
            print("=" * 70)
            print(f"### {ev.name} / {cfg}")
            d = exdir(work)
            print(f"exercise_dir_name: {d.name if d else 'NONE'}")
            tr = rd / "outputs" / "transcript.md"
            if tr.exists():
                m = re.search(r"## Candidate shortlist\s*(.*?)(?=\n## |\Z)", tr.read_text(), re.S)
                if m:
                    print("--- shortlist ---")
                    print(m.group(1).strip()[:600])
            if not d: continue
            print("--- files ---")
            for f in sorted(d.iterdir()):
                ex = "x" if (f.is_file() and isx(f)) else "-"
                print(f"  [{ex}] {f.name}")
            r = d / "README.md"
            if r.exists():
                print("--- README.md ---"); print(r.read_text())
            for f in sorted(d.iterdir()):
                if f.name.endswith(".sh"):
                    print(f"--- {f.name} (exec={isx(f)}) ---"); print(f.read_text())
            for f in sorted(d.iterdir()):
                n = f.name.lower()
                if n.endswith((".test.ts","_test.go","exercise_test.go")) or n.startswith("test_"):
                    print(f"--- {f.name} ---"); print(f.read_text()[:3500])

if __name__ == "__main__":
    write_timing()
    print("timing.json written for 6 iter-2 runs\n")
    dump()
