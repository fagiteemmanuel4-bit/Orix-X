#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/kryonara/orix.git"
INSTALL_DIR="$HOME/.local/share/orix"
PIPX_BIN="$(command -v pipx || true)"
PYTHON_BIN="$(command -v python3 || command -v python || true)"

log() {
  echo "[orix] $1"
}

error() {
  echo "[orix] ERROR: $1" >&2
  exit 1
}

if [[ -z "$PYTHON_BIN" ]]; then
  error "Python 3 is required. Install Python 3 and re-run this script."
fi

if [[ -z "$PIPX_BIN" ]]; then
  if command -v pip >/dev/null 2>&1; then
    log "Installing pipx using pip..."
    "$PYTHON_BIN" -m pip install --user pipx
    export PATH="$HOME/.local/bin:$PATH"
    PIPX_BIN="$(command -v pipx || true)"
  fi
fi

if [[ -z "$PIPX_BIN" ]]; then
  error "pipx is required but was not found. Install pipx and try again."
fi

log "Using Python: $PYTHON_BIN"
log "Using pipx: $PIPX_BIN"

if [[ -d "$INSTALL_DIR" ]]; then
  log "Removing existing temporary directory: $INSTALL_DIR"
  rm -rf "$INSTALL_DIR"
fi

log "Cloning Orix repository..."
git clone "$REPO_URL" "$INSTALL_DIR"
cd "$INSTALL_DIR"

log "Installing Orix in isolated pipx environment..."
"$PIPX_BIN" install --force --spec . orix

log "Installation complete. You can now run 'orix' from your terminal."
