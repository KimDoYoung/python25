# tests/test_rpa_manager.py
import pytest
from unittest.mock import patch, MagicMock
from lib.core.managers.rpa_manager import RpaManager


@pytest.fixture
def mock_executor():
    return MagicMock()


def make_manager(command, **kwargs):
    return RpaManager(command=command, executor=kwargs.pop("executor", None), **kwargs)


@patch("lib.core.managers.rpa_manager.time.sleep")
def test_wait_seconds(mock_sleep, mock_executor):
    manager = make_manager("wait", seconds=2, executor=mock_executor)
    manager.execute()
    mock_sleep.assert_called_once_with(2)


@patch("lib.core.managers.rpa_manager.time.sleep")
def test_wait_minutes(mock_sleep, mock_executor):
    manager = make_manager("wait", minutes=1, executor=mock_executor)
    manager.execute()
    mock_sleep.assert_called_once_with(60)


@patch("lib.core.managers.rpa_manager.pyautogui.write")
def test_put_text_typing(mock_write, mock_executor):
    manager = make_manager("put_text", text="hello", clipboard=False, executor=mock_executor)
    manager.execute()
    mock_write.assert_called_once_with("hello", interval=0.05)


@patch("lib.core.managers.rpa_manager.pyperclip.copy")
@patch("lib.core.managers.rpa_manager.pyautogui.hotkey")
def test_put_text_clipboard(mock_hotkey, mock_copy, mock_executor):
    manager = make_manager("put_text", text="hi!", clipboard=True, executor=mock_executor)
    manager.execute()
    mock_copy.assert_called_once_with("hi!")
    mock_hotkey.assert_called_once_with("ctrl", "v")


@patch("lib.core.managers.rpa_manager.pyperclip.paste", return_value="hello world")
@patch("lib.core.managers.rpa_manager.pyautogui.hotkey")
@patch("lib.core.managers.rpa_manager.time.sleep")
def test_get_text(mock_sleep, mock_hotkey, mock_paste):
    from lib.core.managers.rpa_manager import RpaManager

    mock_executor = MagicMock()

    # ✅ 딕셔너리 말고 키워드 인자로 넘기기
    manager = RpaManager(command="get_text", to_var="result")
    manager.executor = mock_executor  # executor 명시적으로 설정

    manager.get_text()  # execute() 대신 직접 호출

    mock_executor.set_variable.assert_called_once_with("result", "hello world")


@patch("lib.core.managers.rpa_manager.pyautogui.hotkey")
@patch("lib.core.managers.rpa_manager.time.sleep")
def test_key_in(mock_sleep, mock_hotkey, mock_executor):
    manager = make_manager("key_in", keys="ctrl+c", speed=0.1, executor=mock_executor)
    manager.execute()
    mock_hotkey.assert_called_once_with("ctrl", "c")


@patch("lib.core.managers.rpa_manager.pyautogui.screenshot")
@patch("lib.core.managers.rpa_manager.Image")
@patch("lib.core.managers.rpa_manager.RpaManager._get_temp_file_path", return_value="test.png")
def test_capture_to_file(mock_tmp, mock_img_class, mock_screenshot, mock_executor):
    dummy_img = MagicMock()
    mock_screenshot.return_value = dummy_img
    manager = make_manager("capture", to_file="out.png", executor=mock_executor)
    manager.execute()
    dummy_img.save.assert_called_once_with("out.png")
