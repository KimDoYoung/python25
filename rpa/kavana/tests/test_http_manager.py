import pytest
from unittest.mock import patch, MagicMock
from requests.exceptions import SSLError
from lib.core.managers.http_manager import HttpManager


def create_http_manager(command="get", url="https://example.com", **kwargs):
    options = {
        "command": command,
        "url": url,
        **kwargs
    }
    return HttpManager(**options)


@patch("lib.core.managers.http_manager.requests.request")
def test_send_request_with_requests_get(mock_request):
    mock_response = MagicMock()
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"status": "ok"}
    mock_request.return_value = mock_response

    manager = create_http_manager(command="get")
    result = manager.execute()

    mock_request.assert_called_once()
    assert result == {"status": "ok"}


@patch("lib.core.managers.http_manager.requests.request", side_effect=SSLError("boom"))  # ✅ SSLError로 변경
@patch("lib.core.managers.http_manager.subprocess.run")  # ✅ subprocess.run 패치 추가
def test_requests_fail_to_curl(mock_subprocess_run, mock_request):
    mock_subproc = MagicMock()
    mock_subproc.stdout = '{"message": "ok"}'
    mock_subprocess_run.return_value = mock_subproc

    manager = create_http_manager(command="post", body={"msg": "hi"}, content_type="application/json")
    result = manager.execute()
    assert result == {"message": "ok"}


@patch("lib.core.managers.http_manager.requests.request")
def test_send_post_with_json(mock_request):
    mock_response = MagicMock()
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"result": "created"}
    mock_request.return_value = mock_response

    manager = create_http_manager(
        command="post",
        body={"name": "test"},
        content_type="application/json"
    )
    result = manager.execute()

    called_args = mock_request.call_args[1]
    assert called_args["json"] == {"name": "test"}
    assert result == {"result": "created"}


@patch("lib.core.managers.http_manager.requests.request")
def test_send_post_with_form(mock_request):
    mock_response = MagicMock()
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"result": "form"}
    mock_request.return_value = mock_response

    manager = create_http_manager(
        command="post",
        body="name=test",
        content_type="application/x-www-form-urlencoded"
    )
    result = manager.execute()

    called_args = mock_request.call_args[1]
    assert called_args["data"] == "name=test"
    assert result == {"result": "form"}


@patch("lib.core.managers.http_manager.requests.request")
def test_parse_plain_text_response(mock_request):
    mock_response = MagicMock()
    mock_response.headers = {"Content-Type": "text/plain"}
    mock_response.text = "hello world"
    mock_request.return_value = mock_response

    manager = create_http_manager()
    result = manager.execute()

    assert result == "hello world"


@patch("lib.core.managers.http_manager.requests.request")
def test_parse_invalid_json_logs_error(mock_request, capsys):
    mock_response = MagicMock()
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.side_effect = ValueError("invalid json")
    mock_response.text = '{"invalid}'
    mock_request.return_value = mock_response

    manager = create_http_manager()
    result = manager.execute()

    captured = capsys.readouterr()
    assert "HTTP 응답 파싱 실패" in captured.out
    assert result == '{"invalid}'
