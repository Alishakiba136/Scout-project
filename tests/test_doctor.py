from scripts.doctor import run_doctor


def test_doctor_reports_required_checks():
    report = run_doctor()
    required = {
        "python",
        "architecture",
        "operating_system",
        "termux",
        "camera",
        "microphone",
        "tts",
        "stt",
        "storage_permissions",
        "network",
        "local_model",
        "llama_cpp",
        "database",
        "overall",
        "hardware_status",
    }
    assert required.issubset(report.keys())
    assert isinstance(report["overall"], str)
    assert isinstance(report["hardware_status"], str)
