import numpy as np
#=========================================================================
# TYP 3: 
# ...
#=========================================================================
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
    step = rng.choice(np.array([-adaptive_state["step_size"], adaptive_state["step_size"]]))
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
    step = rng.choice(np.array([-adaptive_state["step_size"],
                                adaptive_state["step_size"]]))
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
