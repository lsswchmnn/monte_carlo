from utils import clear_cli, print_separation, input_int, enter_continue, input_float, show_error
from graph import plot_paths, plot_mean_and_std, plot_final_distribution
from montecarlo import MonteCarloSim
#=========================================================================
# CLI-KLasse
class CLI:
    def __init__(self, simulation:MonteCarloSim):
        self.sim = simulation

#=========================================================================
# Hauptmenü
    
    def run(self):
        while True:
            clear_cli()
            print_separation()
            print("- MONTE CARLO SIMULATION -\n")
            print("MENU: ")
            print("1 - Load Data")
            print("2 - Show Sim Settings")
            print("3 - Start Simulation")
            if self.sim.last_result is not None:
                print("4 - Result Menu")
            print("C - Close CLI")
            choice = input("> ").strip().lower()

            if choice == "1":
                self._load_data()
                continue

            elif choice == "2":
                self._show_rules()
                enter_continue()
                continue

            elif choice == "3":
                if not self.sim.check_if_complete():
                    continue
                self._start_sim()

            elif choice == "4" and self.sim.last_result is not None:
                self.result_menu(self.sim.last_result)

            elif choice == "c":
                print("Close simulation...")
                clear_cli()
                break

            else:
                continue

#=========================================================================
# CLI-Methoden

    # Daten für die Simulation abfragen und festlegen
    def _load_data(self):
        self.sim.last_result = None     # Ergebnis zurücksetzen
        clear_cli()
        print_separation()
        print("- MONTE CARLO SIMULATION -\n")
        print("DATA: ")

        # Daten abfragen
        n_steps = input_int(10, 10000, 1000, "Input Number of steps", True)
        n_paths = input_int(10, 10000, 1000, "Input Number of paths", True)
        step_size = input_float(0.1, 100, 1, "Step Size", True)

        # Daten festlegen
        self.sim.n_steps = n_steps
        self.sim.n_paths = n_paths
        self.sim.step_size = step_size

    # Regeln der Simulation anzeigen
    def _show_rules(self):
        clear_cli()
        print_separation()
        print("- MONTE CARLO SIMULATION -\n")
        print("SETTINGS: ")

        if not self.sim.check_if_complete():
            return
        
        print(f"Number of steps: {self.sim.n_steps}")
        print(f"Number of Paths: {self.sim.n_paths}")

        # Später durch kurze Beschreibung tauschen
        print(f"Function for Startvalue:  {self.sim.start_state}")
        print(f"Function for transitions: {self.sim.transitional_rule}")

    # Ergebnis anziegen
    def result_menu(self, paths:list):
        while True:
            clear_cli()
            print_separation()
            print("- MONTE CARLO SIMULATION -\n")
            print("RESULT: ")
            print("1 - Print Data")
            print("2 - Show Sample Paths")
            print("3 - Show Mean Path and Volatility")
            print("4 - Show Distribution of Final Cases")
            print("C - Close")
            choice = input("> ").strip().lower()

            if choice == "1":
                print(paths)
                
            elif choice == "2":
                plot_paths(paths)


            elif choice == "3":
                plot_mean_and_std(paths)

            elif choice == "4":
                plot_final_distribution(paths)        

            elif choice == "c":
                break

    # Simulation starten
    def _start_sim(self):
        self._show_rules()
        enter_continue("Press enter to start the Simulation...")
        self.sim.run()                       # Simulation aufrufen
        self.result_menu(self.sim.last_result)        # Direkt Menü