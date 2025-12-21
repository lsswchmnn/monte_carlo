import random
#=========================================================================
def random_walk(x_t: float, rng, step_size: float = 1.0) -> float:
    step = rng.choice([-step_size, step_size])
    return x_t + step
