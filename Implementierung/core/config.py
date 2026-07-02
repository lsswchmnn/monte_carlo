from   dataclasses import dataclass, field
from   typing      import Callable
import random
#=========================================================================
# SimConfig
# Verantwortlichkeit: Simulationsparameter und Einstellungen zentralisieren.
# Prüft außerdem Gültigkeit, kein UI- und Sim-Bezug.
#=========================================================================
@dataclass
class SimConfig:
    
    seed : int            = 42
    rng  : random.Random  = field(init=False)  # Intern gesetzt

    def __post_init__(self):
        self.rng = random.Random(self.seed)  # Aus Seed ableiten

    # Simulationsparameter
    n_steps     : int   = 1000
    n_paths     : int   = 100
    step_size   : float = 1.0

    # Dimensionalität
    dimensionality : str = "1d"  # "1d" | "nd"
    n_dimensions   : int = 1

    # Prozess (siehe process/)
    process_type      : str      | None = None
    transition_name   : str      | None = None
    start_state_name  : str      | None = None
    transition_fn     : Callable | None = None
    start_state_fn    : Callable | None = None

    # Datapoint-limits (Performance; später evtl. abhängig von Hardware)
    max_datapoints : dict = field(default_factory=lambda: {
        "markov":        100_000_000,
        "variational":   50_000_000,
        "adaptive":      50_000_000,
    })

#-------------------------------------------------------------------------
# Öffentliche Funktionen

    def is_valid(self) -> bool:             # Alle Einträge definiert?
        return len(self.missing_fields()) == 0
 
    def missing_fields(self) -> list[str]:  # Fehlende Einträge zurückgeben
        checks = {
            "process_type":     self.process_type,
            "transition_fn":    self.transition_fn,
            "start_state_fn":   self.start_state_fn,
        }
        return [name for name, value in checks.items() if value is None]
 
    def datapoint_count(self) -> int:       # Anzahl Datenpunkte
        return int(self.n_steps * self.n_paths)
 
    def exceeds_limit(self) -> bool:        # Datenpunkte unter Limit?
        if self.process_type is None:
            return False
        limit = self.max_datapoints.get(self.process_type, 0)
        return self.datapoint_count() > limit
 
    def get_limit(self) -> int | None:      # Limit-Datenpukte
        if self.process_type is None:
            return None
        return self.max_datapoints.get(self.process_type)