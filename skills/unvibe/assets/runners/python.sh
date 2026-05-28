#!/usr/bin/env bash
# Per-exercise runner for Python / pytest exercises.
# Usage:
#   ./run.sh                  # all tests, verbose (shows print/log via -s)
#   ./run.sh <test_name>      # one test function, verbose
#   ./run.sh -q               # all tests, quiet summary
#   ./run.sh -q <test_name>   # one test function, quiet
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
QUIET=0; [ "${1:-}" = "-q" ] && { QUIET=1; shift; }
TEST="${1:-}"
SEL="$DIR/test_exercise.py"
[ -n "$TEST" ] && SEL="$SEL::$TEST"
if [ "$QUIET" = 1 ]; then
  exec python3 -m pytest "$SEL" -q
else
  exec python3 -m pytest "$SEL" -s -v   # -s streams print/log live
fi
