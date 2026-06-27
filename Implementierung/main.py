from core.controller import Controller
from ui.cli          import CLI
#=========================================================================
if __name__ == "__main__":
    
    controller = Controller()
    
    while True:
        print("MONTE-CARLO-SIMULATION\n")
        print("1 - Start CLI")
        print("C - Cancel")
        # evtl. später GUI oder Web
        choice = input("> ").strip().lower()
    
        if choice == "1":
            cli = CLI(controller)
            cli.run()
        elif choice == "c":
            break