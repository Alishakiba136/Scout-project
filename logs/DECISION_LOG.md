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
