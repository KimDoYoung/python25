import pytest
from unittest.mock import patch, MagicMock
from lib.core.managers.sftp_manager import SftpManager


@pytest.fixture
def mock_sftp(monkeypatch):
    mock_ssh = MagicMock()
    mock_sftp = MagicMock()
    mock_ssh.open_sftp.return_value = mock_sftp

    monkeypatch.setattr("paramiko.SSHClient", lambda: mock_ssh)
    return mock_ssh, mock_sftp


def test_list_files(mock_sftp):
    mock_ssh, sftp = mock_sftp
    sftp.listdir.return_value = ["a.txt", "b.txt"]
    sftp.stat.side_effect = lambda path: MagicMock(st_size=123, st_mtime=1680000000)

    manager = SftpManager(
        command="list",
        remote_dir="/remote",
        pattern="*.txt",
        user="tester",
        password="dummy"
    )
    result = manager.execute()
    assert len(result) == 2
    assert result[0]["name"] == "a.txt"
    assert "modified" in result[0]


def test_upload(mock_sftp, tmp_path):
    mock_ssh, sftp = mock_sftp
    test_file = tmp_path / "upload.txt"
    test_file.write_text("data")

    manager = SftpManager(
        command="upload",
        local_dir=str(tmp_path),
        remote_dir="/upload",
        files=[str(test_file.name)],
        user="tester",
        password="dummy"
    )
    manager.execute()
    sftp.put.assert_called_once()


def test_download(mock_sftp, tmp_path):
    mock_ssh, sftp = mock_sftp
    sftp.listdir.return_value = ["test.txt"]
    sftp.get.return_value = None

    manager = SftpManager(
        command="download",
        local_dir=str(tmp_path),
        remote_dir="/remote",
        files=["test.txt"],
        user="tester",
        password="dummy"
    )
    manager.execute()
    sftp.get.assert_called_once()


def test_delete(mock_sftp):
    mock_ssh, sftp = mock_sftp
    manager = SftpManager(
        command="delete",
        remote_dir="/remote",
        files=["delete_me.txt"],
        user="tester",
        password="dummy"
    )
    manager.execute()
    sftp.remove.assert_called_once_with("/remote/delete_me.txt")


def test_mkdir(mock_sftp):
    mock_ssh, sftp = mock_sftp
    manager = SftpManager(
        command="mkdir",
        remote_dir="/remote/newdir",
        user="tester",
        password="dummy"
    )
    manager.execute()
    sftp.mkdir.assert_called_once_with("/remote/newdir")


def test_rmdir(mock_sftp):
    mock_ssh, sftp = mock_sftp
    manager = SftpManager(
        command="rmdir",
        remote_dir="/remote/olddir",
        user="tester",
        password="dummy"
    )
    manager.execute()
    sftp.rmdir.assert_called_once_with("/remote/olddir")
