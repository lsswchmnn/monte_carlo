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


def _levy_stable_sample_nd(rng, alpha: float, size=None):
    '''Chambers-Mallows-Stuck für skalare Schrittlängen.'''
    phi = rng.uniform(-np.pi / 2, np.pi / 2, size=size)
    w   = rng.exponential(1.0, size=size)
 
    if alpha == 1.0:
        return np.abs(np.tan(phi))
 
    term1 = np.sin(alpha * phi) / np.cos(phi) ** (1.0 / alpha)
    term2 = (np.cos((alpha - 1.0) * phi) / w) ** ((1.0 - alpha) / alpha)
    return np.abs(term1 * term2)

 
def levy_flight_nd(x_t: np.ndarray, rng, step_size: float = 1.0, alpha: float = 1.5) -> np.ndarray:
    '''
    Lévy-Flight im n-dimensionalen Raum.
    Schrittlänge folgt einer stabilen Verteilung mit Index alpha,
    Richtung ist gleichmäßig auf der n-dim Einheitssphäre verteilt.
 
    Die Richtung wird über normalverteilte Vektoren berechnet —
    normiert ergibt das eine gleichmäßige Verteilung auf der Einheitssphäre
    für beliebige n (Muller 1959).
    '''
    if x_t.ndim == 2:
        # Vektorisiert: x_t hat Form (n_paths, n_dimensions)
        n_paths, n_dimensions = x_t.shape
 
        lengths     = _levy_stable_sample_nd(rng, alpha, size=n_paths) * step_size
        directions  = rng.normal(size=(n_paths, n_dimensions))
        norms       = np.linalg.norm(directions, axis=1, keepdims=True)
        directions  = directions / norms
 
        steps = directions * lengths[:, np.newaxis]
    else:
        # Skalar: x_t hat Form (n_dimensions,)
        n_dimensions = len(x_t)
 
        length      = _levy_stable_sample_nd(rng, alpha) * step_size
        direction   = rng.normal(size=n_dimensions)
        direction   = direction / np.linalg.norm(direction)
 
        steps = direction * length
 
    return x_t + steps