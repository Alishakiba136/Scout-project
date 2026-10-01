"""Perception subsystem stubs."""

from .camera import CameraInterface, TermuxCamera
from .microphone import MicrophoneInterface, TermuxMicrophone
from .speech_to_text import LocalSpeechToText, SpeechToTextEngine
from .vision import SceneObservation, VisionPipeline

__all__ = [
    "CameraInterface",
    "TermuxCamera",
    "MicrophoneInterface",
    "TermuxMicrophone",
    "SceneObservation",
    "SpeechToTextEngine",
    "LocalSpeechToText",
    "VisionPipeline",
]
