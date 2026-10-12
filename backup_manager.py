"""
Managing the backup process.
"""

from pathlib import Path
from exceptions import CopyFileError

import config
import disk_space
import file_utils
import history_manager
import shutil

def start_backup():
    project_path = Path(config.PROJECT_PATH)

    current_path = project_path / "Current"

    # TODO (v1.x):
    # Scan and comparison results will be used for backup log
    # and backup statistics.

    # source_files = file_utils.scan_files(config.SOURCE_PATH)
    # current_files = file_utils.scan_files(current_path)
    #
    # new_files, removed_files, common_files = compare_with_current(
    #     source_files,
    #     current_files,
    # )

    space_info = disk_space.calculate_required_space(
        config.SOURCE_PATH,
        current_path,
    )

    disk_space_info = disk_space.check_free_space(space_info)

    if not disk_space_info.enough_space:
        handle_low_disk_space(disk_space_info)
        return

    history_path = project_path / "History"

    if file_utils.has_files(current_path):
        history_verification = history_manager.prepare_history(
            current_path,
            history_path,
        )

        if not history_verification.success:
            return

    clear_current(current_path)

    try:
        copy_source_to_current(
            config.SOURCE_PATH,
            current_path,
        )
    except CopyFileError:
        clear_current(current_path)
        raise

    current_verification = file_utils.verify_directories(
        config.SOURCE_PATH,
        current_path,
    )

    if not current_verification.success:
        return

def handle_low_disk_space(disk_space_info):
    print()
    print("Not enough free disk space.")
    print(f"Required: {disk_space_info.required_space} bytes")
    print(f"Available: {disk_space_info.free_space} bytes")

    return

def compare_with_current(source_files, current_files):

    new_files = source_files - current_files
    removed_files = current_files - source_files
    common_files = source_files & current_files

    return new_files, removed_files, common_files

def clear_current(current_path):
    current_path = Path(current_path)
    if not current_path.exists():
        return

    for item in current_path.iterdir():

        if item.is_file():
            item.unlink()

        elif item.is_dir():
            shutil.rmtree(item)

def copy_source_to_current(source_path, current_path):
    source_path = Path(source_path)
    current_path = Path(current_path)

    for item in source_path.rglob("*"):
        if item.is_file():
            relative_path = item.relative_to(source_path)
            destination_path = current_path / relative_path

            destination_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            try:
                shutil.copy2(item, destination_path)
            except PermissionError as error:
                raise CopyFileError(item, error)




