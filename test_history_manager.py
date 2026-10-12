from history_manager import cleanup_history, get_snapshots
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from datetime import datetime

import constants
import config

import pytest
import history_manager

def test_cleanup_history_when_snapshot_disappears():
    with TemporaryDirectory() as temp_dir:
        history_path = Path(temp_dir) / "History"
        history_path.mkdir()

        folders = ["2026-08-12_10-00-00", "2026-08-13_10-00-00", "2026-08-14_10-00-00"]

        for folder_name in folders:
            full_path = history_path / folder_name
            full_path.mkdir()

        config.MAX_HISTORY = 3

        def fake_rmtree(path):
            path.rmdir()
            raise FileNotFoundError

        with patch("history_manager.shutil.rmtree") as mock_rmtree:
            mock_rmtree.side_effect = fake_rmtree

            cleanup_history(history_path)

        snapshots = get_snapshots(history_path)

        assert len(snapshots) == 2


def test_cleanup_history_raises_permission_error():
    with TemporaryDirectory() as temp_dir:
        history_path = Path(temp_dir) / "History"
        history_path.mkdir()

        folders = [
            "2026-08-12_10-00-00",
            "2026-08-13_10-00-00",
            "2026-08-14_10-00-00"
        ]

        for folder_name in folders:
            full_path = history_path / folder_name
            full_path.mkdir()

        config.MAX_HISTORY = 3

        with patch("history_manager.shutil.rmtree") as mock_rmtree:
            mock_rmtree.side_effect = PermissionError

            with pytest.raises(PermissionError):
                cleanup_history(history_path)


def test_save_current_to_history(tmp_path):
    current_path = tmp_path / "Current"
    history_path = tmp_path / "History"

    current_path.mkdir()
    history_path.mkdir()

    test_file = current_path / "test.txt"
    test_file.write_text("test")

    snapshot_path = history_manager.save_current_to_history(
        current_path,
        history_path,
    )

    datetime.strptime(
        snapshot_path.name,
        constants.SNAPSHOT_NAME_FORMAT,
    )

    snapshot_file = snapshot_path / "test.txt"

    assert snapshot_file.exists()
    assert snapshot_file.read_text() == "test"

    assert snapshot_path.exists()


def test_prepare_history_creates_snapshot(tmp_path):
    current_path = tmp_path / "Current"
    history_path = tmp_path / "History"

    current_path.mkdir()
    history_path.mkdir()

    test_file = current_path / "test.txt"
    test_file.write_text("test")

    result = history_manager.prepare_history(
        current_path,
        history_path,
    )

    assert result.success

    snapshots = list(history_path.iterdir())

    assert len(snapshots) == 1


def test_cleanup_history_removes_oldest_snapshot(tmp_path):
    history_path = tmp_path / "History"
    history_path.mkdir()

    folders = [
        "2026-08-12_10-00-00",
        "2026-08-13_10-00-00",
        "2026-08-14_10-00-00",
    ]

    for folder_name in folders:
        full_path = history_path / folder_name
        full_path.mkdir()

    config.MAX_HISTORY = 3

    history_manager.cleanup_history(history_path)

    snapshots = get_snapshots(history_path)

    assert len(snapshots) == 2
    assert snapshots[0].name == "2026-08-13_10-00-00"

def test_cleanup_history_ignores_invalid_folder(tmp_path):

    history_path = tmp_path / "History"
    history_path.mkdir()

    valid_folders = [
        "2026-08-12_10-00-00",
        "2026-08-13_10-00-00",
        "2026-08-14_10-00-00",
    ]

    for folder_name in valid_folders:
        (history_path / folder_name).mkdir()

    invalid_folder = history_path / "MyImportantFolder"
    invalid_folder.mkdir()

    config.MAX_HISTORY = 3

    history_manager.cleanup_history(history_path)

    assert invalid_folder.exists()