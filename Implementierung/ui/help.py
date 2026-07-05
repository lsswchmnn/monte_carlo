from ui.utils.display import print_heading, enter_continue
#=========================================================================
def help_full():
    print_heading("HELP MENU")
    print("This application simulates and visualizes stochastic processes in 1D, 2D, or 3D. You can choose from various transition rules, configure simulation parameters, and analyze the resulting trajectories.")
    enter_continue()

def help_settings():
    print_heading("HELP MENU")
    print("Settings allow you to configure the simulation parameters, including:")
    print(" - Dimensionality: Choose an (int) dimension in which the trajectories evolve. (Only 1D, 2D and 3D can be visualized, but higher dimensions can be calculated without problems.)")
    print(" - Start state: Choose the initial state of the system.")
    print(" - Transition rule: Choose the transition function that governs the evolution of the system.")
    print(" - Number of paths and steps: Specify how many trajectories to simulate and how many time steps to compute.")
    print(" - Seed: Set the random seed for reproducibility of results.")
    enter_continue()

def help_three_types():
    print_heading("HELP MENU")
    print("You can choose several transition rules from three categories:\n")

    print(" 1. Markov Process:")
    print("    The next state depends only on the current state.")
    print("    No memory, no path dependence. The process is time-local")
    print("    and fully described by a transition kernel.\n")

    print(" 2. Variational Process:")
    print("    The transition is influenced by a global functional of the path")
    print("    (e.g. path mean, energy, action-like quantities).")
    print("    Introduces weak memory and drift terms derived from an")
    print("    optimization or stabilization principle.\n")

    print(" 3. Adaptive Process:")
    print("    Transition rules change over time based on observed behavior.")
    print("    Parameters adapt to variance, trends or regime shifts.")
    print("    The process is non-stationary and self-modifying.\n")

    enter_continue()

def help_ergodicity():
    print_heading("HELP MENU")
    print(
    "Ergodicity describes whether time averages equal ensemble averages.\n"
    "A process is ergodic if observing a single system over sufficient time\n"
    "yields the same statistical properties as observing many identical\n"
    "systems at one moment. In non-ergodic systems, individual trajectories\n"
    "matter: long-term outcomes depend on path history, not just expected values."
    )
    enter_continue()