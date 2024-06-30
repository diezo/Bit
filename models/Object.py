from dataclasses import dataclass


@dataclass
class Object():
    """
    Stores object information.
    """

    file_path: str
    content_hash: str
    object_type: str

    """
    Object Types:
        - "b" - Blob
        - "t" - Tree
        - "c" - Commit
    """
