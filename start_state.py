import random
#=========================================================================
def fixed_state() -> float:
    return 100

def random_state(rng) -> float:
    return random.gauss(0, 1)