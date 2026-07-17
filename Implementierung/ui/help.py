from ui.cli.utils.display import print_heading, enter_continue
#=========================================================================
HELP_REGISTRY: dict[str, str] = {
    "full": (
        "This application simulates and visualizes stochastic processes in 1D, 2D, or 3D. "
        "You can select different transition rules, configure simulation parameters, "
        "and analyze the resulting trajectories."
    ),
    "settings": (
        "The settings menu allows you to configure all core simulation parameters:\n"
        " - Dimensionality: Defines the space in which trajectories evolve. "
        "Only 1D, 2D, and 3D are visualized, but higher dimensions can be simulated.\n"
        " - Start state: Sets the initial condition of the system.\n"
        " - Transition rule: Determines the update mechanism governing system evolution.\n"
        " - Number of paths and steps: Controls how many trajectories are simulated "
        "and how many time steps are computed per trajectory.\n"
        " - Seed: Sets the random seed to ensure reproducibility."
    ),
    "transition": (
        "Transition functions define how a trajectory evolves from one time step to the next.\n"
        "They determine the local update rule of the stochastic process and are the core "
        "mechanism behind the dynamics of all simulated paths.\n\n"
        "General form:\n"
        "    x_{t+1} = F(x_t, parameters, randomness)\n\n"
        "Depending on the chosen model, the transition may depend only on the current state "
        "(Markovian), on global path properties (variational), or on evolving parameters "
        "(adaptive).\n\n"
        "Common components:\n"
        " - Deterministic drift: systematic directional change of the state.\n"
        " - Stochastic term: random perturbation, often Gaussian or heavy-tailed.\n"
        " - State-dependent volatility: randomness scales with the current state.\n"
        " - Memory terms: dependence on past trajectory statistics.\n\n"
        "Examples:\n"
        " - Random Walk:         x_{t+1} = x_t + ε_t\n"
        " - Drift Process:       x_{t+1} = x_t + μ + ε_t\n"
        " - Mean-Reverting:      x_{t+1} = x_t - λ x_t + ε_t\n"
        " - Lévy Flight:         x_{t+1} = x_t + L_t (heavy-tailed noise)\n"
        " - Adaptive Process:     x_{t+1} = x_t + σ(x_t, t) ε_t\n\n"
        "The choice of transition function largely determines global behavior: "
        "diffusive spread, stability, explosiveness, or heavy-tailed jumps."
    ),
    "start_states": (
        "The start state defines the initial position of every trajectory. "
        "It serves as the common origin from which all stochastic paths evolve. "
        "Different initial states can significantly influence transient dynamics, "
        "even if long-term statistical properties remain unchanged."
    ),
    "three_types": (
        "You can choose from three categories of transition rules:\n\n"
        "1. Markov Process\n"
        "   The next state depends only on the current state. "
        "There is no memory of past states. "
        "The process is time-local and fully described by a transition kernel.\n\n"
        "2. Variational Process\n"
        "   Transitions are influenced by global properties of the trajectory, "
        "such as running averages, energy-like quantities, or action-inspired terms. "
        "This introduces weak memory effects and drift induced by global structure.\n\n"
        "3. Adaptive Process\n"
        "   Transition rules evolve over time based on observed system behavior. "
        "Parameters adapt to variance, trends, or regime changes. "
        "The process is non-stationary and self-modifying."
    ),
    "system_settings": (
        "System settings control how results are displayed — they have no "
        "effect on the simulation itself and are not saved with exported results.\n\n"
        " - Path smoothing: Applies a moving average to sample paths before "
        "plotting, for a cleaner visual impression of the trend.\n"
        " - Smoothing window: Size of that moving average (larger = smoother, "
        "but more distortion of short-term detail).\n"
        " - Plot alpha: Transparency of plotted lines/markers.\n"
        " - Grid: Toggles the background grid on plots."
    ),
    "analyze": (
        "The analysis menu provides several methods to investigate the properties "
        "of a completed stochastic simulation.\n\n"
        "Available analyses:\n"
        " - Ergodicity:\n"
        "   Compares time averages and ensemble averages to determine whether "
        "a single trajectory represents the overall system behavior.\n"
        " - Autocorrelation Function (ACF):\n"
        "   Measures temporal dependencies and reveals persistence, memory effects, "
        "or mean-reverting behavior within trajectories.\n"
        " - Hurst Exponent:\n"
        "   Estimates long-range dependence and classifies processes as persistent, "
        "anti-persistent, or approximately random.\n"
        " - Variance Growth:\n"
        "   Examines how the spread of trajectories changes over time and helps "
        "identify diffusive, sub-diffusive, or super-diffusive behavior."
        "\nTogether, these methods provide a statistical overview of the dynamics "
        "and scaling properties of the simulated process."
    ),
    "ergodicity": (
        "Ergodicity describes the relationship between time averages and ensemble averages.\n\n"
        "A process is ergodic if observing a single trajectory over sufficient time "
        "yields the same statistical properties as observing many identical systems "
        "at a fixed time.\n\n"
        "In non-ergodic systems, individual trajectories matter: long-term outcomes "
        "depend on path history rather than only on expected values."
    ),
    "autocorrelation": (
        "The autocorrelation function (ACF) measures how correlated a process is "
        "with a delayed version of itself, for a range of time lags.\n\n"
        "For each lag, the ACF is computed per path and then averaged across the "
        "ensemble. Values near zero indicate no linear dependence between distant "
        "points, while large positive or negative values indicate persistence or "
        "mean-reverting behavior respectively.\n\n"
        "The ±1.96/√T confidence bound marks the range expected under the null "
        "hypothesis of white noise (independent increments) at the 95% level."
    ),
    "hurst_exponent": (
        "The Hurst exponent (H) quantifies long-range dependence and self-similarity "
        "in a time series, estimated here via Detrended Fluctuation Analysis (DFA).\n\n"
        "DFA integrates the (demeaned) series, splits it into windows of increasing size, "
        "removes a local linear trend per window, and measures how the residual "
        "fluctuation F(s) scales with window size s. The slope of log F(s) vs log s "
        "on a log-log plot is the Hurst exponent.\n\n"
        "By default this is computed on the increments of each path (not the raw "
        "levels), following standard convention for position/price-like series:\n"
        "  H ≈ 0.5  -> uncorrelated increments (consistent with a random walk)\n"
        "  H > 0.5  -> persistent / trending (increments tend to continue)\n"
        "  H < 0.5  -> anti-persistent (increments tend to reverse, mean-reverting)\n\n"
        "R² of the log-log fit indicates how well the scaling law holds; low R² "
        "suggests the process isn't well described by a single scaling exponent "
        "(e.g. crossover behavior, or too short a series)."
    ),
    "variance_growth": (
        "Variance growth tracks how the ensemble variance of the displacement "
        "(x_t - x_0) grows over time. A power law Var(t) ~ t^gamma is fitted "
        "on a log-log scale.\n\n"
        "  gamma ≈ 1  -> normal (Fickian) diffusion — e.g. an uncorrelated random walk\n"
        "  gamma < 1  -> subdiffusive — a restoring force limits long-term spread\n"
        "  gamma > 1  -> superdiffusive — rare large jumps or persistent trending\n\n"
        "This is closely related to the Hurst exponent (gamma ≈ 2H for "
        "self-similar processes), but measured directly on the ensemble spread "
        "rather than via detrended fluctuation of individual paths.\n\n"
        "A low R² usually means the process doesn't follow a single power law "
        "over the whole time range — e.g. mean-reverting processes saturate "
        "toward a plateau rather than growing indefinitely, which a single "
        "exponent fit describes only roughly."
    )
}
#-------------------------------------------------------------------------

def print_help(key: str) -> None:
    text = HELP_REGISTRY.get(key)
    if text is None:
        raise KeyError(f"No help text registered for key: '{key}'")
    print_heading("HELP MENU")
    print(text)
    enter_continue()