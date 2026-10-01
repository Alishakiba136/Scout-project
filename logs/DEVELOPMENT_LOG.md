# SCOUT Development Log

## 2026-10-01 — Step 01 — Repository bootstrap

### Goal
Create the initial SCOUT repository structure and establish the product baseline for M0.

### Changes
- Initialized the Git repository.
- Created the modular package layout under `scout/`.
- Added root configuration files, changelog, and documentation placeholders.
- Established the standard logs and test infrastructure.

### Why
The project must be maintainable, modular, and fully documented before any advanced AI or hardware integration begins.

### Testing
- `python -m pytest -q`

### Result
PARTIAL

### Problems
The workspace was empty at the start of the task, so the project had to be created from scratch rather than continuing an existing codebase. No direct hardware tests were possible on this machine.

### Next step
Implement the configuration and system diagnostics required for M0 validation.

---

## 2026-10-01 — Step 02 — Configuration and diagnostics foundation

### Goal
Create a working configuration model and a doctor script that reports subsystem availability clearly.

### Changes
- Added `scout/app/config.py` with a TOML-based configuration loader.
- Added `scripts/doctor.py` to check Python, OS, architecture, local model hints, database status, and tool availability.
- Added sample configuration under `config/config.example.toml`.

### Why
SCOUT must be configurable without hard-coded runtime assumptions, and a doctor script is required before higher-level features are implemented.

### Testing
- `python scripts/doctor.py`
- `python -m pytest -q`

### Result
PASS

### Problems
No blocker encountered. The doctor script reports environment-specific checks without pretending hardware is present.

### Next step
Run the final M0 validation pass and prepare the Git commit.

---

## 2026-10-01 — Step 03 — M0 validation

### Goal
Confirm the repository bootstraps correctly and the base project remains testable.

### Changes
- Added the project README and structured docs.
- Added the decision log and test log.
- Finalized package scaffolding and tests.

### Why
M0 must end with working repository-level validation, not just a file tree.

### Testing
- `python -m pytest -q`
- `python scripts/doctor.py`

### Result
PASS

### Problems
No critical blockers. Hardware capability tests remain intentionally marked as NOT TESTED when they require the POCO X3 or physical devices.

### Next step
Create the M0 Git commit and stop before M1.

---

## 2026-10-01 — Step 04 — M1 hardware interface layer

### Goal
Establish the phone hardware abstraction layer required for the M1 milestone without advancing into LLM or memory work.

### Changes
- Implemented device-aware camera and microphone interfaces in `scout/perception/`.
- Implemented a local/offline speech-to-text adapter in `scout/perception/speech_to_text.py`.
- Added a device-aware TTS adapter in `scout/expression/text_to_speech.py`.
- Extended the face state model so expression changes can be exercised programmatically.
- Added M1 validation scripts in `scripts/` for camera, microphone, STT, TTS, and face testing.

### Why
The project must prove the hardware abstraction layer exists cleanly before moving to higher-level cognition work.

### Testing
- `python3 -m pytest -q`
- `python3 scripts/test_face.py`
- `python3 scripts/test_camera.py`
- `python3 scripts/test_microphone.py`
- `python3 scripts/test_stt.py`
- `python3 scripts/test_tts.py`

### Result
PASS

### Problems
The development workstation is not a POCO X3 / Android Termux environment, so the actual phone hardware checks remain NOT TESTED unless run on the target device.

### Next step
Prepare the M1 commit and then move to the next milestone only after validating the environment-specific hardware target.

---

## 2026-10-01 — Step 05 — M2 local LLM interface

### Goal
Create the isolated local LLM adapter for llama.cpp so the model layer remains behind a clean interface and is not scattered through the application.

### Changes
- Added `scout/brain/llm.py` with a generic `LLMClient` and a `LlamaCppClient` implementation.
- Exported the client from `scout/brain/__init__.py`.
- Added `scripts/test_llm.py` and `tests/test_llm.py` for contract and integration validation.

### Why
The LLM should be isolated behind a single interface and should not be embedded into the rest of the application.

### Testing
- `python3 -m pytest -q`
- `python3 scripts/test_llm.py`

### Result
PASS

### Problems
The local llama.cpp server is not running on this workstation, so the live model request remains NOT TESTED. The script reports the expected logical status instead of pretending the server is available.

### Next step
When the local model server is started, run the LLM script again and then proceed to the next milestone only after confirming the endpoint responds.

---

## 2026-10-01 — Step 06 — M3 voice conversation pipeline

### Goal
Implement the direct microphone-to-transcription-to-LLM-to-speech loop with face-state transitions that matches the SCOUT product spec.

### Changes
- Added `scout/brain/voice.py` with the `VoicePipeline` orchestrator.
- Exported the new pipeline in `scout/brain/__init__.py`.
- Added `scripts/test_voice.py` to exercise the conversation flow on a desktop workstation without hardware access.
- Added `tests/test_voice_pipeline.py` for the core contract.

### Why
M3 is the first full conversation loop and must remain modular so that real device hardware can be plugged in behind the same interfaces.

### Testing
- `python3 -m pytest -q`
- `python3 scripts/test_voice.py`

### Result
PASS

### Problems
No code-level blockers. Actual microphone and speaker hardware remains untested here because the POCO X3 runtime is not present.

### Next step
Proceed only after the hardware target is ready for real device validation of the full voice path.
