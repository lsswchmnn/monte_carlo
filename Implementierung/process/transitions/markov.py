#=========================================================================
# TYP 1: 
# Lokale, stochastische markov-Prozesse (zeitdiskret und additiv, klassischer 
# Monte-Carlo-Ansatz)
#=========================================================================

# Zufällig Nach oben und unten gehen
def random_walk(x_t: float, rng, step_size: float = 1.0) -> float:
    step = rng.choice([-step_size, step_size])
    return x_t + step

# Leichter Drift
def drifted_random_walk(x_t, rng, step_size: float = 1.0, drift=0.1):
    noise = rng.choice([-step_size, step_size])
    return x_t + drift + noise

# Zunehmendes ziehen in eine Richtung 
def mean_reverting(x_t, rng, step_size: float = 1.0, strength=0.02, mean=2.0):
    pull = -strength * (x_t - mean)
    noise = rng.gauss(0, step_size)
    return x_t + pull + noise

# Extremere Zustände sind gefährlicher
def state_dependent_vol(x_t, rng, step_size=0.5, factor=0.08):
    step = step_size + factor * abs(x_t)
    noise = rng.gauss(0, step)
    return x_t + noise

# Extremere Ausreißer
def fat_tail_walk(x_t, rng, step_size: float = 1.0):
    if rng.random() < 0.98:
        noise = rng.gauss(0, step_size)
    else:
        noise = rng.gauss(0, step_size * 20)
    return x_t + noise

# Unter- oder Obergrenze
def absorbing_barrier(x_t, rng, step_size: float = 1.0, barrier = -10):
    if x_t <= barrier:
        return barrier
    noise = rng.choice([-step_size, step_size])
    return x_t + noise

# Etwas erhöhte Volatilität
def regime_switch(x_t, rng, step_size):
    if rng.random() < 0.9:
        noise = rng.gauss(0, step_size)
    else:
        noise = rng.gauss(0, step_size * 5)
    return x_t + noise

def linear_step(x_t, rng, step_size):
    return x_t