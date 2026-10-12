from pathlib import Path
from unittest.mock import patch
from exceptions import CopyFileError
from project_dataclasses import DiskSpaceInfo, VerificationResult

import pytest
import backup_manager
import config



def test_copy_source_to_current_raises_copy_file_error(tmp_path, monkeypatch):
    source_path = tmp_path / "Source"
    current_path = tmp_path / "Current"

    source_path.mkdir()
    current_path.mkdir()

    source_file = source_path / "test.txt"
    source_file.write_text("test")

    def fake_copy2(source, destination):
        raise PermissionError("Access denied")

    monkeypatch.setattr(
        backup_manager.shutil,
        "copy2",
        fake_copy2,
    )

    with pytest.raises(CopyFileError) as error:
        backup_manager.copy_source_to_current(
            source_path,
            current_path,
        )

    assert error.value.file_path == source_file
    assert isinstance(error.value.original_error, PermissionError)



def test_clear_current(tmp_path):
    current_path = tmp_path / "Current"
    file_name_1 = "test_text_1.txt"
    folder_name_1 = "test_folder_1"
    file_path_1 = current_path / file_name_1
    folder_path_1 = current_path / folder_name_1
    file_name_2 = "test_text_2.txt"
    file_path_2 = folder_path_1 / file_name_2


    current_path.mkdir()
    folder_path_1.mkdir()

    file_path_1.write_text("test_1")
    file_path_2.write_text("test_2")

    backup_manager.clear_current(current_path)

    assert current_path.exists()
    assert not file_path_1.exists()
    assert not folder_path_1.exists()


def test_start_backup_clears_current_after_copy_error(tmp_path, monkeypatch):
    project_path = tmp_path
    source_path = project_path / "Source"
    current_path = project_path / "Current"

    source_path.mkdir()
    current_path.mkdir()

    monkeypatch.setattr(
        config,
        "PROJECT_PATH",
        str(project_path),
    )

    monkeypatch.setattr(
        config,
        "SOURCE_PATH",
        str(source_path),
    )

    def fake_check_free_space(space_info):
        return DiskSpaceInfo(
            free_space=100,
            required_space=50,
            enough_space=True,
        )

    monkeypatch.setattr(
        backup_manager.disk_space,
        "check_free_space",
        fake_check_free_space,
    )

    test_file = source_path / "problem.txt"
    original_error = PermissionError("Access denied")

    copy_error = CopyFileError(
        test_file,
        original_error,
    )

    def fake_copy_source_to_current(source_path, current_path):
        partial_file = Path(current_path) / "partial_file.txt"
        partial_file.write_text("partial backup")
        raise copy_error

    monkeypatch.setattr(
        backup_manager,
        "copy_source_to_current",
        fake_copy_source_to_current,
    )

    with pytest.raises(CopyFileError):
        backup_manager.start_backup()

    assert current_path.exists()
    assert not (current_path / "partial_file.txt").exists()


def test_copy_source_to_current_copies_files(tmp_path):
    source_path = tmp_path / "Source"
    current_path = tmp_path / "Current"

    source_path.mkdir()
    current_path.mkdir()

    source_file = source_path / "test.txt"
    source_file.write_text("test")

    folder_name_1 = "test_folder_1"
    folder_name_2 = "test_folder_2"

    folder_path_1 = source_path / folder_name_1
    folder_path_2 = source_path / folder_name_2

    folder_path_1.mkdir()
    folder_path_2.mkdir()

    file_path_1 = folder_path_1 / "file1.txt"
    file_path_2 = folder_path_2 / "file2.txt"

    file_path_1.write_text("test 1")
    file_path_2.write_text("test 2")

    backup_manager.copy_source_to_current(
        source_path,
        current_path,
    )

    assert (current_path / "test.txt").exists()
    assert (current_path / "test_folder_1" / "file1.txt").exists()
    assert (current_path / "test_folder_2" / "file2.txt").exists()

    assert (current_path / "test.txt").read_text() == "test"
    assert (current_path / "test_folder_1" / "file1.txt").read_text() == "test 1"
    assert (current_path / "test_folder_2" / "file2.txt").read_text() == "test 2"


def test_start_backup_stops_when_not_enough_space(tmp_path, monkeypatch):
    project_path = tmp_path
    source_path = project_path / "Source"
    current_path = project_path / "Current"

    source_path.mkdir()
    current_path.mkdir()

    monkeypatch.setattr(
        config,
        "PROJECT_PATH",
        str(project_path),
    )

    monkeypatch.setattr(
        config,
        "SOURCE_PATH",
        str(source_path),
    )

    def fake_check_free_space(space_info):
        return DiskSpaceInfo(
            free_space=10,
            required_space=15,
            enough_space=False,
        )

    monkeypatch.setattr(
        backup_manager.disk_space,
        "check_free_space",
        fake_check_free_space,
    )

    with patch("backup_manager.copy_source_to_current") as mock_copy:
        backup_manager.start_backup()

    mock_copy.assert_not_called()


def test_start_backup_stops_when_verification_fails(
    tmp_path,
    monkeypatch,
):
    project_path = tmp_path
    source_path = project_path / "Source"
    current_path = project_path / "Current"

    source_path.mkdir()
    current_path.mkdir()

    monkeypatch.setattr(
        config,
        "PROJECT_PATH",
        str(project_path),
    )

    monkeypatch.setattr(
        config,
        "SOURCE_PATH",
        str(source_path),
    )

    def fake_verify_directories(source_path, target_path):
        return VerificationResult(
            success=False,
            result_code="DIRECTORY_SIZE_MISMATCH",
        )

    monkeypatch.setattr(
        backup_manager.file_utils,
        "verify_directories",
        fake_verify_directories,
    )

    backup_manager.start_backup()


def test_start_backup_creates_verified_current(tmp_path, monkeypatch):
    project_path = tmp_path
    source_path = project_path / "Source"
    current_path = project_path / "Current"

    source_path.mkdir()
    current_path.mkdir()

    source_file = source_path / "test.txt"
    source_file.write_text("test")

    monkeypatch.setattr(
        config,
        "PROJECT_PATH",
        str(project_path),
    )

    monkeypatch.setattr(
        config,
        "SOURCE_PATH",
        str(source_path),
    )

    backup_manager.start_backup()

    assert (current_path / "test.txt").exists()
    assert (current_path / "test.txt").read_text() == "test"