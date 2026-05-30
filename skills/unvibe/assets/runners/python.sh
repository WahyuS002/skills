#!/usr/bin/env bash
# Per-exercise runner for Python / pytest exercises.
#
# Usage:
#   ./run.sh                       Run all tests, verbose (shows print/log via -s)
#   ./run.sh -q                    Run all tests, quiet summary
#   ./run.sh <test_name>           Run one test function (exact, via pytest ::)
#   ./run.sh -q <test_name>        Run one test function, quiet
#   ./run.sh -h | --help           Show help and exit
#
# Why no --list / index here:
#   pytest's `path::name` syntax is already exact — test names are real
#   Python identifiers (no spaces, no over-matching). A numeric index
#   layer would only add ceremony. If you need to discover names, run
#   `python3 -m pytest --collect-only -q test_exercise.py`.
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
TEST_FILE="$DIR/test_exercise.py"

show_help() {
  cat <<'EOF'
Per-exercise runner for Python / pytest exercises.

Usage:
  ./run.sh                       Run all tests, verbose (-s -v, shows print/log)
  ./run.sh -q                    Run all tests, quiet summary
  ./run.sh <test_name>           Run one test function (exact, via pytest ::)
  ./run.sh -q <test_name>        Run one test function, quiet
  ./run.sh -h | --help           Show this help

Recommended workflow for "run one specific test":
  ./run.sh test_indonesian_with_caption_uses_asr_primary

Note:
  pytest test names are Python identifiers (e.g. test_foo_returns_bar) —
  no spaces, exact match via path::test_name. No --list/index needed.
  To discover names:
      python3 -m pytest --collect-only -q test_exercise.py
EOF
  exit 0
}

case "${1:-}" in
  -h|--help) show_help ;;
esac

QUIET=0
[ "${1:-}" = "-q" ] && { QUIET=1; shift; }
TEST="${1:-}"
SEL="$TEST_FILE"
[ -n "$TEST" ] && SEL="$SEL::$TEST"

if [ "$QUIET" = 1 ]; then
  exec python3 -m pytest "$SEL" -q
else
  exec python3 -m pytest "$SEL" -s -v
fi
