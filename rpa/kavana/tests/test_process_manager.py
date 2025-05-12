# tests/test_process_manager.py
import pytest
from unittest.mock import patch, MagicMock
from lib.core.managers.process_manager import ProcessManager, WindowInfo


@pytest.fixture
def process_manager():
    return ProcessManager(executor=MagicMock())


@patch("lib.core.managers.process_manager.psutil.process_iter")
def test_get_pid_by_process_name(mock_iter, process_manager):
    mock_iter.return_value = [
        MagicMock(info={"pid": 1234, "name": "notepad.exe"})
    ]
    pid = process_manager.get_pid_by_process_name("notepad.exe")
    assert pid == 1234


@patch("lib.core.managers.process_manager.psutil.process_iter")
def test_kill_process_by_name(mock_iter, process_manager):
    proc = MagicMock()
    mock_iter.return_value = [proc]
    proc.info = {"name": "test.exe"}
    process_manager.kill_process_by_name("test.exe")
    proc.terminate.assert_called_once()
    proc.wait.assert_called_once()


def test_get_window_info_list(process_manager):
    from lib.core.managers import process_manager as pm

    with patch("lib.core.managers.process_manager.win32gui.EnumWindows") as mock_enum, \
         patch("lib.core.managers.process_manager.psutil.Process") as mock_proc, \
         patch("lib.core.managers.process_manager.win32process.GetWindowThreadProcessId", return_value=(0, 1111)), \
         patch("lib.core.managers.process_manager.win32gui.GetClassName", return_value="MyClass"), \
         patch("lib.core.managers.process_manager.win32gui.GetWindowText", return_value="My Window"), \
         patch("lib.core.managers.process_manager.win32gui.IsWindowVisible", return_value=True):

        mock_proc.return_value.name.return_value = "myapp.exe"
        callback = mock_enum.call_args[0][0] if mock_enum.call_args else lambda hwnd, _: None
        callback(1000, None)  # simulate one window
        result = process_manager.get_window_info_list("myapp.exe")
        assert isinstance(result, list)


@patch("lib.core.managers.process_manager.win32gui.GetForegroundWindow", return_value=5555)
@patch("lib.core.managers.process_manager.win32gui.GetWindowText", return_value="Active")
@patch("lib.core.managers.process_manager.win32gui.GetClassName", return_value="TopClass")
def test_find_top_window_info(_, __, ___, process_manager):
    process_manager.executor = MagicMock()
    info = process_manager.find_top_window_info()
    assert isinstance(info, WindowInfo)
    process_manager.executor.log_command.assert_called()


def test_find_mdi_top_window_info(process_manager):
    with patch("lib.core.managers.process_manager.win32gui.IsWindowVisible", return_value=True), \
         patch("lib.core.managers.process_manager.win32gui.IsWindowEnabled", return_value=True), \
         patch("lib.core.managers.process_manager.win32gui.GetWindowText", return_value="child title"), \
         patch("lib.core.managers.process_manager.win32gui.GetClassName", return_value="mdi_child"), \
         patch("lib.core.managers.process_manager.win32gui.EnumChildWindows") as mock_enum:

        hwnd = 1234
        mock_enum.side_effect = lambda parent, cb, l: cb(hwnd, l)
        info = process_manager.find_mdi_top_window_info(9999)
        assert info.hwnd == hwnd

@patch("lib.core.managers.process_manager.win32gui.GetWindowRect", return_value=(10, 20, 110, 220))
def test_get_window_region(mock_rect, process_manager):
    region = process_manager.get_window_region(123)
    assert region == (10, 20, 100, 200)



def test_find_top_modal_window(process_manager):
    with patch("lib.core.managers.process_manager.win32gui.IsWindowVisible", return_value=True), \
         patch("lib.core.managers.process_manager.win32gui.IsWindowEnabled", return_value=True), \
         patch("lib.core.managers.process_manager.win32gui.GetWindowText", return_value="modal window"), \
         patch("lib.core.managers.process_manager.win32gui.GetClassName", return_value="DialogClass"), \
         patch("lib.core.managers.process_manager.win32gui.EnumWindows") as mock_enum, \
         patch("lib.core.managers.process_manager.win32process.GetWindowThreadProcessId", return_value=(0, 7777)), \
         patch("lib.core.managers.process_manager.psutil.Process") as mock_proc:

        mock_proc.return_value.name.return_value = "modal.exe"
        mock_enum.side_effect = lambda cb, l: cb(5000, l)

        info = process_manager.find_top_modal_window("modal.exe")
        assert info.hwnd == 5000
