from unittest.mock import patch
from project_dataclasses import SpaceInfo

import disk_space
import config
import disk_space


def test_calculate_required_space(tmp_path):
    source_path = tmp_path / "Source"
    current_path = tmp_path / "Current"

    source_path.mkdir()
    current_path.mkdir()

    file_1 = source_path / "file1.txt"
    file_2 = source_path / "file2.txt"
    file_3 = current_path / "file3.txt"

    file_1.write_text("12345")
    file_2.write_text("1234567")
    file_3.write_text("123")

    space_info = disk_space.calculate_required_space(
        source_path,
        current_path,
    )

    assert space_info.source_size == 12
    assert space_info.current_size == 3
    assert space_info.required_space == 15


def test_check_free_space():
    space_info = SpaceInfo(
        source_size=12,
        current_size=3,
        required_space=15,
    )

    with patch("disk_space.shutil.disk_usage") as mock_disk_usage:
        mock_disk_usage.return_value = (100, 50, 20)

        result = disk_space.check_free_space(space_info)

def test_check_free_space_not_enough():
    space_info = SpaceInfo(
        source_size=12,
        current_size=3,
        required_space=15,
    )

    with patch("disk_space.shutil.disk_usage") as mock_disk_usage:
        mock_disk_usage.return_value = (100, 90, 10)

        result = disk_space.check_free_space(space_info)

        assert result.enough_space is False