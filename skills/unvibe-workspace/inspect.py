#!/usr/bin/env python3
import json, os, re, stat
from pathlib import Path

IT = Path(__file__).parent / "iteration-1"

# timing captured from subagent completion notifications
TIMING = {
    ("python-video-strategy", "new_skill"): (29828, 116316),
    ("python-video-strategy", "old_skill"): (26842, 108642),
    ("go-ratelimiter-refill", "new_skill"): (34125, 161941),
    ("go-ratelimiter-refill", "old_skill"): (29874, 136756),
    ("ts-jwt-verify", "new_skill"): (32023, 150919),
    ("ts-jwt-verify", "old_skill"): (28752, 135074),
}

def write_timing():
    for (ev, cfg), (tok, ms) in TIMING.items():
        rd = IT / f"eval-{ev}" / cfg / "run-1"
        (rd / "timing.json").write_text(json.dumps({
            "total_tokens": tok, "duration_ms": ms,
            "total_duration_seconds": round(ms/1000, 1)
        }, indent=2))

def find_exercise_dir(work):
    base = work / ".unvibe" / "exercises"
    if not base.is_dir():
        return None
    subs = [d for d in base.iterdir() if d.is_dir()]
    return subs[0] if subs else None

def is_exec(p):
    return bool(p.stat().st_mode & stat.S_IXUSR)

def dump():
    for ev in sorted(IT.glob("eval-*")):
        if not ev.is_dir():
            continue
        for cfg in ["new_skill", "old_skill"]:
            rd = ev / cfg / "run-1"
            work = rd / "work"
            print("=" * 70)
            print(f"### {ev.name} / {cfg}")
            exdir = find_exercise_dir(work)
            print(f"exercise_dir_name: {exdir.name if exdir else 'NONE'}")
            # transcript shortlist
            tr = rd / "outputs" / "transcript.md"
            if tr.exists():
                t = tr.read_text()
                m = re.search(r"## Candidate shortlist\s*(.*?)(?=\n## |\Z)", t, re.S)
                if m:
                    print("--- shortlist ---")
                    print(m.group(1).strip()[:600])
            if not exdir:
                continue
            files = sorted(exdir.iterdir())
            print("--- files ---")
            for f in files:
                ex = "x" if (f.is_file() and is_exec(f)) else "-"
                print(f"  [{ex}] {f.name}")
            # README
            readme = exdir / "README.md"
            if readme.exists():
                print("--- README.md ---")
                print(readme.read_text())
            # run script
            for rs in files:
                if rs.name.endswith(".sh"):
                    print(f"--- {rs.name} (exec={is_exec(rs)}) ---")
                    print(rs.read_text())
            # test file(s)
            for f in files:
                n = f.name.lower()
                if "test" in n or "_test" in n or n.endswith(".test.ts"):
                    print(f"--- {f.name} ---")
                    print(f.read_text())

if __name__ == "__main__":
    write_timing()
    print("timing.json written for 6 runs\n")
    dump()
