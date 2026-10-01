from pathlib import Path

from scout.brain.voice import VoicePipeline
from scout.expression.face import FaceExpression


class FakeSTT:
    def transcribe(self, audio_path: str | Path) -> str:
        return "hello scout"


class FakeLLM:
    def generate(self, messages, tools=None):
        return "Hello to you too."


class FakeTTS:
    def __init__(self):
        self.last_text = ""

    def speak(self, text: str) -> str:
        self.last_text = text
        return text


class FakeFace:
    def __init__(self):
        self.history = []

    def set_expression(self, expression):
        self.history.append(expression)
        return expression


def test_voice_pipeline_handles_listen_think_speak_cycle():
    stt = FakeSTT()
    llm = FakeLLM()
    tts = FakeTTS()
    face = FakeFace()

    pipeline = VoicePipeline(stt_engine=stt, llm_client=llm, tts_engine=tts, face=face)
    result = pipeline.process_audio(Path("tmp/test.wav"))

    assert result["transcript"] == "hello scout"
    assert result["response"] == "Hello to you too."
    assert result["spoken"] == "Hello to you too."
    assert face.history[0] == FaceExpression.LISTENING
    assert FaceExpression.THINKING in face.history
    assert FaceExpression.SPEAKING in face.history
    assert face.history[-1] == FaceExpression.IDLE
