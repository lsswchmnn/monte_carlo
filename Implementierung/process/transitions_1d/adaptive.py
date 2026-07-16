import numpy as np
#=========================================================================
# TYP 3: 
# ...
#=========================================================================

def adaptive_random_walk(
    x_t: np.ndarray,
    t: int,
    path: np.ndarray,
    adaptive_state: dict,
    rng,
    step_size: float = 1.0
) -> tuple[np.ndarray, dict]:
    '''
    Vektorisiert über alle Pfade: zufälliger Schritt +-step_size pro Pfad,
    triviale Adaption über Schrittzähler (reine Platzhalter-Logik).
    '''
    n_paths = len(x_t)

    if not adaptive_state:
        adaptive_state = {
            "step_size": np.full(n_paths, step_size),
            "n_steps": np.zeros(n_paths, dtype=int),
        }

    signs = rng.choice(np.array([-1.0, 1.0]), size=n_paths)
    step  = signs * adaptive_state["step_size"]
    x_next = x_t + step

    adaptive_state["n_steps"] += 1

    return x_next, adaptive_state

def adaptive_volatility_walk(
    x_t: np.ndarray,
    t: int,
    path: np.ndarray,
    adaptive_state: dict,
    rng,
    step_size: float = 1.0  # Basis-Schrittweite, bleibt über die Simulation konstant
) -> tuple[np.ndarray, dict]:
    '''
    Vektorisiert über alle Pfade: Schrittweite wird pro Pfad endogen an die
    zuletzt beobachtete Volatilität angepasst (negative Rückkopplung).
    Pfadabhängig und nicht-ergodisch im klassischen Sinne.
    '''
    n_paths = len(x_t)

    if not adaptive_state:
        adaptive_state = {
            "step_size": np.full(n_paths, step_size),
            "ema_vol":   np.zeros(n_paths),
            "alpha":     0.2,
        }

    signs = rng.choice(np.array([-1.0, 1.0]), size=n_paths)
    step  = signs * adaptive_state["step_size"]
    x_next = x_t + step

    realized_vol = np.abs(step)
    alpha = adaptive_state["alpha"]
    adaptive_state["ema_vol"]    = alpha * realized_vol + (1 - alpha) * adaptive_state["ema_vol"]
    adaptive_state["step_size"]  = step_size / (1 + adaptive_state["ema_vol"])

    return x_next, adaptive_state