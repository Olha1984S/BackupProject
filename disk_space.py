"""
Working with disk space.
"""
from pathlib import Path
from project_dataclasses import DiskSpaceInfo
from project_dataclasses import SpaceInfo

import config
import file_utils
import shutil


def calculate_required_space(source_path, current_path):
    source_size = file_utils.get_directory_size(source_path)
    current_size = file_utils.get_directory_size(current_path)
    required_space = source_size + current_size

    space_info = SpaceInfo(
        source_size=source_size,
        current_size=current_size,
        required_space=required_space,
    )

    return space_info

def check_free_space(space_info):
    _, _, free_space = shutil.disk_usage(config.PROJECT_PATH)

    enough_space = free_space >= space_info.required_space

    disk_space_info = DiskSpaceInfo(
        free_space=free_space,
        required_space=space_info.required_space,
        enough_space=enough_space,
    )

    return disk_space_info

