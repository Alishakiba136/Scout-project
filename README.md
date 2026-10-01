# SCOUT

SCOUT is a local-first embodied AI robot platform designed for on-device voice, vision, memory, and task execution. It is intended to run on a phone through Termux as well as on a Linux workstation for development and testing.

The project is structured around a robot loop:

OBSERVE → PERCEIVE → UNDERSTAND → REMEMBER → REASON → DECIDE → ACT → OBSERVE

SCOUT is meant to provide a practical robot companion experience with:

- a robot face UI
- camera and vision awareness
- microphone input and speech recognition
- text-to-speech output
- local LLM support via llama.cpp
- local memory and task planning
- safety-aware mission execution

## Features

- local-first AI with no required cloud dependency
- Android/Termux-friendly runtime setup
- browser-based robot dashboard
- face-state transitions for listening, speaking, thinking, happy, confused, and more
- local SQLite-backed memory
- behavior planning and task execution loops
- modular subsystem layout for future hardware integration

## Requirements

### Desktop / development machine

- Python 3.11+ recommended
- Git
- pytest
- working local terminal

### Android / Termux phone

- Termux installed
- storage access enabled as needed
- internet access for model download
- optional camera and microphone permissions in the browser

## Installation

### 1) Clone the project

```bash
git clone <repository-url>
cd Scout-Project
```

### 2) Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Run the project checks

```bash
python scripts/doctor.py
pytest -q
```

### 4) Start the app

```bash
python3 -m scout.app.main
```

Then open the browser at:

```text
http://localhost:8000
```

If port 8000 is occupied, SCOUT will automatically use the next free port and print the URL.

## Termux install guide

On Android/Termux, install the basic runtime dependencies:

```bash
pkg update
pkg install -y git python ffmpeg espeak termux-api
```

Clone the repo to the phone:

```bash
git clone <repository-url>
cd Scout-Project
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Install llama.cpp and a local model, then run the app:

```bash
pkg install -y llama-cpp
mkdir -p ~/models
curl -L -o ~/models/SmolLM2-360M-Instruct-Q8_0.gguf \
  https://huggingface.co/bartowski/SmolLM2-360M-Instruct-GGUF/resolve/main/SmolLM2-360M-Instruct-Q8_0.gguf

nohup llama-server -m ~/models/SmolLM2-360M-Instruct-Q8_0.gguf --host 127.0.0.1 --port 8080 --ctx-size 2048 > ~/llama_server.log 2>&1 &

python3 -m scout.app.main
```

Then open the browser on the same device at:

```text
http://127.0.0.1:8000
```

## User launcher

A launcher script is included for a direct Termux command:

```bash
./scripts/start_termux.sh
```

The script creates a virtual environment when needed, checks for the local model, starts llama-server if needed, and launches the app.

## Project layout

```text
scout/
  app/
  brain/
  perception/
  expression/
  memory/
  tools/
  body/

scripts/
config/
docs/
logs/
tests/
```

## Development notes

- keep modules small and explicit
- validate by running pytest before release candidates
- keep device-side runtime logic local-first
- do not assume hardware tests pass without running them on the target device

## License

This project is intended for local robotics experimentation and product bootstrapping. Update the license before production or public release.
