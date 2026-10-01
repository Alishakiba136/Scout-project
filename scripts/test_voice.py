#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scout.brain.voice import VoicePipeline
from scout.expression.face import FaceExpression


class FakeSTT:
    def transcribe(self, audio_path: str | Path) -> str:
        return "hello scout"


class FakeLLM:
    def generate(self, messages, tools=None):
        return "Hello to you too."


class FakeTTS:
    def speak(self, text: str) -> str:
        return text


def main() -> int:
    pipeline = VoicePipeline(
        stt_engine=FakeSTT(),
        llm_client=FakeLLM(),
        tts_engine=FakeTTS(),
    )
    result = pipeline.process_audio(Path("tmp/user_input.wav"), user_text="hello scout")
    print(f"Transcript: {result['transcript']}")
    print(f"Response: {result['response']}")
    print(f"Face state: {pipeline.face.current.value}")
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
