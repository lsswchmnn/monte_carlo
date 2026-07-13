import sys
import os
#=========================================================================

# Trennlinien im Terminal für saubere CLI-Abschnitte
def print_separation(length: int=50, linebreak: bool=True):
    if linebreak:
        print(f"\n{length*'='}")
    else:
        print(f"{length*'='}")

# Dünne Trennlinie
def print_thin_separation(length: int=50, linebreak: bool=True):
    if linebreak:
        print(f"\n{length*'-'}")
    else:
        print(f"{length*'-'}")

# Überschrift
def print_heading(title: str="HEADING", length: int=50, clear: bool=True, linebreak: bool=True):
    if clear:
        clear_cli()
    print_separation(length, linebreak=False)
    print(title)
    print_separation(length, linebreak=False)
    if linebreak:
        print()

# Mit Enter fortfahren
def enter_continue(msg: str="Press Enter to continue...", seperation: bool=True, linebreak: bool=True):
    if seperation:
        print_thin_separation()
    if linebreak:
        input(f"\n{msg}")
    else:
        input(f"{msg}")

# Leert das CLI komplett
def clear_cli():
    os.system('cls' if os.name == 'nt' else 'clear')
    sys.stdout.write("\r\033[2K")
    sys.stdout.flush()
    sys.stdout.write("\n")
    sys.stdout.flush()