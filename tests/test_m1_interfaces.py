from scout.expression.face import FaceExpression, RobotFace
from scout.expression.text_to_speech import TextToSpeechInterface, TermuxTextToSpeech
from scout.perception.camera import CameraInterface, TermuxCamera
from scout.perception.speech_to_text import SpeechToTextEngine, LocalSpeechToText


def test_camera_interface_contract():
    camera = CameraInterface(camera_id=1, resolution="640x480")
    assert camera.camera_id == 1
    assert camera.resolution == "640x480"
    assert callable(camera.list_cameras)
    assert callable(camera.get_camera_info)
    assert callable(camera.capture_image)


def test_termux_camera_declares_phone_capabilities():
    camera = TermuxCamera(camera_id=0)
    assert camera.camera_id == 0
    assert 0 in camera.list_cameras()
    info = camera.get_camera_info()
    assert info["camera_id"] == 0


def test_face_interface_has_all_states():
    face = RobotFace()
    states = face.cycle_demo()
    expected = {
        FaceExpression.IDLE,
        FaceExpression.LISTENING,
        FaceExpression.THINKING,
        FaceExpression.SPEAKING,
        FaceExpression.HAPPY,
        FaceExpression.CONFUSED,
        FaceExpression.SURPRISED,
        FaceExpression.SLEEPING,
        FaceExpression.ERROR,
    }
    assert set(states) == expected


def test_tts_interface_uses_local_adapter_contract():
    engine = TextToSpeechInterface(voice="default")
    assert engine.list_voices() == ["default"]
    engine2 = TermuxTextToSpeech()
    assert isinstance(engine2, TextToSpeechInterface)


def test_stt_interface_exposes_transcribe_method():
    engine = LocalSpeechToText()
    assert isinstance(engine, SpeechToTextEngine)
    assert callable(engine.transcribe)
