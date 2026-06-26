import numpy as np
from typing import List
from utils import printProgressBar, clear_cli
#=========================================================================
'''
Misst ergodisches Verhalten im (begrenzten) Rahmen dieser Simulation. Man kann 
hiermit prinzipiell keine Aussage über die Ergodizität des Systems treffen, da 
Ergodizität eine Eigenschaft der Prozesse ohne Einschränkung von t ist (die es
in einer solchen Simulation zwangsläufig geben muss). Innerhalb dieser Einschränkungen
sind die Methoden aber (heuristisch) brauchbar.
'''
#=========================================================================
def calculate_ergodicity(paths: List[List[float]],
                         observable = lambda x: x,
                         tail_fraction: float = 0.5) -> dict:   
    
    data = np.array(paths)
    T = data.shape[1]
    cut = int((1 - tail_fraction) * T)
    obs_data = observable(data)
    tail_data = obs_data[:, cut:]
    
    time_means = []
    total = tail_data.shape[0]
    
    clear_cli()
    
    for i, path in enumerate(tail_data, 1):
        time_means.append(time_average(path))
        printProgressBar(i, total, prefix='Calculating Ergodicity:', suffix='Finished', length=50)
    
    time_means = np.array(time_means)
    ensemble_mean = ensemble_average(tail_data)
    threshold = 0.10
    ergodic = (time_means.std() / abs(ensemble_mean)) < threshold

    return {
        "ensemble_mean": ensemble_mean,
        "time_mean_mean": time_means.mean(),
        "time_mean_std": time_means.std(),
        "time_means": time_means,
        "ergodic_heuristic": ergodic
    }

def time_average(path) -> float:
    return path.mean()

def ensemble_average(data: np.ndarray) -> float:
    return data.mean()