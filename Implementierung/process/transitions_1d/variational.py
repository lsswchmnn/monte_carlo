import numpy as np
#=========================================================================
# TYP 2: 
# Pfadabhängige, nicht lokale Prozesse. Darf mehr kontext als nur den 
# aktuellen Zustand nutzen, nämlich gesamten bisherigen Verlauf und die Zeit.
#=========================================================================

def variational_baseline(
    x_t: np.ndarray,
    t: int,
    path: np.ndarray,
    aux_state: dict,
    rng,
    step_size: float,
    memory_strength: float = 0.01
) -> tuple[np.ndarray, dict]:
    '''
    Minimaler variationaler Übergang, vektorisiert über alle Pfade:
    - schwache Rückkopplung an den bisherigen (pfadeigenen) Mittelwert,
      berechnet über eine laufende Summe (O(1) pro Schritt)
    - additive stochastische Komponente
    '''
    if not aux_state:
        aux_state = {"running_sum": np.zeros_like(x_t)}

    n = t + 1
    aux_state["running_sum"] = aux_state["running_sum"] + x_t

    if n > 1:
        path_mean = aux_state["running_sum"] / n
        feedback = -memory_strength * (x_t - path_mean)
    else:
        feedback = 0.0

    noise = rng.normal(0, step_size, size=x_t.shape)

    return x_t + feedback + noise, aux_state

def variational_trend_feedback(
    x_t: np.ndarray,
    t: int,
    path: np.ndarray,
    aux_state: dict,
    rng,
    step_size: float,
    memory_strength: float = 0.02,
    trend_strength: float = 0.01,
    vol_factor: float = 0.05
) -> tuple[np.ndarray, dict]:
    '''
    Variationaler Übergang mit Pfad-Rückkopplung und Trendverstärkung,
    vektorisiert über alle Pfade:

    - Rückkopplung an den Mittelwert des bisherigen Pfads, über eine
      laufende Summe (O(1) pro Schritt)
    - Verstärkung des bestehenden Trends (letzter Schritt, pro Pfad)
    - Additive stochastische Komponente, abhängig von der bisherigen
      Pfad-Volatilität (max. Abweichung vom Pfadmittel, pro Pfad)

    Die Volatilitätsberechnung bleibt bewusst O(t) pro Schritt: sie
    braucht das Maximum der Abweichung ALLER bisherigen Werte vom
    AKTUELLEN (sich jeden Schritt ändernden) Mittelwert -- das lässt
    sich ohne Bedeutungsänderung nicht laufend mitführen, da sich die
    Referenz für "Abweichung" bei jedem Schritt verschiebt.
    '''
    if not aux_state:
        aux_state = {"running_sum": np.zeros_like(x_t)}

    n = t + 1
    aux_state["running_sum"] = aux_state["running_sum"] + x_t

    # Mittelwert-Rückkopplung (O(1) via laufender Summe)
    if n > 1:
        path_mean = aux_state["running_sum"] / n
        feedback = -memory_strength * (x_t - path_mean)
    else:
        path_mean = x_t
        feedback = 0.0

    # Trendverstärkung
    if n > 2:
        recent_trend = path[-1] - path[-2]
        trend = trend_strength * recent_trend
    else:
        trend = 0.0

    # Pfadabhängige Volatilität (weiterhin O(t) pro Schritt, siehe Docstring)
    if n > 1:
        deviations = np.abs(path - path_mean)
        vol = step_size + vol_factor * deviations.max(axis=0)
    else:
        vol = step_size

    noise = rng.normal(0, vol, size=x_t.shape)

    return x_t + feedback + trend + noise, aux_state
