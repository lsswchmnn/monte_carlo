from ui.cli.utils.display import print_heading, enter_continue
#=========================================================================
def help_full():
    print_heading("HELP MENU")
    print(
        "This application simulates and visualizes stochastic processes in 1D, 2D, or 3D. "
        "You can select different transition rules, configure simulation parameters, "
        "and analyze the resulting trajectories."
    )
    enter_continue()

#-------------------------------------------------------------------------
# Einstellungen und Konfiguration

def help_settings():
    print_heading("HELP MENU")
    print(
        "The settings menu allows you to configure all core simulation parameters:\n\n"
    )
    print(
        " - Dimensionality: Defines the space in which trajectories evolve. "
        "Only 1D, 2D, and 3D are visualized, but higher dimensions can be simulated."
    )
    print(
        " - Start state: Sets the initial condition of the system."
    )
    print(
        " - Transition rule: Determines the update mechanism governing system evolution."
    )
    print(
        " - Number of paths and steps: Controls how many trajectories are simulated "
        "and how many time steps are computed per trajectory."
    )
    print(
        " - Seed: Sets the random seed to ensure reproducibility."
    )
    enter_continue()

def help_transition():
    print_heading("HELP MENU")

    print(
        "Transition functions define how a trajectory evolves from one time step to the next.\n"
        "They determine the local update rule of the stochastic process and are the core "
        "mechanism behind the dynamics of all simulated paths.\n"
    )

    print("General form:")
    print("    x_{t+1} = F(x_t, parameters, randomness)\n")

    print(
        "Depending on the chosen model, the transition may depend only on the current state "
        "(Markovian), on global path properties (variational), or on evolving parameters "
        "(adaptive)."
    )

    print("\nCommon components:")
    print(
        " - Deterministic drift: systematic directional change of the state.\n"
        " - Stochastic term: random perturbation, often Gaussian or heavy-tailed.\n"
        " - State-dependent volatility: randomness scales with the current state.\n"
        " - Memory terms: dependence on past trajectory statistics."
    )

    print("\nExamples:")
    print(
        " - Random Walk:         x_{t+1} = x_t + ε_t\n"
        " - Drift Process:       x_{t+1} = x_t + μ + ε_t\n"
        " - Mean-Reverting:      x_{t+1} = x_t - λ x_t + ε_t\n"
        " - Lévy Flight:         x_{t+1} = x_t + L_t (heavy-tailed noise)\n"
        " - Adaptive Process:     x_{t+1} = x_t + σ(x_t, t) ε_t"
    )

    print(
        "\nThe choice of transition function largely determines global behavior: "
        "diffusive spread, stability, explosiveness, or heavy-tailed jumps."
    )

    enter_continue()

def help_start_states():
    print_heading("HELP MENU")
    print(
        "The start state defines the initial position of every trajectory. "
        "It serves as the common origin from which all stochastic paths evolve. "
        "Different initial states can significantly influence transient dynamics, "
        "even if long-term statistical properties remain unchanged."
    )
    enter_continue()

def help_three_types():
    print_heading("HELP MENU")

    print("You can choose from three categories of transition rules:\n")

    print("1. Markov Process")
    print(
        "   The next state depends only on the current state. "
        "There is no memory of past states. "
        "The process is time-local and fully described by a transition kernel."
    )

    print("\n2. Variational Process")
    print(
        "   Transitions are influenced by global properties of the trajectory, "
        "such as running averages, energy-like quantities, or action-inspired terms. "
        "This introduces weak memory effects and drift induced by global structure."
    )

    print("\n3. Adaptive Process")
    print(
        "   Transition rules evolve over time based on observed system behavior. "
        "Parameters adapt to variance, trends, or regime changes. "
        "The process is non-stationary and self-modifying."
    )
    enter_continue()

#-------------------------------------------------------------------------
# Analyse

def help_analyze():
    print_heading("HELP MENU")

    print(
        "The analysis menu provides several methods to investigate the properties "
        "of a completed stochastic simulation.\n\n"
        "Available analyses:\n"
    )

    print(
        " - Ergodicity:\n"
        "   Compares time averages and ensemble averages to determine whether "
        "a single trajectory represents the overall system behavior.\n"
    )

    print(
        " - Autocorrelation Function (ACF):\n"
        "   Measures temporal dependencies and reveals persistence, memory effects, "
        "or mean-reverting behavior within trajectories.\n"
    )

    print(
        " - Hurst Exponent:\n"
        "   Estimates long-range dependence and classifies processes as persistent, "
        "anti-persistent, or approximately random.\n"
    )

    print(
        " - Variance Growth:\n"
        "   Examines how the spread of trajectories changes over time and helps "
        "identify diffusive, sub-diffusive, or super-diffusive behavior."
    )

    print(
        "\nTogether, these methods provide a statistical overview of the dynamics "
        "and scaling properties of the simulated process."
    )
    enter_continue()

def help_ergodicity():
    print_heading("HELP MENU")
    print(
        "Ergodicity describes the relationship between time averages and ensemble averages.\n\n"
        "A process is ergodic if observing a single trajectory over sufficient time "
        "yields the same statistical properties as observing many identical systems "
        "at a fixed time.\n\n"
        "In non-ergodic systems, individual trajectories matter: long-term outcomes "
        "depend on path history rather than only on expected values."
    )
    enter_continue()

def help_autocorrelation():
    print_heading("HELP MENU")
    print(
        "The autocorrelation function (ACF) measures how correlated a process is "
        "with a delayed version of itself, for a range of time lags.\n\n"
        "For each lag, the ACF is computed per path and then averaged across the "
        "ensemble. Values near zero indicate no linear dependence between distant "
        "points, while large positive or negative values indicate persistence or "
        "mean-reverting behavior respectively.\n\n"
        "The ±1.96/√T confidence bound marks the range expected under the null "
        "hypothesis of white noise (independent increments) at the 95% level."
    )
    enter_continue()

def help_hurst_exponent():
    print_heading("HELP MENU")
    print(
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
    )
    enter_continue()