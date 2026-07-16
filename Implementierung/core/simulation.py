from   core.config  import SimConfig
from   typing       import Callable
import numpy        as     np
#=========================================================================
# Simulation
# Verantwortlichkeit: Pfade berechnen und korrekte run-Methode auswählen.
# Fortschritt durch (optionalen) Callback nach außen gegeben.
#=========================================================================
class MonteCarloSim:

    MAX_PROGRESS_UPDATES: int = 200

#-------------------------------------------------------------------------
# Entrypoint (öffentlich)

    def run(self, config: SimConfig, on_progress: Callable | None):
        '''
        Startet Simulation für gesetzten process_type. 
        '''
        runners = {
            "markov":       self._run_markov,
            "variational":  self._run_variational,
            "adaptive":     self._run_adaptive
        }

        runner = runners.get(config.process_type)
        if runner is None:
            raise ValueError(f"Unknown process type: '{config.process_type}")

        return runner(config, on_progress)

#-------------------------------------------------------------------------
# Hilfsmethoden (privat)

    @staticmethod
    def _init_state(config: SimConfig):
        '''Erzeugt passenden Startzustand, abhängig von Dimensionalität.'''
        if config.dimensionality == "nd":
            return config.start_state_fn(config.rng, n_dimensions=config.n_dimensions)
        else:
            return config.start_state_fn(config.rng)

    @classmethod
    def _progress_interval(cls, n_steps: int) -> int:
        '''
        Bestimmt ein Update-Intervall für on_progress, sodass über die
        gesamte Simulation höchstens MAX_PROGRESS_UPDATES Aufrufe erfolgen.
        Verhindert, dass die Ladeleiste bei sehr vielen Schritten selbst
        spürbaren Overhead erzeugt.
        '''
        return max(1, n_steps // cls.MAX_PROGRESS_UPDATES)

#-------------------------------------------------------------------------
# Run-Methoden (privat)

    def _run_markov(self, config: SimConfig, on_progress: Callable | None) -> list:
        x = np.array([self._init_state(config) for _ in range(config.n_paths)])
        # 1D: shape (n_paths,)
        # ND: shape (n_paths, n_dimensions)

        if config.dimensionality == "nd":
            all_steps = np.empty((config.n_steps, config.n_paths, config.n_dimensions))
        else:
            all_steps = np.empty((config.n_steps, config.n_paths))

        interval = self._progress_interval(config.n_steps)

        for t in range(config.n_steps):
            all_steps[t] = x
            x = config.transition_fn(
                x, config.rng, config.step_size,
                **config.transition_params)   # Params optional

            if on_progress and ((t + 1) % interval == 0 or (t + 1) == config.n_steps):
                on_progress(t + 1, config.n_steps)

        return all_steps.transpose(1, 0, *range(2, all_steps.ndim)).tolist()

    def _run_variational(self, config: SimConfig, on_progress: Callable | None) -> list:
        x = np.array([self._init_state(config) for _ in range(config.n_paths)])

        if config.dimensionality == "nd":
            all_steps = np.empty((config.n_steps, config.n_paths, config.n_dimensions))
        else:
            all_steps = np.empty((config.n_steps, config.n_paths))

        interval = self._progress_interval(config.n_steps)

        for t in range(config.n_steps):
            all_steps[t] = x
            x = config.transition_fn(
                x_t=x, t=t, path=all_steps[:t + 1],
                rng=config.rng, step_size=config.step_size,
                **config.transition_params)   # Params optional

            if on_progress and ((t + 1) % interval == 0 or (t + 1) == config.n_steps):
                on_progress(t + 1, config.n_steps)

        return all_steps.transpose(1, 0, *range(2, all_steps.ndim)).tolist()

    def _run_adaptive(self, config: SimConfig, on_progress: Callable | None) -> list:
        x = np.array([self._init_state(config) for _ in range(config.n_paths)])

        if config.dimensionality == "nd":
            all_steps = np.empty((config.n_steps, config.n_paths, config.n_dimensions))
        else:
            all_steps = np.empty((config.n_steps, config.n_paths))

        interval = self._progress_interval(config.n_steps)
        adaptive_state = {}

        for t in range(config.n_steps):
            all_steps[t] = x
            x, adaptive_state = config.transition_fn(
                x_t=x, t=t, path=all_steps[:t + 1],
                adaptive_state=adaptive_state,
                rng=config.rng, step_size=config.step_size,
                **config.transition_params)   # Params optional

            if on_progress and ((t + 1) % interval == 0 or (t + 1) == config.n_steps):
                on_progress(t + 1, config.n_steps)

        return all_steps.transpose(1, 0, *range(2, all_steps.ndim)).tolist()
