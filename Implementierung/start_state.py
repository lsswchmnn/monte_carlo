import random
#=========================================================================
start_state_data = {
    "fixed_state": {
        "Name": "Fixed State",
        "Desc": (
            "Starting at a fixed Value."
        )
    },

    "random_state": {
        "Name": "Random State",
        "Desc": (
            "Starting at a random Value."
        )
    },
}
#=========================================================================
def fixed_state(rng) -> float:
    return 1

def random_state(rng) -> float:
    return random.gauss(0, 1)