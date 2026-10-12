from datetime import datetime
from pathlib import Path

import config
import constants
import file_utils
import shutil


def save_current_to_history(current_path, history_path):
    current_path = Path(current_path)
    history_path = Path(history_path)

    snapshot_name = datetime.now().strftime(constants.SNAPSHOT_NAME_FORMAT)
    snapshot_path = history_path / snapshot_name

    shutil.copytree(current_path, snapshot_path)

    return snapshot_path

# def cleanup_history(history_path):
#     history_path = Path(history_path)
#     snapshots = get_snapshots(history_path)
#
#     while len(snapshots) >= config.MAX_HISTORY:
#         oldest_snapshot = snapshots[0]
#
#         if oldest_snapshot.exists():
#             try:
#                 shutil.rmtree(oldest_snapshot)
#                 snapshots.pop(0)
#             except FileNotFoundError:
#                 snapshots = get_snapshots(history_path)
#         else:
#             snapshots = get_snapshots(history_path)
#
#
#     return

def cleanup_history(history_path):
    history_path = Path(history_path)
    snapshots = get_snapshots(history_path)

    while len(snapshots) >= config.MAX_HISTORY:
        oldest_snapshot = snapshots[0]

        try:
            shutil.rmtree(oldest_snapshot)
            snapshots.pop(0)
        except FileNotFoundError:
            snapshots = get_snapshots(history_path)
        # except PermissionError:
        #     raise

    return

def prepare_history(current_path, history_path):
    cleanup_history(history_path)

    snapshot_path = save_current_to_history(
        current_path,
        history_path,
    )

    verification_result = file_utils.verify_directories(
        current_path,
        snapshot_path,
    )

    return verification_result

def get_snapshots(history_path):
    history_path = Path(history_path)
    snapshots = []

    for item in history_path.iterdir():
        if item.is_dir():
            try:
                datetime.strptime(
                    item.name,
                    constants.SNAPSHOT_NAME_FORMAT
                )
                snapshots.append(item)
            except ValueError:
                continue

    snapshots.sort()
    return snapshots