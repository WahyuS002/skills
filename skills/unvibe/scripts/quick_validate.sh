#!/usr/bin/env bash
# Self-check that a generated exercise directory follows the unvibe contract.
# Run at the end of Phase 2 / start of Phase 3 to catch shape problems early,
# before the user tries to use the exercise.
#
# Usage: bash scripts/quick_validate.sh <path-to-exercise-dir>
#
# Checks (exits non-zero on the first failure):
#   1. Directory name matches YYYY-MM-DD_HH-MM-SS_<slug>
#   2. README.md exists and the first line starts with [EASY|MEDIUM|HARD]
#   3. run.sh exists and is executable
#   4. At least one of: test_*.py, *_test.go, *.test.ts
#   5. exercise.* stub file present
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

# 1. Directory name format ----------------------------------------------------
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

# 3. run.sh exists and is executable ------------------------------------------
RUN="$DIR/run.sh"
if [ ! -f "$RUN" ]; then
  echo "FAIL [3/5] run.sh missing in $DIR" >&2
  exit 1
fi
if [ ! -x "$RUN" ]; then
  echo "FAIL [3/5] run.sh is not executable (chmod +x $RUN)" >&2
  exit 1
fi

# 4. At least one test file --------------------------------------------------
HAS_TEST=0
for pat in 'test_*.py' '*_test.go' '*.test.ts'; do
  for f in "$DIR"/$pat; do
    [ -e "$f" ] && HAS_TEST=1 && break 2
  done
done
if [ "$HAS_TEST" -eq 0 ]; then
  echo "FAIL [4/5] no test file (test_*.py / *_test.go / *.test.ts) in $DIR" >&2
  exit 1
fi

# 5. Exercise stub file ------------------------------------------------------
HAS_EXERCISE=0
for f in "$DIR"/exercise.*; do
  [ -e "$f" ] && HAS_EXERCISE=1 && break
done
if [ "$HAS_EXERCISE" -eq 0 ]; then
  echo "FAIL [5/5] no exercise.* stub file in $DIR" >&2
  exit 1
fi

echo "OK: $NAME passed all 5 shape checks"
