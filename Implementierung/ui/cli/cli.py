from   ui.cli.utils.display   import clear_cli, print_heading, print_thin_separation, enter_continue
from   ui.cli.utils.errors    import show_error, cli_blocking_message
from   ui.cli.utils.input     import input_float, input_int, input_confirm
from   ui.cli.utils.progress  import print_progress_bar, Spinner
from   ui.cli.help            import print_help
from   ui.plots               import Plotter
from   ui.text                import *
from   core.controller        import Controller
from   core.history           import HistoryEntry
from   core.config            import SimConfig
from   pathlib                import Path
from   tkinter                import filedialog
import tkinter                as     tk
#=========================================================================
class CLI:

    def __init__(self, controller: Controller):
        self.controller = controller
        self.plotter    = Plotter()

#-------------------------------------------------------------------------
# Hauptmenü

    def run(self):

        while True:
            print_heading("MONTE CARLO SIMULATION")
            print("1 - Start Simulation")
            print("2 - Configuration")
            print("3 - History")
            print("4 - System")
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
            elif choice == "4":
                self._menu_system_settings()

            elif choice == "h":
                print_help("full")
            elif choice == "c":
                if not self.controller.history_is_empty():
                    if not input_confirm("Are you sure? Results that are not exported will be lost upon exiting the CLI."):
                        continue
                print("Exit CLI...")
                clear_cli()
                break

#-------------------------------------------------------------------------
# Menüebene 1

    def _menu_sim_start(self):
        '''Simulation starten'''
        print_heading("START SIMULATION")
 
        if not self.controller.config.is_valid():
            missing = ", ".join(self.controller.config.missing_fields())
            cli_blocking_message(
                "START SIMULATION",
                "ConfigError",
                f"Simulation not fully configured. Missing: {missing}",
            )
            return
 
        print(format_simulation_settings(self.controller.config))
 
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
        '''Einstellungsmenü'''
        while True:
            print_heading("SIMULATION SETTINGS")
            
            config  = self.controller.config
            dp      = config.datapoint_count()
            limit   = config.get_limit()

            if limit is None:
                print(f"⚪ Datapoints: {dp} (Limit: — no process type set)\n")
            else:
                symbol = "🟢" if dp <= limit else "🔴"
                print(f"{symbol} Datapoints: {dp:_} (Limit: {limit:_})\n")

            print(f"1 - Dimensionality  (Current: {self.controller.get_dimensions()}D)")
            print(f"2 - Startstate      (Current: {config.start_state_name})")
            print(f"3 - Transition      (Current: {config.transition_name})")
            print(f"4 - Paths           (Current: {config.n_paths})")
            print(f"5 - Steps           (Current: {config.n_steps})")
            print(f"6 - Step size       (Current: {config.step_size})")
            print(f"7 - Seed            (Current: {config.seed})")
            print("R - Reset")
            print("H - Help")
            print("C - Close")

            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()
            print()

            if choice == "1":
                self._settings_dimensions()
            elif choice == "2":
                self._settings_startstate()
            elif choice == "3":
                self._menu_transition()

            try:
                if choice == "4":
                    n_paths = input_int(1, 1_000_000, self.controller.config.n_paths, msg="Number of paths", raise_error=False)
                    if n_paths is not None:
                        self.controller.set_parameters(self.controller.config.n_steps, n_paths, self.controller.config.step_size)
                elif choice == "5":
                    n_steps = input_int(10, 10_0000, self.controller.config.n_steps, msg="Number of steps", raise_error=False)
                    if n_steps is not None:
                        self.controller.set_parameters(n_steps, self.controller.config.n_paths, self.controller.config.step_size)
                elif choice == "6":
                    step_size = input_float(0.01, 100.0, self.controller.config.step_size, msg="Step size", raise_error=False)
                    if step_size is not None:
                        self.controller.set_parameters(self.controller.config.n_steps, self.controller.config.n_paths, step_size)
                elif choice == "7":
                    seed = input_int(1, 99999, self.controller.config.seed, msg="Seed", raise_error=False)
                    if seed is not None:
                        self.controller.set_seed(seed)

            except ValueError as e:
                show_error("InputError", str(e))
                enter_continue()

            if choice == "r":
                self.controller.reset_config()
            elif choice == "h":
                print_help("settings")
            elif choice == "c":
                break

    def _menu_history(self):
        '''Gebündelte Aktionen auf fertige Ergebnisse'''
        while True:
            print_heading("HISTORY")
            print(f"Number of results: {len(self.controller.get_history_entries())}\n")
            print("1 - Show result")
            print("2 - Export result")
            print("3 - Import result")
            print("4 - Delete entry")
            print("5 - Clear all")
            print("C - Close")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()

            if choice == "1":
                if self.controller.history_is_empty():
                    cli_blocking_message("HISTORY", "HistoryEmpty", "No simulation results available yet.")
                    return
                entry, idx = self._menu_pick_history_entry()
                if entry:
                    self._menu_result(entry, idx)

            elif choice == "2":
                if self.controller.history_is_empty():
                    cli_blocking_message("HISTORY", "HistoryEmpty", "No simulation results available yet.")
                    return
                entry, idx = self._menu_pick_history_entry()
                if entry:
                    self._menu_export(entry, idx)

            elif choice == "3": 
                self._menu_import()

            elif choice == "4":
                if self.controller.history_is_empty():
                    cli_blocking_message("HISTORY", "HistoryEmpty", "No simulation results available yet.")
                    return
                entry, idx = self._menu_pick_history_entry()
                if idx is not None:
                    self.controller.delete_history_entry(idx)
                    print("\nEntry deleted.")
                    enter_continue()
                    if self.controller.history_is_empty():
                        break

            elif choice == "5":
                if self.controller.history_is_empty():
                    cli_blocking_message("HISTORY", "HistoryEmpty", "No simulation results available yet.")
                    return
                if input_confirm("Clear all history?", default_true=False, warn_symbol=True):
                    self.controller.clear_history()
                    print("\nHistory cleared.")
                    enter_continue()
                    break

            elif choice == "c":
                break

    def _menu_system_settings(self):
            '''Programmweite Anzeige-Einstellungen (kein Bezug zur Simulation).'''
            while True:
                print_heading("SYSTEM SETTINGS")

                settings = self.plotter.settings
                symbol_path = "🟢 Active" if settings.smooth else "🔴 Inactive"
                symbol_grid = "🟢 Active" if settings.grid   else "🔴 Inactive"

                print(f"1 - Grid                 (Current: {symbol_grid})")
                print(f"2 - Path smoothing       (Current: {symbol_path})")
                print(f"3 - Smoothing window     (Current: {settings.smooth_window})")
                print(f"4 - Plot alpha           (Current: {settings.alpha})")
                print("R - Reset")
                print("H - Help")
                print("C - Close")
                print_thin_separation(linebreak=False)
                choice = input("> ").strip().lower()
                
                if choice == "1":
                    self.plotter.toggle_grid()
                elif choice == "2":
                    self.plotter.toggle_smooth()
                print()
                if choice == "3":
                    window = input_int(2, 100, settings.smooth_window, msg="Smoothing window", raise_error=False)
                    if window is not None:
                        self.plotter.set_smooth_window(window)
                elif choice == "4":
                    alpha = input_float(0.0, 1.0, settings.alpha, msg="Plot alpha", raise_error=False)
                    if alpha is not None:
                        self.plotter.set_alpha(alpha)
                elif choice == "r":
                    self.plotter.reset_settings()
                elif choice == "h":
                    print_help("system_settings")
                elif choice == "c":
                    break

#-------------------------------------------------------------------------
# Menüebene 2 - Settings

    def _menu_transition(self):
        '''Menü für Übergangsfunktion'''
        while True:
            print_heading("SETTINGS: TRANSITION")
            print("1 - Change Transition")
            print("2 - View current")
            print("3 - Edit params")
            print("H - Help")
            print("C - Close")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()
 
            if choice == "1":
                self._settings_change_transition()
            elif choice == "2":
                self._show_transition_complete()
                enter_continue()
            elif choice == "3":
                self._settings_transition_params()
            elif choice == "h":
                print_help("transition")
            elif choice == "c":
                return

#-------------------------------------------------------------------------
# Menüebene 2 - History

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
            print(f"{i} - {format_result_name(entry.config)}")
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

    def _menu_export(self, entry: HistoryEntry, index: int):
        '''Export fertiger Ergebnisse als JSON oder CSV'''
        while True:
            print_heading("EXPORT")
            print(f"Transition: {entry.config.transition_name} | "
                f"{entry.config.n_paths} paths × {entry.config.n_steps} steps\n")
            
            formats = self.controller.supported_export_formats()
            for i, fmt in enumerate(formats, start=1):
                print(f"{i} - Export as {fmt.upper()}")
            print("C - Cancel")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()

            if choice == "c":
                return

            try:
                idx = int(choice) - 1
            except ValueError:
                show_error("InputError", "Enter a number or C.")
                continue

            if 0 <= idx < len(formats):
                fmt = formats[idx]
                try:
                    
                    # Verzeichnis für Export wählen
                    output_dir = self._pick_directory()
                    if output_dir is None:
                        print("\nExport cancelled.")
                        enter_continue()
                        return

                    # Exportieren
                    path = self.controller.export_result(index, fmt=fmt, output_dir=output_dir)
                    print(f"\nExported to: {path}")
                    enter_continue()
                    return

                except Exception as e:
                    show_error("ExportError", str(e))
                    enter_continue()
            else:
                show_error("InputError", "Invalid choice.")
                enter_continue()

    def _menu_import(self):
        '''Menü für den Import von vorher exportierten Ergebnissen (JSON)'''
        while True:
            print_heading("IMPORT")
            print("1 - Import from JSON")
            print("C - Cancel")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()

            if choice == "1":
                filepath = self._pick_json_file()
                if filepath is None:
                    print("\nImport cancelled.")
                    enter_continue()
                    return

                try:
                    self.controller.import_result(filepath)
                    print(f"\nImported successfully: {filepath.name}")
                    enter_continue()
                except Exception as e:
                    show_error("ImportError", str(e))

            elif choice == "c":
                return

#-------------------------------------------------------------------------
# Menüebene 3/4 - Einzelergebnis

    def _menu_result(self, entry: HistoryEntry, index: int):
        '''Hauptmenü für spezifisches Ergebnis.'''
        is_nd = entry.config.dimensionality == "nd"
        n_dim = entry.config.n_dimensions

        while True:
            print_heading("RESULT")

            if (is_nd and n_dim > 3):
                print("⚠️ Plotting is not available for >3D.\n")

            print("1 - Print summary")
            print("2 - Print full data")

            if not is_nd:
                print("3 - Plot trajectories")
                print("4 - Plot volatility")
                print("5 - Plot distribution")
                print("6 - Analysis")
            elif n_dim <= 3:
                print(f"3 - Sample paths ({n_dim}D)")

            print("C - Close")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()

            if choice == "1":
                self._show_result_terminal(entry, index)
            elif choice == "2":
                self._show_full_result_terminal(entry, index)
            elif choice == "3" and (not is_nd or n_dim <= 3):
                if entry.config.datapoint_count() > entry.config.limit_graph_warning:
                    if not input_confirm("The number of datapoints is large and plotting may be slow. Continue?", warn_symbol=True):
                        continue
                self.plotter.show(entry.result, "sample_paths", entry.config)
            elif choice == "4" and not is_nd:
                self.plotter.show(entry.result, "mean_volatility", entry.config)
            elif choice == "5" and not is_nd:
                self.plotter.show(entry.result, "final_dist", entry.config)
            elif choice == "6" and not is_nd:
                self._menu_analysis(entry, index)
            elif choice == "c":
                break

    def _menu_analysis(self, entry: HistoryEntry, index: int):
        '''Menü für statistische Analyse auf ein fertiges Ergebnis.'''
        while True:
            print_heading("ANALYSIS")
            print("1 - Ergodicity")
            print("2 - Autocorrelation")
            print("3 - Hurst exponent")
            print("4 - Variance growth")
            print("H - Help")
            print("C - Close")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()

            if choice == "1":
                self._menu_ergodicity(entry, index)
            elif choice == "2":
                self._menu_autocorrelation(entry, index)
            elif choice == "3":
                self._menu_hurst_exponent(entry, index)
            elif choice == "4":
                self._menu_variance_growth(entry, index)

            elif choice == "h":
                print_help("analyze")
            elif choice == "c":
                break
            elif choice == "cc":
                self.run()

    def _menu_ergodicity(self, entry: HistoryEntry, index: int):
        '''Analysemenü: Ergodizität'''
        if entry.erg_result is None:    # Langfristig: sollte CLI über Status entscheiden?
            spinner = Spinner()
            print()
            spinner.start("Calculating ergodicity")
            try:
                entry.erg_result = self.controller.calculate_ergodicity(index)
            except Exception as e:
                spinner.stop()
                cli_blocking_message("Could not calculate Ergodicity", "CalculatingError", str(e))
                return
            spinner.stop()

        erg_data = entry.erg_result

        while True:
            print_heading("ERGODICITY DATA")
            print("1 - Show ergodicity data")
            print("2 - Plot ergodicity")
            print("3 - Heuristic check")
            print("H - Help")
            print("C - Close")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()
 
            if choice == "1":
                print_heading("ERGODICITY DATA")
                print(format_ergodicity(erg_data))
                enter_continue()
            elif choice == "2":
                self.plotter.show_ergodicity(erg_data, entry.config)
            elif choice == "3":
                print(format_ergodicity_heuristic(erg_data))
                enter_continue()
            elif choice == "h":
                print_help("ergodicity")
            elif choice == "c":
                break

    def _menu_autocorrelation(self, entry: HistoryEntry, index: int):
        '''Analysemenü: Autokorrelation'''
        if entry.acf_result is None:
            spinner = Spinner()
            print()
            spinner.start("Calculating autocorrelation")
            try:
                entry.acf_result = self.controller.calculate_autocorrelation(index)
            except Exception as e:
                spinner.stop()
                cli_blocking_message("Could not calculate autocorrelation", "CalculatingError", str(e))
                return
            spinner.stop()

        acf_data = entry.acf_result

        while True:
            print_heading("AUTOCORRELATION DATA")
            print("1 - Show ACF values")
            print("2 - Plot ACF")
            print("3 - White noise test")
            print("H - Help")
            print("C - Close")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()

            if choice == "1":
                print_heading("AUTOCORRELATION DATA")
                print(format_autocorrelation(acf_data))
                enter_continue()
            elif choice == "2":
                self.plotter.show_autocorrelation(acf_data, entry.config)
            elif choice == "3":
                print(format_autocorrelation_significance(acf_data))
                enter_continue()            
            elif choice == "h":
                print_help("autocorrelation")
            elif choice == "c":
                break
            elif choice == "cc":
                self.run()

    def _menu_hurst_exponent(self, entry: HistoryEntry, index: int):
        '''Analysemenü: Hurst-Exponent (DFA)'''
        if entry.hurst_result is None:
            spinner = Spinner()
            print()
            spinner.start("Calculating Hurst exponent (DFA)")
            try:
                entry.hurst_result = self.controller.calculate_hurst_exponent(index)
            except Exception as e:
                spinner.stop()
                cli_blocking_message("COULD NOT CALCULATE HURST EXPONENT", "CalculatingError", str(e))
                return
            spinner.stop()

        hurst_data = entry.hurst_result

        while True:
            print_heading("HURST EXPONENT DATA (DFA)")
            print("1 - Show fluctuation data")
            print("2 - Plot DFA (log-log)")
            print("3 - Interpretation")
            print("H - Help")
            print("C - Close")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()

            if choice == "1":
                print_heading("HURST EXPONENT DATA (DFA)")
                print(format_hurst_exponent(hurst_data))
                enter_continue()
            elif choice == "2":
                self.plotter.show_hurst(hurst_data, entry.config)
            elif choice == "3":
                print(format_hurst_interpretation(hurst_data))
                enter_continue()
            elif choice == "h":
                print_help("hurst_exponent")
            elif choice == "c":
                break

    def _menu_variance_growth(self, entry: HistoryEntry, index: int):
        '''Analysemenü: Varianzwachstum'''
        if entry.variance_result is None:
            spinner = Spinner()
            print()
            spinner.start("Calculating variance growth")
            try:
                entry.variance_result = self.controller.calculate_variance_growth(index)
            except Exception as e:
                spinner.stop()
                cli_blocking_message("COULD NOT CALCULATE VARIANCE GROWTH", "CalculatingError", str(e))
                return
            spinner.stop()

        var_data = entry.variance_result

        while True:
            print_heading("VARIANCE GROWTH DATA")
            print("1 - Show variance data")
            print("2 - Plot variance growth (log-log)")
            print("3 - Interpretation")
            print("H - Help")
            print("C - Close")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()

            if choice == "1":
                print_heading("VARIANCE GROWTH DATA")
                print(format_variance_growth(var_data))
                enter_continue()
            elif choice == "2":
                self.plotter.show_variance_growth(var_data, entry.config)
            elif choice == "3":
                print(format_variance_growth_interpretation(var_data))
                enter_continue()
            elif choice == "h":
                print_help("variance_growth")
            elif choice == "c":
                break
            elif choice == "cc":
                self.run()

#-------------------------------------------------------------------------
# Ausführung

    def _run_simulation(self):
        clear_cli()
        try:
            self.controller.run_simulation(on_progress=print_progress_bar)
        except ValueError as e:
            show_error("SimulationError", str(e))
            enter_continue()
            return

        last_index = len(self.controller.get_history_entries()) - 1
        entry = self.controller.get_history_entries()[last_index]
        self._menu_result(entry, last_index)

#-------------------------------------------------------------------------
# Einstellungsmenüs

    def _settings_dimensions(self):                     # Dimensionalität
        n_dim = input_int(1, 100, 1, msg="Input number of Dimensions", raise_error=False)

        if n_dim is None:
            return
        if n_dim > 1:
            self.controller.set_dimensionality("nd", n_dimensions=n_dim)
            return
        self.controller.set_dimensionality("1d", n_dimensions=1)        

    def _settings_startstate(self):                     # Startzustand
        options = self.controller.get_start_state_options()
        keys = list(options.keys())
 
        while True:
            print_heading("SETTINGS: START STATE")
            print(f"Current: {self.controller.config.start_state_name}\n")
            print("Choose new start state:")
            for i, key in enumerate(keys, start=1):
                print(f"{i} - {options[key]['name']}")
            print("H - Help")
            print("C - Cancel")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()
 
            if choice == "c":
                return
            elif choice == "cc":
                self.run()
            elif choice == "h":
                print_help("start_states")

            try:
                idx = int(choice)
            except ValueError:
                continue
 
            if 1 <= idx <= len(keys):
                key = keys[idx - 1]
                self.controller.set_start_state(key)

                # Zusammenfassung des Startstate
                print_heading(f"SETTINGS: START STATE")
                print(f"Start state set to: {options[key]['name']}")
                print(f"\n{options[key]['desc']}")

                enter_continue()
                return

            show_error("InputError", "Invalid choice.")

    def _settings_change_transition(self):              # Übergang wählen
        process_type = self._choose_process_type()
        if process_type is None:
            return

        options = self.controller.get_transition_options(process_type)  # Registry für Prozesstyp zurückgeben
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
            elif choice == "cc":
                self.run()
            try:
                idx = int(choice)
            except ValueError:
                continue

            if 1 <= idx <= len(keys):
                key = keys[idx - 1]
                self.controller.set_transition(process_type, key)

                self._show_transition_complete()
                enter_continue()
                return

            else:
                show_error("InputError", "Invalid choice.")

    def _settings_transition_params(self):              # Parameter der Übergangsfunktion
        params = self.controller.get_transition_params()

        # Guard
        if not params:
            cli_blocking_message(
                "TRANSITION PARAMETERS",
                "NoParams",
                f"'{self.controller.config.transition_name}' has no configurable parameters."
            )
            return

        while True:
            print_heading("SETTINGS: TRANSITION PARAMETERS")
            print(f"Transition: {self.controller.config.transition_name}\n")

            # Parameter auflisten
            keys = list(params.keys())
            for i, key in enumerate(keys, start=1):
                p = params[key]
                current = self.controller.config.transition_params.get(key, p["default"])
                print(f"{i} - {key:<20} {current}  ({p['desc']})")

            print("R - Reset to defaults")
            print("C - Cancel")
            print_thin_separation(linebreak=False)
            choice = input("> ").strip().lower()

            if choice == "c":
                return
            elif choice == "cc":
                self.run()
            if choice == "r":
                self.controller.reset_transition_params() # Reset
                print("\nParameters reset to defaults.")
                enter_continue()
                continue

            try:
                idx = int(choice) - 1
            except ValueError:
                show_error("InputError", "Enter a number, R, or C.")
                continue

            if not (0 <= idx < len(keys)):
                show_error("InputError", "Invalid choice.")
                continue

            print()
            key = keys[idx]
            p   = params[key]

            if p["type"] == "float":
                value = input_float(
                    min_value=p["min"], max_value=p["max"],
                    default=self.controller.config.transition_params.get(key, p["default"]),
                    msg=f"{key}", raise_error=False
                )
                if value is not None:
                    self.controller.set_transition_param(key, value)

            elif p["type"] == "int":
                value = input_int(
                    min_value=int(p["min"]), max_value=int(p["max"]),
                    default=self.controller.config.transition_params.get(key, p["default"]),
                    msg=f"{key}", raise_error=False
                )
                if value is not None:
                    self.controller.set_transition_param(key, value)

            elif p["type"] == "str":
                options = p.get("options", [])
                print(f"\nOptions for {key}:")
                for i, opt in enumerate(options, start=1):
                    print(f"  {i} - {opt}")
                print_thin_separation(linebreak=False)
                opt_choice = input("> ").strip().lower()

                try:
                    opt_idx = int(opt_choice) - 1
                    if 0 <= opt_idx < len(options):
                        self.controller.set_transition_param(key, options[opt_idx])
                    else:
                        show_error("InputError", "Invalid choice.")
                except ValueError:
                    show_error("InputError", "Enter a number.")

    def _choose_process_type(self) -> str | None:       # Übergangstyp
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
                print_help("three_types")
            elif choice == "c":
                return None
            elif choice == "cc":
                self.run()
                return None

#-------------------------------------------------------------------------
# Anzeige von Einstellungen und Ergebnissen

    def _show_result_terminal(self, entry: HistoryEntry, index: int):
        '''Zeigt eine Zusammenfassung des Ergebnisses an.'''
        print_heading("RESULT DATA (SUMMARY)")
        print(format_result_summary(entry))
        enter_continue()

    def _show_full_result_terminal(self, entry: HistoryEntry, index: int):
        '''Zeigt alle Datenpunkte im Terminal an.'''
        print_heading("RESULT DATA (FULL)")
        print(entry.result)
        enter_continue()

    def _show_transition_complete(self):
        '''Zeigt alle Daten einer Übergangsfunktion.'''
        cfg    = self.controller.config
        params = self.controller.get_transition_params()
        desc   = self.controller.get_transition_desc()

        print_heading("SETTINGS: TRANSITION")
        print(format_transition_details(cfg, desc, params))

#-------------------------------------------------------------------------
# Hilfsfunktionen und TKinter-Interaktion

    def _round_nested(self, value, digits=4):
        '''Rundet verschachtelte Ergebnisse auf n Nachkommastellen.'''
        if isinstance(value, numbers.Number):
            return round(value, digits)
        return [self._round_nested(v, digits) for v in value]

    def _pick_directory(self) -> Path | None:
        '''Öffnet nativen Dateidialog zur Verzeichnisauswahl.'''
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askdirectory(title="Select output directory")
        root.destroy()
        return Path(path) if path else None

    def _pick_json_file(self) -> Path | None:
        '''Öffnet nativen Dateidialog zur JSON-Auswahl.'''
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askopenfilename(
            title="Select result file",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        root.destroy()
        return Path(path) if path else None