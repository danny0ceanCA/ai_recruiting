#!/usr/bin/env bash
# Install Python dependencies from the local vendor directory.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

python -m pip install --no-index --find-links "$REPO_ROOT/vendor" -r "$REPO_ROOT/requirements.txt"
