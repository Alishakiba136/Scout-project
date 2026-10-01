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

---

## Decision D009 — Local metadata-based vision analysis for M5

Date: 2026-10-01
Status: Accepted
Decision: The M5 perception layer should use lightweight local metadata analysis to summarize images and expose a stable, testable interface before deeper vision models are introduced.
Reason: The project still needs a reliable first perception contract without depending on heavy vision libraries or hardware-only camera access.
Alternatives considered: A monolithic imaging script or a fully model-driven vision stack too early in the roadmap.
Consequences: The repository gains an explicit and portable image analysis interface that can evolve into richer object detection or scene understanding later without breaking the local-first design.

---

## Decision D010 — Deterministic local cognition for M6

Date: 2026-10-01
Status: Accepted
Decision: The M6 cognition layer should be a deterministic, local planner that converts an objective into an explicit action sequence and decision record before more advanced reasoning is introduced.
Reason: SCOUT needs a first reasoning loop that is inspectable, testable, and safe to evolve without requiring heavy AI models or unbounded autonomous behavior.
Alternatives considered: Jumping directly to high-autonomy planning or embedding free-form reasoning inside the LLM response path.
Consequences: The system gains a stable cognitive contract that can later support memory-aware behavior, tool selection, and richer planning without breaking the architecture.

---

## Decision D011 — Safety-first tool execution for M7

Date: 2026-10-01
Status: Accepted
Decision: Tools must be registered with explicit safety classifications and executable only through the registry, which blocks unsafe calls before any command or hardware action is attempted.
Reason: The product requires a deterministic guardrail between high-level intent and action execution, especially when a model or planner proposes a physical or privileged operation.
Alternatives considered: Letting any registered callable run directly or bypassing the registry with ad hoc shell calls.
Consequences: The system gains a clear, auditable operational boundary that prevents unsafe actions from leaking through the agent loop.

---

## Decision D012 — Deterministic movement control for M8

Date: 2026-10-01
Status: Accepted
Decision: The body layer should expose a deterministic `BodyController` plus a serialized `ESP32Controller`, and all movement commands must still pass through the safety gate before approval.
Reason: SCOUT needs a physical action contract that is explicit, testable, and safe before any actual robot hardware or ESP32 layer is connected.
Alternatives considered: Direct motor commands from the planner or a stateful, unvalidated hardware script.
Consequences: The system preserves a clear operational boundary between cognition, tool validation, and hardware actuation.

---

## Decision D013 — Explicit task planning for M9

Date: 2026-10-01
Status: Accepted
Decision: The next milestone should introduce a lightweight task planner that turns a goal into explicit steps and flags motion-related directives for the safety gate before execution.
Reason: SCOUT needs a predictable goal-to-plan conversion layer that is inspectable and local-first before higher-level autonomy is added.
Alternatives considered: Skipping a planning layer and letting free-form model output drive commands directly.
Consequences: The system gains a clear bridge between cognition and downstream execution, making role boundaries easier to test and reason about.

---

## Decision D014 — Mission execution for M10

Date: 2026-10-01
Status: Accepted
Decision: The M10 milestone should add a deterministic mission loop that executes a validated plan, records the result, and blocks movement-based missions when the emergency-stop boundary is engaged.
Reason: After planning and safety validation, the project needs one final execution boundary that turns a plan into a concrete outcome without allowing unbounded or unsafe action dispatch.
Alternatives considered: Letting the planner or LLM directly issue commands without an execution gate.
Consequences: The architecture preserves a clean separation between planning, safety control, and mission execution, which is easier to test and safer to evolve.

---

## Decision D015 — Memory-aware planning for M11

Date: 2026-10-01
Status: Accepted
Decision: The M11 milestone should add a memory-aware planner that retrieves the most relevant stored facts and injects them into the plan context before execution is considered.
Reason: Local-first autonomy becomes more useful when a planner can reason over previously remembered facts without making the system rely on opaque external memory services.
Alternatives considered: Ignoring memory during planning or embedding unbounded free-form retrieval into the LLM path.
Consequences: The system gains a traceable memory window that improves contextual planning while keeping the architecture deterministic and auditable.

---

## Decision D016 — Session memory for M12

Date: 2026-10-01
Status: Accepted
Decision: The M12 milestone should add a session memory layer that records recent goals and exposes them as a bounded planning context for successive tasks.
Reason: After memory-aware planning and mission execution, the next useful step is to preserve recent intent history so the robot can behave coherently over a short interaction sequence without become overly stateful or opaque.
Alternatives considered: Resetting the planner on every request or letting the LLM keep ephemeral state outside the local memory system.
Consequences: The system becomes more context-aware over a single interaction while preserving local-first determinism and traceability.

---

## Decision D017 — Goal queue for M13

Date: 2026-10-01
Status: Accepted
Decision: The M13 milestone should add a simple local goal queue that orders pending objectives by priority and preserves insertion order for ties.
Reason: Once a robot has memory and session awareness, the next practical layer is a bounded scheduler that can choose the next objective deterministically without introducing a complicated autonomous planner too early.
Alternatives considered: Unbounded model-driven prioritization or a fully asynchronous multi-agent scheduler.
Consequences: The system gets a clear, inspectable prioritization layer that can evolve into richer scheduling later while staying simple and auditable.

---

## Decision D018 — Goal scheduler for M14

Date: 2026-10-01
Status: Accepted
Decision: The M14 milestone should add a local scheduler that selects the highest-priority queued goal and converts it into the next plan without hiding any state in an opaque control loop.
Reason: Once planning and queueing exist, a real scheduling layer is the natural next boundary for turning pending objectives into concrete next actions.
Alternatives considered: Letting the planner act on all goals at once or embedding queue resolution inside the LLM path.
Consequences: The system gains a transparent execution ordering layer that can later support mission scheduling and more advanced autonomy without sacrificing determinism.

---

## Decision D019 — Behavior loop for M15

Date: 2026-10-01
Status: Accepted
Decision: The M15 milestone should add a minimal behavior loop that takes queued goals, asks the scheduler for the next task, and turns that task into a concrete plan result without introducing any hidden or unbounded autonomy.
Reason: At this stage the project has queueing, scheduling, and planning; the natural next boundary is a single local decision cycle that orchestrates them in one explicit behavior step.
Alternatives considered: Scattering task selection across modules or letting the LLM and planner handle orchestration ad hoc.
Consequences: The architecture gains a clear top-level control loop that can later be extended with richer mission policy, but it remains deterministic and easy to inspect.
