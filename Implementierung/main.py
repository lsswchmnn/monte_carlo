from core.controller import Controller
from ui.cli          import CLI
#=========================================================================
if __name__ == "__main__":
    
    controller = Controller()
    
    while True:
        # Sobald GUI oder Web implementiert, hier Startmenü

        # print("1 - Start CLI")
        # print("C - Cancel")
        # choice = input("> ").strip().lower()
    
        choice = "1"

        if choice == "1":
            cli = CLI(controller)
            cli.run()
            break
        elif choice == "c":
            break