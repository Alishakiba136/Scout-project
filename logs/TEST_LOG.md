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
