from   analyze.results import *
from   typing          import List
import numpy           as     np
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

#-------------------------------------------------------------------------
# Autokorrelation

    def calculate_autocorrelation(self, paths: List[List[float]],
                                   max_lag: int | None = None) -> AutoCorrelationResult:
        '''
        Berechnet die Autokorrelationsfunktion (ACF) pro Pfad und mittelt
        über das Ensemble. max_lag default: min(40, T-1) (Faustregel).
        '''
        data = np.array(paths)
        n_paths, T = data.shape

        if max_lag is None:
            max_lag = min(40, T - 1)
        max_lag = min(max_lag, T - 1)

        # ACF für jeden Pfad berechnen
        acf_matrix = np.array([
            self._autocorrelation_single(path, max_lag) for path in data
        ])  # shape (n_paths, max_lag+1)

        acf_mean = acf_matrix.mean(axis=0)
        acf_std  = acf_matrix.std(axis=0)

        confidence_bound  = 1.96 / np.sqrt(T)               # weißes Rauschen, 95%
        significant_lags  = np.abs(acf_mean) > confidence_bound
        significant_lags[0] = False                          # Lag 0 ist trivial 1.0

        return AutoCorrelationResult(
            lags=np.arange(max_lag + 1),
            acf_mean=acf_mean,
            acf_std=acf_std,
            confidence_bound=confidence_bound,
            significant_lags=significant_lags,
        )

    @staticmethod
    def _autocorrelation_single(path: np.ndarray, max_lag: int) -> np.ndarray:
        '''
        ACF eines einzelnen Pfads für Lags 0..max_lag, normalisiert über
        die Varianz des gesamten Pfads (Standard-Zeitreihen-ACF).
        '''
        x   = path - path.mean()
        n   = len(x)
        var = np.dot(x, x) / n

        if var == 0:
            return np.zeros(max_lag + 1)

        acf = np.empty(max_lag + 1)
        for lag in range(max_lag + 1):
            acf[lag] = 1.0 if lag == 0 else np.dot(x[:n - lag], x[lag:]) / (n * var)
        return acf
