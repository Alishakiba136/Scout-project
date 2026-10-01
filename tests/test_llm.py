from unittest.mock import patch

from scout.brain.llm import LLMClient, LlamaCppClient


def test_llm_client_contract():
    client = LLMClient()
    try:
        client.generate([{"role": "user", "content": "hello"}])
    except NotImplementedError:
        pass
    else:
        raise AssertionError("Base LLM client should require implementation.")


def test_llama_client_builds_http_request_and_returns_text():
    with patch("scout.brain.llm.urlopen") as mocked_urlopen:
        class MockResponse:
            def __init__(self, payload):
                self.payload = payload

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def read(self):
                return b'{"choices": [{"message": {"content": "hello from scout"}}]}'

        mocked_urlopen.return_value = MockResponse({})

        client = LlamaCppClient(server_url="http://127.0.0.1:8080")
        response = client.generate([{"role": "user", "content": "hello"}], tools=[{"name": "speak"}])

    assert response == "hello from scout"
    assert mocked_urlopen.called
