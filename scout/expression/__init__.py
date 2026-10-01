"""Expression package for speech and face logic."""

from .face import FaceExpression, RobotFace
from .text_to_speech import TermuxTextToSpeech, TextToSpeechInterface

__all__ = ["FaceExpression", "RobotFace", "TextToSpeechInterface", "TermuxTextToSpeech"]
