from pathlib import Path

import config


def initialize_project():
    ensure_project_folder()
    ensure_current_folder()
    ensure_history_folder()


def ensure_project_folder():
    project_path = Path(config.PROJECT_PATH)

    if project_path.exists():
        return

    project_path.mkdir(parents=True, exist_ok=True)

def ensure_current_folder():
    project_path = Path(config.PROJECT_PATH)
    current_path = project_path / "Current"

    if current_path.exists():
        return

    current_path.mkdir(parents=True, exist_ok=True)

def ensure_history_folder():
    project_path = Path(config.PROJECT_PATH)
    history_path = project_path / "History"

    if history_path.exists():
        return

    history_path.mkdir(parents=True, exist_ok=True)