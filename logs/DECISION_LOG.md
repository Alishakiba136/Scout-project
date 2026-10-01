# SCOUT Decision Log

## Decision D001 — Local-first architecture

Date: 2026-10-01
Status: Accepted
Decision: Build SCOUT as a local-first, on-device embodied AI platform with an Android/Termux runtime target and optional later ESP32 integration.
Reason: Local processing, privacy, and offline operation are central product requirements. The robot must work without requiring a cloud service for its core loop.
Alternatives considered: Cloud-first robot architecture, remote-only processing, and a monolithic prototype script.
Consequences: The project must keep computation, memory, and privacy decisions local by default and must be structured around modular components rather than a giant single file.

---

## Decision D002 — Explicit safety boundary for hardware control

Date: 2026-10-01
Status: Accepted
Decision: The LLM may produce high-level intent, but deterministic software must validate and execute physical actions.
Reason: Safety-critical hardware must never be directly controlled by a model response. This reduces hardware risk and keeps the control loop understandable and auditable.
Alternatives considered: Direct model output to GPIO or shell execution; full model-driven actuator control.
Consequences: The architecture requires a safety/controller layer between cognitive intent and motor commands, even though M0 does not implement hardware actuation.

---

## Decision D003 — SQLite for memory foundations

Date: 2026-10-01
Status: Accepted
Decision: Use SQLite as the initial durable local storage layer for memory and structured records.
Reason: SQLite is reliable, portable, lightweight, and a good fit for a local-first robot project that must remain simple to maintain.
Alternatives considered: JSON files, MySQL, and custom in-memory stores.
Consequences: Future memory subsystems can evolve around a consistent local database layer without requiring a large database stack.

---

## Decision D004 — Modular architecture before cognition

Date: 2026-10-01
Status: Accepted
Decision: Keep the repository organized with explicit modules for app, brain, perception, expression, memory, tools, and body.
Reason: A maintainable product needs clear responsibility boundaries before advanced features are added.
Alternatives considered: One large `scout.py` file and ad hoc feature growth.
Consequences: The repository remains extensible and easier for another engineer to onboard, debug, and evolve.

---

## Decision D005 — M0 is architecture and diagnostics only

Date: 2026-10-01
Status: Accepted
Decision: M0 focuses on repository bootstrap, docs, configuration, tests, and diagnostics; no memory, vision, or advanced cognition is implemented yet.
Reason: The specification explicitly requires a staged approach and forbids jumping ahead to M1 or M2 before M0 is complete and validated.
Alternatives considered: Implementing camera, TTS, and LLM prototypes prematurely.
Consequences: The project remains disciplined and aligned with the milestone plan, which reduces rework and keeps M0 deliverables clear.

---

## Decision D006 — Device-aware hardware abstractions for M1

Date: 2026-10-01
Status: Accepted
Decision: Each physical capability receives a module-level interface with a Termux-aware implementation and a conservative development-mode fallback.
Reason: This allows the project to test well on desktop machines while still supporting the actual POCO X3 runtime later without hard-coding device-specific logic into the rest of the system.
Alternatives considered: Hard-coded shell calls across the app and a non-portable monolithic M1 implementation.
Consequences: The architecture remains modular and stays aligned with the future requirement to swap providers behind stable interfaces.

---

## Decision D007 — Local LLM interface isolated behind a single adapter

Date: 2026-10-01
Status: Accepted
Decision: Use a single llama.cpp-compatible client behind the `scout.brain.llm` interface rather than scattering HTTP calls throughout the project.
Reason: The LLM should be an active cognitive component but must remain modular, testable, and configurable without coupling the rest of the system to one inference server implementation.
Alternatives considered: Direct requests from multiple modules and an unbounded HTTP client spread across the codebase.
Consequences: The model integration stays clean, configurable, and easy to replace if a newer local inference stack is introduced later.

---

## Decision D008 — Voice loop uses explicit face-state transitions

Date: 2026-10-01
Status: Accepted
Decision: The voice pipeline must explicitly move through listening → thinking → speaking → idle states before returning to baseline.
Reason: This makes the robot feel coherent and helps future UI and hardware debugging without hard-coding emotion into the LLM response logic.
Alternatives considered: A silent internal pipeline with no visible state change.
Consequences: All future conversation code can rely on a consistent state machine, which keeps the product readable and easier to debug.
