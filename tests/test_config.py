from scout.app.config import load_config, resolve_config_path


def test_config_example_loads():
    config = load_config()
    assert isinstance(config, dict)
    assert config["project"]["name"] == "scout"


def test_config_path_resolution_uses_example_when_local_missing():
    path = resolve_config_path()
    assert path.name in {"config.toml", "config.example.toml"}
