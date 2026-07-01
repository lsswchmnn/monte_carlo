import numpy as np
#=========================================================================
# TYP 1 (ND): Markov-Prozesse im n-dimensionalen Raum.
# Zustand x_t ist ein np.ndarray der Form (n_dimensions,).
# Parallel zu process/transitions/markov.py — bewusst keine gemeinsame
# Abstraktion mit der 1D-Variante, da die Operationen unterschiedlich sind.
#=========================================================================

def random_walk_nd(x_t: np.ndarray, rng, step_size: float = 1.0) -> np.ndarray:
    '''
    Bewegt sich in jedem Schritt zufällig um ±step_size entlang
    einer zufällig gewählten Dimension (z.B. Norden/Süden/Osten/Westen in 2D).
    '''
    n_dimensions = len(x_t)
    direction = rng.randrange(n_dimensions)
    sign = rng.choice([-1.0, 1.0])
 
    step = np.zeros(n_dimensions)
    step[direction] = sign * step_size
 
    return x_t + step
 