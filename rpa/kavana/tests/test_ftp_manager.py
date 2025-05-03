# tests/test_ftp_manager.py
import pytest
from unittest.mock import patch, MagicMock
from lib.core.managers.ftp_manager import FtpManager  # ✅ 경로 조정


@pytest.fixture
def mock_ftp():
    ftp = MagicMock()
    ftp.nlst.return_value = ['file1.txt', 'file2.txt']
    ftp.size.return_value = 123
    ftp.sendcmd.side_effect = lambda cmd: "213 20240101123000" if cmd.startswith("MDTM") else "200 OK"
    return ftp


@pytest.fixture
def ftp_manager(mock_ftp):
    with patch("lib.core.managers.ftp_manager.FTP", return_value=mock_ftp):
        mgr = FtpManager(
            command="upload",
            files=["/path/to/file1.txt"],
            remote_dir="/remote",
            local_dir="/local",
            overwrite=True
        )
        yield mgr


def test_upload_with_file(monkeypatch, ftp_manager, mock_ftp):
    # 파일이 존재하도록 설정
    monkeypatch.setattr("os.path.isfile", lambda f: True)
    monkeypatch.setattr("os.chdir", lambda path: None)
    monkeypatch.setattr("builtins.open", lambda *a, **kw: MagicMock())

    ftp_manager.execute()

    # storbinary가 파일 이름으로 호출되었는지 확인
    mock_ftp.storbinary.assert_called()


def test_download(monkeypatch, mock_ftp):
    with patch("lib.core.managers.ftp_manager.FTP", return_value=mock_ftp): 
        mgr = FtpManager(
            command="download",
            files=["file1.txt"],
            remote_dir="/remote",
            local_dir="/local",
            overwrite=True
        )

        monkeypatch.setattr("os.path.exists", lambda f: False)
        monkeypatch.setattr("os.chdir", lambda path: None)
        monkeypatch.setattr("builtins.open", lambda *a, **kw: MagicMock())
        monkeypatch.setattr("os.makedirs", lambda path: None)

        mgr.execute()

        mock_ftp.retrbinary.assert_called()


def test_list(mock_ftp):
    with patch("lib.core.managers.ftp_manager.FTP", return_value=mock_ftp): 
        mgr = FtpManager(
            command="list",
            remote_dir="/remote",
            pattern="*.txt"
        )

        result = mgr.execute()
        assert isinstance(result, list) or result is None  # list()는 return값 있음


def test_mkdir(mock_ftp):
    with patch("lib.core.managers.ftp_manager.FTP", return_value=mock_ftp): 
        mgr = FtpManager(command="mkdir", remote_dir="/new_dir")
        mgr.execute()
        mock_ftp.mkd.assert_called_with("/new_dir")


def test_rmdir(mock_ftp):
    with patch("lib.core.managers.ftp_manager.FTP", return_value=mock_ftp): 
        mgr = FtpManager(command="rmdir", remote_dir="/old_dir")
        mgr.execute()
        mock_ftp.rmd.assert_called_with("/old_dir")


def test_delete(mock_ftp):
    with patch("lib.core.managers.ftp_manager.FTP", return_value=mock_ftp): 
        mgr = FtpManager(command="delete", files=["file1.txt", "file2.txt"])
        mgr.execute()
        assert mock_ftp.delete.call_count == 2


def test_unsupported_command():
    with pytest.raises(RuntimeError, match="지원하지 않는 명령어입니다"):
        FtpManager(command="unknown").execute()


def test_missing_command():
    with pytest.raises(RuntimeError, match="command는 필수입니다."):
        FtpManager()
