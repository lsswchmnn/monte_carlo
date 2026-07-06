from ui.utils.display import print_heading, enter_continue
#=========================================================================
def help_full():
    print_heading("HELP MENU")
    print(
        "This application simulates and visualizes stochastic processes in 1D, 2D, or 3D. "
        "You can select different transition rules, configure simulation parameters, "
        "and analyze the resulting trajectories."
    )
    enter_continue()

def help_settings():
    print_heading("HELP MENU")
    print(
        "The settings menu allows you to configure all core simulation parameters:"
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