from   process.registry import TRANSITION_REGISTRY, START_STATE_REGISTRY, TRANSITION_REGISTRY_ND, START_STATE_REGISTRY_ND
from   core.config      import SimConfig
from   core.simulation  import MonteCarloSim
from   core.history     import HistoryManager, HistoryEntry
from   analyze.analyzer import Analyzer, ErgodicityResult
from   exporter         import Exporter          
from   typing           import Callable
from   pathlib          import Path
import numpy            as     np, math, time
#=========================================================================
# Controller
# Verantwortlichkeit: Koordination aller Kernkomponenten und Zustandsver-
# waltung. Einzige Vermittlung zwischen UI und Backend.
#=========================================================================
class Controller:

    def __init__(self):

        self.config      : SimConfig        = SimConfig()
        self.simulation  : MonteCarloSim    = MonteCarloSim()
        self.history     : HistoryManager   = HistoryManager()
        self.analyzer    : Analyzer         = Analyzer()
        self._exporter   : Exporter | None  = None
        self._setup()

    def _setup(self) -> None:
        self._set_defaults()

#-------------------------------------------------------------------------
# Dimensionalität (1D oder ND)
 
    def set_dimensionality(self, mode: str, n_dimensions: int = 2) -> None:
        '''
        Wechselt zwischen "1d" und "nd".
        Setzt dabei automatisch passende Defaults zurück.
        '''
        if mode not in ("1d", "nd"):
            raise ValueError(f"Invalid dimensionality: '{mode}'. Use '1d' or 'nd'.")

        self.config.dimensionality = mode
        self.config.n_dimensions   = n_dimensions

        # Transition und Startzustand auf passende Defaults zurücksetzen
        if mode == "nd":
            default_start = START_STATE_REGISTRY_ND["fixed_state_nd"]
            default_tr    = TRANSITION_REGISTRY_ND["markov"]["random_walk_nd"]
        else:
            default_start = START_STATE_REGISTRY["fixed_state"]
            default_tr    = TRANSITION_REGISTRY["markov"]["random_walk"]

        self.config.start_state_fn   = default_start["fn"]
        self.config.start_state_name = default_start["name"]
        self.config.transition_fn    = default_tr["fn"]
        self.config.transition_name  = default_tr["name"]
        self.config.process_type     = "markov"

    def get_dimensionality(self) -> str:
        return self.config.dimensionality

    def get_dimensions(self) -> int:
        return self.config.n_dimensions

#-------------------------------------------------------------------------
# Allgemeine Konfiguration (-> config.py)

    def get_transition_params(self) -> dict:
        '''Gibt params-Dict des aktuellen Registry-Eintrags zurück.'''
        registry = self._transition_registry()
        for process_entries in registry.values():
            for key, entry in process_entries.items():
                if entry["name"] == self.config.transition_name:
                    return entry.get("params", {})
        return {}

    def get_transition_desc(self) -> str:
        registry = self._transition_registry()
        for process_entries in registry.values():
            for key, entry in process_entries.items():
                if entry["name"] == self.config.transition_name:
                    return entry.get("desc", "")
        return ""

    def set_start_state(self, key: str) -> None:
        '''Setzt den Startzustand anhand eines Registry-Keys.'''
        try:
            registry = self._start_state_registry()
            entry = registry[key]
            self.config.start_state_fn   = entry["fn"]
            self.config.start_state_name = entry["name"]
        except Exception:
            raise

    def set_transition(self, process_type: str, key: str) -> None:
        '''
        Setzt Prozesstyp und Übergangsfunktion anhand von Registry-Keys.
        '''
        try:
            registry = self._transition_registry()    # gibt je nach dimensionality die richtige zurück
            entry = registry[process_type][key]
            self.config.process_type      = process_type
            self.config.transition_fn     = entry["fn"]
            self.config.transition_name   = entry["name"]
            self.config.transition_params = {}                  # Params zurücksetzen
        except Exception:
            raise
 
    def set_parameters(self, n_steps: int, n_paths: int, step_size: float) -> None:
        '''Setzt die numerischen Simulationsparameter.'''
        self.config.n_steps     = n_steps
        self.config.n_paths     = n_paths
        self.config.step_size   = step_size

    def set_seed(self, seed: int) -> None:
        self.config.seed = seed
        self.config.rng  = np.random.default_rng(seed)

    def set_transition_param(self, key: str, value) -> None:
        self.config.transition_params[key] = value

#-------------------------------------------------------------------------
# Reset von Einstellungen und Konfiguration

    def reset_transition_params(self) -> None:
        self.config.transition_params = {}

    def reset_config(self):
        '''Setzt gesamte Konfiguration zurück.'''
        self.config = SimConfig()
        self._set_defaults()

    def _set_defaults(self):
        '''Setzt Defaults für Startzustand und Übergangsfunktion.'''
        # Startzustand-Default setzen
        default_start                 = START_STATE_REGISTRY["fixed_state"]
        self.config.start_state_fn    = default_start["fn"]
        self.config.start_state_name  = default_start["name"]

        # Übergangsfunktion-Default setzen
        self.config.process_type      = "markov"
        default_transition            = TRANSITION_REGISTRY["markov"]["random_walk"]
        self.config.transition_fn     = default_transition["fn"]
        self.config.transition_name   = default_transition["name"]

#-------------------------------------------------------------------------
# Registry-Zugriff (-> process/registry.py)

    def get_transition_options(self, process_type: str) -> dict:
        '''Gibt passende Trnasition-Optionen zurück, abhängig von Dimensionalität und Prozesstyp.'''
        return self._transition_registry()[process_type]

    def get_start_state_options(self) -> dict:
        '''Gibt passende Startzustand-Optionen zurück, abhängig von Dimensionalität.'''
        return self._start_state_registry()

#-------------------------------------------------------------------------
# Simulation (-> simulation.py)

    def run_simulation(self, on_progress: Callable | None = None) -> list:
        '''Führt Monte Carlo Simulation aus. Config wird automatisch übergeben.'''

        if not self.config.is_valid():
            missing = ", ".join(self.config.missing_fields())
            raise ValueError(f"Simulation config imcomplete. Missing: {missing}")
        
        if self.config.exceeds_limit():
            raise ValueError(
                    f"Datapoint count ({self.config.datapoint_count():,}) exceeds limit "
                    f"for '{self.config.process_type}' ({self.config.get_limit():,}). "
                    f"Reduce n_steps or n_paths."
                )
        
        self.config.rng = np.random.default_rng(self.config.seed)                   # RNG-Reset (sont unt. Ergebnisse bei gleicher Seed)

        # Simulation starten und Zeit messen
        start = time.perf_counter()
        result = self.simulation.run(config=self.config, on_progress=on_progress)
        end = time.perf_counter()
        calc_time = end - start

        # Zu Historie hinzufügen und Liste zurückgeben
        self.add_history_entry(result, calc_time=calc_time)
        return result

    def get_safe_datapoints(self) -> tuple[int, int]:
        '''
        Berechnet n_steps und n_paths die das Limit nicht überschreiten.
        Gibt ein quadratisches (steps, paths) Paar zurück.
        '''
        limit = self.config.get_limit() // max(self.config.n_dimensions, 1) # Dimension berücksichtigen
        root = math.isqrt(limit)
        return root, root

#-------------------------------------------------------------------------
# Ergebniszugriff (-> history.py)

    def add_history_entry(self, result: list, calc_time: float | None = None) -> None:
        self.history.add(result, self.config, calc_time)

    def get_history_entry(self, index: int) -> HistoryEntry:
        return self.history.get(index)

    def get_history_entries(self) -> list:
        return self.history.all()

    def delete_history_entry(self, index: int) -> None:
        self.history.delete(index)

    def clear_history(self) -> None:
        self.history.clear()

    def history_is_empty(self) -> bool:
        return self.history.is_empty()

#-------------------------------------------------------------------------
# Analyse auf Ergebnis (-> analyzer.py)

    def calculate_ergodicity(self, index: int) -> ErgodicityResult:
        '''Untersucht ergodisches Verhalten eines Prozesses.'''
        if self.config.dimensionality != "1d":
            raise ValueError("Ergodicity is not implemented for nd-processes yet.")
        entry = self.get_history_entry(index)
        result = self.analyzer.calculate_ergodicity(entry.result)
        entry.erg_result = result   # Ergebnis hinzufügen
        return result

#-------------------------------------------------------------------------
# Export/Import (-> exporter.py)

    @property
    def exporter(self) -> Exporter:
        if self._exporter is None:
            self._exporter = Exporter()
        return self._exporter
    
    def export_result(self, index: int, fmt: str = "json", output_dir=None) -> Path:
        '''Exportiert gewählten Eintrag in gewünschtem Format.'''
        entry = self.get_history_entry(index)
        return self.exporter.export(entry.result, entry.config, fmt=fmt, output_dir=output_dir)

    def import_result(self, filepath) -> None:
        '''Importiert eine JSON-Datei und fügt sie zur History hinzu.'''
        result, config = self.exporter.import_result(filepath)
        self.history.add(result, config)

    def supported_export_formats(self) -> list[str]:
        return self.exporter.supported_formats()

#-------------------------------------------------------------------------
# Allgemeine Hilfsmethoden (privat)

    def _start_state_registry(self) -> dict[str, dict]:
        '''Gibt die passende Startzustands-Registry zurück, abhängig von Dimensionalität.'''
        if self.config.dimensionality == "1d":
            return START_STATE_REGISTRY
        else:
            return START_STATE_REGISTRY_ND

    def _transition_registry(self) -> dict[str, dict]:
        '''Gibt die passende Transition-Registry zurück, abhängig von Dimensionalität.'''
        if self.config.dimensionality == "1d":
            return TRANSITION_REGISTRY
        else:
            return TRANSITION_REGISTRY_ND