from utils import clear_cli, print_separation, input_int, print_thin_separation, enter_continue, input_float, show_error, printProgressBar, print_heading
from start_state import start_state_data as sd
from graph import plot_paths, plot_mean_and_std, plot_final_distribution
from montecarlo import MonteCarloSim
from ergodicity import calculate_ergodicity
from help import help_three_types, help_full, help_settings
import start_state
import math
import transition_rules

# Dict mit Beschreibungen der Übergangsfunktionen
from transition_rules import transition_data_markov as tdm
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
            print_heading("- MONTE CARLO SIMULATION -")
            print(f"1 - Load Transition Rule (Current: {self.sim.function_name})")
            print("2 - Show Sim-Settings")
            print("3 - Change Sim-Settings")
            print("4 - Start Simulation")
            if self.sim.last_result:
                print("5 - Show Result")
            print("S - Program Settings")
            print("H - Help")
            print("C - Close CLI")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()
        
            if choice == "1":
                self.change_transitional_function()
                continue
        
            elif choice == "2":
                if not self.sim.transition_function :
                    show_error(True, "SimulationError", "No Transitional Function loaded.")
                    continue

                if not self.sim.check_if_complete():
                    return

                self._show_rules(True)
                enter_continue()
                continue

            elif choice == "3":
                if not self.sim.transition_function :
                    show_error(True, "SimulationError", "No Transitional Function loaded.")
                    continue

                self._load_data()
                continue

            elif choice == "4":
                if not self.sim.check_if_complete():
                    continue

                self._start_sim()

            elif choice == "5" and self.sim.last_result is not None:
                self.result_menu(self.sim.last_result)

            elif choice == "s":
                self.system_settings()
                continue

            elif choice == "h":
                help_full() # Siehe help.py
                enter_continue("Press enter to return to the main menu")

            elif choice == "c":
                clear_cli()
                enter_continue("Press Enter to Leave the Simulation", seperation=False)
                clear_cli()
                print("Goodbye! :) \n")
                break

            else:
                continue

#-------------------------------------------------------------------------
# Menüs

    # Daten für die Sim1ulation abfragen und festlegen
    def _load_data(self):
        self.sim.last_result = None     # Ergebnis zurücksetzen
        print_heading("- MONTE CARLO SIMULATION -")
        print("DATA: ")

        # Daten abfragen
        n_steps = input_int(10, 10000, 1000, "Input Number of steps", True)
        n_paths = input_int(5, 10000, 100, "Input Number of paths", True)
        step_size = input_float(0.1, 100, 1, "Step Size", True)

        # Daten festlegen
        self.sim.n_steps = n_steps
        self.sim.n_paths = n_paths
        self.sim.step_size = step_size

        print_thin_separation()
        self._show_rules()
        enter_continue()

    # Regeln der Simulation anzeigen
    def _show_rules(self, info: bool = True, clear: bool = True):
        print_heading("SETTINGS:")
        
        print(f"Number of steps:            {self.sim.n_steps}")
        print(f"Number of Paths:            {self.sim.n_paths}")
        print(f"Datapoints to calculate:    {int(self.sim.n_paths * self.sim.n_steps)}")
        print(f"Step Size:                  {self.sim.step_size}")
        print(f"Random Seed:                {self.sim.seed}")
        print(f"Process Type:               {self.sim.process_type}")

        # Startwert-Regel
        key = self.sim.start_state.__name__
        print(f"\nFunction for Startvalue: {sd[key]['Name']}")
        if info:
             print(f"Description: {sd[key]['Desc']}")

        # Transitions-Regel
        key = self.sim.transition_function.__name__
        print(f"\nTransition Rule: {self.sim.dict_transition_function[key]['Name']}")
        if info:
            print(f"Description: {self.sim.dict_transition_function[key]['Desc']}")

    # Ergebnis anziegen
    def result_menu(self, paths:list):
        while True:
            print_heading("- MONTE CARLO SIMULATION -")
            print(f"Result ({self.sim.function_name}): ")
            print("1 - Print Data")
            print("2 - Show Sample Paths")
            print("3 - Show Mean Path and Volatility")
            print("4 - Show Distribution of Final Cases")
            print("5 - Calculate Ergodicity")
            print("C - Close")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()

            if choice == "1":
                clear_cli()
                print("Is loading...")
                print(paths)
                enter_continue()
                
            elif choice == "2":
                clear_cli()
                print("Is loading...")
                plot_paths(paths, self.sim.seed, self.sim.n_paths, 
                           self.sim.n_steps, self.sim.function_name)
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
            print_heading("ERGODICITY")
            print("1 - Show Ergodicitiy Data")
            print("2 - Check if ergodic (heuristic)")
            print("H - Help")
            print("C - Close")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()

            if choice == "1":
                clear_cli()
                print_separation()
                print("- MONTE CARLO SIMULATION -\n")
                
                data = self.sim.last_erg_data
                
                print_heading("ERGODICITY DATA")
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

            elif choice == "h":
                print_heading("HELP")
                print("Ergodicity describes whether time averages equal ensemble averages." \
                "A process is ergodic if observing a single system over sufficient time yields the same " \
                "statistical properties as observing many identical systems at one moment. " \
                "In non-ergodic systems, individual trajectories matter: long-term outcomes depend on " \
                "path history, not just expected values.")
                enter_continue("Press enter to return to menu")
                continue

            elif choice == "c":
                break

            else:
                pass

    # Simulation starten
    def _start_sim(self):
        self._show_rules(False)             # Informationen ohne Beschreibung aufrufen
        
        dp = self.sim.n_steps * self.sim.n_paths

        if self.sim.process_type == "markov" and dp > self.sim.markov_max_datapoints:
            show_error(True, "DataError", f"Number of datapoints ({dp}) exceeds maximum allowed for markov processes ({self.sim.markov_max_datapoints}). Proceeding with maximal allowed datapoints.")
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

    # Übergangsfunktion laden/ändern
    def change_transitional_function(self):
        while True:
            print_heading("TRANSITION RULES")
            print("Choose Type of Process: ")
            print("1 - Markov Process")
            print("2 - Variational Process")
            print("3 - Adaptive Process")
            print("H - Help")
            print("C - Cancel")
            print_thin_separation(linebreak = False)
            choice = input("> ").strip().lower()

            if choice == "1":
                self.sim.process_type = "markov"
                print("\nProcess type set to markov Process.")
                self.choose_markov()

            elif choice == "2":
                self.sim.process_type = "variational"
                print("\nProcess type set to Variational Process.")
                self.choose_variational()

            elif choice == "3":
                self.sim.process_type = "adaptive"
                print("\nProcess type set to Adaptive Process.")
                self.choose_adaptive()

            elif choice == "h":
                help_three_types()  # Siehe help.py
                continue

            elif choice == "c":
                return

            else:
                continue

            return

    # System-Einstellungen
    def system_settings(self):
        while True:
            print_heading("SYSTEM-SETTINGS")
            print(f"1 - Seed (Current: {self.sim.seed})")
            print("2 - Start State")
            print("H - Help")
            print("C - Close")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()

            if choice == "1":
                print_heading("SETTINGS: SEED")
                print(f"Current Seed: {self.sim.seed}\n")
                new = input_int(1, 10000, 10, "Enter new Seed (Integer)", True)
                self.sim.seed = new
                print(f"Seed set to {new}.")
                continue

            elif choice == "2":
                self.change_start_state()   # Abschnitt "Hilfsfunktionen"

            elif choice == "h":
                help_settings()
                continue
            
            elif choice == "c":
                return

#-------------------------------------------------------------------------
# Übergangsfunktion wählen

    def choose_markov(self):
        self.sim.process_type = "markov"
        self.sim.dict_transition_function = tdm
        self._choose_transition_from_dict(tdm)

    def choose_variational(self):
        self.sim.process_type = "variational"
        self.sim.dict_transition_function = tdv
        self._choose_transition_from_dict(tdv)

    def choose_adaptive(self):
        self.sim.process_type = "adaptive"
        self.sim.dict_transition_function = tda
        self._choose_transition_from_dict(tda)

    def _choose_transition_from_dict(self, data_dict: dict):
        while True:
            print_heading("TRANSITION RULES")

            keys = list(data_dict.keys())

            print("Choose Transition Rule:")
            for i, key in enumerate(keys, start=1):
                meta = data_dict[key]
                print(f"{i} - {meta['Name']}")

            print("C - Cancel")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()

            if choice == "c":
                return
            
            try:
                idx = int(choice)
            except:
                show_error(True, "InputError", "Input must be 'C' or Integer")
                continue

            if 1 <= idx <= len(keys):
                func_name = keys[idx - 1]

                try:
                    func = getattr(transition_rules, func_name)
                except AttributeError:
                    show_error(True, "TransitionError", f"Function {func_name} not found in Dictionary.")
                    continue
                
                print_heading("TRANSITION RULES")
                self.sim.transition_function  = func
                self.sim.function_name = data_dict[func_name]["Name"]
                print(f"Transition function set to: {data_dict[func_name]['Name']}\n")
                self.show_desc(data_dict, func_name)
                return

            print("\nInvalid choice.")

    def show_desc(self, dict, func_name):
        print(f"{dict[func_name]['Desc']}")
        enter_continue()

#-------------------------------------------------------------------------
# Hilfsfunktionen

    def get_allowed_datapoints(self, type:str) -> int:
        if type == "markov":
            adp = self.sim.markov_max_datapoints
        
        elif type == "variational":
            adp = self.sim.variational_max_datapoints

        elif type == "adaptive":
            adp = self.sim.adaptive_max_datapoints

        root = math.sqrt(adp)
        steps = math.floor(root)
        paths = math.floor(root)

        return steps, paths
    
    def change_start_state(self):
        while True:
            print_heading("SETTINGS: START STATE")
            print

            keys = list(sd.keys())
            print("Choose Start State:")

            for i, key in enumerate(keys, start=1):
                meta = sd[key]
                print(f"{i} - {meta['Name']}")

            print("C - Cancel")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()

            if choice == "c":
                return
            
            try:
                idx = int(choice)
            except:
                show_error(True, "InputError", "Input must be 'C' or Integer")

            if 1 <= idx <= len(keys):
                func_name = keys[idx - 1]

                try:
                    func = getattr(start_state, func_name)
                except AttributeError:
                    show_error(True, "TransitionError", f"Function {func_name} not found in Dictionary.")
                    continue
                
                print_heading("SETTINGS: START STATE")
                self.sim.start_state  = func
                self.sim.function_name = sd[func_name]["Name"]
                print(f"Start State set to: {sd[func_name]['Name']}\n")
                self.show_desc(sd, func_name)
                return