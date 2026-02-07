from utils import print_heading, enter_continue

def help_full():
    print_heading("HELP-MENU")
    print("...")

def help_three_types():
    print_heading("HELP-MENU")
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

    enter_continue("Press enter to return to the settings")