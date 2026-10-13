# Backup Project Architecture

## Project Purpose

Backup Project is a backup application designed to create and maintain an up-to-date copy of user data while preserving previous states.

The main architectural goals are:

- user data safety;
- straightforward recovery;
- a clear modular structure;
- independence of backup logic from the user interface.

---

# Project Structure

The user selects only the root project directory.

The internal structure is created and maintained automatically by the application.

```text
BackupProject/
├── Current/
└── History/
```

The directory names `Current` and `History` are part of the project architecture and cannot be changed by the user.

---

# Current

The `Current` directory always contains a **full snapshot** of the `Source` directory as it was at the time of the last successful backup.

After a backup completes successfully, the contents of `Current` fully match the contents of `Source`.

`Current` never contains partially updated data.

---

# History

The `History` directory stores previous states of the `Current` directory.

Before `Current` is updated, its previous state is saved in `History` as a separate snapshot.

The number of retained snapshots is limited by the `MAX_HISTORY` setting.

Before a new snapshot is saved, old snapshots are cleaned up according to the `MAX_HISTORY` setting.

---

## Error Handling During History Cleanup

When deleting old snapshots, the application distinguishes between situations based on why deletion is not possible.

### Snapshot No Longer Exists

If a snapshot selected for deletion no longer exists, the application does not treat this as a critical error.

`cleanup_history()` rechecks the `History` directory, builds an up-to-date list of snapshots, and continues using the directory's current state.

The recheck includes only directories whose names match the snapshot naming format.

### Snapshot Exists but Cannot Be Deleted

If deleting a snapshot raises `PermissionError`, the application does not attempt to change access permissions or retry the operation.

The error is propagated to the top level of the application.

`app.py` stops the current backup run and informs the user about the problem.

The user-facing message is stored in `messages.py`.

The business logic in the backup modules does not contain user-interaction code.

---

## Snapshot Names

Each snapshot created by the application is named using the following format:

```text
%Y-%m-%d_%H-%M-%S
```

For example:

```text
2026-08-13_18-42-17
```

When working with `History`, the application identifies snapshots by checking whether their names match this format.

Only directories whose names match the snapshot format are included when counting `MAX_HISTORY`, sorting snapshots, and deleting them.

Other files and directories located in `History` are not considered snapshots and are not deleted by the application.

If a snapshot selected for deletion no longer exists, the application rechecks `History` and continues using the directory's current state.

---

# Storage Types

Backup Project supports several destination storage types:

- Local Disk
- External USB Drive
- Network Storage (NAS)

Each type may have its own availability checks.

After the checks succeed, the remaining backup logic is the same regardless of the storage type.

---

# Backup Lifecycle

Each backup consists of a sequence of independent stages.

```text
Configuration check
        ↓
Project structure preparation
        ↓
Storage validation
        ↓
Free disk space check
        ↓
Current validation
        ↓
Save Current → History
        ↓
Snapshot verification
        ↓
Clear Current
        ↓
Copy Source → Current
        ↓
Current verification
        ↓
Completion
```

Each stage is responsible only for its own task.

---

# Comparing Source and Current

The comparison of `Source` and `Current` is used to analyze the state of the data.

The comparison does not determine which files will be copied.

Backup Project creates a complete new snapshot of `Source`. Therefore, after the previous state of `Current` has been saved to `History`, the `Current` directory is fully updated with the contents of `Source`.

Comparison results can be used for:

- identifying new files;
- identifying deleted files;
- identifying modified files;
- analyzing matching files;
- calculating data size;
- generating a backup log;
- displaying information to the user.

The comparison mechanism is part of the project architecture and is intended to support the future development of analysis and logging features.

In the main backup workflow of version `1.1`, comparison results are not used to select files for copying.

---

# Module Responsibilities

## app.py

Coordinates application execution.

Controls the order in which stages are performed.

Does not contain specialized backup logic.

---

## backup_manager.py

Implements the backup algorithm.

Coordinates the individual stages of the process.

---

## project_initializer.py

Prepares the project's working structure.

Creates missing directories:

- `BackupProject`
- `Current`
- `History`

---

## storage_validator.py

Checks whether the selected storage type is ready for use.

---

## history_manager.py

Manages the `History` directory.

Is responsible for retaining and deleting old snapshots.

---

## messages.py

Stores all user-facing application messages.

Does not contain backup logic.

Prepares the project for future localization.

---

# Data Flow

The main backup workflow in BackupProject version `1.1` is:

```text
Source
    │
    ▼
Configuration check
    │
    ▼
Project structure preparation
    │
    ▼
Storage validation
    │
    ▼
Calculate required free space
    │
    ▼
Free disk space check
    │
    ▼
Validate Current
    │
    ├── Current is empty
    │       │
    │       ▼
    │   Skip saving to History
    │
    └── Current contains files
            │
            ▼
        Save Current → History
            │
            ▼
        Snapshot verification
            │
            ▼
        Clear Current
            │
            ▼
        Copy Source → Current
            │
            ▼
        Current verification
            │
            ▼
        Completion
```

Each function receives the result of the previous stage and is responsible for only one task.

This reduces coupling between modules and makes the project easier to maintain.

### Free Disk Space Check

The free disk space check is performed before any changes are made to the `Current` and `History` directories.

If there is not enough free space, the backup does not start, and existing backups remain unchanged.

The free disk space check compares:

- the amount of data required to create the new backup;
- the amount of free space on the destination drive.

If there is not enough free space, further actions are determined by the user interface (Console / GUI).

### Current and History

`Current` is the working snapshot from the most recent backup.

After `Current` has been saved successfully to `History`, the `Current` directory is cleared and recreated from `Source`.

If an error occurs while the new `Current` snapshot is being created, the existing backups in `History` remain unchanged.

### Clearing Current

Updating the `Current` directory is a separate stage of the backup process.

Before clearing it, the application must successfully save the current snapshot to `History` and verify that the snapshot is valid.

Clearing `Current` removes only its contents.

The `Current` directory itself is not deleted and remains part of the project structure.

After clearing is complete, the `Current` directory still exists and is ready for a new full snapshot of `Source`.

### Recovery After an Interrupted Copy

When a backup starts, the application checks the state of `Current`.

If `Current` is missing, empty, or corrupted, it is not moved to `History`.

In this case, the application creates a new `Current` directly from `Source`.

## Shared Data Models

Shared project data structures are defined in a separate module, `project_dataclasses.py`.

The module contains dataclasses used by multiple project subsystems.

Currently, these are:

- `SpaceInfo`
- `DiskSpaceInfo`
- `VerificationResult`

This avoids duplicating data structures and reduces coupling between modules.

## General File Operations

In addition to scanning files, the module contains general-purpose directory operations.

Currently, these are:

- `scan_files()`
- `get_directory_size()`

The module also implements the general-purpose function `verify_directories()`.

## Directory Verification

Directory verification is a general-purpose project operation.

It does not depend on the purpose of the directories and can be used to verify:

- `Source` ↔ `Current`;
- `Current` ↔ a `History` snapshot;
- other project directories.

Verification includes:

1. checking that the directory exists;
2. checking that the file structure matches;
3. checking that the total size matches.

The result of verification is a `VerificationResult` object.
