from pathlib import Path
from unittest.mock import patch
import messages
import app

from exceptions import CopyFileError


def test_main_handles_permission_error(capsys):
    test_file = Path(r"D:\Test\Source\problem.txt")
    original_error = PermissionError("Access denied")

    with patch("app.backup_manager.start_backup") as mock_start_backup:
        mock_start_backup.side_effect = CopyFileError(
            test_file,
            original_error,
        )

        app.main()

    captured = capsys.readouterr()

    assert messages.COPY_FILE_ERROR.format(test_file) in captured.out


