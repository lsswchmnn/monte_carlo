#=========================================================================
def fixed_state(rng) -> float:
    return 1

def random_state(rng) -> float:
    return rng.gauss(0, 1)