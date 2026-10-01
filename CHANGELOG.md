# Changelog

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
