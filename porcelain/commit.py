import zlib
import os
import string

message_allowed_chars: list[str] = string.digits + string.ascii_letters + " -_"


def commit(args: list[str]) -> None:
    """
    Command to commit staged items.
    """

    try: message: str = args[0]
    except IndexError: return print("Where's the commit message?? 😱")
    
    # Validate Message
    if False in [x in message_allowed_chars for x in message]:
        return print("Message can only include letters, digits, spaces, \"-\" & \"_\" 😏")
    
    # Read Index
    with open(os.path.join(os.getcwd(), ".bit", "index"), "rb") as file:
        decompressed_index: str = zlib.decompress(file.read()).decode("utf-8")
        print(decompressed_index)
