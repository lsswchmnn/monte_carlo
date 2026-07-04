import numpy as np
#=========================================================================
# TYP 1: 
# Lokale, stochastische Markov-Prozesse in 1D. Zeitdiskret und additiv.
#=========================================================================
# Hilfsfunktionen

def _levy_stable_sample(rng, alpha: float, size=None):
    '''
    Chambers-Mallows-Stuck (1976): Samples aus symmetrischer stabiler Verteilung.
    alpha in (0, 2]: Stabilitätsindex.
      alpha = 2.0 → Gauß (klassischer Random Walk)
      alpha = 1.5 → typischer Lévy-Flight
      alpha → 0   → zunehmend extremere Sprünge
    '''
    phi = rng.uniform(-np.pi / 2, np.pi / 2, size=size)
    w   = rng.exponential(1.0, size=size)
 
    if alpha == 1.0:
        return np.tan(phi)
 
    term1 = np.sin(alpha * phi) / np.cos(phi) ** (1.0 / alpha)
    term2 = (np.cos((alpha - 1.0) * phi) / w) ** ((1.0 - alpha) / alpha)
    return term1 * term2

def _size(x_t) -> int | None:
    '''Gibt die Anzahl der Pfade zurück, oder None für skalaren Aufruf.'''
    return len(x_t) if isinstance(x_t, np.ndarray) else None

#=========================================================================
# Markov-Übergänge in 1D

def random_walk(x_t, rng, step_size: float = 1.0, 
                drift: float = 0.0):
    '''Zufälliger Schritt +-step_size, optional mit Drift (drift != 0).'''
    steps = rng.choice(np.array([-step_size, step_size]), size=_size(x_t))
    return x_t + steps + drift

def mean_reverting(x_t, rng, step_size: float = 1.0,
                   strength: float = 0.1, mean: float = 0.5):
    '''Zieht den Zustand mit Stärke strength zum Mittelwert mean zurück.'''
    pull  = -strength * (x_t - mean)
    noise = rng.normal(0, step_size, size=_size(x_t))
    return x_t + pull + noise

def state_dependent_vol(x_t, rng, step_size: float = 0.5, 
                        factor: float = 0.08):
    '''Volatilität wächst mit Betrag des Zustands, stärkere Ausreißer.'''
    step  = step_size + factor * np.abs(x_t)
    noise = rng.normal(0, step)
    return x_t + noise

def fat_tail_walk(x_t, rng, step_size: float = 1.0, 
                  p_tail: float = 0.02, tail_factor: float = 20.0):
    '''Mit Wahrscheinlichkeit p_tail extremer, sonst normaler Schritt.'''
    n = _size(x_t)
    if n is not None:
        noise  = rng.normal(0, step_size, size=n)
        fat    = rng.normal(0, step_size * tail_factor, size=n)
        is_fat = rng.random(size=n) < p_tail
        noise  = np.where(is_fat, fat, noise)
    else:
        noise = (rng.normal(0, step_size * tail_factor)
                 if rng.random() < p_tail
                 else rng.normal(0, step_size))
    return x_t + noise

def absorbing_barrier(x_t, rng, step_size: float = 1.0,
                      barrier: float = -10.0,
                      barrier_type: str = "absorbing"):
    '''
    Barriere bei barrier. Zwei Typen:
      'absorbing'  → Zustand friert bei Barriere ein
      'reflecting' → Zustand wird zurückgeworfen
    '''
    n = _size(x_t)
    if n is not None:
        noise  = rng.choice(np.array([-step_size, step_size]), size=n)
        x_next = x_t + noise
        if barrier_type == "reflecting":
            x_next = np.where(x_next <= barrier, 2 * barrier - x_next, x_next)
        else:
            x_next = np.where(x_next <= barrier, barrier, x_next)
        return x_next
    else:
        noise  = rng.choice(np.array([-step_size, step_size]))
        x_next = x_t + noise
        if x_next <= barrier:
            return 2 * barrier - x_next if barrier_type == "reflecting" else barrier
        return x_next

def regime_switch(x_t, rng, step_size: float = 1.0, 
                  p_switch: float = 0.1, vol_factor: float = 5.0):
    '''Wechselt mit Wahrscheinlichkeit p_switch zwischen normaler und hoher Volatilität.'''
    n = _size(x_t)
    if n is not None:
        normal   = rng.normal(0, step_size,              size=n)
        high_vol = rng.normal(0, step_size * vol_factor, size=n)
        is_high  = rng.random(size=n) < p_switch
        noise    = np.where(is_high, high_vol, normal)
    else:
        noise = (rng.normal(0, step_size * vol_factor)
                 if rng.random() < p_switch
                 else rng.normal(0, step_size))
    return x_t + noise

def levy_flight(x_t, rng, step_size: float = 1.0, 
                alpha: float = 1.5):
    '''
    Lévy-Flight in 1D.
    Schrittlänge folgt einer stabilen Verteilung mit Index alpha,
    Richtung ist zufällig ±1.
 
    alpha in (0, 2]:
      ~1.5  klassischer Lévy-Flight mit seltenen Riesensprüngen
      ~1.0  Cauchy-Verteilung, sehr schwere Schwänze
      ~2.0  nähert sich dem Gauß-Random-Walk an
    '''
    n     = _size(x_t)
    steps = _levy_stable_sample(rng, alpha, size=n)
    signs = rng.choice(np.array([-1.0, 1.0]), size=n)
    return x_t + signs * np.abs(steps) * step_size