from utils import show_error, printProgressBar                       # Hilfsfunktionen
from start_state import fixed_state, random_state               # Startwert auswählen
from transition_rules import random_walk, drifted_random_walk, more_volatility, mean_reverting, state_dependent_vol, linear_step, fat_tail_walk, absorbing_barrier, regime_switch
import random
#=========================================================================
# Methoden für Startzustand in start_state.py; für Transitionsregeln in 
# transition_rule.py. Sim darf nicht wissen, welche Regeln sie nutzt
#=========================================================================
class MonteCarloSim:
    def __init__(self):
        self.n_steps            = 1000                      # Schritte eines Pfades
        self.n_paths            = 1000                      # Anzahl an simulierten Pfaden
        self.start_state        = fixed_state               # Startbedingung
        self.transitional_rule  = random_walk
        self.seed               = 12                        
        self.rng                = random.Random(self.seed)  # Eigener Random-Numbers-Generator mit Seed
        self.step_size          = 1.0                       # Paramter für die Übergangsfunktionen
        self.last_result        = None                      # Auf letztes Ergebnis zugreifen
        self.last_erg_data      = None                      # Ergodizitäts-Ergebnis
#=========================================================================
# Sim-Methoden

    # für lokale, stochastische markov-Prozesse (zeitdiskret und additiv)
    def run_local_marcov(self)-> list:
        self.last_result = None     # Ergebnis zurücksetzen
        self.last_erg_data = None

        all_paths = []

        for i in range(self.n_paths):
            path = []
            x = self.start_state(self.rng)

            for _ in range(self.n_steps):
                path.append(x)
                x = self.transitional_rule(x, self.rng, self.step_size)
            
            all_paths.append(path)

            printProgressBar(i, self.n_paths, prefix='PGenerating Trajectories:', suffix='Finished', length=50)

        
        self.last_result = all_paths

        return all_paths

    def run_variational(self)-> list:
        self.last_result = None
        self.last_erg_data = None
        
    def run_adaptive(self)-> list:
        pass

#=========================================================================
# Hilfsmethoden

    def check_if_complete(self)-> bool:
        if self.n_steps is None:
            show_error(True, "DataError", "No Number of steps defined.")
            return False
        
        if self.n_paths is None:
            show_error(True, "DataError", "No Number of paths defined.")
            return False
        
        if self.start_state is None:
            show_error(True, "DataError", "No Startstate defined.")
            return False
        
        if self.transitional_rule is None:
            show_error(True, "DataError", "No Transitionrule defined.")
            return False
        
        if self.step_size is None:
            show_error(True, "DataError", "No step size defined.")
            return False
        
        return True