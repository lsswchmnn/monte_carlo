from process.transitions_1d import markov, variational, adaptive
from process.transitions_nd import markov_nd, variational_nd, adaptive_nd
from process                import start_states
#=========================================================================
# Zentrales Register: Metadaten und Funktionsreferenz an einem Ort.
# Für 1D- und ND-Transitions und Startzustände.
#
# Struktur pro Eintrag:
#   "fn"   → direkte Referenz auf Funktion
#   "name" → Anzeigename
#   "desc" → Beschreibung für den Nutzer
#=========================================================================
TRANSITION_REGISTRY:     dict[str, dict] = {
    "markov": {
        "random_walk": {
            "fn":   markov.random_walk,
            "name": "Random Walk",
            "desc": (
                "At each step, the state moves up or down by a fixed amount. "
                "Both directions are equally likely and independent of the past."
            ),
        },
        "levy_flight": {
            "fn":   markov.levy_flight,
            "name": "Lévy Flight",
            "desc": (
                "Steps follow a stable distribution with heavy tails. "
                "Most steps are small, but rare steps are extremely large — "
                "orders of magnitude larger than typical. "
                "Controlled by stability index alpha (default 1.5). "
                "alpha=2 approximates a Gaussian random walk; alpha→0 yields increasingly extreme jumps."
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
START_STATE_REGISTRY:    dict[str, dict] = {
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
TRANSITION_REGISTRY_ND:  dict[str, dict] = {
    "markov": {
        "random_walk_nd": {
            "fn":   markov_nd.random_walk_nd,
            "name": "Random Walk (ND)",
            "desc": (
                "At each step, moves by ±step_size along one randomly "
                "chosen axis. Direct n-dimensional analogue of the 1D random walk."
            ),
        },
        "levy_flight_nd": {
            "fn":   markov_nd.levy_flight_nd,
            "name": "Lévy Flight (ND)",
            "desc": (
                "N-dimensional Lévy Flight. Step length follows a stable distribution, "
                "direction is uniformly distributed on the n-dimensional unit sphere. "
                "Stability index alpha=1.5 by default."
            ),
        },
    },
    "variational": {
        "variational_baseline_nd": {
            "fn":   variational_nd.variational_baseline_nd,
            "name": "Variational Baseline (ND)",
            "desc": (
                "N-dimensional analogue of the variational baseline: weak "
                "feedback toward the path mean, applied independently per axis."
            ),
        },
    },
    "adaptive": {
        "adaptive_random_walk_nd": {
            "fn":   adaptive_nd.adaptive_random_walk_nd,
            "name": "Adaptive Random Walk (ND)",
            "desc": (
                "N-dimensional analogue of the adaptive random walk: random axis, "
                "random sign, trivial step counter as placeholder."
            ),
        },
    },
}
START_STATE_REGISTRY_ND: dict[str, dict] = {
    "fixed_state_nd": {
        "fn":   start_states.fixed_state_nd,
        "name": "Fixed State (ND)",
        "desc": "Every path starts at the origin (0, 0, ..., 0).",
    },
    "random_state_nd": {
        "fn":   start_states.random_state_nd,
        "name": "Random State (ND)",
        "desc": "Every path starts at a random point, each axis drawn from N(0, 1).",
    },
}