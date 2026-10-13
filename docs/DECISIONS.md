# DECISIONS

This document records the architectural decisions made during the development of Backup Project.

Each decision is considered part of the project architecture and must not be changed without deliberate review.

---

## 2026-08-07

# Decision No. 1

## Data Safety Has Absolute Priority

### Decision

If the application cannot guarantee that a backup will be completed correctly, it must stop without modifying existing backups.

### Reason

Losing one new backup is significantly less dangerous than damaging data that already exists.

### Consequences

- Backup is stopped whenever a critical error occurs.
- Existing backups remain unchanged.

---

# Decision No. 2

## Design First, Code Second

### Decision

Before implementing each new feature, its behavior is designed first, the documentation is updated next, and only then is the code written.

### Reason

This approach makes it possible to make architectural decisions before implementation and reduces the amount of rework later.

### Consequences

Before each new function is written, the following are discussed:

- purpose;
- input data;
- output data;
- operating scenarios;
- possible errors;
- the function's place in the overall architecture.

---

# Decision No. 3

## Separation of Logic and User Interface

### Decision

All business logic must be completely separated from the user interface.

### Reason

This makes it possible to:

- run the application automatically;
- use different interfaces;
- test the logic independently of the interface;
- change the interface without changing the backup algorithms.

### Consequences

The backup modules do not contain code for interacting with the user.

---

# Decision No. 4

## Support for Multiple Storage Types

### Decision

Backup Project supports multiple destination storage types.

Each type may have its own availability checks.

Once these checks succeed, the subsequent backup algorithm remains the same.

### Reason

The backup logic must not depend on a specific storage type.

### Consequences

Adding a new storage type does not require changes to the backup algorithm.

---

# Decision No. 5

## A Single Access Point for Settings

### Decision

All user settings are accessed only through the `config.py` module.

### Reason

In the future, the way settings are stored may change without requiring changes to the rest of the application.

### Consequences

At the current stage, settings are defined directly in `config.py`.

Later, they may be moved to an external configuration file.

---

# Decision No. 6

## User Messages Are Separate from Logic

### Decision

All text messages shown to the user are stored in the `messages.py` module.

### Reason

The application logic should not contain user-facing text strings.

### Consequences

- Localization is easier.
- Messages can be changed independently of the application algorithms.

---

# Decision No. 7

## One Module, One Responsibility

### Decision

Each module is responsible for one major application subsystem.

### Reason

This reduces coupling between parts of the project and makes maintenance easier.

### Consequences

For example:

- `app.py` — application coordination;
- `backup_manager.py` — backup operations;
- `storage_validator.py` — storage validation;
- `project_initializer.py` — project structure preparation;
- `history_manager.py` — History management.

---

# Decision No. 8

## Configuration Validation and Storage Validation Are Separate Stages

### Decision

User settings are validated separately from the availability of the selected storage.

### Reason

Configuration rarely changes.

Storage availability may change before each application run.

### Consequences

Each validation step is responsible only for its own task.

---

# Decision No. 9

## The Project Structure Is Created Automatically

### Decision

The user selects only the location of the project root directory.

The internal directories are created automatically by the application.

### Consequences

When the application starts, it creates any missing directories:

- `BackupProject`
- `Current`
- `History`

If a directory already exists, it is not modified.

---

# Decision No. 10

## Free Space Is Checked After Changes Are Analyzed

### Decision

The required free space is estimated after comparing `Source` and `Current`.

### Reason

Before analyzing the changes, it is not possible to determine how much data will need to be written.

### Consequences

The check is based on the actual volume of the planned operations.

---

# Decision No. 11

## Current Is Always a Full Snapshot of Source

### Decision

The `Current` directory always contains a full copy of the `Source` directory as it was at the time of the last successful backup.

Before it is updated, the entire contents of `Current` are saved to `History`.

After that, `Current` is fully updated with the contents of `Source`.

### Reason

A full snapshot makes the backup structure simple, clear, and predictable.

After a successful backup, the user always knows that `Current` fully matches `Source`.

### Consequences

- `History` stores previous full states.
- `Current` does not contain partially updated data.
- Restoring the latest backup does not require additional logic.

---

# Decision No. 12

## File Comparison Is for Analysis, Not for Deciding What to Copy

### Decision

Comparing `Source` and `Current` is used to analyze changes, create logs, and calculate the volume of operations.

The comparison results do not determine which files will be copied.

### Reason

Backup Project creates a new full snapshot of `Source`, regardless of how many changes have occurred.

### Consequences

The comparison makes it possible to:

- identify new files;
- identify deleted files;
- identify matching files;
- compare the properties of matching files;
- generate a detailed backup log.

However, `Current` is fully updated only after its previous state has been saved to `History`.

---

# Decision No. 13

## The Free Space Check Does Not Control the Backup Process

### Decision

The free space check function is responsible only for determining whether enough free space is available.

It does not interact with the user, pause application execution, or decide how the backup process should proceed.

### Reason

The free space check is part of the business logic.

User interaction depends on the interface being used (console, GUI, etc.) and must be kept separate from the backup logic.

### Consequences

- The backup algorithm does not depend on the interface type.
- In the console version, the application can exit after displaying an error message.
- In a GUI, it is possible to implement waiting for user input, checking free space again, and continuing the backup without changing the business logic.

---

# Decision No. 14

## Current Is Moved to History Only If It Contains a Valid Working Snapshot

### Reason

After `Current` has been saved successfully to `History`, the `Current` directory is cleared before a new snapshot is created.

If copying `Source` → `Current` fails, `Current` may be empty or incomplete.

Moving such a directory to `History` is not allowed.

### Consequences

- Backups in `History` contain only completed snapshots.
- After a failed copy, the next run does not create an empty snapshot.
- The application automatically creates a new `Current` from `Source`.

---

# Decision No. 15

## Clearing Current Is a Separate Backup Stage

### Decision

Before creating a new snapshot of `Source`, the `Current` directory is cleared as a separate stage of the backup process.

Clearing removes only the contents of the directory.

The `Current` directory itself is not deleted.

### Reason

Keeping the directory simplifies the project architecture, eliminates the need to recreate the working structure, and reduces the number of file-system operations.

Separating clearing from the subsequent copy makes it possible to control each backup stage independently.

### Consequences

- `Current` is cleared only after a snapshot has been successfully created and verified in `History`.
- The `Current` directory always exists.
- The clearing function is responsible only for preparing the directory for copying.
- Creating the new snapshot is a separate stage.

---

# Decision No. 16

## Shared Dataclasses Are Stored in a Separate Module

### Decision

All data structures used by multiple project modules are defined in `project_dataclasses.py`.

### Reason

Dataclasses do not belong to the business logic of individual subsystems; they are shared project data models.

### Consequences

- Module coupling is reduced.
- Duplicate dataclasses are avoided.
- New data structures (for example, `CopyResult`) are added to one module.

---

# Decision No. 17

## Directory Verification Is a General-Purpose Operation

### Decision

Directory verification is implemented by one general-purpose function, `verify_directories()`.

The function does not depend on the purpose of the directories and can be used by different project subsystems.

### Reason

Directory structure is verified using the same algorithm whether `Source` and `Current` or `Current` and `History` are being compared.

### Consequences

- Code duplication is eliminated.
- Directory verification has a single implementation.
- `history_manager.py` and `backup_manager.py` use the same verification function.

---

# Decision No. 18

## The First Run Does Not Create an Empty History Snapshot

### Decision

Before saving `Current` to `History`, the application checks whether `Current` contains at least one file.

### Reason

The first application run must not create an empty snapshot.

### Consequences

- The first run does not create an entry in `History`.
- `History` contains only actual backups.

---

# Decision No. 19

## The Snapshot Count Is Limited Before a New Snapshot Is Created

### Decision

Before creating a new snapshot, the application deletes the oldest snapshots until the number of snapshots is less than `MAX_HISTORY`.

### Reason

After the new snapshot is created, the number of backups must not exceed `MAX_HISTORY`.

The application must also automatically correct the situation if `History` already contains more snapshots than the setting allows.

### Consequences

- After the backup finishes, the number of snapshots never exceeds `MAX_HISTORY`.
- `cleanup_history()` automatically restores `History` to a valid state.

---

# Decision No. 20

## A Snapshot Is Identified by Its Name Format

### Decision

A snapshot in `History` is identified by a name matching this format:

```text
%Y-%m-%d_%H-%M-%S
```

Only directories with names in this format are considered snapshots and included in:

- counting `MAX_HISTORY`;
- sorting snapshots;
- selecting the oldest snapshot for deletion.

Files and directories with other names are not considered snapshots, are not included in History management, and are not deleted by the application.

If a snapshot selected for deletion is already missing when deletion is attempted, the application rechecks `History` and continues using the directory's current state.

### Reason

The user or another application may change the contents of `History` while Backup Project is running.

The application must work only with objects it can unambiguously identify as its own snapshots. It must not delete objects unknown to the user.

The snapshot name format includes the creation date and time to the nearest second and is used by the application to identify snapshots.

### Consequences

- A renamed snapshot is no longer recognized by the application as a snapshot.
- User files and directories in `History` do not affect `MAX_HISTORY`.
- Unknown objects in `History` are not deleted by the application.
- If an expected snapshot is already missing, rechecking `History` allows the application to continue without user intervention, provided the number of recognized snapshots is within the allowed limit.

---

# Decision No. 21

## Failure to Delete a Snapshot Is Handled According to the Cause

### Decision

When deleting an old snapshot, the application distinguishes between a snapshot that is missing and one that cannot be deleted.

If the snapshot is already missing, `cleanup_history()` rechecks `History` and continues using the directory's current state.

If the snapshot exists but deletion raises `PermissionError`, the error is not suppressed in `history_manager.py`; it is propagated to the top level of the application.

`app.py` stops the current backup run and informs the user that access permissions are insufficient.

The application does not attempt to change permissions itself or continue the backup after this error.

### Reason

These situations require different behavior.

A missing snapshot is an external change to the state of `History` that can be handled safely by rechecking the directory.

Insufficient permissions cannot be safely resolved by the application itself. Continuing the backup in this state could result in incorrect management of existing backups.

### Consequences

- `FileNotFoundError` during snapshot deletion is handled in `history_manager.py`.
- `PermissionError` is propagated to `app.py`.
- On `PermissionError`, the current backup is stopped.
- Existing backups are not modified after a critical error occurs.
- The user receives a clear error message.
- The backup modules do not contain user-interface code.

---

# Decision No. 22

## BackupProject_1.1 Is the Stable Baseline Version

### Decision

BackupProject_1.1 is designated as the stable baseline version before development of BackupProject_1.2 begins.

### Status

- 21 automated tests;
- 21 tests passed;
- 0 pytest warnings.

### Reason

Before further development, the project needs a verified working baseline against which subsequent changes can be compared.

### Consequences

Changes introduced from version 1.2 onward must not alter the behavior established in version 1.1 unless the relevant architectural decision is deliberately reviewed.

---

# Decision No. 23

## Core Backup Logic Must Have Automated Test Coverage

### Decision

Before moving to the next project version, the main functions and critical backup scenarios must be covered by automated tests.

Testing must verify not only successful scenarios but also critical errors that could leave backup data in an invalid state.

### Reason

Backup Project works with user data, so correct behavior must be demonstrated through repeatable automated tests as well as manual checks.

Particular attention is paid to scenarios in which an error could result in a partial or invalid backup.

### Consequences

The full automated test suite is run before moving to the next project version.

For BackupProject_1.1, the baseline includes:

- 21 automated tests;
- 21 tests passed;
- 0 pytest warnings.

The tests cover:

- project initialization;
- file copying;
- copy error handling;
- clearing a partial `Current`;
- free disk space checks;
- stopping the backup when there is insufficient space;
- snapshot creation and management;
- `History` cleanup;
- handling a missing snapshot;
- handling `PermissionError`;
- directory structure verification;
- data size verification;
- the main `start_backup()` scenario.
