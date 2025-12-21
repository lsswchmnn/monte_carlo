from utils import clear_cli, print_separation, input_int, enter_continue, input_float
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

            elif choice == "c":
                print("Close simulation...")
                clear_cli()
                break

#=========================================================================
# CLI-Methoden

    # Daten für die Simulation abfragen und festlegen
    def _load_data(self):
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

    # Ergebnis anziegen
    def _show_result(self, paths:list):
        print(paths)
        enter_continue()

    # Simulation starten
    def _start_sim(self):
        self._show_rules()
        enter_continue("Press enter to start the Simulation.")
        result = self.sim.run()
        self._show_result(result)

