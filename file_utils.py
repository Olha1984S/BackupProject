from pathlib import Path
from project_dataclasses import VerificationResult

import messages

def scan_files(directory_path):
    directory_path = Path(directory_path)

    files = set()

    for item in directory_path.rglob("*"):
        if item.is_file():
            relative_path = item.relative_to(directory_path)
            files.add(relative_path)

    return files

def get_directory_size(directory_path):
    directory_path = Path(directory_path)

    total_size = 0

    for item in directory_path.rglob("*"):
        if item.is_file():
            total_size += item.stat().st_size

    return total_size

def verify_directories(source_path, target_path):
    source_path = Path(source_path)
    target_path = Path(target_path)

    if not source_path.exists():
        return VerificationResult(
            success=False,
            result_code=messages.DIRECTORY_NOT_FOUND,
        )

    if not target_path.exists():
        return VerificationResult(
            success=False,
            result_code=messages.DIRECTORY_NOT_FOUND,
        )

    source_files = scan_files(source_path)
    target_files = scan_files(target_path)

    if source_files != target_files:
        return VerificationResult(
            success=False,
            result_code=messages.DIRECTORY_STRUCTURE_MISMATCH,
            checked_files=len(target_files),
            checked_size=0,
        )

    source_size = get_directory_size(source_path)
    target_size = get_directory_size(target_path)

    if source_size != target_size:
        return VerificationResult(
            success=False,
            result_code=messages.DIRECTORY_SIZE_MISMATCH,
            checked_files=len(target_files),
            checked_size=target_size,
        )

    return VerificationResult(
        success=True,
        result_code=messages.DIRECTORY_VERIFIED,
        checked_files=len(target_files),
        checked_size=target_size,
    )

def has_files(directory_path):
    directory_path = Path(directory_path)

    for item in directory_path.rglob("*"):
        if item.is_file():
            return True

    return False

