"""
Common data classes used by multiple project modules.
"""
from dataclasses  import dataclass

@dataclass
class SpaceInfo:
    source_size: int
    current_size: int
    required_space: int

@dataclass
class DiskSpaceInfo:
    free_space: int
    required_space: int
    enough_space: bool

@dataclass
class VerificationResult:
    success: bool
    result_code: str
    checked_files: int = 0
    checked_size: int = 0