import subprocess
import sys
from   core.controller  import Controller
from   ui.cli.cli       import CLI
#=========================================================================

if __name__ == "__main__":

    while True:
        print("1 - Start CLI")
        print("2 - Start Streamlit")
        print("C - Cancel")
        choice = input("> ").strip().lower()

        if choice == "1":
            controller = Controller()
            cli = CLI(controller)
            cli.run()
            break

        elif choice == "2":
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "streamlit",
                    "run",
                    "ui/web/app.py"
                ]
            )
            break

        elif choice == "c":
            break