from pathlib import Path

import file_utils
import messages


def test_verify_directories_success(tmp_path):
    source_path = tmp_path / "Source"
    target_path = tmp_path / "Target"

    source_path.mkdir()
    target_path.mkdir()

    source_file = source_path / "test.txt"
    target_file = target_path / "test.txt"

    source_file.write_text("test")
    target_file.write_text("test")

    result = file_utils.verify_directories(
        source_path,
        target_path,
    )

    assert result.success is True
    assert result.result_code == messages.DIRECTORY_VERIFIED


def test_verify_directories_structure_mismatch(tmp_path):
    source_path = tmp_path / "Source"
    target_path = tmp_path / "Target"

    source_path.mkdir()
    target_path.mkdir()

    source_file = source_path / "test.txt"
    source_file.write_text("test")

    result = file_utils.verify_directories(
        source_path,
        target_path,
    )

    assert result.success is False
    assert result.result_code == messages.DIRECTORY_STRUCTURE_MISMATCH


def test_verify_directories_size_mismatch(tmp_path):
    source_path = tmp_path / "Source"
    target_path = tmp_path / "Target"

    source_path.mkdir()
    target_path.mkdir()

    source_file = source_path / "test.txt"
    target_file = target_path / "test.txt"

    source_file.write_text("test")
    target_file.write_text("different")

    result = file_utils.verify_directories(
        source_path,
        target_path,
    )

    assert result.success is False
    assert result.result_code == messages.DIRECTORY_SIZE_MISMATCH