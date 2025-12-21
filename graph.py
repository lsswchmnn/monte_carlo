import matplotlib.pyplot as plt
import numpy as np
from typing import List
#=========================================================================
# Funktionen für Visualisierung

# Zeichent alle Sample Paths
def plot_paths(paths: List[List[float]]) -> None:
    for path in paths:
        plt.plot(path, alpha=0.9)

    plt.title("Monte Carlo Simulation Paths")
    plt.xlabel("Step")
    plt.ylabel("State")
    plt.show()

# Komprimiert zu Erwartungswert und Streuung
def plot_mean_and_std(paths: List[List[float]]) -> None:
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
    plt.show()

# Fokus auf Ergebnis statt Weg
def plot_final_distribution(paths: List[List[float]]) -> None:
    final_values = [path[-1] for path in paths]

    plt.hist(final_values, bins=30, alpha=0.7)
    plt.title("Distribution of Final States")
    plt.xlabel("Final State")
    plt.ylabel("Frequency")
    plt.show()
