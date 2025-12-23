from utils import clear_cli, print_separation, input_int, enter_continue, input_float, show_error
from transition_rules import transition_data as td
from start_state import start_state_data as sd
from graph import plot_paths, plot_mean_and_std, plot_final_distribution
from montecarlo import MonteCarloSim
from ergodicity import calculate_ergodicity
#=========================================================================
# CLI-KLasse
class CLI:
    def __init__(self, simulation: MonteCarloSim):
        self.sim = simulation

#=========================================================================
# Hauptmenü
    
    def run(self):
        while True:
            clear_cli()
            print_separation()
            print("- MONTE CARLO SIMULATION -\n")
            print("MENU: ")
            print("1 - Change Settings")
            print("2 - Show Settings")
            print("3 - Start Simulation")
            if self.sim.last_result is not None:
                print("4 - Show Result")
            print("C - Close CLI")
            choice = input("> ").strip().lower()

            if choice == "1":
                self._load_data()
                continue

            elif choice == "2":
                self._show_rules(True)
                enter_continue()
                continue

            elif choice == "3":
                if not self.sim.check_if_complete():
                    continue
                self._show_rules(False)             # Informationen ohne Beschreibung aufrufen
                print_separation()
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

    # Daten für die Sim1ulation abfragen und festlegen
    def _load_data(self):
        self.sim.last_result = None     # Ergebnis zurücksetzen
        clear_cli()
        print_separation()
        print("- MONTE CARLO SIMULATION -\n")
        print("DATA: ")

        # Daten abfragen
        n_steps = input_int(10, 10000, 1000, "Input Number of steps", True)
        n_paths = input_int(1, 10000, 100, "Input Number of paths", True)
        step_size = input_float(0.1, 100, 1, "Step Size", True)

        # Daten festlegen
        self.sim.n_steps = n_steps
        self.sim.n_paths = n_paths
        self.sim.step_size = step_size

    # Regeln der Simulation anzeigen
    def _show_rules(self, info: bool = True):
        clear_cli()
        print_separation()
        print("- MONTE CARLO SIMULATION -\n")
        print("SETTINGS: \n")

        if not self.sim.check_if_complete():
            return
        
        print(f"Number of steps: {self.sim.n_steps}")
        print(f"Number of Paths: {self.sim.n_paths}")
        print(f"Step Size: {self.sim.step_size}")

        # Startwert
        key = self.sim.start_state.__name__
        print(f"\nFunction for Startvalue: {sd[key]["Name"]}")
        if info:
             print(f"Description: {sd[key]["Desc"]}")

        # Transitions-Regel
        key = self.sim.transitional_rule.__name__
        print(f"\nFunction for transitions: {td[key]["Name"]}")
        if info:
             print(f"Description: {td[key]["Desc"]}\n")

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
            print("5 - Calculate Ergodicity")
            print("C - Close")
            choice = input("> ").strip().lower()

            if choice == "1":
                print(paths)
                enter_continue()
                
            elif choice == "2":
                plot_paths(paths, self.sim.seed, self.sim.n_paths)
                continue

            elif choice == "3":
                plot_mean_and_std(paths, self.sim.seed, self.sim.n_paths)
                continue

            elif choice == "4":
                plot_final_distribution(paths, self.sim.seed, self.sim.n_paths)
                continue

            elif choice == "5":
                calculate_ergodicity(paths)
                continue

            elif choice == "c":
                break

    # Simulation starten
    def _start_sim(self):
        enter_continue("Press enter to start the Simulation...")
        print("\nSample-paths are being calculated...")
        self.sim.run()                       # Simulation aufrufen
        self.result_menu(self.sim.last_result)        # Direkt Menü