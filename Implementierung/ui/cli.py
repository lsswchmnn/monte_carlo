from ui.utils.display   import clear_cli, print_heading, print_separation, print_thin_separation, enter_continue
from ui.utils.errors    import enter_continue, show_error
from ui.utils.input     import input_float, input_int
from ui.utils.progress  import printProgressBar, finishProgressBar, Spinner
from ui.help            import help_three_types, help_full, help_settings
from core.controller    import Controller
#=========================================================================
class CLI:

    def __init__(self, Controller: Controller):

        self.sim = Controller

#-------------------------------------------------------------------------
# Hauptmenü

    def run(self):
        
        while True:
            print_heading("MONTE CARLO SIMULATION")
            print("...")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()
        
            if choice == "":
                pass

            elif choice == "c":
                clear_cli()
                enter_continue("Press Enter to Leave the Simulation", seperation=False)
                clear_cli()
                print("Goodbye! :) \n")
                break

#-------------------------------------------------------------------------
# Menüs

# ...