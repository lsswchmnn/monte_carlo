import numpy as np
from typing import List
#=========================================================================
def calculate_ergodicity(paths: List[List[float]],      # Daten des stochastischen Prozesses als Rohmaterial
                         observable = lambda x: x,      # Die Observable. Ergodizität ist nicht absolut
                         tail_fraction: float = 0.5     # Ergodizität ist asymptotisch; der Startzustand wird also irgnoiert (als näherung)
                         ) -> dict:   
    
    data = np.array(paths)              # Daten formalisieren
    T = data.shape[1]                   # Wie viele Zeitabschnitte hat ein Pfad?
    cut = int((1- tail_fraction) * T)   # Startbedingungen rausfiltern
    obs_data = observable(data)         # Observable auf jedes einzelne Zustandereignis anwenden
    tail_data = obs_data[:, cut:]       # Fokus auf letzte Zeitabschnitte aller Pfade
    
    # Für jeden Pfad Zeitdurchschnitt anwenden (langfristige Erfahrung eines einzelnen Systems)
    time_means = np.array([
        time_average(path) for path in tail_data
    ])

    # Durchschnitt vieler Pfade in Zeitraum
    ensemble_mean = ensemble_average(tail_data)

    # Grobe Heuristik - ergodisch oder nicht?
    threshold = 0.10  # 5 % relative Abweichung als Faustregel
    ergodic = (time_means.std() / abs(ensemble_mean)) < threshold

    # Rückgabe
    result = {
        "ensemble_mean": ensemble_mean,         # Durchschnitt aller Zustände aller Pfade im asymptotischen Bereich
        "time_mean_mean": time_means.mean(),    # Mittel der Zeitmittel
        "time_mean_std": time_means.std(),      # Streuung der Zeitmittel
        "time_means": time_means,               # Zeitmittel einzelner Pfade
        "ergodic_heuristic": ergodic            # bool
    }
    return result


def time_average(path) -> float:
    return path.mean()

def ensemble_average(data: np.ndarray) -> float:
    return data.mean()