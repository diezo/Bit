from porcelain import stage, commit
import sys

# Parse Command
try:
    command: str = sys.argv[1]
    args: list[str] = sys.argv[2:]

    # Porcelain Commands
    if command == "add": stage(args)  # Stage Items
    elif command == "commit": commit(args)  # Commit Staged Items

    # Command Not Recognised
    else: print(f"What do you mean by \"{command}\" :(")
    

# No Command Given
except IndexError: print("Welcome to Bit! Please include a command to proceed. 😊")
