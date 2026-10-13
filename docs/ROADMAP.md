# Development Roadmap

## Stage 1

- [ ] Project structure
- [ ] Settings
- [ ] NAS validation
- [ ] Logging

---

## Stage 2

- [x] File comparison
- [x] Current
- [x] History

---

## Stage 3

- [ ] Open files
- [x] History cleanup

---

## Stage 4

- [ ] General error-handling system
- [ ] Recovery after errors
- [ ] Backup log

---

## Stage 5

- [ ] GUI
- [ ] Windows Task Scheduler

---

## Stage 6

- [ ] Testing
- [ ] Transfer to another computer

## Testing Baseline for BackupProject_1.1

| Module | Tests | Result |
| --- | ---: | --- |
| `test_app.py` | 1 | Passed |
| `test_backup_manager.py` | 7 | Passed |
| `test_disk_space.py` | 3 | Passed |
| `test_file_utils.py` | 3 | Passed |
| `test_history_manager.py` | 6 | Passed |
| `test_project_initializer.py` | 1 | Passed |
| **Total** | **21** | **21 passed** |

## GUI Stage

- Insufficient free disk space dialog.
- Pause the backup process.
- Timer for waiting for user actions.
- Check free disk space again.
- Resume the backup after space has been freed.

## Planned Features

- Filter files by extension.
- Exclude temporary files.
- Exclude hidden files.
- Check file checksums.
- Display copy progress.
- Display copy speed.
- Display remaining time.
- Allow copying to be cancelled.
- Detailed execution statistics (`CopyResult`).
