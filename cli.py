from utils import clear_cli, print_separation, input_int, enter_continue, input_float, show_error, printProgressBar
from start_state import start_state_data as sd
from graph import plot_paths, plot_mean_and_std, plot_final_distribution
from montecarlo import MonteCarloSim
from ergodicity import calculate_ergodicity
import math

# Dict mit Beschreibungen der Übergangsfunktionen
from transition_rules import transition_data_marcov as tdm
from transition_rules import transition_data_variational as tdv
from transition_rules import transition_data_adaptive as tda
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
            print("MAINMENU: ")
            print("1 - Change Settings")
            print("2 - Show Settings")
            print("3 - Start Simulation")
            print(f"4 - Change Process Type (Current: {self.sim.process_type})")
            if self.sim.last_result is not None:
                print("5 - Show Result")
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
                self._start_sim()

            elif choice == "4":
                self._change_process_type()
                continue

            elif choice == "5" and self.sim.last_result is not None:
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
        n_paths = input_int(5, 10000, 100, "Input Number of paths", True)
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
        print(f"Datapoints to calculate: {int(self.sim.n_paths * self.sim.n_steps)}")
        print(f"Step Size: {self.sim.step_size}")
        print(f"Random Seed: {self.sim.seed}")
        print(f"Process Type: {self.sim.process_type}")

        # Startwert-Regel
        key = self.sim.start_state.__name__
        print(f"\nFunction for Startvalue: {sd[key]['Name']}")
        if info:
             print(f"Description: {sd[key]['Desc']}")

        # Transitions-Regel. Langfristig umbauen mit Dict
        if self.sim.process_type == "markov":
            key = self.sim.transition_markov.__name__
            print(f"\nFunction for transitions: {tdm[key]['Name']}")
            if info:
                print(f"Description: {tdm[key]['Desc']}\n")

        elif self.sim.process_type == "variational":
            key = self.sim.transition_variational.__name__
            print(f"\nFunction for transitions: {tdv[key]['Name']}")
            if info:
                 print(f"Description: {tdv[key]['Desc']}\n")

        elif self.sim.process_type == "adaptive":
            key = self.sim.transition_adaptive.__name__
            print(f"\nFunction for transitions: {tda[key]['Name']}")
            if info:
                 print(f"Description: {tda[key]['Desc']}\n")

        else:
            show_error(True, "Error", "Unknown process type.")
            return

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
                clear_cli()
                print("Is loading...")
                print(paths)
                enter_continue()
                
            elif choice == "2":
                clear_cli()
                print("Is loading...")
                plot_paths(paths, self.sim.seed, self.sim.n_paths)
                continue

            elif choice == "3":
                clear_cli()
                print("Is loading...")
                plot_mean_and_std(paths, self.sim.seed, self.sim.n_paths)
                continue

            elif choice == "4":
                clear_cli()
                print("Is loading...")
                plot_final_distribution(paths, self.sim.seed, self.sim.n_paths)
                continue

            elif choice == "5":
                clear_cli()
                print("Ergodicity data is being calculated...")
                self.ergodicity_menu(paths)
                continue

            elif choice == "c":
                break

    # Submenü für Ergodizität
    def ergodicity_menu(self, paths:list):
        ergodicity_data = calculate_ergodicity(paths)
        self.sim.last_erg_data = ergodicity_data

        while True:
            clear_cli()
            print_separation()
            print("- MONTE CARLO SIMULATION -\n")
            print("RESULT/ERGODICITY: ")
            print("1 - Show Ergodicitiy Data")
            print("2 - Check if ergodic (heuristic)")
            print("C - Close")
            choice = input("> ").strip().lower()

            if choice == "1":
                clear_cli()
                print_separation()
                print("- MONTE CARLO SIMULATION -\n")
                
                data = self.sim.last_erg_data
                
                print("RESULT/ERGODICITY/ERGODICITY DATA: ")
                print(f"Ensemble Mean:         {data['ensemble_mean']:.4f}")
                print(f"Mean of Time Means:    {data['time_mean_mean']:.4f}")
                print(f"Std of Time Means:     {data['time_mean_std']:.4f}")
                print(f"Number of Paths:       {len(data['time_means'])}")
                
                enter_continue()
                continue

            elif choice == "2":
                if self.sim.last_erg_data["ergodic_heuristic"]:
                    print("\nProcess is ergodic.")
                else:
                    print("\nProcess is not ergodic.")

                enter_continue()
                continue

            elif choice == "c":
                break

            else:
                pass

    # Simulation starten
    def _start_sim(self):
        self._show_rules(False)             # Informationen ohne Beschreibung aufrufen
        
        dp = self.sim.n_steps * self.sim.n_paths

        if self.sim.process_type == "markov" and dp > self.sim.marcov_max_datapoints:
            show_error(True, "DataError", f"Number of datapoints ({dp}) exceeds maximum allowed for Markov processes ({self.sim.marcov_max_datapoints}). Proceeding with maximal allowed datapoints.")
            self.sim.n_steps, self.sim.n_paths = self.get_allowed_datapoints("markov")
            self._start_sim()   # Rekursiver Aufruf mit angepassten Daten

        elif self.sim.process_type == "variational" and dp > self.sim.variational_max_datapoints:
            show_error(True, "DataError", f"Number of datapoints ({dp}) exceeds maximum allowed for Variational processes ({self.sim.variational_max_datapoints}). Proceeding with maximal allowed datapoints.")
            self.sim.n_steps, self.sim.n_paths = self.get_allowed_datapoints("variational")
            self._start_sim()   # Rekursiver Aufruf mit angepassten Daten

        elif self.sim.process_type == "adaptive" and dp > self.sim.adaptive_max_datapoints:
            show_error(True, "DataError", f"Number of datapoints ({dp}) exceeds maximum allowed for Adaptive processes ({self.sim.adaptive_max_datapoints}). Proceeding with maximal allowed datapoints.")
            self.sim.n_steps, self.sim.n_paths = self.get_allowed_datapoints("adaptive")
            self._start_sim()   # Rekursiver Aufruf mit angepassten Daten

        enter_continue("Press enter to start the Simulation...")
        clear_cli()
        self.sim.run()                       # Simulation aufrufen; entscheidung zwischen Typ in der Sim-Klasse
        self.result_menu(self.sim.last_result)        # Direkt Menü

    def get_allowed_datapoints(self, type:str) -> int:
        if type == "markov":
            adp = self.sim.marcov_max_datapoints
        
        elif type == "variational":
            adp = self.sim.variational_max_datapoints

        elif type == "adaptive":
            adp = self.sim.adaptive_max_datapoints

        root = math.sqrt(adp)
        steps = math.floor(root)
        paths = math.floor(root)

        return steps, paths

    def _change_process_type(self):
        clear_cli()
        print_separation()
        print("- MONTE CARLO SIMULATION -\n")
        print("CHANGE PROCESS TYPE: ")
        print("1 - Markov Process")
        print("2 - Variational Process")
        print("3 - Adaptive Process")
        choice = input("> ").strip().lower()

        if choice == "1":
            self.sim.process_type = "markov"
            print("\nProcess type set to Markov Process.")
            enter_continue()
            return

        elif choice == "2":
            self.sim.process_type = "variational"
            print("\nProcess type set to Variational Process.")
            enter_continue()
            return

        elif choice == "3":
            self.sim.process_type = "adaptive"
            print("\nProcess type set to Adaptive Process.")
            enter_continue()
            return

        else:
            print("\nInvalid choice. Process type not changed.")
            enter_continue()
            return