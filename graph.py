import matplotlib.pyplot as plt
import numpy as np
from typing import List
from utils import clear_cli, printProgressBar
#=========================================================================
# Verschiedenes

# Default-Speicherpfad
plt.rcParams["savefig.directory"] = r"C:/Users/Lasse/Pictures/Projekte/Monte Carlo Sim"

ALPHA : int = 0.5

# Für Glättung der Linien
def smooth_path(path, window=10):
    if len(path) < window:
        return np.array(path)
    return np.convolve(path, np.ones(window)/window, mode="same")

#=========================================================================
# Funktionen für Visualisierung

# Zeichent alle Sample Paths
def plot_paths(paths: List[List[float]], seed: int, 
               num_paths: int, length_paths: int,
               function_name : int) -> None:
    for path in paths:
        smooth = smooth_path(path, window=10)
        plt.plot(smooth, alpha=ALPHA)

    plt.title("All Sample-paths")
    plt.xlabel("Step")
    plt.ylabel("State")
    plt.grid(True, which='both', linestyle='--', alpha=ALPHA)

    # Seed ausgeben
    if seed is not None:
        plt.text(
            0.02, 0.95,
            f"Transition Function: {function_name}\nSeed: {seed} | Paths: {num_paths}",
            transform=plt.gca().transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(facecolor='white', alpha=ALPHA, edgecolor='none')
        )

    clear_cli()
    plt.show()


# Komprimiert zu Erwartungswert und Streuung
def plot_mean_and_std(paths: List[List[float]], seed: int, num_paths: int) -> None:
    data = np.array(paths)

    mean = data.mean(axis=0)
    std = data.std(axis=0)

    x = range(len(mean))

    plt.plot(x, mean, label="Mean", color="black")
    plt.fill_between(
        x,
        mean - std,
        mean + std,
        alpha=0.3,
        label="±1 Std Dev"
    )

    plt.title("Mean Path with Volatility")
    plt.xlabel("Step")
    plt.ylabel("State")
    plt.legend()
    plt.grid(True, which='both', linestyle='--', alpha=ALPHA)


    # Seed ausgeben
    if seed is not None:
        plt.text(
            0.02, 0.95,
            f"Seed: {seed} | Paths: {num_paths}",
            transform=plt.gca().transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(facecolor='white', alpha=ALPHA, edgecolor='none')
        )

    clear_cli()
    plt.show()

# Fokus auf Ergebnis statt Weg
def plot_final_distribution(paths: List[List[float]], seed: int, num_paths: int) -> None:
    final_values = [path[-1] for path in paths]

    plt.hist(final_values, bins=30, alpha=0.7)
    plt.title("Distribution of Final States")
    plt.xlabel("Final State")
    plt.ylabel("Frequency")
    plt.grid(True, which='both', linestyle='--', alpha=ALPHA)

    # Seed ausgeben
    if seed is not None:
        plt.text(
            0.02, 0.95,
            f"Seed: {seed} | Paths: {num_paths}",
            transform=plt.gca().transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(facecolor='white', alpha=ALPHA, edgecolor='none')
        )

    clear_cli()
    plt.show()