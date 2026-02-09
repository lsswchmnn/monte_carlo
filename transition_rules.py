import random
#=========================================================================
transition_data_markov = {
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
    },

    "linear_step": {
        "Name": "Linear Step",
        "Desc": (
            "The Process creates one linear line."
        )
    },
}

transition_data_variational = {
    "variational_baseline": {
        "Name": "Variational Baseline",
        "Desc": (
            "A simple variational transition that incorporates feedback from the path's history. "
            "The state is influenced by its deviation from the path mean."
        )
    },

    "variational_trend_feedback": {
        "Name": "Variational Trend Feedback",
        "Desc": (
            "A variational transition that incorporates feedback from the path's history, "
            "with an emphasis on trend feedback and path-dependent volatility."
        )
    }
}

transition_data_adaptive = {
    "adaptive_random_walk": {
        "Name": "Adaptive Random Walk",
        "Desc": (
            "A simple adaptive Random Walk with trivial increasing of the value as placeholder."
        )
    },

    "adaptive_volatility_walk": {
        "Name": "Adaptive Volatility Walk",
        "Desc": (
            "an adaptive random walk in which the step size is endogenously "
            "adjusted based on recently observed volatility. Each step is stochastic, "
            "but the magnitude of future steps depends on an exponential moving average "
            "of past step sizes. Higher realized volatility leads to a reduction in step size, "
            "introducing negative feedback and non-stationarity. As a result, the process "
            "is path-dependent and no longer ergodic in the classical sense, since its dynamics evolve "
            "with its own history."
        )
    }
}
#=========================================================================
'''
Sammlung an Übergangsfunktionen. Simulation benutzt jeweils nur EINE 
dieser Methoden und kennt deren Logik auch nicht. Die Funktionen sind in
drei Typen unterteilt, je nachdem, wieviel Kontext sie für die
Übergangsentscheidung nutzen dürfen und mit welcher run-Methode sie kombiniert
werden können.

Die Dynamik wird zunehmend kontextabhängig und abnehmend ergodisch.
'''
#=========================================================================
'''
TYP 2: 
Lokale, stochastische markov-Prozesse (zeitdiskret und additiv, klassischer 
Monte-Carlo-Ansatz)
'''
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
    return x_t + 0

#=========================================================================
''' 
TYP 2: 
Pfadabhängige, nicht lokale Prozesse. Darf mehr kontext als nur den 
aktuellen Zustand nutzen, nämlich gesamten bisherigen Verlauf und die Zeit.
'''
# Minimaler variationaler Übergang
def variational_baseline(
    x_t: float,
    t: int,
    path: list,
    rng,
    step_size: float,
    memory_strength: float = 0.01
) -> float:
    """
    Minimaler variationaler Übergang:
    - schwache Rückkopplung an den bisherigen Pfadmittelwert
    - additive stochastische Komponente
    """

    if len(path) > 1:
        path_mean = sum(path) / len(path)
        feedback = -memory_strength * (x_t - path_mean)
    else:
        feedback = 0.0

    noise = rng.gauss(0, step_size)

    return x_t + feedback + noise

def variational_trend_feedback(
    x_t: float,
    t: int,
    path: list,
    rng,
    step_size: float,
    memory_strength: float = 0.02,
    trend_strength: float = 0.01,
    vol_factor: float = 0.05
) -> float:
    """
    Variationaler Übergang mit Pfad-Rückkopplung und Trendverstärkung:
    
    - Rückkopplung an den Mittelwert des bisherigen Pfads
    - Verstärkung des bestehenden Trends (lineare Steigung des Pfads)
    - Additive stochastische Komponente, leicht abhängig von der bisherigen Pfad-Volatilität
    """

    n = len(path)
    
    # Mittelwert-Rückkopplung
    if n > 1:
        path_mean = sum(path) / n
        feedback = -memory_strength * (x_t - path_mean)
    else:
        feedback = 0.0

    # Trendverstärkung
    if n > 2:
        recent_trend = path[-1] - path[-2]
        trend = trend_strength * recent_trend
    else:
        trend = 0.0

    # Pfadabhängige Volatilität (extremere Abweichungen führen zu größeren Zufallsschritten)
    if n > 1:
        deviations = [abs(x - path_mean) for x in path]
        vol = step_size + vol_factor * max(deviations)
    else:
        vol = step_size

    noise = rng.gauss(0, vol)

    return x_t + feedback + trend + noise

#=========================================================================
''' 
TYP 3: 

'''
def adaptive_random_walk(
    x_t: float,
    t: int,
    path: list,
    adaptive_state: dict,
    rng,
    step_size: float = 1.0
) -> tuple[float, dict]:
    
    # Initialisierung des adaptiven Zustands
    if not adaptive_state:
        adaptive_state = {
            "step_size": step_size,
            "n_steps": 0
        }

    # stochastischer Schritt (noch völlig klassisch)
    step = rng.choice([-adaptive_state["step_size"], adaptive_state["step_size"]])
    x_next = x_t + step

    # triviale Adaption: Zähler erhöhen (reine Platzhalter-Logik)
    adaptive_state["n_steps"] += 1

    return x_next, adaptive_state

def adaptive_volatility_walk(
    x_t: float,
    t: int,
    path: list,
    adaptive_state: dict,
    rng,
    step_size: float = 1.0  # Step Size ebenfalls randomisieren!
) -> tuple[float, dict]:

    # Initialisierung
    if not adaptive_state:
        adaptive_state = {
            "step_size": step_size,
            "ema_vol": 0.0,      # exponentieller Volatilitätsschätzer
            "alpha": 0.2         # Adaptionsrate
        }

    # stochastischer Schritt
    step = rng.choice([-adaptive_state["step_size"],
                        adaptive_state["step_size"]])
    x_next = x_t + step

    # beobachtete lokale "Volatilität"
    realized_vol = abs(step)

    # exponentiell gleitender Mittelwert
    adaptive_state["ema_vol"] = (
        adaptive_state["alpha"] * realized_vol
        + (1 - adaptive_state["alpha"]) * adaptive_state["ema_vol"]
    )

    # adaptive Regel: hohe Volatilität → kleinere Schritte
    adaptive_state["step_size"] = step_size / (1 + adaptive_state["ema_vol"])

    return x_next, adaptive_state
