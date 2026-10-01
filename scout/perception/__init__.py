"""Perception subsystem stubs."""

from .camera import CameraInterface, TermuxCamera
from .microphone import MicrophoneInterface, TermuxMicrophone
from .speech_to_text import LocalSpeechToText, SpeechToTextEngine

__all__ = [
    "CameraInterface",
    "TermuxCamera",
    "MicrophoneInterface",
    "TermuxMicrophone",
    "SpeechToTextEngine",
    "LocalSpeechToText",
]
