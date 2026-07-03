import numpy as np
#=========================================================================
# TYP 3 (ND): Adaptive Prozesse im n-dimensionalen Raum.
# Zustand x_t ist ein np.ndarray der Form (n_dimensions,).
# Parallel zu process/transitions/adaptive.py.
#=========================================================================

def adaptive_random_walk_nd(
    x_t: np.ndarray,
    t: int,
    path: list,
    adaptive_state: dict,
    rng,
    step_size: float = 1.0,
    ) -> tuple[np.ndarray, dict]:
    '''
    ND-Analogon zu adaptive_random_walk: zufällige Achse, zufälliges
    Vorzeichen, triviale Adaption über Schrittzähler.
    '''
    n_dimensions = len(x_t)

    if not adaptive_state:
        adaptive_state = {
            "step_size": step_size,
            "n_steps": 0,
        }

    direction = int(rng.integers(n_dimensions))
    sign = rng.choice(np.array([-1.0, 1.0]))

    step = np.zeros(n_dimensions)
    step[direction] = sign * adaptive_state["step_size"]

    x_next = x_t + step
    adaptive_state["n_steps"] += 1

    return x_next, adaptive_state