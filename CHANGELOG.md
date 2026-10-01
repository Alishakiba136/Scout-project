# Changelog

## 0.1.14
- Added the M15 behavior-loop layer with a deterministic `BehaviorLoop` and `BehaviorResult`.
- Orchestrated queued goals into a single local decision cycle that chooses the next task, plans it, and hands it to the execution pipeline without introducing hidden state or external autonomy.
- Added the behavior-loop contract covering normal scheduling and empty-loop fallback.

## 0.1.13
- Added the M14 goal-scheduler layer with a deterministic `GoalScheduler` that picks the highest-priority queued goal and converts it into a concrete task plan.
- Bound task selection to a visible queue and planner interaction so the system remains inspectable and local-first without introducing hidden autonomous behavior.
- Added the goal-scheduler contract covering queue selection and empty-queue fallback.

## 0.1.12
- Added the M13 goal-queue layer with a deterministic `GoalQueue` and `GoalItem` object.
- Prioritized pending goals in a clear local queue so the planner can resolve the next most important task without introducing a heavyweight scheduler or opaque state machine.
- Added the goal-queue contract covering priority ordering and empty-queue fallback.

## 0.1.11
- Added the M12 session-memory planning layer with a `SessionMemory` store and `SessionPlanner`.
- Tracked recent goals in the local SQLite-backed memory store and injected them into the plan context as an explicit, inspectable session history.
- Added the session-memory contract covering recent-goal tracking, context injection, and graceful empty-session fallback.

## 0.1.10
- Added the M11 memory-aware planning layer with a `MemoryContext` and `MemoryAwarePlanner`.
- Folded relevant local memory facts into the planner context without bypassing the project’s deterministic safety and execution boundaries.
- Added the memory-aware planning contract covering memory retrieval, memory injection, and graceful empty-memory fallback.

## 0.1.9
- Added the M10 mission-execution layer with a deterministic `MissionLoop` and `MissionResult`.
- Converted validated plans into explicit execution outcomes while respecting the emergency-stop safety boundary.
- Added the mission-loop contract covering successful execution, blocked movement plans, and empty plans.

## 0.1.8
- Added the M9 task-planning layer with a deterministic `TaskPlanner` and `TaskPlan` record.
- Converted high-level objectives into explicit, inspectable steps with a safety-aware movement path for robotics directives.
- Added the task-planner contract covering normal goals, movement goals, and empty goals.

## 0.1.7
- Added the M8 body-control layer with a deterministic `BodyController` and future-facing `ESP32Controller`.
- Enforced the hardware safety boundary through the body controller before any movement command is accepted.
- Added the M8 contract test covering safe movement, emergency-stop rejection, and serialized ESP32 commands.

## 0.1.6
- Added the M7 tool-safety layer with a validated `ToolRegistry` and a deterministic `SafetyController`.
- Enforced tool execution rules so unsafe tools are blocked before hardware or command execution can occur.
- Added a direct safety test that verifies the gating logic and emergency-stop behavior.

## 0.1.5
- Added the M6 active-cognition layer with a deterministic `ActiveCognition` object and `CognitiveDecision` record.
- Exposed the planning and cognition API through the brain package for local, testable reasoning before advanced ML is introduced.
- Added an active-cognition contract test for empty-goal and goal-oriented planning behavior.

## 0.1.4
- Added the M4 memory layer using a SQLite-backed `MemoryStore` with `remember`, `recall`, and `list_facts` operations.
- Exported the memory API from the package entrypoint and added a direct memory verification script.
- Added the M5 perception layer for local image metadata analysis and basic scene summaries via `VisionPipeline`.
- Added the vision contract test and direct script runner to validate the local perception API.

## 0.1.3
- Added the M3 voice conversation pipeline: microphone/STT → brain → TTS → speaker, with face-state transitions.
- Added the voice-session orchestrator and a developer-facing voice test script.
- Kept all voice behavior modular and isolated behind the brain-level interface.

## 0.1.2
- Added the M2 local-LLM integration layer using a llama.cpp-compatible HTTP client interface.
- Added the brain-level LLM contract and a local model test script.
- Kept all model invocation isolated behind one module to preserve architecture boundaries.

## 0.1.1
- Added the M1 hardware interface layer for camera, microphone, speech-to-text, and TTS.
- Added modular face/state controls and test scripts for each M1 capability.
- Recorded hardware-specific checks as device-dependent and non-blocking on desktop-only workstations.

## 0.1.0
- Initial SCOUT repository bootstrap.
- Added modular package layout.
- Added README, architecture docs, deployment docs, logs, and configuration template.
- Added basic diagnostics and test scaffolding.
- Added M0 validation and commit readiness checks.
