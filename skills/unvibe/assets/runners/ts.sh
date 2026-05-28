#!/usr/bin/env bash
# Per-exercise runner for TypeScript / vitest exercises.
# Usage:
#   ./run.sh                  # all tests, verbose reporter
#   ./run.sh <test name>      # one test by name, verbose (vitest -t)
#   ./run.sh -q               # all tests, default reporter
#   ./run.sh -q <test name>   # one test by name, default reporter
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
QUIET=0; [ "${1:-}" = "-q" ] && { QUIET=1; shift; }
TEST="${1:-}"
ARGS=(run "$DIR/exercise.test.ts")
[ -n "$TEST" ] && ARGS+=(-t "$TEST")
if [ "$QUIET" = 1 ]; then
  exec npx vitest "${ARGS[@]}"
else
  exec npx vitest "${ARGS[@]}" --reporter verbose
fi
