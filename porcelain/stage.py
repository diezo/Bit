import zlib
from core import Stager
import os


def stage(items: list[str]) -> None:
    """
    Command to index specified items.
    """
    
    # Validate Items
    if len(items) < 1: return print("Give me something to stage! 😕")

    # Stage Items
    stager: Stager = Stager(items)
    raw_index: str = stager.index()

    # Write Index
    with open(os.path.join(os.getcwd(), ".bit", "index"), "wb") as file:
        file.write(zlib.compress(raw_index.encode("utf-8"), level=6))
