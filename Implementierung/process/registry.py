from process.transitions    import markov, variational, adaptive
from process                import start_states
#=========================================================================
# Zentrales Register: Metadaten und Funktionsreferenz an einem Ort.
# Die CLI und MonteCarloSim importieren nur noch von hier.
#
# Struktur pro Eintrag:
#   "fn"   → direkte Referenz auf Funktion
#   "name" → Anzeigename
#   "desc" → Beschreibung für den Nutzer
#=========================================================================
TRANSITION_REGISTRY:  dict[str, dict] = {
    "markov": {
        "random_walk": {
            "fn":   markov.random_walk,
            "name": "Random Walk",
            "desc": (
                "At each step, the state moves up or down by a fixed amount. "
                "Both directions are equally likely and independent of the past."
            ),
        },
        "drifted_random_walk": {
            "fn":   markov.drifted_random_walk,
            "name": "Drifted Random Walk",
            "desc": (
                "A random walk with an added constant drift. "
                "The process tends to move in one direction over time."
            ),
        },
        "mean_reverting": {
            "fn":   markov.mean_reverting,
            "name": "Mean Reversion",
            "desc": (
                "The state is pulled toward a long-term mean. "
                "Deviations from the mean tend to shrink over time."
            ),
        },
        "state_dependent_vol": {
            "fn":   markov.state_dependent_vol,
            "name": "State-Dependent Volatility",
            "desc": (
                "The size of fluctuations depends on the current state. "
                "More extreme states lead to higher volatility."
            ),
        },
        "fat_tail_walk": {
            "fn":   markov.fat_tail_walk,
            "name": "Fat-Tail Walk",
            "desc": (
                "Most steps are small, but rare steps are extremely large. "
                "The distribution of changes has heavy tails."
            ),
        },
        "absorbing_barrier": {
            "fn":   markov.absorbing_barrier,
            "name": "Absorbing Barrier",
            "desc": (
                "Once the state crosses a fixed boundary, it becomes trapped. "
                "After that point, no further movement is possible."
            ),
        },
        "regime_switch": {
            "fn":   markov.regime_switch,
            "name": "Regime Switch",
            "desc": (
                "The process alternates between normal and high-volatility behavior. "
                "Transitions between regimes occur randomly."
            ),
        },
        "linear_step": {
            "fn":   markov.linear_step,
            "name": "Linear Step",
            "desc": "The state remains constant at every step.",
        },
    },

    "variational": {
        "variational_baseline": {
            "fn":   variational.variational_baseline,
            "name": "Variational Baseline",
            "desc": (
                "A simple variational transition that incorporates feedback from the path's history. "
                "The state is influenced by its deviation from the path mean."
            ),
        },
        "variational_trend_feedback": {
            "fn":   variational.variational_trend_feedback,
            "name": "Variational Trend Feedback",
            "desc": (
                "A variational transition that incorporates feedback from the path's history, "
                "with an emphasis on trend feedback and path-dependent volatility."
            ),
        },
    },

    "adaptive": {
        "adaptive_random_walk": {
            "fn":   adaptive.adaptive_random_walk,
            "name": "Adaptive Random Walk",
            "desc": "A simple adaptive Random Walk with a trivial step counter as placeholder.",
        },
        "adaptive_volatility_walk": {
            "fn":   adaptive.adaptive_volatility_walk,
            "name": "Adaptive Volatility Walk",
            "desc": (
                "An adaptive random walk in which the step size is endogenously "
                "adjusted based on recently observed volatility. Higher realized volatility "
                "leads to smaller future steps (negative feedback). The process is "
                "path-dependent and non-ergodic in the classical sense."
            ),
        },
    },
}
START_STATE_REGISTRY: dict[str, dict] = {
    "fixed_state": {
        "fn":   start_states.fixed_state,
        "name": "Fixed State",
        "desc": "Every path starts at the same fixed value (1.0).",
    },
    "random_state": {
        "fn":   start_states.random_state,
        "name": "Random State",
        "desc": "Every path starts at a random value drawn from N(0, 1).",
    },
}