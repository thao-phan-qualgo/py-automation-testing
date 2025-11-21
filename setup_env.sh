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

# 4) Check Playwright and install browsers if needed
if python -c "import playwright" >/dev/null 2>&1; then
  echo "Playwright Python package found. Ensuring browsers are installed..."
else
  echo "Playwright Python package not found in this venv. Installing..."
  pip install playwright
fi

echo "Installing Playwright browsers (this is safe to run multiple times)..."
python -m playwright install

echo "✅ Environment ready. Use: source .venv/bin/activate"
