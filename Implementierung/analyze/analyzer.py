from   analyze.results import *
from   typing          import List
import numpy           as     np
#=========================================================================
# Klasse für Operationen auf fertige Analyseergebnisse.
# Aktuell: Ergodizität, Autokorrelation, Hurs-Exponent.
#=========================================================================
class Analyzer:

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

    @staticmethod
    def time_average(path) -> float:
        return path.mean()

    @staticmethod
    def ensemble_average(data: np.ndarray) -> float:
        return data.mean()

#-------------------------------------------------------------------------
# Autokorrelation (ACF)

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
            self._acf_single(path, max_lag) for path in data
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
    def _acf_single(path: np.ndarray, max_lag: int) -> np.ndarray:
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

#-------------------------------------------------------------------------
# Hurst-Exponent (DFA)

    def calculate_hurst_exponent(self, paths: List[List[float]],
                                  on_increments: bool = True,
                                  min_window: int = 4,
                                  max_window: int | None = None,
                                  n_scales: int = 20) -> HurstExponentResult:
        '''
        Berechnet den Hurst-Exponenten via Detrended Fluctuation Analysis (DFA).

        Standardmäßig auf den Zuwächsen (Differenzen) jedes Pfads, analog zur
        üblichen Konvention bei Positions-/Preisreihen: H=0.5 entspricht einem
        reinen Random Walk (unkorrelierte Schritte), H>0.5 persistentem
        (trendfolgendem), H<0.5 anti-persistentem (mean-reverting) Verhalten.
        Bei on_increments=False wird DFA direkt auf den Leveln berechnet.
        '''
        data = np.array(paths)
        series = np.diff(data, axis=1) if on_increments else data
        n_paths = series.shape[0]

        hurst_per_path      = np.empty(n_paths)
        r_squared_per_path  = np.empty(n_paths)
        fluct_matrix         = []
        scales_ref            = None

        for i, s in enumerate(series):
            scales, F, H, r2 = self._dfa_single(s, min_window, max_window, n_scales)
            hurst_per_path[i]     = H
            r_squared_per_path[i] = r2
            fluct_matrix.append(F)
            scales_ref = scales   # identisch für alle Pfade (gleiche Länge)

        fluct_matrix = np.array(fluct_matrix)

        return HurstExponentResult(
            scales=scales_ref,
            fluctuation_mean=fluct_matrix.mean(axis=0),
            hurst_mean=hurst_per_path.mean(),
            hurst_std=hurst_per_path.std(),
            hurst_per_path=hurst_per_path,
            r_squared_mean=r_squared_per_path.mean(),
            on_increments=on_increments,
        )

    @staticmethod
    def _dfa_single(series: np.ndarray, min_window: int, max_window: int | None,
                     n_scales: int) -> tuple:
        '''
        DFA (Ordnung 1, linearer lokaler Trend) für eine einzelne Reihe.
        Gibt (scales, F(s), H, R²) zurück.
        '''
        n = len(series)
        if max_window is None:
            max_window = n // 4
        max_window = max(max_window, min_window + 1)

        # Log-verteilte Fensterskalen, Duplikate nach int-Rundung entfernt
        raw_scales = np.logspace(np.log10(min_window), np.log10(max_window), n_scales)
        scales = np.unique(raw_scales.astype(int))
        scales = scales[scales >= min_window]

        # Integriertes Profil (kumulierte Summe der demeanten Reihe)
        y = np.cumsum(series - series.mean())

        fluctuations = np.empty(len(scales))
        for idx, s in enumerate(scales):
            n_windows = n // s
            trimmed = y[: n_windows * s].reshape(n_windows, s)

            x_local = np.arange(s)
            residual_sq_sum = 0.0
            for window in trimmed:
                coeffs = np.polyfit(x_local, window, deg=1)
                trend = np.polyval(coeffs, x_local)
                residual_sq_sum += np.sum((window - trend) ** 2)

            fluctuations[idx] = np.sqrt(residual_sq_sum / (n_windows * s))

        # Log-Log-Regression: log F(s) = H * log(s) + c
        log_s = np.log(scales)
        log_f = np.log(fluctuations)
        H, c = np.polyfit(log_s, log_f, deg=1)

        # Bestimmtheitsmaß R² der Regression (Anpassungsgüte)
        predicted = H * log_s + c
        ss_res = np.sum((log_f - predicted) ** 2)
        ss_tot = np.sum((log_f - log_f.mean()) ** 2)
        r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0

        return scales, fluctuations, H, r_squared

#-------------------------------------------------------------------------
# Varianzwachstum

    def calculate_variance_growth(self, paths: List[List[float]],
                                   min_t: int = 2,
                                   max_t: int | None = None,
                                   n_points: int = 30) -> VarianceGrowthResult:
        '''
        Untersucht, wie die Ensemble-Varianz der Verschiebung (x_t - x_0) mit
        der Zeit wächst. Fit von log(Var(t)) gegen log(t) liefert den
        Wachstumsexponenten gamma:
          gamma ≈ 1  -> normale (Fick'sche) Diffusion, z.B. Random Walk
          gamma < 1  -> subdiffusiv (Sättigung), z.B. Mean Reversion
          gamma > 1  -> superdiffusiv, z.B. Lévy Flight (seltene große Sprünge)
        Verwandt zum Hurst-Exponenten über gamma ≈ 2H bei selbstähnlichen Prozessen.
        '''
        data = np.array(paths)
        n_paths, T = data.shape

        displacement  = data - data[:, [0]]             # x_t - x_0 pro Pfad
        variance_full = displacement.var(axis=0)         # Ensemble-Varianz pro Zeitschritt

        if max_t is None:
            max_t = T - 1
        max_t = min(max_t, T - 1)

        # Log-verteilte Zeitpunkte (t=0 ausgeschlossen wegen log(0))
        raw_times = np.logspace(np.log10(min_t), np.log10(max_t), n_points)
        times = np.unique(raw_times.astype(int))
        times = times[times >= min_t]
        variance = variance_full[times]

        # Schutz gegen log(0), falls Varianz an einem Punkt exakt 0 ist
        valid        = variance > 0
        times_fit    = times[valid]
        variance_fit = variance[valid]

        log_t = np.log(times_fit)
        log_v = np.log(variance_fit)
        gamma, c = np.polyfit(log_t, log_v, deg=1)

        predicted = gamma * log_t + c
        ss_res = np.sum((log_v - predicted) ** 2)
        ss_tot = np.sum((log_v - log_v.mean()) ** 2)
        r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0

        if gamma < 0.9:
            diffusive_type = "subdiffusive"
        elif gamma > 1.1:
            diffusive_type = "superdiffusive"
        else:
            diffusive_type = "diffusive"

        return VarianceGrowthResult(
            times=times_fit,
            variance=variance_fit,
            growth_exponent=gamma,
            r_squared=r_squared,
            diffusive_type=diffusive_type,
        )