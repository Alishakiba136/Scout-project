# SCOUT Architecture

SCOUT is structured as a modular platform rather than a large single application file. The repository is intentionally organized around functional domains so that future milestones remain understandable and testable.

## Core domains

- `scout/app`: application bootstrap and runtime lifecycle
- `scout/brain`: cognition, context, planning, and inference interfaces
- `scout/perception`: camera, microphones, STT, and vision abstractions
- `scout/expression`: TTS and face/UI logic
- `scout/memory`: persistent memory and retrieval layers
- `scout/tools`: tool registry and tool execution safety wrappers
- `scout/body`: hardware interface and future ESP32 safety layer
- `scripts`: diagnostics and subsystem test utilities
- `logs`: project development, testing, and decisions

## Design principles

1. Keep modules small and explicit.
2. Keep the LLM isolated behind a deterministic interface.
3. Validate tool requests before execution.
4. Prefer local processing and local privacy by default.
5. Keep deployment and development modes distinct.

## Long-term loop

The eventual system is meant to follow a full embodied cognition cycle:

OBSERVE → PERCEIVE → UNDERSTAND → REMEMBER → REASON → DECIDE → ACT → OBSERVE

This repository currently covers only the repository bootstrap and architectural foundation needed before M1.
