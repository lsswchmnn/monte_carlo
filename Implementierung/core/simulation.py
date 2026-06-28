from   core.config      import SimConfig
from   typing           import Callable
#=========================================================================
# Simulation
# Verantwortlichkeit: Pfade berechnen und korrekte run-Methode auswählen.
# Fortschritt durch (optionalen) Callback nach außen gegeben.
#=========================================================================
class MonteCarloSim:

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

        runner = runners.get(config.process_type)
        if runner is None:
            raise ValueError(f"Unknown process type: '{config.process_type}")
        
        # History zurücksetzen
        self.last_result    = None
        self.last_erg_data  = None

        return runner(config, on_progress)

#-------------------------------------------------------------------------
# Run-Methoden (Privat)

    def _run_markov(self, config: SimConfig, on_progress: Callable | None)-> list:
        all_paths = []

        for i in range(config.n_paths):
            path = []
            x = config.start_state_fn(config.rng)

            for _ in range(config.n_steps):
                path.append(x)
                x = config.transition_fn(x, config.rng, config.step_size)
            
            all_paths.append(path)

            if on_progress:
                on_progress(i + 1, config.n_paths)

        self.last_result = all_paths
        return all_paths

    def _run_variational(self, config: SimConfig, on_progress: Callable | None)-> list:
        all_paths = []

        for i in range(config.n_paths):
            path = []
            x = config.start_state_fn(config.rng)

            for t in range(config.n_steps):
                path.append(x)
                x = config.transition_fn (
                    x_t= x,
                    t= t,
                    path= path,
                    rng= config.rng,
                    step_size= config.step_size
                )

            all_paths.append(path)

            if on_progress:
                on_progress(i + 1, config.n_paths)

        self.last_result = all_paths
        return all_paths

    def _run_adaptive(self, config: SimConfig, on_progress: Callable | None)-> list:
        all_paths = []
        all_adaptive_states = []

        for i in range(config.n_paths):
            path = []
            x = config.start_state_fn(config.rng)
            adaptive_state = {}

            for t in range(config.n_steps):
                path.append(x)
                x, adaptive_state = config.transition_fn(
                    x_t=x,
                    t=t,
                    path=path,
                    adaptive_state = adaptive_state,
                    rng=config.rng,
                    step_size=config.step_size
                )
            
            all_paths.append(path)
            all_adaptive_states.append(adaptive_state)

            if on_progress:
                on_progress(i + 1, config.n_paths)

        self.last_result = all_paths
        self.last_adaptive_state = all_adaptive_states
        return all_paths
