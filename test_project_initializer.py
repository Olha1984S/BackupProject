from pathlib import Path

import project_initializer
import config

def test_initialize_project_creates_project_structure(tmp_path, monkeypatch):
    monkeypatch.setattr(
        config,
        "PROJECT_PATH",
        str(tmp_path / "BackupProject"),
    )

    project_initializer.initialize_project()

    project_path = Path(config.PROJECT_PATH)
    current_path = project_path / "Current"
    history_path = project_path / "History"

    assert project_path.exists()
    assert current_path.exists()
    assert history_path.exists()