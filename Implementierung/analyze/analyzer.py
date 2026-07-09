from   analyze.analyze_results import *
from   typing                  import List
import numpy                   as     np
#=========================================================================
# Klasse für Operationen auf fertige Analyseergebnisse.
# Aktuell: Ergodizität.
#=========================================================================
class Analyzer:

#-------------------------------------------------------------------------
# Allgemein

    @staticmethod
    def time_average(path) -> float:
        return path.mean()

    @staticmethod
    def ensemble_average(data: np.ndarray) -> float:
        return data.mean()

#-------------------------------------------------------------------------
# Ergodizität

    def calculate_ergodicity(self, paths: List[List[float]],
                            observable = lambda x: x,
                            tail_fraction: float = 0.5) -> ErgodicityResult:   

        data = np.array(paths)
        T = data.shape[1]
        cut = int((1 - tail_fraction) * T)
        obs_data = observable(data)
        tail_data = obs_data[:, cut:]

        time_means = []

        for i, path in enumerate(tail_data, 1):
            time_means.append(self.time_average(path))

        time_means = np.array(time_means)
        ensemble_mean = self.ensemble_average(tail_data)
        threshold = 0.10
        ergodic = (time_means.std() / abs(ensemble_mean)) < threshold

        return ErgodicityResult(
            ensemble_mean=ensemble_mean,
            time_mean_mean=time_means.mean(),
            time_mean_std=time_means.std(),
            time_means=time_means,
            ergodic_heuristic=ergodic
        )
