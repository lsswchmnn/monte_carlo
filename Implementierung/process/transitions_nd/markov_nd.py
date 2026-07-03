import numpy as np
#=========================================================================
# TYP 1 (ND): Markov-Prozesse im n-dimensionalen Raum.
# Zustand x_t ist ein np.ndarray der Form (n_dimensions,).
# Parallel zu process/transitions/markov.py — bewusst keine gemeinsame
# Abstraktion mit der 1D-Variante, da die Operationen unterschiedlich sind.
#=========================================================================

def random_walk_nd(x_t: np.ndarray, rng, step_size: float = 1.0) -> np.ndarray:
    if x_t.ndim == 2:
        # Vektorisiert: x_t hat Form (n_paths, n_dimensions)
        n_paths, n_dimensions = x_t.shape
        directions = rng.integers(n_dimensions, size=n_paths)
        signs = rng.choice(np.array([-1.0, 1.0]), size=n_paths)
        steps = np.zeros((n_paths, n_dimensions))
        steps[np.arange(n_paths), directions] = signs * step_size
    else:
        # Skalar: x_t hat Form (n_dimensions,)
        n_dimensions = len(x_t)
        direction = int(rng.integers(n_dimensions))
        sign = rng.choice(np.array([-1.0, 1.0]))
        steps = np.zeros(n_dimensions)
        steps[direction] = sign * step_size

    return x_t + steps