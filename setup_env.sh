#!/usr/bin/env bash
set -e  # stop on first error

# Always run from the script's folder
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# 1) Create venv if not exists
if [ ! -d ".venv" ]; then
  echo "Creating virtual env in .venv..."
  python3 -m venv .venv
fi

# 2) Activate venv
source .venv/bin/activate

# 3) Upgrade pip + install/upgrade all requirements
python -m pip install --upgrade pip
pip install --upgrade -r requirements.txt

echo "✅ Environment ready. Use: source .venv/bin/activate"
