#!/usr/bin/env bash
# Self-check that a generated exercise directory follows the unvibe contract.
# Run at the end of Phase 2 / start of Phase 3 to catch shape problems early,
# before the user tries to use the exercise.
#
# Usage: bash scripts/quick_validate.sh <path-to-exercise-dir>
#
# Supports two layouts:
#   * single   — the container holds README + run.sh + test + exercise stub.
#   * sliced   — the container holds a progression-map README + stepN_*/ leaf
#                dirs; each leaf holds run.sh + test + exercise stub. Detected
#                automatically by the presence of stepN_*/ subdirs.
#
# Checks (exits non-zero on the first failure):
#   1. Container dir name matches YYYY-MM-DD_HH-MM-SS_<slug>
#   2. README.md exists and the first line starts with [EASY|MEDIUM|HARD]
#   3. run.sh exists and is executable          (per leaf)
#   4. At least one of: test_*.py, *_test.go, *.test.ts   (per leaf)
#   5. exercise.* stub file present             (per leaf)
#
# In the single layout the container itself is the (only) leaf. In the sliced
# layout each stepN_*/ subdir is a leaf and the container is exempt from 3-5.
#
# Phase 4 may add a 6th check (notes.md exists) once notes are written.
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "usage: $0 <path-to-exercise-dir>" >&2
  exit 2
fi

DIR="$1"
if [ ! -d "$DIR" ]; then
  echo "quick_validate: not a directory: $DIR" >&2
  exit 1
fi

NAME="$(basename "$DIR")"

# 1. Container dir name format ------------------------------------------------
NAME_RE='^[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{2}_.+$'
if [[ ! "$NAME" =~ $NAME_RE ]]; then
  echo "FAIL [1/5] dir name '$NAME' does not match YYYY-MM-DD_HH-MM-SS_<slug>" >&2
  exit 1
fi

# 2. README.md exists with difficulty tag ------------------------------------
README="$DIR/README.md"
if [ ! -f "$README" ]; then
  echo "FAIL [2/5] README.md missing in $DIR" >&2
  exit 1
fi
FIRST_LINE="$(head -n1 "$README")"
DIFF_RE='^#[[:space:]]*\[(EASY|MEDIUM|HARD)\][[:space:]]'
if [[ ! "$FIRST_LINE" =~ $DIFF_RE ]]; then
  echo "FAIL [2/5] README.md first line must start with '# [EASY|MEDIUM|HARD]'; got: $FIRST_LINE" >&2
  exit 1
fi

# Leaf checks (run.sh, test file, exercise stub) -----------------------------
# $1 = leaf dir, $2 = label for messages. Exits non-zero on first failure.
check_leaf() {
  local leaf="$1" label="$2"

  local run="$leaf/run.sh"
  if [ ! -f "$run" ]; then
    echo "FAIL [3/5] run.sh missing in $label" >&2
    exit 1
  fi
  if [ ! -x "$run" ]; then
    echo "FAIL [3/5] run.sh is not executable (chmod +x $run)" >&2
    exit 1
  fi

  local has_test=0 pat f
  for pat in 'test_*.py' '*_test.go' '*.test.ts'; do
    for f in "$leaf"/$pat; do
      [ -e "$f" ] && has_test=1 && break 2
    done
  done
  if [ "$has_test" -eq 0 ]; then
    echo "FAIL [4/5] no test file (test_*.py / *_test.go / *.test.ts) in $label" >&2
    exit 1
  fi

  local has_exercise=0
  for f in "$leaf"/exercise.*; do
    [ -e "$f" ] && has_exercise=1 && break
  done
  if [ "$has_exercise" -eq 0 ]; then
    echo "FAIL [5/5] no exercise.* stub file in $label" >&2
    exit 1
  fi
}

# Detect sliced layout: any stepN_*/ subdir -----------------------------------
shopt -s nullglob
STEPS=("$DIR"/step*/)
shopt -u nullglob

if [ "${#STEPS[@]}" -gt 0 ]; then
  # Sliced: validate each step as a leaf; container is exempt from 3-5.
  for step in "${STEPS[@]}"; do
    check_leaf "${step%/}" "$(basename "${step%/}")"
  done
  echo "OK: $NAME (sliced, ${#STEPS[@]} steps) passed all shape checks"
else
  # Single: the container itself is the leaf.
  check_leaf "$DIR" "$DIR"
  echo "OK: $NAME passed all 5 shape checks"
fi
