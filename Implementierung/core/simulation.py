from   process.registry import START_STATE_REGISTRY
from   core.config      import SimConfig
from   typing           import Callable
import random
#=========================================================================
# Simulation
# Verantwortlichkeit: Pfade berechnen und korrekte run-Methode auswählen.
# Fortschritt durch (optionalen) Callback nach außen gegeben.

# Config noch in _run*-Methoden einbauen!
#=========================================================================
class MonteCarloSim:

    def __init__(self):

        # Später evtl auslagern in dedizierten HistoryManager
        self.last_result      : list | None = None  # Auf letztes Ergebnis zugreifen
        self.last_erg_data    : list | None = None  # Ergodizitäts-Ergebnis
        self.last_adaptive_states

#-------------------------------------------------------------------------
# Entrypoint (Öffentlich)

    def run(self, config: SimConfig, on_progress: Callable | None):
        '''
        Startet Simulation für gesetzten process_type. 
        '''
        runners = {
            "markov": self._run_markov,
            "variational": self._run_variational,
            "adaptive": self._run_adaptive
        }

        runner = runners.get(self.process_type)
        if runner is None:
            raise ValueError(f"Unknown process type: '{self.process_type}")
        
        # History zurücksetzen
        self.last_result    = None
        self.last_erg_data  = None

        return runner(config, on_progress)

#-------------------------------------------------------------------------
# Run-Methoden (Privat)

    def _run_markov(self, on_progress: Callable | None)-> list:
        all_paths = []

        for i in range(self.n_paths):
            path = []
            x = self.start_state(self.rng)

            for _ in range(self.n_steps):
                path.append(x)
                x = self.transition_function (x, self.rng, self.step_size)
            
            all_paths.append(path)

            if on_progress:
                on_progress(i + 1, self.n_paths)

        self.last_result = all_paths
        return all_paths

    def _run_variational(self, on_progress: Callable | None)-> list:
        all_paths = []

        for i in range(self.n_paths):
            path = []
            x = self.start_state(self.rng)

            for t in range(self.n_steps):
                path.append(x)
                x = self.transition_function (
                    x_t= x,
                    t= t,
                    path= path,
                    rng= self.rng,
                    step_size= self.step_size
                )

            all_paths.append(path)

            if on_progress:
                on_progress(i + 1, self.n_paths)

        self.last_result = all_paths
        return all_paths

    def _run_adaptive(self, on_progress: Callable | None)-> list:
        all_paths = []
        all_adaptive_states = []

        for i in range(self.n_paths):
            path = []
            x = self.start_state(self.rng)
            adaptive_state = {}

            for t in range(self.n_steps):
                path.append(x)
                x, adaptive_state = self.transition_function(
                    x_t=x,
                    t=t,
                    path=path,
                    adaptive_state = adaptive_state,
                    rng=self.rng,
                    step_size=self.step_size
                )
            
            all_paths.append(path)
            all_adaptive_states.append(adaptive_state)

            if on_progress:
                on_progress(i + 1, self.n_paths)

        self.last_result = all_paths
        self.last_adaptive_state = all_adaptive_states
        return all_paths

#-------------------------------------------------------------------------
# Hilfsmethoden (evtl. auslagern)

    def is_ready(self) -> bool:
        '''Gibt True zurück wenn alle Pflichtfelder gesetzt sind.'''
        return all([
            self.transition_fn      is not None,
            self.start_state_fn     is not None,
            self.process_type       is not None,
            self.n_steps            is not None,
            self.n_paths            is not None,
            self.seed               is not None,
            self.step_size          is not None,
        ])
 
    def missing_fields(self) -> list[str]:
        '''Gibt eine Liste der noch nicht gesetzten Pflichtfelder zurück.'''
        checks = {
            "transition_fn":    self.transition_fn,
            "start_state_fn":   self.start_state_fn,
            "process_type":     self.process_type,
            "n_steps":          self.n_steps,
            "n_paths":          self.n_paths,
            "seed":             self.seed,
            "step_size":        self.step_size,
        }
        return [name for name, value in checks.items() if value is None]