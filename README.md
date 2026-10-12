# Backup Project

A modular Python application for backing up files on Windows, with a focus on data safety, error handling, and automated testing.

## Features

- Full file backups from a source directory to a selected storage location
- Current backup and historical snapshots
- Automatic cleanup of old snapshots based on a configurable limit
- Disk space validation before backup operations
- Directory structure and size verification
- Error handling designed to protect existing backups
- Support for local disks, external USB drives, and network storage (NAS)

## Architecture

The application uses a modular structure that separates backup logic, storage validation, file operations, history management, and user-facing messages.

Detailed documentation is available in the `docs/` directory.

## Testing

The stable baseline, **BackupProject 1.1**, has 21 automated tests.

**Latest test result: 21 passed.**

Tests cover file operations, backup workflows, disk space checks, history management, directory verification, and error handling.

## Project Status

The core backup logic is implemented and tested.

The graphical user interface (GUI), Windows Task Scheduler integration, and additional features are planned for future development.

This is a personal learning project developed to practise Python programming, modular application design, error handling, and automated testing.

## Technologies

- Python
- pytest
- Git / GitHub

## Getting Started

1. Install Python.
2. Clone or download this repository.
3. Install the required dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Review `config.py` and configure the source and destination paths for your environment.
5. Run the application:

   ```bash
   python app.py
   ```

6. Run the tests:

   ```bash
   python -m pytest -v
   ```

**Note:** This project is under development. Review the configuration and test the application with non-critical sample files before using it with important data.