from __future__ import annotations


class TextToSpeechInterface:
    """Abstract TTS interface intended to wrap Android Termux or local engines."""

    def __init__(self, voice: str | None = None) -> None:
        self.voice = voice

    def list_voices(self) -> list[str]:
        return [self.voice] if self.voice else []

    def speak(self, text: str) -> str:
        raise NotImplementedError("Speech synthesis is intentionally deferred until M1 hardware validation.")

    def stop(self) -> None:
        return None
