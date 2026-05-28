#!/usr/bin/env python3
"""Render notes.md with status-conditional body sections.

The notes file's body section list depends on `status`:
    owned          -> 5 sections (What it does / Why / Gotchas / Reimpl / Re-check)
    partial        -> same 5 + "What I'm still stuck on"
    explained-only -> What it does / Why / Gotchas / Why I didn't drill further
    abandoned      -> What it does / Why I stopped

Doing this conditional logic in Python keeps the agent from having to remember
which sections apply to which status — the single failure mode iter-1 showed
is exactly this kind of structural-rule compliance.

Usage:
    python scripts/render_notes.py --config <path-to-config.json>

The config JSON shape:
    {
      "date": "2026-05-28",
      "first_drilled": "2026-05-28",
      "piece": "choose_strategy",
      "source": "process_video.py",
      "confidence_before": "partial",
      "confidence_after": "solid",
      "status": "owned",
      "time_minutes": 18,
      "difficulty": "MEDIUM",
      "tags": ["branching", "whitelist"],
      "re_drills": 0,
      "sections": {
        "What it does (in 2 lines)": "...",
        "The non-obvious part (the \"why\")": "...",
        "Gotchas I missed at first": "- ...\n- ...",
        "My reimplementation choice": "...",
        "What to re-check in 3 months": "..."
      }
    }

Output goes to stdout — redirect to the notes.md path.
"""

import argparse
import json
import sys
from pathlib import Path

VALID_STATUSES = ["owned", "partial", "explained-only", "abandoned"]

SECTIONS_BY_STATUS = {
    "owned": [
        "What it does (in 2 lines)",
        "The non-obvious part (the \"why\")",
        "Gotchas I missed at first",
        "My reimplementation choice",
        "What to re-check in 3 months",
    ],
    "partial": [
        "What it does (in 2 lines)",
        "The non-obvious part (the \"why\")",
        "Gotchas I missed at first",
        "My reimplementation choice",
        "What to re-check in 3 months",
        "What I'm still stuck on",
    ],
    "explained-only": [
        "What it does (in 2 lines)",
        "The non-obvious part (the \"why\")",
        "Gotchas I missed at first",
        "Why I didn't drill further",
    ],
    "abandoned": [
        "What it does (in 2 lines)",
        "Why I stopped",
    ],
}


def render(cfg: dict) -> str:
    status = cfg["status"]
    if status not in VALID_STATUSES:
        raise SystemExit(
            f"render_notes: invalid status {status!r}; must be one of {VALID_STATUSES}"
        )

    tags = ", ".join(cfg.get("tags", []))
    fm = (
        f"---\n"
        f"date: {cfg['date']}\n"
        f"first_drilled: {cfg['first_drilled']}\n"
        f"piece: {cfg['piece']}\n"
        f"source: {cfg['source']}\n"
        f"confidence_before: {cfg['confidence_before']}\n"
        f"confidence_after: {cfg['confidence_after']}\n"
        f"status: {status}\n"
        f"time_minutes: {cfg['time_minutes']}\n"
        f"difficulty: {cfg['difficulty']}\n"
        f"tags: [{tags}]\n"
        f"re_drills: {cfg['re_drills']}\n"
        f"---\n\n"
        f"# {cfg['piece']} — {status} {cfg['date']}\n"
    )

    sections = cfg.get("sections", {})
    body_parts = []
    for heading in SECTIONS_BY_STATUS[status]:
        content = sections.get(heading, "<TODO>")
        body_parts.append(f"\n## {heading}\n\n{content}\n")

    return fm + "".join(body_parts)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--config", required=True, help="Path to JSON config file")
    args = p.parse_args()

    try:
        cfg = json.loads(Path(args.config).read_text())
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"render_notes: cannot read config {args.config}: {e}")

    sys.stdout.write(render(cfg))


if __name__ == "__main__":
    main()
