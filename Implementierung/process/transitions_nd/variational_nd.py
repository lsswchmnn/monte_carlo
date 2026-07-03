import numpy as np
#=========================================================================
# TYP 2 (ND): Variational-Prozesse im n-dimensionalen Raum.
# Zustand x_t ist ein np.ndarray der Form (n_dimensions,).
# Parallel zu process/transitions/variational.py.
#=========================================================================

def variational_baseline_nd(
    x_t: np.ndarray,
    t: int,
    path: list,
    rng,
    step_size: float,
    memory_strength: float = 0.01,
    ) -> np.ndarray:
    '''
    ND-Analogon zu variational_baseline: schwache Rückkopplung an den
    bisherigen Pfadmittelwert, additive stochastische Komponente pro Achse.
    '''
    n_dimensions = len(x_t)

    if len(path) > 1:
        path_mean = np.mean(path, axis=0)
        feedback = -memory_strength * (x_t - path_mean)
    else:
        feedback = np.zeros(n_dimensions)

    noise = np.array([rng.normal(0, step_size) for _ in range(n_dimensions)])
    return x_t + feedback + noise