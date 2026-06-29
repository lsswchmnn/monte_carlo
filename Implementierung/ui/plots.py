from   typing            import List
from   core.config       import SimConfig
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

#-------------------------------------------------------------------------
# Entry-Point
 
def show(result: list, plot_type: str, config: SimConfig) -> None:
    plots = {
        "sample_paths":    _plot_paths,
        "mean_volatility": _plot_mean_and_std,
        "final_dist":      _plot_final_distribution,
    }
    fn = plots.get(plot_type)
    if fn is None:
        raise ValueError(f"Unknown plot type: '{plot_type}'")
    fn(result, config)
 
#-------------------------------------------------------------------------
# Private Plotting-Funktionen

def _plot_paths(paths: List[List[float]], config: SimConfig) -> None:
    for path in paths:
        plt.plot(_smooth_path(path), alpha=ALPHA)

    plt.title("All Sample Paths")
    plt.xlabel("Step")
    plt.ylabel("State")
    plt.grid(True, which="both", linestyle="--", alpha=ALPHA)
    _add_label(config)
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
    plt.show()

def _plot_final_distribution(paths: List[List[float]], config: SimConfig) -> None:
    final_values = [path[-1] for path in paths]

    plt.hist(final_values, bins=30, alpha=0.7)
    plt.title("Distribution of Final States")
    plt.xlabel("Final State")
    plt.ylabel("Frequency")
    plt.grid(True, which="both", linestyle="--", alpha=ALPHA)
    _add_label(config)
    plt.show()