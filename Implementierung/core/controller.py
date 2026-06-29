from   process.registry import TRANSITION_REGISTRY, START_STATE_REGISTRY
from   core.config      import SimConfig
from   core.simulation  import MonteCarloSim
from   core.history     import HistoryManager
from   typing           import Callable
import math
import random
#=========================================================================
# Controller
# Verantwortlichkeit: Koordination aller Kernkomponenten und Zustandsver-
# waltung. Einzige Vermittlung zwischen UI und Backend.
#=========================================================================
class Controller:
    
    def __init__(self):

        self.config      = SimConfig()
        self.simulation  = MonteCarloSim()
        self.history     = HistoryManager()
        self._setup()
    
    def _setup(self) -> None:

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
# Konfiguration

    def set_start_state(self, key: str) -> None:
        '''Setzt den Startzustand anhand eines Registry-Keys.'''
        try:
            entry = START_STATE_REGISTRY[key]
            self.config.start_state_fn      = entry["fn"]
            self.config.start_state_name    = entry["name"]
        except Exception:
            raise

    def set_transition(self, process_type: str, key: str) -> None:
        '''
        Setzt Prozesstyp und Übergangsfunktion anhand von Registry-Keys.
        '''
        try:
            entry = TRANSITION_REGISTRY[process_type][key]
            self.config.process_type        = process_type
            self.config.transition_fn       = entry["fn"]
            self.config.transition_name     = entry["name"]
        except Exception:
            raise
 
    def set_parameters(self, n_steps: int, n_paths: int, step_size: float) -> None:
        '''Setzt die numerischen Simulationsparameter.'''
        self.config.n_steps     = n_steps
        self.config.n_paths     = n_paths
        self.config.step_size   = step_size
 
    def set_seed(self, seed: int) -> None:
        self.config.seed = seed
        self.config.rng  = random.Random(seed)

#-------------------------------------------------------------------------
# Registry-Zugriff

    def get_transition_options(self, process_type: str) -> dict:
        '''Rückgabe aller Transitionsfunktionen eines Prozesstypes.'''
        return TRANSITION_REGISTRY[process_type]
    
    def get_start_state_options(self) -> dict:
        '''Rückgabe aller Startzustandsfunktionen.'''
        return START_STATE_REGISTRY
    
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
        
        self._apply_config()
        result = self.simulation.run(config=self.config, on_progress=on_progress)
        self.add_history_entry(result)
        return result

    def get_safe_datapoints(self) -> tuple[int, int]:
            '''
            Berechnet n_steps und n_paths die das Limit nicht überschreiten.
            Gibt ein quadratisches (steps, paths) Paar zurück.
            '''
            limit = self.config.get_limit()
            root = math.isqrt(limit)
            return root, root
    
#-------------------------------------------------------------------------
# Ergebniszugriff (-> history.py)

    def add_history_entry(self, result: list) -> None:
        self.history.add(result, self.config)

    def get_history_entries(self) -> list:
        return self.history.all()

    def delete_history_entry(self, index: int) -> None:
        self.history.delete(index)

    def clear_history(self) -> None:
        self.history.clear()

    def history_is_empty(self) -> bool:
        return self.history.is_empty()

 #-------------------------------------------------------------------------
 # Hilfsmethoden (privat)
 
    def _apply_config(self) -> None:
        '''Überträgt die aktuelle Config auf die Simulation.'''
        sim = self.simulation
        cfg = self.config
 
        sim.n_steps         = cfg.n_steps
        sim.n_paths         = cfg.n_paths
        sim.step_size       = cfg.step_size
        sim.seed            = cfg.seed
        sim.rng             = random.Random(cfg.seed)
        sim.process_type    = cfg.process_type
        sim.transition_fn   = cfg.transition_fn
        sim.start_state_fn  = cfg.start_state_fn