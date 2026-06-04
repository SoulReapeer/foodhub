#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
#  FoodHub – one-command startup script
# ─────────────────────────────────────────────────────────────────
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR"
PORT=5000

# ── Colours ──
GREEN="\033[0;32m"; YELLOW="\033[1;33m"; RED="\033[0;31m"; RESET="\033[0m"
info()  { echo -e "${GREEN}[FoodHub]${RESET} $*"; }
warn()  { echo -e "${YELLOW}[FoodHub]${RESET} $*"; }
error() { echo -e "${RED}[FoodHub]${RESET} $*"; }

info "Starting FoodHub..."

# ── Check Python ──
if ! command -v python3 &>/dev/null; then
  error "Python 3 is required. Install from https://python.org"
  exit 1
fi

# ── Create & activate virtual environment ──
if [ ! -d "$BACKEND_DIR/venv" ]; then
  info "Creating virtual environment..."
  python3 -m venv "$BACKEND_DIR/venv"
fi

source "$BACKEND_DIR/venv/bin/activate"

# ── Install dependencies ──
info "Installing Python dependencies..."
pip install -r "$BACKEND_DIR/requirements.txt" -q

# ── Copy .env if not present ──
if [ ! -f "$BACKEND_DIR/.env" ] && [ -f "$BACKEND_DIR/.env.example" ]; then
  cp "$BACKEND_DIR/.env.example" "$BACKEND_DIR/.env"
  warn ".env created from .env.example – edit it to set your own secrets"
fi

# ── Kill any existing process on port 5000 ──
if lsof -Pi :$PORT -sTCP:LISTEN -t &>/dev/null; then
  warn "Port $PORT already in use – attempting to free it..."
  kill "$(lsof -ti :$PORT)" 2>/dev/null || true
  sleep 1
fi

# ── Launch Flask backend ──
info "Launching Flask backend on http://localhost:$PORT ..."
cd "$BACKEND_DIR"
python app.py &
FLASK_PID=$!
echo "$FLASK_PID" > "$BACKEND_DIR/.flask.pid"

# ── Wait for Flask to be ready ──
echo -n "Waiting for backend"
for i in {1..20}; do
  if curl -s "http://localhost:$PORT/api/v1/restaurants" &>/dev/null; then
    echo " ✓"
    break
  fi
  echo -n "."
  sleep 0.5
done

# ── Open frontend in browser ──
FRONTEND_URL="file://$FRONTEND_DIR/index.html"
info "Opening frontend: $FRONTEND_URL"
if command -v xdg-open &>/dev/null; then
  xdg-open "$FRONTEND_URL"
elif command -v open &>/dev/null; then
  open "$FRONTEND_URL"
else
  warn "Open manually: $FRONTEND_URL"
fi

echo ""
echo -e "${GREEN}════════════════════════════════════════════${RESET}"
echo -e "${GREEN}  FoodHub is running!${RESET}"
echo -e "${GREEN}════════════════════════════════════════════${RESET}"
echo -e "  Backend API  →  http://localhost:$PORT/api/v1"
echo -e "  Frontend     →  $FRONTEND_URL"
echo ""
echo -e "  Demo login (admin):    admin@foodhub.com / admin123"
echo -e "  Demo login (customer): rahim@example.com / customer123"
echo ""
echo -e "  Press Ctrl+C to stop the server."
echo -e "${GREEN}════════════════════════════════════════════${RESET}"

# ── Keep running & clean up on exit ──
trap "info 'Shutting down...'; kill $FLASK_PID 2>/dev/null; deactivate 2>/dev/null" EXIT INT TERM
wait $FLASK_PID
