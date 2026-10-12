from pathlib import Path
from exceptions import CopyFileError

import backup_manager
import config
import constants
import messages
import project_initializer
import storage_validator

def check_configuration():
    errors = []

    if config.SOURCE_PATH == "":
        errors.append(messages.SOURCE_PATH_EMPTY)
    elif not Path(config.SOURCE_PATH).exists():
        errors.append(messages.SOURCE_PATH_NOT_FOUND)

    if config.PROJECT_PATH == "":
        errors.append(messages.PROJECT_PATH_EMPTY)

    return errors

def main():
    print("========================================")
    print(f"Backup Project v.{constants.VERSION} started.")
    print("========================================")
    # print(f"Language: {config.LANGUAGE}")
    # print(f"Maximum history: {config.MAX_HISTORY}")

    errors = check_configuration()

    if errors:
        print()
        print(messages.CONFIGURATION_ERRORS)

        for error in errors:
            print(f"- {error}")

        return

    print(messages.CONFIGURATION_VALID)

    project_initializer.initialize_project()

    errors = storage_validator.check_storage()

    if errors:
        print()

        for error in errors:
            print(f"- {error}")

        return

    try:
        backup_manager.start_backup()
    except CopyFileError as error:
        print(messages.COPY_FILE_ERROR.format(error.file_path))
        return

if __name__ == "__main__":
    main()

