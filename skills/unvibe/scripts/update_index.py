#!/usr/bin/env python3
"""Update `.unvibe/INDEX.md` from a notes.md frontmatter — one row per piece.

Reads the YAML frontmatter at the top of the notes.md, then either updates the
existing row for that piece (matched by the `piece` column) or appends a new
row. Re-drills update the existing row in place; do NOT duplicate rows.

The table format is:

    | Date | Piece | Source | Status | Conf. |

Status column carries a `(×N)` suffix when `re_drills > 0`.
Conf. column uses an icon from `confidence_after`:
    solid   -> ✅
    partial -> ⚠️
    fuzzy   -> ❓

Doing this in a script (instead of asking the agent to edit a markdown table by
hand) is the single most table-error-prone operation in the unvibe flow.

Usage:
    python scripts/update_index.py --notes <path-to-notes.md>
    python scripts/update_index.py --notes <path> --index <path-to-INDEX.md>

If --index is omitted, defaults to <notes.md>/../../INDEX.md (i.e. the workspace
.unvibe/INDEX.md sitting two levels above the exercise dir). If INDEX.md does
not exist, it is created with the canonical header.
"""

import argparse
import re
import sys
from pathlib import Path

CONFIDENCE_ICON = {"solid": "✅", "partial": "⚠️", "fuzzy": "❓"}

INDEX_HEADER = (
    "# Unvibe ownership log\n\n"
    "| Date | Piece | Source | Status | Conf. |\n"
    "|------|-------|--------|--------|-------|\n"
)


def parse_frontmatter(text: str) -> dict:
    """Pull simple `key: value` pairs from the leading `---` block."""
    if not text.startswith("---"):
        raise SystemExit("update_index: notes.md missing leading `---` frontmatter")
    end = text.find("\n---", 3)
    if end == -1:
        raise SystemExit("update_index: notes.md frontmatter has no closing `---`")
    fm: dict[str, str] = {}
    for line in text[3:end].strip().splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip()
    return fm


def build_row(fm: dict) -> str:
    date = fm.get("date", "")
    piece = fm.get("piece", "")
    source = fm.get("source", "")
    status = fm.get("status", "")
    conf = fm.get("confidence_after", "")
    try:
        re_drills = int(fm.get("re_drills", "0"))
    except ValueError:
        re_drills = 0
    if re_drills > 0:
        status = f"{status} (×{re_drills + 1})"
    icon = CONFIDENCE_ICON.get(conf, "")
    return f"| {date} | {piece} | {source} | {status} | {icon} |\n"


def upsert_row(index_text: str, piece: str, new_row: str) -> str:
    """Replace the row whose `Piece` column equals `piece`, else append."""
    lines = index_text.splitlines(keepends=True)
    piece_re = re.compile(r"^\|\s*[^|]+\s*\|\s*" + re.escape(piece) + r"\s*\|")
    for i, line in enumerate(lines):
        if piece_re.match(line):
            lines[i] = new_row
            return "".join(lines)
    # No existing row — append (ensure the file ends with a newline first).
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    lines.append(new_row)
    return "".join(lines)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--notes", required=True, help="Path to the exercise notes.md")
    p.add_argument(
        "--index",
        default=None,
        help="Path to INDEX.md (default: <notes>/../../INDEX.md)",
    )
    args = p.parse_args()

    notes_path = Path(args.notes).resolve()
    if not notes_path.exists():
        raise SystemExit(f"update_index: notes file not found: {notes_path}")

    fm = parse_frontmatter(notes_path.read_text())
    piece = fm.get("piece", "")
    if not piece:
        raise SystemExit("update_index: notes.md frontmatter missing `piece`")

    if args.index:
        index_path = Path(args.index).resolve()
    else:
        # exercise dir is notes_path.parent; .unvibe is one level above that.
        index_path = notes_path.parent.parent.parent / "INDEX.md"

    new_row = build_row(fm)
    if index_path.exists():
        updated = upsert_row(index_path.read_text(), piece, new_row)
    else:
        updated = INDEX_HEADER + new_row
    index_path.write_text(updated)
    sys.stdout.write(f"INDEX updated: {index_path}\n")


if __name__ == "__main__":
    main()
