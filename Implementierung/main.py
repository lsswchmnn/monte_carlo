from montecarlo import MonteCarloSim
from ui.cli import CLI
#=========================================================================
if __name__ == "__main__":
    sim = MonteCarloSim()
    cli = CLI(sim)
    cli.run()