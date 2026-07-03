import numpy as np
#=========================================================================
# 1D-Startstates

def fixed_state(rng) -> float:
    return 1

def random_state(rng) -> float:
    return rng.normal(0, 1)

#=========================================================================
# ND-Startstates

def fixed_state_nd(rng, n_dimensions: int = 2) -> np.ndarray:
    return np.zeros(n_dimensions)

def random_state_nd(rng, n_dimensions: int = 2) -> np.ndarray:
    return np.array([rng.normal(0,1) for _ in range(n_dimensions)])