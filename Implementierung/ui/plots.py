from   typing            import List
from   core.config       import SimConfig
from   datetime          import datetime
import matplotlib.pyplot as plt
import numpy             as np
#=========================================================================
# Verschiedenes und Hilfsfunktionen

ALPHA: float = 0.5

def _smooth_path(path: list, window: int = 10) -> np.ndarray:
    if len(path) < window:
        return np.array(path)
    return np.convolve(path, np.ones(window) / window, mode="same")

def _add_label(config: SimConfig) -> None:
    '''Fügt Transition-Name und Seed als Textbox in den Plot ein.'''
    plt.text(
        0.02, 0.95,
        f"Transition: {config.transition_name}\nSeed: {config.seed} | Paths: {config.n_paths}",
        transform=plt.gca().transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=dict(facecolor="white", alpha=ALPHA, edgecolor="none"),
    )

def _set_plot_title(name: str) -> None:
    plt.gcf().canvas.manager.set_window_title(
        f"{name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    )

#-------------------------------------------------------------------------
# Entry-Point
 
def show(result: list, plot_type: str, config: SimConfig) -> None:
    '''
    Verteilt auf die passende Plot-Funktion abhängig von Dimensionalität
    und Plot-Typ.
    '''
    # ND Plotting
    if config.dimensionality == "nd":
        if plot_type == "sample_paths":
            if config.n_dimensions == 2:
                _plot_paths_2d(result, config)
            elif config.n_dimensions == 3:
                _plot_paths_3d(result, config)
            else:
                raise ValueError(f"Plotting not supported for {config.n_dimensions}D.")
        else:
            raise ValueError(f"Plot type '{plot_type}' is not available for ND results.")
        return

    # 1D Plotting
    plots = {
        "sample_paths":    _plot_paths_1d,
        "mean_volatility": _plot_mean_and_std,
        "final_dist":      _plot_final_distribution,
    }
    fn = plots.get(plot_type)
    if fn is None:
        raise ValueError(f"Unknown plot type: '{plot_type}'")
    fn(result, config)
 
#-------------------------------------------------------------------------
# Private Plotting-Funktionen

def _plot_paths_1d(paths: List[List[float]], config: SimConfig) -> None:
    for path in paths:
        plt.plot(_smooth_path(path), alpha=ALPHA)

    plt.title("All Sample Paths")
    plt.xlabel("Step")
    plt.ylabel("State")
    plt.grid(True, which="both", linestyle="--", alpha=ALPHA)
    _add_label(config)
    _set_plot_title("sample_paths_1d")
    plt.show()

def _plot_paths_2d(paths: list, config: SimConfig) -> None:
    '''
    Zeichnet alle Sample Paths im 2D-Raum.
    x- und y-Achse sind die beiden Dimensionen, Zeit ist implizit der Verlauf.
    Startpunkt als Marker hervorgehoben.
    '''
    for path in paths:
        coords = np.array(path)         # shape: (n_steps, 2)
        plt.plot(coords[:, 0], coords[:, 1], alpha=ALPHA, linewidth=0.8)
        plt.plot(coords[0, 0], coords[0, 1],                   # Startpunkt
                 marker="o", markersize=3, color="black", alpha=ALPHA)
 
    plt.title("All Sample Paths (2D)")
    plt.xlabel("Dimension 1")
    plt.ylabel("Dimension 2")
    plt.grid(True, which="both", linestyle="--", alpha=ALPHA)
    plt.axis("equal")                   # gleiche Skalierung beider Achsen
    _add_label(config)
    _set_plot_title("sample_paths_2d")
    plt.show()

def _plot_paths_3d(paths: list, config: SimConfig) -> None:
    '''
    Zeichnet alle Sample Paths im 3D-Raum.
    Drei Dimensionen auf x/y/z-Achsen, Zeit implizit als Verlauf der Linie.
    '''
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
 
    for path in paths:
        coords = np.array(path)         # shape: (n_steps, 3)
        ax.plot(coords[:, 0], coords[:, 1], coords[:, 2],
                alpha=ALPHA, linewidth=0.8)
 
    ax.set_title("All Sample Paths (3D)")
    ax.set_xlabel("Dimension 1")
    ax.set_ylabel("Dimension 2")
    ax.set_zlabel("Dimension 3")
    _set_plot_title("sample_paths_3d")
    plt.show()


def _plot_mean_and_std(paths: List[List[float]], config: SimConfig) -> None:
    data = np.array(paths)
    mean = data.mean(axis=0)
    std  = data.std(axis=0)
    x    = range(len(mean))

    plt.plot(x, mean, label="Mean", color="black")
    plt.fill_between(x, mean - std, mean + std, alpha=0.3, label="±1 Std Dev")

    plt.title("Mean Path with Volatility")
    plt.xlabel("Step")
    plt.ylabel("State")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=ALPHA)
    _add_label(config)
    _set_plot_title("mean_and_std_1d")
    plt.show()


def _plot_final_distribution(paths: List[List[float]], config: SimConfig) -> None:
    final_values = [path[-1] for path in paths]

    plt.hist(final_values, bins=30, alpha=0.7)
    plt.title("Distribution of Final States")
    plt.xlabel("Final State")
    plt.ylabel("Frequency")
    plt.grid(True, which="both", linestyle="--", alpha=ALPHA)
    _add_label(config)
    _set_plot_title("distribution_1d")
    plt.show()
