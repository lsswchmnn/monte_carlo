#=========================================================================
# TYP 2: 
# Pfadabhängige, nicht lokale Prozesse. Darf mehr kontext als nur den 
# aktuellen Zustand nutzen, nämlich gesamten bisherigen Verlauf und die Zeit.
#=========================================================================
# Minimaler variationaler Übergang
def variational_baseline(
    x_t: float,
    t: int,
    path: list,
    rng,
    step_size: float,
    memory_strength: float = 0.01
) -> float:
    '''
    Minimaler variationaler Übergang:
    - schwache Rückkopplung an den bisherigen Pfadmittelwert
    - additive stochastische Komponente
    '''

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
    '''
    Variationaler Übergang mit Pfad-Rückkopplung und Trendverstärkung:
    
    - Rückkopplung an den Mittelwert des bisherigen Pfads
    - Verstärkung des bestehenden Trends (lineare Steigung des Pfads)
    - Additive stochastische Komponente, leicht abhängig von der bisherigen Pfad-Volatilität
    '''

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