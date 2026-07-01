from ui.utils.display   import clear_cli, print_heading, print_thin_separation, enter_continue
from ui.utils.errors    import show_error, cli_blocking_message
from ui.utils.input     import input_float, input_int, input_confirm
from ui.utils.progress  import print_progress_bar, Spinner
from ui.help            import help_three_types, help_full, help_ergodicity
from ui.plots           import show
from core.config        import SimConfig
from core.controller    import Controller
from core.history       import HistoryEntry
#=========================================================================
class CLI:

    def __init__(self, controller: Controller):

        self.controller = controller

#-------------------------------------------------------------------------
# Hauptmenü

    def run(self):

        while True:
            print_heading("MONTE CARLO SIMULATION")
            print("1 - Start Simulation")
            print("2 - Settings")
            print("3 - History")
            print("H - Help")
            print("C - Close")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()

            if choice == "1":
                self._menu_sim_start()
            elif choice == "2":
                self._menu_sim_settings()
            elif choice == "3":
                self._menu_history()

            elif choice == "h":
                help_full()
                enter_continue()

            elif choice == "c":
                if not self.controller.history_is_empty():
                    if not input_confirm("Are you sure? Results that are not exported will be lost upon exiting the CLI."):
                        continue
                print("Exit CLI...")
                clear_cli()
                break

#-------------------------------------------------------------------------
# Menüs 

    def _menu_sim_start(self):
        print_heading("START SIMULATION")
 
        if not self.controller.config.is_valid():
            missing = ", ".join(self.controller.config.missing_fields())
            cli_blocking_message(
                "START SIMULATION",
                "ConfigError",
                f"Simulation not fully configured. Missing: {missing}",
            )
            return
 
        self._show_simulation_settings()
 
        if self.controller.config.exceeds_limit():
            steps, paths = self.controller.get_safe_datapoints()
            show_error(
                "DatapointError",
                f"Datapoint count exceeds limit for '{self.controller.config.process_type}'. "
                f"Adjusting to {steps} steps × {paths} paths."
            )
            self.controller.set_parameters(steps, paths, self.controller.config.step_size)
 
        if input_confirm("Run simulation?"):
            self._run_simulation()

    def _menu_sim_settings(self):
        while True:
            print_heading("SIMULATION SETTINGS")
            print(f"1 - Dimensionality  (Current: {self.controller.get_dimensionality()})")
            print(f"2 - Startstate      (Current: {self.controller.config.start_state_name})")
            print(f"3 - Transition      (Current: {self.controller.config.transition_name})")
            print(f"4 - Paths           (Current: {self.controller.config.n_paths})")
            print(f"5 - Steps           (Current: {self.controller.config.n_steps})")
            print(f"6 - Step size       (Current: {self.controller.config.step_size})")
            print(f"7 - Seed            (Current: {self.controller.config.seed})")
            print("C - Close")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()
            print()

            if choice == "1":
                self.controller.set_dimensionality(mode=("1d" if self.controller.get_dimensionality() == "nd" else "nd"))
            elif choice == "2":
                self._settings_startstate()
            elif choice == "3":
                self._settings_transition()

            elif choice == "4":
                n_paths = input_int(1, 10000, self.controller.config.n_paths, msg="Number of paths", error=False)
                self.controller.set_parameters(self.controller.config.n_steps, n_paths, self.controller.config.step_size)
            elif choice == "5":
                n_steps = input_int(10, 100000, self.controller.config.n_steps, msg="Number of steps", error=False)
                self.controller.set_parameters(n_steps, self.controller.config.n_paths, self.controller.config.step_size)
            elif choice == "6":
                step_size = input_float(0.01, 100.0, self.controller.config.step_size, msg="Step size", error=False)
                self.controller.set_parameters(self.controller.config.n_steps, self.controller.config.n_paths, step_size)
            elif choice == "7":
                seed = input_int(1, 99999, self.controller.config.seed, msg="Seed", error=False)
                self.controller.set_seed(seed)

            elif choice == "c":
                break
        
    def _menu_history(self):
        if self.controller.history_is_empty():
            cli_blocking_message("HISTORY", "HistoryEmpty", "No simulation results available yet.")
            return

        while True:
            print_heading("HISTORY")
            print(f"Number of results: {len(self.controller.get_history_entries())}\n")
            print("1 - Show result")
            print("2 - Export result")
            print("3 - Delete entry")
            print("4 - Clear all")
            print("C - Cancel")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()

            if choice == "1":
                entry, idx = self._menu_pick_history_entry()
                if entry:
                    self._menu_result(entry, idx)

            elif choice == "2":
                entry, idx = self._menu_pick_history_entry()
                if entry:
                    self._menu_export(entry.result)

            elif choice == "3":
                entry, idx = self._menu_pick_history_entry()
                if idx is not None:
                    self.controller.delete_history_entry(idx)
                    print("\nEntry deleted.")
                    enter_continue()
                    if self.controller.history_is_empty():
                        break

            elif choice == "4":
                if input_confirm("Clear all history?", default_true=False):
                    self.controller.clear_history()
                    print("\nHistory cleared.")
                    enter_continue()
                    break

            elif choice == "c":
                break

    def _menu_pick_history_entry(self) -> tuple[HistoryEntry, int] | tuple[None, None]:
        '''
        Zeigt alle History-Einträge an und lässt den Nutzer einen auswählen.
        Gibt den Eintrag zurück, oder den Index wenn return_index=True.
        '''
        entries = self.controller.get_history_entries()

        # Ein Eintrag: direkte Rückgabe
        if len(entries) == 1:
            return entries[0], 0

        print_heading("SELECT RESULT")
        for i, entry in enumerate(entries, start=1):
            cfg = entry.config
            print(f"{i} - {cfg.transition_name} | {cfg.n_paths} paths × {cfg.n_steps} steps | seed {cfg.seed}")
        print("C - Cancel")
        print_thin_separation(linebreak=False)
        choice = input("> ").strip().lower()

        if choice == "c":
            return None, None

        try:
            idx = int(choice) - 1
        except ValueError:
            show_error("InputError", "Enter a number or C.")
            return None, None

        if 0 <= idx < len(entries):
            return entries[idx], idx
        
        show_error("InputError", "Invalid choice.")
        return None, None

    def _menu_result(self, entry: HistoryEntry, index: int):
        while True:
            print_heading("RESULT")
            print("1 - Print summary")
            print("2 - Print full data")
            print("3 - Sample paths")
            print("4 - Mean and volatility")
            print("5 - Final distribution")
            print("6 - Ergodicity")
            print("C - Close")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()
 
            if choice == "1":
                self._show_result_terminal(entry, index)
            elif choice == "2":
                self._show_full_result_terminal(entry, index)
            elif choice == "3":
                show(entry.result, "sample_paths", entry.config)
            elif choice == "4":
                show(entry.result, "mean_volatility", entry.config)
            elif choice == "5":
                show(entry.result, "final_dist", entry.config)
            elif choice == "6":
                self._menu_ergodicity(entry, index)
            elif choice == "c":
                break
 
    def _menu_export(self, result: list):
        pass # später implementieren. Z.B. als PDF mit allen drei Garfiken etc. Klasse Exporter dann im Controller bei Bedarf initialisiert (lazy)

    def _menu_ergodicity(self, entry: HistoryEntry, index: int):
        if entry.erg_result is None:    # Langfristig: sollte CLI über Status entscheiden?
            spinner = Spinner()
            print()
            spinner.start("Calculating ergodicity")
            try:
                entry.erg_result = self.controller.calculate_ergodicity(index)
            except Exception as e:
                spinner.stop()
                cli_blocking_message("COULD NOT CALCULATE ERGODICITY", "CalculatingError", str(e))
                return
            spinner.stop()

        erg_data = entry.erg_result

        while True:
            print_heading("ERGODICITY DATA")
            print("1 - Show ergodicity data")
            print("2 - Heuristic check")
            print("H - Help")
            print("C - Close")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()
 
            if choice == "1":
                print_heading("ERGODICITY DATA")
                print(f"Ensemble Mean:       {erg_data.ensemble_mean:.4f}")
                print(f"Mean of Time Means:  {erg_data.time_mean_mean:.4f}")
                print(f"Std of Time Means:   {erg_data.time_mean_std:.4f}")
                print(f"Number of Paths:     {len(erg_data.time_means)}")
                enter_continue()
            elif choice == "2":
                result_str = "ergodic" if erg_data.ergodic_heuristic else "not ergodic"
                print(f"\nProcess is {result_str} (heuristic).")
                enter_continue()
            elif choice == "h":
                help_ergodicity()
            elif choice == "c":
                break
 
#-------------------------------------------------------------------------
# Ausführung
 
    def _run_simulation(self):
        clear_cli()
        try:
            self.controller.run_simulation(on_progress=print_progress_bar)
        except ValueError as e:
            show_error("SimulationError", str(e))
            return

        last_index = len(self.controller.get_history_entries()) - 1     # Index
        entry = self.controller.get_history_entries()[last_index]       # Eintrag
        self._menu_result(entry, last_index)                            # Ergebnismenü

#-------------------------------------------------------------------------
# Einstellungsmenüs

    def _settings_startstate(self):
        options = self.controller.get_start_state_options()
        keys = list(options.keys())
 
        while True:
            print_heading("SETTINGS: START STATE")
            print(f"Current: {self.controller.config.start_state_name}\n")
            print("Choose new start state:")
            for i, key in enumerate(keys, start=1):
                print(f"{i} - {options[key]['name']}")
            print("C - Cancel")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()
 
            if choice == "c":
                return
 
            try:
                idx = int(choice)
            except ValueError:
                show_error("InputError", "Enter a number or C.")
                continue
 
            if 1 <= idx <= len(keys):
                key = keys[idx - 1]
                self.controller.set_start_state(key)
                print(f"\nStart state set to: {options[key]['name']}")
                print(f"{options[key]['desc']}")
                enter_continue()
                return
 
            show_error("InputError", "Invalid choice.")

    def _settings_transition(self):
        # Erst Prozesstyp wählen
        process_type = self._choose_process_type()
        if process_type is None:
            return
 
        options = self.controller.get_transition_options(process_type)
        keys = list(options.keys())
 
        while True:
            print_heading(f"SETTINGS: TRANSITION ({process_type.upper()})")
            print(f"Current: {self.controller.config.transition_name}\n")
            print("Choose transition rule:")
            for i, key in enumerate(keys, start=1):
                print(f"{i} - {options[key]['name']}")
            print("C - Cancel")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()
 
            if choice == "c":
                return
 
            try:
                idx = int(choice)
            except ValueError:
                show_error("InputError", "Enter a number or C.")
                continue
 
            if 1 <= idx <= len(keys):
                key = keys[idx - 1]
                self.controller.set_transition(process_type, key)
                print(f"\nTransition set to: {options[key]['name']}")
                print(f"{options[key]['desc']}")
                enter_continue()
                return
 
            show_error("InputError", "Invalid choice.")

    def _choose_process_type(self) -> str | None:
        while True:
            print_heading("SETTINGS: PROCESS TYPE")
            print("1 - Markov Process")
            print("2 - Variational Process")
            print("3 - Adaptive Process")
            print("H - Help")
            print("C - Cancel")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()
 
            if choice == "1":
                return "markov"
            elif choice == "2":
                return "variational"
            elif choice == "3":
                return "adaptive"
            elif choice == "h":
                help_three_types()
            elif choice == "c":
                return None

#-------------------------------------------------------------------------
# Anzeige von Einstellungen und Ergebnissen

    def _show_simulation_settings(self):
        print(f"  Start State:  {self.controller.config.start_state_name}")
        print(f"  Transition:   {self.controller.config.transition_name}")
        print(f"  Process Type: {self.controller.config.process_type}")
        print(f"  Paths:        {self.controller.config.n_paths}")
        print(f"  Steps:        {self.controller.config.n_steps}")
        print(f"  Step Size:    {self.controller.config.step_size}")
        print(f"  Seed:         {self.controller.config.seed}")
        print(f"  Datapoints:   {self.controller.config.datapoint_count()}")
 
    def _show_result_terminal(self, entry: HistoryEntry, index: int):
        result = entry.result
        print_heading("RESULT DATA (SUMMARY)")
        print(f"Paths:   {len(result)}")
        print(f"Steps:   {len(result[0]) if result else 0}")
        print(f"First path (first 10 values): {result[0][:10] if result else '—'}")
        enter_continue()

    def _show_full_result_terminal(self, entry: HistoryEntry, index: int):
        print_heading("RESULT DATA (FULL)")
        print(entry.result)
        enter_continue()
