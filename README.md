# SCOUT

SCOUT is a local-first embodied AI robot platform built for an Android/Termux runtime, with a future path to ESP32 hardware and a broader autonomous cognition stack.

This repository is the authoritative project source for the SCOUT development lifecycle. The current milestone is M0: repository bootstrap and system foundations.

## Purpose

SCOUT is designed to run primarily on-device, with local models, local memory, local perception, and local privacy protections. The long-term architecture follows this loop:

OBSERVE → PERCEIVE → UNDERSTAND → REMEMBER → REASON → DECIDE → ACT → OBSERVE

The current repository does not implement advanced cognition, M1 hardware integration, or M2 local LLM integration. Those are intentionally deferred until M0 is complete and validated.

## Quick start

```bash
git clone <repository-url>
cd Scout-Project
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/doctor.py
pytest -q
```

## Repository structure

```text
scout/
  app/
  brain/
  perception/
  expression/
  memory/
  tools/
  body/
  tests/
scripts/
config/
docs/
logs/
```

## M0 scope

M0 includes:

- repository bootstrap
- project structure and modular layout
- README and architecture docs
- configuration example
- structured logs
- changelog
- test framework
- system doctor script

Advanced AI, memory, vision, and motor logic remain intentionally out of scope for M0.

## Development workflow

1. Use the desktop workspace as the source of truth.
2. Keep the phone filesystem as a runtime target, not the master copy.
3. Commit in small, reviewable increments.
4. Run tests before finishing a milestone.
5. Record all meaningful decisions in the logs.

## Diagnostics

```bash
python scripts/doctor.py
```

## Configuration

Copy the sample configuration before deploying or tailoring runtime settings:

```bash
cp config/config.example.toml config/config.toml
```

## Contributing

- Keep modules small and clear.
- Avoid monolithic scripts.
- Prefer simple abstractions over premature complexity.
- Document design decisions in the decision log.
- Do not claim hardware tests pass without running them on the target device.

## License

This project is intended for local robotics experimentation and product bootstrapping. Update the license before any production or public release.
