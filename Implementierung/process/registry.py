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
#   "params: → Paramter für Übergänge
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
            "params": {
                "drift": {
                    "default": 0.0, "min": -10.0, "max": 10.0,
                    "type": "float",
                    "desc": "Constant drift added each stept (0 = symmetric)"
                }
            }
        },
        "mean_reverting": {
            "fn":   markov.mean_reverting,
            "name": "Mean Reversion",
            "desc": (
                "The state is pulled toward a long-term mean. "
                "Deviations from the mean tend to shrink over time."
            ),
            "params": {
                "strength": {
                    "default": 0.1, "min": 0.001, "max": 1.0,
                    "type": "float",
                    "desc": "Pull strength toward mean (higher = faster convergence)"
                },
                "mean":  {
                    "default": 0.0, "min": -10.0, "max": 10.0,
                    "type": "float",
                    "desc": "Target mean value"
                },
            },
        },
        "state_dependent_vol": {
            "fn":   markov.state_dependent_vol,
            "name": "State-Dependent Volatility",
            "desc": (
                "The size of fluctuations depends on the current state. "
                "More extreme states lead to higher volatility."
            ),
            "params": {
                "factor": {
                    "default": 0.08, "min": 0.001, "max": 5.0,
                    "type": "float",
                    "desc": "Volatility growth factor (higher = more extreme outliers)"
                }
            }
        },
        "absorbing_barrier": {
            "fn":   markov.absorbing_barrier,
            "name": "Absorbing Barrier",
            "desc": (
                "Once the state crosses a fixed boundary, it becomes trapped. "
                "After that point, no further movement is possible."
            ),
            "params": {
                "barrier": {
                    "default": -10.0, "min": -1000.0, "max": 1000.0,
                    "type": "float",
                    "desc": "Position of the barrier (on y-axis)",
                },
                "barrier_type": {
                    "default": "absorbing", "min": None, "max": None,
                    "type": "str",
                    "options": ["absorbing", "reflecting"],
                    "desc": "absorbing: freezes at barrier | reflecting: bounces back",
                },
            },
        },
        "regime_switch": {
            "fn":   markov.regime_switch,
            "name": "Regime Switch",
            "desc": (
                "The process alternates between normal and high-volatility behavior. "
                "Transitions between regimes occur randomly."
            ),
            "params": {
                "p_switch": {
                    "default": 0.1, "min": 0.001, "max": 0.999,
                    "type": "float",
                    "desc": "Probability of entering the high-volatility regime",
                },
                "vol_factor": {
                    "default": 5.0, "min": 1.1, "max": 100.0,
                    "type": "float",
                    "desc": "Volatility multiplier in the high regime",
                },
            },
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
            "params": {
                "alpha": {
                    "default": 1.5, "min": 0.1, "max": 2.0,
                    "type": "float",
                    "desc": "Stability index (2=Gaussian, 1=Cauchy, lower=more extreme)",
                },
            },
        },
        "fat_tail_walk": {
            "fn":   markov.fat_tail_walk,
            "name": "Fat-Tail Walk",
            "desc": (
                "Most steps are small, but rare steps are extremely large. "
                "The distribution of changes has heavy tails."
            ),
            "params": {
                "p_tail": {
                    "default": 0.02, "min": 0.001, "max": 0.5,
                    "type": "float",
                    "desc": "Probability of an extreme step",
                },
                "tail_factor": {
                    "default": 20.0, "min": 2.0, "max": 200.0,
                    "type": "float",
                    "desc": "Size multiplier for extreme steps",
                },
            },
        },

    },

    "variational": {
        "variational_baseline": {
            "fn":   variational.variational_baseline,
            "name": "Variational Baseline",
            "desc": (
                "A simple variational transition that incorporates feedback from "
                "the path's history. The state is influenced by its deviation "
                "from the path mean."
            ),
            "params": {
                "memory_strength": {
                    "default": 0.01, "min": 0.0001, "max": 1.0,
                    "type": "float",
                    "desc": "Strength of feedback toward path mean",
                },
            },
        },
        "variational_trend_feedback": {
            "fn":   variational.variational_trend_feedback,
            "name": "Variational Trend Feedback",
            "desc": (
                "A variational transition with path feedback and trend amplification. "
                "Incorporates path mean, recent trend, and path-dependent volatility."
            ),
            "params": {
                "memory_strength": {
                    "default": 0.02, "min": 0.0001, "max": 1.0,
                    "type": "float",
                    "desc": "Strength of feedback toward path mean",
                },
                "trend_strength": {
                    "default": 0.01, "min": 0.0001, "max": 1.0,
                    "type": "float",
                    "desc": "Amplification of the recent trend direction",
                },
                "vol_factor": {
                    "default": 0.05, "min": 0.0, "max": 5.0,
                    "type": "float",
                    "desc": "Path-deviation contribution to volatility",
                },
            },
        },
    },

    "adaptive": {
        "adaptive_random_walk": {
            "fn":   adaptive.adaptive_random_walk,
            "name": "Adaptive Random Walk",
            "desc": "A simple adaptive Random Walk with a trivial step counter.",
            "params": {},
        },
        "adaptive_volatility_walk": {
            "fn":   adaptive.adaptive_volatility_walk,
            "name": "Adaptive Volatility Walk",
            "desc": (
                "An adaptive random walk in which the step size is endogenously "
                "adjusted based on recently observed volatility. Higher realized "
                "volatility leads to smaller future steps (negative feedback). "
                "Path-dependent and non-ergodic in the classical sense."
            ),
            "params": {},
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
                "At each step, moves by +-step_size along one randomly chosen axis. "
                "N-dimensional analogue of the 1D random walk."
            ),
            "params": {
                "drift": {
                    "default": 0.0, "min": -10.0, "max": 10.0,
                    "type": "float",
                    "desc": "Constant drift added to each axis each step",
                },
            },
        },
        "mean_reverting_nd": {
            "fn":   markov_nd.mean_reverting_nd,
            "name": "Mean Reversion (ND)",
            "desc": (
                "Pulls the state toward a target point in n-dimensional space. "
                "Noise is applied independently along each axis."
            ),
            "params": {
                "strength": {
                    "default": 0.1, "min": 0.001, "max": 1.0,
                    "type": "float",
                    "desc": "Pull strength toward the target point",
                },
                "mean": {
                    "default": 0.0, "min": -100.0, "max": 100.0,
                    "type": "float",
                    "desc": "Target value applied to all dimensions",
                },
            },
        },
        "state_dependent_vol_nd": {
            "fn":   markov_nd.state_dependent_vol_nd,
            "name": "State-Dependent Volatility (ND)",
            "desc": (
                "Volatility grows with the distance from the origin. "
                "More extreme positions lead to larger steps in all directions."
            ),
            "params": {
                "factor": {
                    "default": 0.08, "min": 0.001, "max": 5.0,
                    "type": "float",
                    "desc": "Scales how strongly distance amplifies volatility",
                },
            },
        },
        "absorbing_barrier_nd": {
            "fn":   markov_nd.absorbing_barrier_nd,
            "name": "Absorbing Barrier (ND)",
            "desc": (
                "A hyperplane barrier orthogonal to the first dimension. "
                "absorbing: freezes when crossed | reflecting: bounces back."
            ),
            "params": {
                "barrier": {
                    "default": -10.0, "min": -1000.0, "max": 1000.0,
                    "type": "float",
                    "desc": "Barrier position along the first dimension",
                },
                "barrier_type": {
                    "default": "absorbing", "min": None, "max": None,
                    "type": "str",
                    "options": ["absorbing", "reflecting"],
                    "desc": "absorbing: freezes | reflecting: bounces back",
                },
            },
        },
        "regime_switch_nd": {
            "fn":   markov_nd.regime_switch_nd,
            "name": "Regime Switch (ND)",
            "desc": (
                "Alternates between normal and high-volatility behavior. "
                "High-volatility steps are applied equally in all directions."
            ),
            "params": {
                "p_switch": {
                    "default": 0.1, "min": 0.001, "max": 0.999,
                    "type": "float",
                    "desc": "Probability of entering the high-volatility regime",
                },
                "vol_factor": {
                    "default": 5.0, "min": 1.1, "max": 100.0,
                    "type": "float",
                    "desc": "Volatility multiplier in the high regime",
                },
            },
        },
        "levy_flight_nd": {
            "fn":   markov_nd.levy_flight_nd,
            "name": "Lévy Flight (ND)",
            "desc": (
                "Step length from a stable distribution, direction uniformly "
                "distributed on the n-dimensional unit sphere (Muller 1959)."
            ),
            "params": {
                "alpha": {
                    "default": 1.5, "min": 0.1, "max": 2.0,
                    "type": "float",
                    "desc": "Stability index (2=Gaussian, 1=Cauchy, lower=more extreme)",
                },
            },
        },
    },

    "variational": {
        "variational_baseline_nd": {
            "fn":   variational_nd.variational_baseline_nd,
            "name": "Variational Baseline (ND)",
            "desc": (
                "Weak feedback toward the path mean, applied independently per axis. "
                "N-dimensional analogue of the variational baseline."
            ),
            "params": {
                "memory_strength": {
                    "default": 0.01, "min": 0.0001, "max": 1.0,
                    "type": "float",
                    "desc": "Strength of feedback toward path mean per axis",
                },
            },
        },
    },

    "adaptive": {
        "adaptive_random_walk_nd": {
            "fn":   adaptive_nd.adaptive_random_walk_nd,
            "name": "Adaptive Random Walk (ND)",
            "desc": (
                "N-dimensional adaptive random walk: random axis, random sign, "
                "trivial step counter as placeholder."
            ),
            "params": {},
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