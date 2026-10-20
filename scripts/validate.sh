#!/usr/bin/env bash
# Run every Phase 1 check (D-008). Needs python3 (standard library only) and,
# for the plugin manifest check, the claude CLI. A skipped check is never a
# pass: the script then exits 2 and says INCOMPLETE.
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONDONTWRITEBYTECODE=1

python3 scripts/verify_core.py
python3 scripts/check_core_coverage.py
python3 scripts/check_pack.py
python3 -m unittest discover -s tests -q
if command -v claude >/dev/null 2>&1; then
  claude plugin validate .
else
  echo "validate.sh: INCOMPLETE - claude CLI not found, plugin manifest check NOT RUN"
  exit 2
fi
echo "validate.sh: all checks passed"
