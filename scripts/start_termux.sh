#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-$HOME/Scout-Project}"
VENV_DIR="$PROJECT_DIR/.venv"
MODEL_PATH="$PROJECT_DIR/models/SmolLM2-360M-Instruct-Q8_0.gguf"
LOG_PATH="$PROJECT_DIR/llama_server.log"

if [ ! -d "$PROJECT_DIR" ]; then
  echo "SCOUT repo not found at $PROJECT_DIR"
  exit 1
fi

cd "$PROJECT_DIR"
mkdir -p "$PROJECT_DIR/models"

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/python" -m pip install -r "$PROJECT_DIR/requirements.txt" >/dev/null 2>&1 || true

if [ ! -f "$MODEL_PATH" ]; then
  echo "Model not found at $MODEL_PATH"
  echo "Downloading SmolLM2-360M-Instruct-Q8_0.gguf..."
  mkdir -p "$PROJECT_DIR/models"
  curl -L --fail -o "$MODEL_PATH" \
    "https://huggingface.co/bartowski/SmolLM2-360M-Instruct-GGUF/resolve/main/SmolLM2-360M-Instruct-Q8_0.gguf"
fi

if ! pgrep -f "llama-server.*SmolLM2-360M-Instruct-Q8_0.gguf" >/dev/null 2>&1; then
  echo "Starting local LLM server..."
  nohup llama-server \
    -m "$MODEL_PATH" \
    --host 127.0.0.1 \
    --port 8080 \
    --ctx-size 2048 \
    --threads 4 \
    > "$LOG_PATH" 2>&1 &
  sleep 5
fi

if [ "${1:-run}" = "doctor" ]; then
  "$VENV_DIR/bin/python" "$PROJECT_DIR/scripts/doctor.py"
  exit 0
fi

"$VENV_DIR/bin/python" -m scout.app.main
