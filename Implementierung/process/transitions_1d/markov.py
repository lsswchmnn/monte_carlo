import numpy as np
#=========================================================================
# TYP 1: 
# Lokale, stochastische markov-Prozesse (zeitdiskret und additiv, klassischer 
# Monte-Carlo-Ansatz)
#=========================================================================

def _size(x_t) -> int | None:
    """Gibt die Anzahl der Pfade zurück, oder None für skalaren Aufruf."""
    return len(x_t) if isinstance(x_t, np.ndarray) else None
 
 
def random_walk(x_t, rng, step_size: float = 1.0):
    steps = rng.choice(np.array([-step_size, step_size]), size=_size(x_t))
    return x_t + steps
 
 
def drifted_random_walk(x_t, rng, step_size: float = 1.0, drift: float = 0.1):
    noise = rng.choice(np.array([-step_size, step_size]), size=_size(x_t))
    return x_t + drift + noise
 
 
def mean_reverting(x_t, rng, step_size: float = 1.0,
                   strength: float = 0.02, mean: float = 2.0):
    pull  = -strength * (x_t - mean)
    noise = rng.normal(0, step_size, size=_size(x_t))
    return x_t + pull + noise
 
 
def state_dependent_vol(x_t, rng, step_size: float = 0.5, factor: float = 0.08):
    step  = step_size + factor * np.abs(x_t)
    noise = rng.normal(0, step)
    return x_t + noise
 
 
def fat_tail_walk(x_t, rng, step_size: float = 1.0):
    n = _size(x_t)
    if n is not None:
        noise  = rng.normal(0, step_size, size=n)
        fat    = rng.normal(0, step_size * 20, size=n)
        is_fat = rng.random(size=n) >= 0.98
        noise  = np.where(is_fat, fat, noise)
    else:
        noise = rng.normal(0, step_size * 20) if rng.random() >= 0.98 else rng.normal(0, step_size)
    return x_t + noise
 
 
def absorbing_barrier(x_t, rng, step_size: float = 1.0, barrier: float = -10.0):
    n = _size(x_t)
    if n is not None:
        noise  = rng.choice(np.array([-step_size, step_size]), size=n)
        x_next = x_t + noise
        return np.where(x_t <= barrier, barrier, x_next)
    else:
        if x_t <= barrier:
            return barrier
        return x_t + rng.choice(np.array([-step_size, step_size]))
 
 
def regime_switch(x_t, rng, step_size: float = 1.0):
    n = _size(x_t)
    if n is not None:
        normal   = rng.normal(0, step_size,     size=n)
        high_vol = rng.normal(0, step_size * 5, size=n)
        is_high  = rng.random(size=n) >= 0.9
        noise    = np.where(is_high, high_vol, normal)
    else:
        noise = rng.normal(0, step_size * 5) if rng.random() >= 0.9 else rng.normal(0, step_size)
    return x_t + noise
 
 
def linear_step(x_t, rng, step_size: float = 1.0):
    return x_t