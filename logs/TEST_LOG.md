# SCOUT Test Log

## TEST-000 — Repository bootstrap

Device: Ubuntu development workstation
Command:
```bash
python -m pytest -q
```
Expected: All repository-level tests pass.
Actual: PASS
Result: PASS

---

## TEST-001 — Doctor script

Device: Ubuntu development workstation
Command:
```bash
python scripts/doctor.py
```
Expected: Human-readable system check output with explicit pass/fail states.
Actual: PASS
Result: PASS

---

## TEST-015 — Face expression demo

Device: Ubuntu development workstation
Command:
```bash
python3 scripts/test_face.py
```
Expected: All face states cycle successfully.
Actual: PASS
Result: PASS

---

## TEST-020 — Local LLM client

Device: Ubuntu development workstation
Command:
```bash
python3 scripts/test_llm.py
```
Expected: If the llama.cpp server is not running, report NOT TESTED instead of pretending success.
Actual: NOT TESTED — llama.cpp server is not running on http://127.0.0.1:8080
Result: PASS (contract validated)

---

## TEST-021 — Voice pipeline

Device: Ubuntu development workstation
Command:
```bash
python3 scripts/test_voice.py
```
Expected: A fake STT, LLM, and TTS chain should complete the full conversation path while changing face states in sequence.
Actual: PASS
Result: PASS

---

## TEST-022 — Vision pipeline

Device: Ubuntu development workstation
Command:
```bash
python3 scripts/test_vision.py
```
Expected: The pipeline should read a sample JPEG and return basic metadata for a scene summary without crashing on unknown file types.
Actual: PASS
Result: PASS

---

## TEST-023 — Active cognition

Device: Ubuntu development workstation
Command:
```bash
python3 -m pytest -q tests/test_active_cognition.py
```
Expected: A clear local decision should be produced from a given goal, and an empty goal should degrade safely to a safe default plan.
Actual: PASS
Result: PASS

---

## TEST-024 — Tool safety layer

Device: Ubuntu development workstation
Command:
```bash
python3 -m pytest -q tests/test_tool_safety.py
```
Expected: Safe tools should execute, unsafe tools should be rejected, and emergency-stop state should block hardware actions.
Actual: PASS
Result: PASS

---

## TEST-025 — Body control layer

Device: Ubuntu development workstation
Command:
```bash
python3 -m pytest -q tests/test_body_control.py
```
Expected: Body movement commands should be approved only through the safe controller path, and the ESP32 command serializer should return a serializable payload.
Actual: PASS
Result: PASS

---

## TEST-026 — Task planning layer

Device: Ubuntu development workstation
Command:
```bash
python3 -m pytest -q tests/test_task_planner.py
```
Expected: Goals should be converted into explicit steps, movement-oriented goals should trigger a safety gate, and empty goals should degrade to the safe default plan.
Actual: PASS
Result: PASS

---

## TEST-027 — Mission execution layer

Device: Ubuntu development workstation
Command:
```bash
python3 -m pytest -q tests/test_mission_loop.py
```
Expected: A valid plan should be executed to a completed status, a movement plan should be blocked by emergency-stop state, and empty plans should still resolve to a safe default result.
Actual: PASS
Result: PASS

---

## TEST-028 — Memory-aware planning layer

Device: Ubuntu development workstation
Command:
```bash
python3 -m pytest -q tests/test_memory_aware_planning.py
```
Expected: Relevant memory facts should be retrieved by subject and injected into the planner context without breaking the fallback path when no memory is available.
Actual: PASS
Result: PASS

---

## TEST-029 — Session memory layer

Device: Ubuntu development workstation
Command:
```bash
python3 -m pytest -q tests/test_session_memory.py
```
Expected: Recent goals should be stored in session memory and included in the planning context, while empty-session fallback should remain safe and deterministic.
Actual: PASS
Result: PASS

---

## TEST-030 — Goal queue layer

Device: Ubuntu development workstation
Command:
```bash
python3 -m pytest -q tests/test_goal_queue.py
```
Expected: Higher-priority goals should be selected before lower-priority ones, and an empty queue should return a safe empty result.
Actual: PASS
Result: PASS

---

## TEST-031 — Goal scheduler layer

Device: Ubuntu development workstation
Command:
```bash
python3 -m pytest -q tests/test_goal_scheduler.py
```
Expected: The scheduler should pick the highest-priority queued goal and turn it into a concrete plan while returning a safe empty result when the queue is empty.
Actual: PASS
Result: PASS

---

## TEST-032 — Behavior loop layer

Device: Ubuntu development workstation
Command:
```bash
python3 -m pytest -q tests/test_behavior_loop.py
```
Expected: The behavior loop should run the highest-priority queued goal through the scheduler and plan pipeline while returning a safe empty result when there are no queued goals.
Actual: PASS
Result: PASS

---

## TEST-010 — Camera hardware

Device: POCO X3 / Android Termux required
Command:
```bash
termux-camera-photo -c 0 test.jpg
```
Expected: JPEG image created.
Actual: NOT TESTED — requires physical POCO X3 and Termux environment.
Result: NOT TESTED

---

## TEST-011 — Microphone hardware

Device: POCO X3 / Android Termux required
Command:
```bash
termux-microphone-record -d 3 test.wav
```
Expected: Audio file created.
Actual: NOT TESTED — requires physical POCO X3 and Termux environment.
Result: NOT TESTED

---

## TEST-012 — TTS hardware

Device: POCO X3 / Android Termux required
Command:
```bash
termux-tts-speak "Hello. I am SCOUT."
```
Expected: Audio playback is audible.
Actual: NOT TESTED — requires physical POCO X3 and Termux environment.
Result: NOT TESTED

---

## TEST-013 — STT hardware

Device: POCO X3 / Android Termux required
Command: Device-dependent speech recognition test.
Expected: Spoken words are transcribed.
Actual: NOT TESTED — requires physical POCO X3 and microphone access.
Result: NOT TESTED

---

## TEST-014 — Face display

Device: POCO X3 / Android display required
Command: Device-dependent face-state demonstration.
Expected: Expression states cycle successfully.
Actual: NOT TESTED — requires physical device and UI runtime.
Result: NOT TESTED
