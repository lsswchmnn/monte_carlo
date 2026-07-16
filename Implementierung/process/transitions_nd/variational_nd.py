import numpy as np
#=========================================================================
# TYP 2 (ND): Variational-Prozesse im n-dimensionalen Raum.
# Zustand x_t ist ein np.ndarray der Form (n_dimensions,).
# Parallel zu process/transitions/variational.py.
#=========================================================================

def variational_baseline_nd(
    x_t: np.ndarray,
    t: int,
    path: np.ndarray,
    rng,
    step_size: float,
    memory_strength: float = 0.01,
    ) -> np.ndarray:
    '''
    ND-Analogon zu variational_baseline, vektorisiert über alle Pfade:
    schwache Rückkopplung an den bisherigen Pfadmittelwert pro Achse,
    additive stochastische Komponente.
    '''
    n = path.shape[0]

    if n > 1:
        path_mean = path.mean(axis=0)
        feedback = -memory_strength * (x_t - path_mean)
    else:
        feedback = np.zeros_like(x_t)

    noise = rng.normal(0, step_size, size=x_t.shape)
    return x_t + feedback + noise
