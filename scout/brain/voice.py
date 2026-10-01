from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from scout.expression.face import FaceExpression, RobotFace
from scout.expression.text_to_speech import TermuxTextToSpeech, TextToSpeechInterface
from scout.perception.speech_to_text import LocalSpeechToText, SpeechToTextEngine


class VoicePipeline:
    """Microphone -> STT -> brain -> TTS -> speaker loop with face-state progression."""

    def __init__(
        self,
        stt_engine: SpeechToTextEngine | None = None,
        llm_client: Any | None = None,
        tts_engine: TextToSpeechInterface | None = None,
        face: RobotFace | None = None,
        system_prompt: str | None = None,
    ) -> None:
        self.stt_engine = stt_engine or LocalSpeechToText()
        self.llm_client = llm_client
        self.tts_engine = tts_engine or TermuxTextToSpeech()
        self.face = face or RobotFace()
        self.system_prompt = system_prompt or "You are SCOUT, a helpful local robot. Respond briefly and naturally."

    def process_audio(self, audio_path: str | Path, user_text: str | None = None) -> dict[str, str]:
        audio_file = Path(audio_path)
        self.face.set_expression(FaceExpression.LISTENING)

        transcript = user_text or self.stt_engine.transcribe(audio_file)
        self.face.set_expression(FaceExpression.THINKING)

        if self.llm_client is None:
            response = transcript
        else:
            response = self.llm_client.generate(
                [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": transcript},
                ]
            )

        self.face.set_expression(FaceExpression.SPEAKING)
        spoken = self.tts_engine.speak(response)
        self.face.set_expression(FaceExpression.IDLE)

        return {
            "transcript": transcript,
            "response": response,
            "spoken": spoken,
        }
