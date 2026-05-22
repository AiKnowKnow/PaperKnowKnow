#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -d ".venv" ]]; then
  echo "[ERROR] .venv not found. Create it first:"
  echo "        python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
  exit 1
fi

if [[ -f ".env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

export PAPER_ENV="${PAPER_ENV:-production}"
export PAPER_DESKTOP_MODE=false
export PAPER_OPEN_BROWSER=false
export PAPER_HOST="${PAPER_HOST:-0.0.0.0}"
export PAPER_PORT="${PAPER_PORT:-8000}"

exec .venv/bin/gunicorn -c gunicorn.conf.py main:app
