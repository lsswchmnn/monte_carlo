import numpy as np
#=========================================================================
# TYP 2: 
# Pfadabhängige, nicht lokale Prozesse. Darf mehr kontext als nur den 
# aktuellen Zustand nutzen, nämlich gesamten bisherigen Verlauf und die Zeit.
#=========================================================================
# Minimaler variationaler Übergang

def variational_baseline(
    x_t: "np.ndarray",
    t: int,
    path: "np.ndarray",
    rng,
    step_size: float,
    memory_strength: float = 0.01
) -> "np.ndarray":
    '''
    Minimaler variationaler Übergang, vektorisiert über alle Pfade:
    - schwache Rückkopplung an den bisherigen (pfadeigenen) Mittelwert
    - additive stochastische Komponente

    Nutzt eine einfache Vektor-Mittelwertbildung über die Zeitachse
    (path.mean(axis=0)) statt sum(path)/len(path) pro Pfad einzeln —
    identischer Wert, aber in einem Schritt für alle Pfade berechnet
    statt in einer Python-Schleife neu aufsummiert.
    '''
    n = path.shape[0]

    if n > 1:
        path_mean = path.mean(axis=0)
        feedback = -memory_strength * (x_t - path_mean)
    else:
        feedback = 0.0

    noise = rng.normal(0, step_size, size=x_t.shape)

    return x_t + feedback + noise

def variational_trend_feedback(
    x_t: "np.ndarray",
    t: int,
    path: "np.ndarray",
    rng,
    step_size: float,
    memory_strength: float = 0.02,
    trend_strength: float = 0.01,
    vol_factor: float = 0.05
) -> "np.ndarray":
    '''
    Variationaler Übergang mit Pfad-Rückkopplung und Trendverstärkung,
    vektorisiert über alle Pfade:
    
    - Rückkopplung an den Mittelwert des bisherigen Pfads (pro Pfad)
    - Verstärkung des bestehenden Trends (letzter Schritt, pro Pfad)
    - Additive stochastische Komponente, abhängig von der bisherigen
      Pfad-Volatilität (max. Abweichung vom Pfadmittel, pro Pfad)
    '''
    n = path.shape[0]

    # Mittelwert-Rückkopplung
    if n > 1:
        path_mean = path.mean(axis=0)
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

    # Pfadabhängige Volatilität (extremere Abweichungen -> größere Zufallsschritte)
    if n > 1:
        deviations = np.abs(path - path_mean)
        vol = step_size + vol_factor * deviations.max(axis=0)
    else:
        vol = step_size

    noise = rng.normal(0, vol, size=x_t.shape)

    return x_t + feedback + trend + noise
