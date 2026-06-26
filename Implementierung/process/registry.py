#=========================================================================
transition_data_markov = {
    "random_walk": {
        "Name": "Random Walk",
        "Desc": (
            "At each step, the state moves up or down by a fixed amount. "
            "Both directions are equally likely and independent of the past."
        )
    },

    "drifted_random_walk": {
        "Name": "Drifted Random Walk",
        "Desc": (
            "A random walk with an added constant drift. "
            "The process tends to move in one direction over time."
        )
    },

    "mean_reverting": {
        "Name": "Mean Reversion",
        "Desc": (
            "The state is pulled toward a long-term mean. "
            "Deviations from the mean tend to shrink over time."
        )
    },

    "state_dependent_vol": {
        "Name": "State-Dependent Volatility",
        "Desc": (
            "The size of fluctuations depends on the current state. "
            "More extreme states lead to higher volatility."
        )
    },

    "fat_tail_walk": {
        "Name": "Fat-Tail Walk",
        "Desc": (
            "Most steps are small, but rare steps are extremely large. "
            "The distribution of changes has heavy tails."
        )
    },

    "absorbing_barrier": {
        "Name": "Absorbing Barrier",
        "Desc": (
            "Once the state crosses a fixed boundary, it becomes trapped. "
            "After that point, no further movement is possible."
        )
    },

    "regime_switch": {
        "Name": "Regime Switch",
        "Desc": (
            "The process alternates between normal and high-volatility behavior. "
            "Transitions between regimes occur randomly."
        )
    },

    "linear_step": {
        "Name": "Linear Step",
        "Desc": (
            "The Process creates one linear line."
        )
    },
}

transition_data_variational = {
    "variational_baseline": {
        "Name": "Variational Baseline",
        "Desc": (
            "A simple variational transition that incorporates feedback from the path's history. "
            "The state is influenced by its deviation from the path mean."
        )
    },

    "variational_trend_feedback": {
        "Name": "Variational Trend Feedback",
        "Desc": (
            "A variational transition that incorporates feedback from the path's history, "
            "with an emphasis on trend feedback and path-dependent volatility."
        )
    }
}

transition_data_adaptive = {
    "adaptive_random_walk": {
        "Name": "Adaptive Random Walk",
        "Desc": (
            "A simple adaptive Random Walk with trivial increasing of the value as placeholder."
        )
    },

    "adaptive_volatility_walk": {
        "Name": "Adaptive Volatility Walk",
        "Desc": (
            "an adaptive random walk in which the step size is endogenously "
            "adjusted based on recently observed volatility. Each step is stochastic, "
            "but the magnitude of future steps depends on an exponential moving average "
            "of past step sizes. Higher realized volatility leads to a reduction in step size, "
            "introducing negative feedback and non-stationarity. As a result, the process "
            "is path-dependent and no longer ergodic in the classical sense, since its dynamics evolve "
            "with its own history."
        )
    }
}