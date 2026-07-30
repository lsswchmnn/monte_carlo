import numpy as np
#=========================================================================
# TYP 1 (ND): Markov-Prozesse im n-dimensionalen Raum.
# Zustand x_t ist np.ndarray der Form:
#   (n_dimensions,)         — skalarer Aufruf (variational/adaptive)
#   (n_paths, n_dimensions) — vektorisierter Aufruf (_run_markov)
#
# Parallel zu transitions_1d/markov.py — bewusst keine gemeinsame
# Abstraktion, da Vektor-Arithmetik sich grundlegend von Skalar-Arithmetik
# unterscheidet.
#=========================================================================
# Hilfsfunktionen (privat)

def _levy_stable_sample_nd(rng, alpha: float, size=None):
    '''Chambers-Mallows-Stuck für skalare Schrittlängen (immer positiv).'''
    phi = rng.uniform(-np.pi / 2, np.pi / 2, size=size)
    w   = rng.exponential(1.0, size=size)

    if alpha == 1.0:
        return np.abs(np.tan(phi))

    term1 = np.sin(alpha * phi) / np.cos(phi) ** (1.0 / alpha)
    term2 = (np.cos((alpha - 1.0) * phi) / w) ** ((1.0 - alpha) / alpha)
    return np.abs(term1 * term2)

def _uniform_direction(rng, n_paths, n_dimensions):
    '''
    Gleichmäßig verteilte Richtungsvektoren auf der n-dim Einheitssphäre.
    Muller (1959): normierte Normalvektoren sind gleichmäßig auf der Sphäre verteilt.
    '''
    dirs  = rng.normal(size=(n_paths, n_dimensions))
    norms = np.linalg.norm(dirs, axis=1, keepdims=True)
    return dirs / norms

#-------------------------------------------------------------------------
# Übergangsfunktionen

def random_walk_nd(x_t: np.ndarray, rng, step_size: float = 1.0,
                   drift: float = 0.0, mode: str = "isotropic") -> np.ndarray:
    '''
    Zufälliger Schritt fester Länge step_size, Richtung abhängig von mode:
      'isotropic'    -> gleichverteilt zufällige Richtung im Raum (Muller 1959),
                         keine Gitterstruktur.
      'axis_aligned' -> klassischer Gitter-Random-Walk: Schritt entlang einer
                         zufällig gewählten Achse (N-dim. Analogon des 1D-Walks).
    Optional mit konstantem Drift entlang jeder Achse.
    '''
    if x_t.ndim == 2:
        n_paths, n_dimensions = x_t.shape
        if mode == "axis_aligned":
            directions = rng.integers(n_dimensions, size=n_paths)
            signs      = rng.choice(np.array([-1.0, 1.0]), size=n_paths)
            steps      = np.zeros((n_paths, n_dimensions))
            steps[np.arange(n_paths), directions] = signs * step_size
        else:
            directions = _uniform_direction(rng, n_paths, n_dimensions)
            steps = directions * step_size
    else:
        n_dimensions = len(x_t)
        if mode == "axis_aligned":
            direction = int(rng.integers(n_dimensions))
            sign      = rng.choice(np.array([-1.0, 1.0]))
            steps     = np.zeros(n_dimensions)
            steps[direction] = sign * step_size
        else:
            direction = rng.normal(size=n_dimensions)
            direction = direction / np.linalg.norm(direction)
            steps = direction * step_size

    return x_t + steps + drift

def mean_reverting_nd(x_t: np.ndarray, rng, step_size: float = 1.0,
                      strength: float = 0.1, mean: float = 0.0) -> np.ndarray:
    '''
    Zieht den Zustand mit Stärke strength zum Zielpunkt mean.
    mean ist ein Skalar (wird auf alle Dimensionen angewendet) oder
    kann als Vektor übergeben werden.
    Rauschen gleichmäßig in alle Richtungen.
    '''
    if x_t.ndim == 2:
        n_paths, n_dimensions = x_t.shape
        pull  = -strength * (x_t - mean)
        noise = rng.normal(0, step_size, size=(n_paths, n_dimensions))
    else:
        n_dimensions = len(x_t)
        pull  = -strength * (x_t - mean)
        noise = rng.normal(0, step_size, size=n_dimensions)

    return x_t + pull + noise

def state_dependent_vol_nd(x_t: np.ndarray, rng, step_size: float = 0.5,
                           factor: float = 0.08) -> np.ndarray:
    '''
    Volatilität wächst mit dem Abstand zum Ursprung (np.linalg.norm).
    Extremere Positionen → größere Schritte in alle Richtungen.
    '''
    if x_t.ndim == 2:
        n_paths, n_dimensions = x_t.shape
        norms     = np.linalg.norm(x_t, axis=1, keepdims=True)  # (n_paths, 1)
        vol       = step_size + factor * norms
        noise     = rng.normal(0, 1, size=(n_paths, n_dimensions)) * vol
    else:
        n_dimensions = len(x_t)
        norm      = np.linalg.norm(x_t)
        vol       = step_size + factor * norm
        noise     = rng.normal(0, vol, size=n_dimensions)

    return x_t + noise

def absorbing_barrier_nd(x_t: np.ndarray, rng, step_size: float = 1.0,
                         barrier: float = -10.0,
                         barrier_type: str = "absorbing") -> np.ndarray:
    '''
    Hyperebene-Barriere orthogonal zur ersten Dimension bei x[0] <= barrier.
    'absorbing'  → Pfad friert ein wenn x[0] die Barriere kreuzt
    'reflecting' → Pfad wird zurückgeworfen
    '''
    if x_t.ndim == 2:
        n_paths, n_dimensions = x_t.shape
        directions = rng.integers(n_dimensions, size=n_paths)
        signs      = rng.choice(np.array([-1.0, 1.0]), size=n_paths)
        steps      = np.zeros((n_paths, n_dimensions))
        steps[np.arange(n_paths), directions] = signs * step_size
        x_next     = x_t + steps

        crossed = x_next[:, 0] <= barrier   # prüft erste Dimension
        if barrier_type == "reflecting":
            x_next[crossed, 0] = 2 * barrier - x_next[crossed, 0]
        else:
            x_next[crossed, 0] = barrier
        return x_next
    else:
        n_dimensions = len(x_t)
        direction    = int(rng.integers(n_dimensions))
        sign         = rng.choice(np.array([-1.0, 1.0]))
        steps        = np.zeros(n_dimensions)
        steps[direction] = sign * step_size
        x_next = x_t + steps

        if x_next[0] <= barrier:
            if barrier_type == "reflecting":
                x_next[0] = 2 * barrier - x_next[0]
            else:
                x_next[0] = barrier
        return x_next

def regime_switch_nd(x_t: np.ndarray, rng, step_size: float = 1.0,
                     p_switch: float = 0.1, vol_factor: float = 5.0) -> np.ndarray:
    '''
    Mit Wahrscheinlichkeit p_switch wechselt der Prozess in ein hochvolatiles
    Regime (vol_factor x step_size in alle Richtungen), sonst normaler Schritt.
    '''
    if x_t.ndim == 2:
        n_paths, n_dimensions = x_t.shape
        normal   = rng.normal(0, step_size,              size=(n_paths, n_dimensions))
        high_vol = rng.normal(0, step_size * vol_factor, size=(n_paths, n_dimensions))
        is_high  = rng.random(size=(n_paths, 1)) < p_switch   # (n_paths, 1) → broadcast
        noise    = np.where(is_high, high_vol, normal)
    else:
        n_dimensions = len(x_t)
        if rng.random() < p_switch:
            noise = rng.normal(0, step_size * vol_factor, size=n_dimensions)
        else:
            noise = rng.normal(0, step_size, size=n_dimensions)

    return x_t + noise

def levy_flight_nd(x_t: np.ndarray, rng, step_size: float = 1.0,
                   alpha: float = 1.5) -> np.ndarray:
    '''
    Lévy-Flight im n-dimensionalen Raum.
    Schrittlänge aus stabiler Verteilung (Chambers-Mallows-Stuck),
    Richtung gleichmäßig auf der n-dim Einheitssphäre (Muller 1959).
    '''
    if x_t.ndim == 2:
        n_paths, n_dimensions = x_t.shape
        lengths    = _levy_stable_sample_nd(rng, alpha, size=n_paths) * step_size
        directions = _uniform_direction(rng, n_paths, n_dimensions)
        steps      = directions * lengths[:, np.newaxis]
    else:
        n_dimensions = len(x_t)
        length     = _levy_stable_sample_nd(rng, alpha) * step_size
        direction  = rng.normal(size=n_dimensions)
        direction  = direction / np.linalg.norm(direction)
        steps      = direction * length

    return x_t + steps