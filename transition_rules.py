import random
#=========================================================================
# Beschreibungen und Namen jeder Funktion

transition_data = {
    "random_walk": {
        "Name": "Random Walk",
        "Desc": (
            "At each step, the state moves up or down by a fixed amount. "
            "Both directions are equally likely and independent of the past."
        )
    },

    "drifted_random_walk": {
        "Name": "Drifted Random Walk",
        "Desc": (
            "A random walk with an added constant drift. "
            "The process tends to move in one direction over time."
        )
    },

    "mean_reverting": {
        "Name": "Mean Reversion",
        "Desc": (
            "The state is pulled toward a long-term mean. "
            "Deviations from the mean tend to shrink over time."
        )
    },

    "state_dependent_vol": {
        "Name": "State-Dependent Volatility",
        "Desc": (
            "The size of fluctuations depends on the current state. "
            "More extreme states lead to higher volatility."
        )
    },

    "fat_tail_walk": {
        "Name": "Fat-Tail Walk",
        "Desc": (
            "Most steps are small, but rare steps are extremely large. "
            "The distribution of changes has heavy tails."
        )
    },

    "absorbing_barrier": {
        "Name": "Absorbing Barrier",
        "Desc": (
            "Once the state crosses a fixed boundary, it becomes trapped. "
            "After that point, no further movement is possible."
        )
    },

    "regime_switch": {
        "Name": "Regime Switch",
        "Desc": (
            "The process alternates between normal and high-volatility behavior. "
            "Transitions between regimes occur randomly."
        )
    }
}

#=========================================================================
# Sammlung an Übergangsfunktionen. Simulation benutzt jeweils nur EINE 
# dieser Methoden und kennt deren Logik auch nicht.

# Zufällig Nach oben und unten gehen
def random_walk(x_t: float, rng, step_size: float = 1.0) -> float:
    step = rng.choice([-step_size, step_size])
    return x_t + step

# Leichter Drift
def drifted_random_walk(x_t, rng, step_size: float = 1.0, drift=0.1):
    noise = rng.choice([-step_size, step_size])
    return x_t + drift + noise

# Zunehmendes zurückziehen 
def mean_reverting(x_t, rng, step_size: float = 1.0, strength=0.02, mean=2.0):
    pull = -strength * (x_t - mean)
    noise = rng.gauss(0, step_size)
    return x_t + pull + noise

# Extremere Zustände sind gefährlicher
def state_dependent_vol(x_t, rng, step_size=0.5, factor=0.2):
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
