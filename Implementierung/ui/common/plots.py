from   analyze.results   import *
from   core.config       import SimConfig
from   dataclasses       import dataclass
from   typing            import List
from   datetime          import datetime
import matplotlib.pyplot as     plt
import numpy             as     np
#=========================================================================
@dataclass
class PlotSettings:
    smooth        : bool  = True
    grid          : bool  = True
    smooth_window : int   = 10
    alpha         : float = 0.5

#=========================================================================
class Plotter:

    def __init__(self, settings: PlotSettings | None = None):
        self.settings: PlotSettings = settings or PlotSettings()

#-------------------------------------------------------------------------
# Einstellungen (öffentlich)

    def toggle_smooth(self) -> None:
        self.settings.smooth = not self.settings.smooth

    def toggle_grid(self) -> None:
        self.settings.grid = not self.settings.grid

    def set_smooth_window(self, window: int) -> None:
        self.settings.smooth_window = window

    def set_alpha(self, alpha: float) -> None:
        self.settings.alpha = alpha

    def reset_settings(self) -> None:
        self.settings = PlotSettings()

#-------------------------------------------------------------------------
# Ressourcen-Verwaltung (öffentlich)

    @staticmethod
    def close(fig) -> None:
        '''
        Schließt eine Figure, um Speicher freizugeben.
        '''
        plt.close(fig)

#-------------------------------------------------------------------------
# Entry-Points: Sample Paths und Analysen (öffentlich)

    def plot(self, result: list, plot_type: str, config: SimConfig):
        '''
        Baut die passende Figure abhängig von Dimensionalität und Plot-Typ.
        Zeigt nichts an, somit nutzbar für CLI und Web.
        '''
        # ND Plotting
        if config.dimensionality == "nd":
            if plot_type == "sample_paths":
                if config.n_dimensions == 2:
                    return self.plot_paths_2d(result, config)
                elif config.n_dimensions == 3:
                    return self.plot_paths_3d(result, config)
                else:
                    raise ValueError(f"Plotting not supported for {config.n_dimensions}D.")
            else:
                raise ValueError(f"Plot type '{plot_type}' is not available for ND results.")

        # 1D Plotting: sample_paths gesondert behandeln
        if plot_type == "sample_paths":
            return self.plot_paths_1d(result, config)

        # 1D Plotting: allgemeine Behandlung
        plots = {"mean_volatility": self.plot_mean_and_std, "final_dist": self.plot_final_distribution}
        fn = plots.get(plot_type)
        if fn is None:
            raise ValueError(f"Unknown plot type: '{plot_type}'")
        return fn(result, config)

    def show(self, result: list, plot_type: str, config: SimConfig) -> None:
        '''CLI-Pfad: baut die passende Figure und zeigt sie an.'''
        self.plot(result, plot_type, config)
        plt.show()

    def show_ergodicity(self, result: ErgodicityResult, config: SimConfig) -> None:
        self.plot_ergodicity(result, config)
        plt.show()

    def show_autocorrelation(self, result: AutoCorrelationResult, config: SimConfig) -> None:
        self.plot_autocorrelation(result, config)
        plt.show()

    def show_hurst(self, result: HurstExponentResult, config: SimConfig) -> None:
        self.plot_hurst(result, config)
        plt.show()

    def show_variance_growth(self, result: VarianceGrowthResult, config: SimConfig) -> None:
        self.plot_variance_growth(result, config)
        plt.show()

#-------------------------------------------------------------------------
# Hilfsfunktionen (privat)

    @staticmethod
    def _smooth_path(path: list, window: int = 10) -> np.ndarray:
        '''Glättet Darstellung eines Pfades.'''
        if len(path) < window:
            return np.array(path)
        return np.convolve(path, np.ones(window) / window, mode="same")

    @staticmethod
    def _set_plot_title(name: str) -> None:
        '''Erstellt Titel für Graph mit Timestamp.'''
        plt.gcf().canvas.manager.set_window_title(
            f"{name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        )

    def _add_label(self, config: SimConfig) -> None:
        '''Fügt Transition-Name und Seed als Textbox in den Plot ein.'''
        plt.text(
            0.02, 0.95,
            f"Transition: {config.transition_name}\nSeed: {config.seed} | Paths: {config.n_paths}",
            transform=plt.gca().transAxes,
            fontsize=10,
            verticalalignment="top",
            bbox=dict(facecolor="white", alpha=self.settings.alpha, edgecolor="none"),
        )

    def _apply_grid(self):
        if self.settings.grid:
            plt.grid(True, which="both", linestyle="--", alpha=0.5)
        else:
            plt.grid(False)

#-------------------------------------------------------------------------
# Plotting-Funktionen (privat)

    def plot_paths_1d(self, paths: List[List[float]], config: SimConfig):
        plt.figure()
        for path in paths:
            if self.settings.smooth:
                plt.plot(self._smooth_path(path, window=self.settings.smooth_window), alpha=self.settings.alpha)
            else:
                plt.plot(path, alpha=self.settings.alpha)

        plt.title("All Sample Paths")
        plt.xlabel("Step")
        plt.ylabel("State")
        self._apply_grid()
        self._add_label(config)
        self._set_plot_title("sample_paths_1d")
        return plt.gcf()

    def plot_paths_2d(self, paths: list, config: SimConfig):
        '''
        Zeichnet alle Sample Paths im 2D-Raum.
        x- und y-Achse sind die beiden Dimensionen, Zeit ist implizit der Verlauf.
        Startpunkt als Marker hervorgehoben.
        '''
        plt.figure()
        for path in paths:
            coords = np.array(path)         # shape: (n_steps, 2)
            plt.plot(coords[:, 0], coords[:, 1], alpha=self.settings.alpha, linewidth=0.8)
            plt.plot(coords[0, 0], coords[0, 1],                   # Startpunkt
                     marker="o", markersize=3, color="black", alpha=self.settings.alpha)

        plt.title("All Sample Paths (2D)")
        plt.xlabel("Dimension 1")
        plt.ylabel("Dimension 2")
        plt.axis("equal")                   # gleiche Skalierung beider Achsen
        self._apply_grid()
        self._add_label(config)
        self._set_plot_title("sample_paths_2d")
        return plt.gcf()

    def plot_paths_3d(self, paths: list, config: SimConfig):
        '''
        Zeichnet alle Sample Paths im 3D-Raum.
        Drei Dimensionen auf x/y/z-Achsen, Zeit implizit als Verlauf der Linie.
        '''
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        for path in paths:
            coords = np.array(path)         # shape: (n_steps, 3)
            ax.plot(coords[:, 0], coords[:, 1], coords[:, 2],
                    alpha=self.settings.alpha, linewidth=0.8)

        ax.set_title("All Sample Paths (3D)")
        ax.set_xlabel("Dimension 1")
        ax.set_ylabel("Dimension 2")
        ax.set_zlabel("Dimension 3")
        self._set_plot_title("sample_paths_3d")
        return plt.gcf()

    def plot_final_distribution(self, paths: List[List[float]], config: SimConfig):
        plt.figure()
        final_values = [path[-1] for path in paths]

        plt.hist(final_values, bins=30, alpha=self.settings.alpha)
        plt.title("Distribution of Final States")
        plt.xlabel("Final State")
        plt.ylabel("Frequency")
        self._apply_grid()
        self._add_label(config)
        self._set_plot_title("distribution_1d")
        return plt.gcf()

    def plot_mean_and_std(self, paths: List[List[float]], config: SimConfig):
        plt.figure()
        data = np.array(paths)
        mean = data.mean(axis=0)
        std  = data.std(axis=0)
        x    = range(len(mean))

        plt.plot(x, mean, label="Mean", color="black")
        plt.fill_between(x, mean - std, mean + std, alpha=self.settings.alpha, label="±1 Std Dev")

        plt.title("Mean Path with Volatility")
        plt.xlabel("Step")
        plt.ylabel("State")
        plt.legend()
        self._apply_grid()
        self._add_label(config)
        self._set_plot_title("mean_and_std_1d")
        return plt.gcf()

    def plot_ergodicity(self, result: ErgodicityResult, config: SimConfig):
        plt.figure()
        plt.hist(result.time_means, bins=30, color="steelblue", alpha=self.settings.alpha, zorder=2)

        plt.axvline(result.ensemble_mean, color="black", linewidth=1.5,
                    label=f"Ensemble Mean ({result.ensemble_mean:.4f})", zorder=3)

        threshold = 0.10  # muss mit dem Schwellenwert in Analyzer.calculate_ergodicity übereinstimmen
        band = threshold * abs(result.ensemble_mean)
        plt.axvspan(result.ensemble_mean - band, result.ensemble_mean + band,
                    color="green" if result.ergodic_heuristic else "red",
                    alpha=0.15, zorder=1,
                    label=f"±{threshold:.0%} reference band (visual aid, not the exact test)")

        verdict = "Ergodic (heuristic)" if result.ergodic_heuristic else "Not ergodic (heuristic)"
        plt.text(
            0.02, 0.85,
            f"{verdict}\n"
            f"Std of time means: {result.time_mean_std:.4f}\n"
            f"Relative spread: {result.time_mean_std / abs(result.ensemble_mean):.2%}",
            transform=plt.gca().transAxes, fontsize=9, verticalalignment="top",
            bbox=dict(facecolor="white", alpha=self.settings.alpha, edgecolor="none"),
        )

        plt.title("Distribution of Path Time-Averages vs. Ensemble Mean")
        plt.xlabel("Time Average per Path")
        plt.ylabel("Frequency")
        plt.legend(loc="upper right", fontsize=8)
        self._apply_grid()
        self._add_label(config)
        self._set_plot_title("ergodicity")
        return plt.gcf()

    def plot_autocorrelation(self, result: AutoCorrelationResult, config: SimConfig):
        plt.figure()
        lags  = result.lags
        acf   = result.acf_mean
        bound = result.confidence_bound

        plt.bar(lags, acf, width=0.6, color="steelblue", alpha=0.8)
        plt.axhline(bound, color="red", linestyle="--", linewidth=1, alpha=self.settings.alpha)
        plt.axhline(-bound, color="red", linestyle="--", linewidth=1, alpha=self.settings.alpha)
        plt.axhline(0, color="black", linewidth=0.8)

        plt.title("Autocorrelation Function (Ensemble Mean)")
        plt.xlabel("Lag")
        plt.ylabel("ACF")
        self._apply_grid()
        self._add_label(config)
        self._set_plot_title("autocorrelation")
        return plt.gcf()

    def plot_hurst(self, result: HurstExponentResult, config: SimConfig):
        plt.figure()
        log_s = np.log10(result.scales)
        log_f = np.log10(result.fluctuation_mean)

        plt.scatter(log_s, log_f, color="steelblue", label="F(s), Ensemble-Mittel", zorder=3)

        coeffs = np.polyfit(log_s, log_f, deg=1)
        plt.plot(log_s, np.polyval(coeffs, log_s), color="red", linestyle="--",
                  label=f"Fit (Steigung ≈ {coeffs[0]:.3f})", zorder=2)

        plt.text(
            0.02, 0.85,
            f"H (Pfad-Mittel): {result.hurst_mean:.4f} ± {result.hurst_std:.4f}\n"
            f"R² (mittel): {result.r_squared_mean:.4f}\n"
            f"Basis: {'Increments' if result.on_increments else 'Levels'}",
            transform=plt.gca().transAxes, fontsize=9, verticalalignment="top",
            bbox=dict(facecolor="white", alpha=self.settings.alpha, edgecolor="none"),
        )

        plt.title("Detrended Fluctuation Analysis (DFA)")
        plt.xlabel("log₁₀(Fenstergröße s)")
        plt.ylabel("log₁₀(F(s))")
        plt.legend(loc="lower right")
        self._apply_grid()
        self._add_label(config)
        self._set_plot_title("dfa_hurst")
        return plt.gcf()

    def plot_variance_growth(self, result: VarianceGrowthResult, config: SimConfig):
        plt.figure()
        log_t = np.log10(result.times)
        log_v = np.log10(result.variance)

        plt.scatter(log_t, log_v, color="steelblue", label="Var(t), Ensemble", zorder=3)

        coeffs = np.polyfit(log_t, log_v, deg=1)
        plt.plot(log_t, np.polyval(coeffs, log_t), color="red", linestyle="--",
                  label=f"Fit (γ ≈ {coeffs[0]:.3f})", zorder=2)

        # Referenzlinie: normale Diffusion (gamma=1), durch denselben Startpunkt gelegt
        ref = log_v[0] + 1.0 * (log_t - log_t[0])
        plt.plot(log_t, ref, color="gray", linestyle=":", alpha=self.settings.alpha,
                  label="Referenz: γ=1 (diffusiv)", zorder=1)

        plt.text(
            0.02, 0.85,
            f"γ (Wachstumsexponent): {result.growth_exponent:.4f}\n"
            f"R²: {result.r_squared:.4f}\n"
            f"Klassifikation: {result.diffusive_type}",
            transform=plt.gca().transAxes, fontsize=9, verticalalignment="top",
            bbox=dict(facecolor="white", alpha=self.settings.alpha, edgecolor="none"),
        )

        plt.title("Variance Growth")
        plt.xlabel("log₁₀(t)")
        plt.ylabel("log₁₀(Var(t))")
        plt.legend(loc="lower right")
        self._apply_grid()
        self._add_label(config)
        self._set_plot_title("variance_growth")
        return plt.gcf()