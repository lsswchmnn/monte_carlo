import numpy as np
#=========================================================================
# TYP 3 (ND): Adaptive Prozesse im n-dimensionalen Raum.
# Zustand x_t ist ein np.ndarray der Form (n_dimensions,).
# Parallel zu process/transitions/adaptive.py.
#=========================================================================

def adaptive_random_walk_nd(
    x_t: np.ndarray,
    t: int,
    path: np.ndarray,
    adaptive_state: dict,
    rng,
    step_size: float = 1.0,
    ) -> tuple[np.ndarray, dict]:
    '''
    ND-Analogon zu adaptive_random_walk, vektorisiert über alle Pfade:
    zufällige Achse, zufälliges Vorzeichen pro Pfad, triviale Adaption
    über Schrittzähler.
    '''
    n_paths, n_dimensions = x_t.shape

    if not adaptive_state:
        adaptive_state = {
            "step_size": np.full(n_paths, step_size),
            "n_steps": np.zeros(n_paths, dtype=int),
        }

    directions = rng.integers(n_dimensions, size=n_paths)
    signs      = rng.choice(np.array([-1.0, 1.0]), size=n_paths)

    step = np.zeros((n_paths, n_dimensions))
    step[np.arange(n_paths), directions] = signs * adaptive_state["step_size"]

    x_next = x_t + step
    adaptive_state["n_steps"] += 1

    return x_next, adaptive_state