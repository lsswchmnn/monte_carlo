from utils import show_error, printProgressBar, clear_cli             # Hilfsfunktionen
from start_state import fixed_state, random_state               # Startwert auswählen
import random

# Verschiedene Übergangsfunktionen importieren
from transition_rules import random_walk, drifted_random_walk, more_volatility, mean_reverting, state_dependent_vol, linear_step, fat_tail_walk, absorbing_barrier, regime_switch
from transition_rules import variational_baseline, variational_trend_feedback
#=========================================================================
# Methoden für Startzustand in start_state.py; für Transitionsregeln in 
# transition_rule.py. Sim darf nicht wissen, welche Regeln sie nutzt
#=========================================================================
class MonteCarloSim:
    def __init__(self):
        self.n_steps : int      = 1000                      # Schritte eines Pfades
        self.n_paths : int      = 400                      # Anzahl an simulierten Pfaden
        self.start_state        = fixed_state               # Startbedingung
        self.seed : int         = 12                        
        self.rng                = random.Random(self.seed)  # Eigener Random-Numbers-Generator mit Seed
        self.step_size : float  = 1.0                       # Paramter für die Übergangsfunktionen

        # Höchstgrenzen für Datenpunkte (Performance)
        self.markov_max_datapoints : int        = 50_000_000
        self.variational_max_datapoints : int   = 5_000_000
        self.adaptive_max_datapoints : int      = 200_000

        # Standard-Übergangsfunktion
        self.process_type : str     = "variational"     # Aktueller Prozess-Typ: markov, variational, adaptive
        self.transition_function    = None              # Funktion
        self.function_name          = None
        self.dict_transition_function = None

        # Ergebnis der Simulation
        self.last_result        = None  # Auf letztes Ergebnis zugreifen
        self.last_erg_data      = None  # Ergodizitäts-Ergebnis

#-------------------------------------------------------------------------
# Sim-Methoden

    def run(self):
        if self.process_type == "markov":
            return self.run_markov()
        elif self.process_type == "variational":
            return self.run_variational()
        elif self.process_type == "adaptive":
            return self.run_adaptive()

    # für lokale, stochastische markov-Prozesse (zeitdiskret und additiv, klassischer Monte-Carlo-Ansatz)
    def run_markov(self)-> list:
        self.last_result = None     # Ergebnis zurücksetzen
        self.last_erg_data = None

        all_paths = []

        for i in range(self.n_paths):
            path = []
            x = self.start_state(self.rng)

            for _ in range(self.n_steps):
                path.append(x)
                x = self.transition_function (x, self.rng, self.step_size)
            
            all_paths.append(path)

            printProgressBar(i+1, self.n_paths, prefix='Generating Trajectories:', suffix='Finished', length=50)

        self.last_result = all_paths

        return all_paths

    # Pfadabhnägige, nicht lokale Prozesse. Darf mehr kontext als nur den aktuellen Zustand nutzen
    def run_variational(self)-> list:
        self.last_result = None
        self.last_erg_data = None

        all_paths = []

        for i in range(self.n_paths):
            path = []
            x = self.start_state(self.rng)

            for t in range(self.n_steps):
                path.append(x)
                x = self.transition_function (
                    x_t= x,
                    t= t,
                    path= path,
                    rng= self.rng,
                    step_size= self.step_size
                )

            all_paths.append(path)

            printProgressBar(i, self.n_paths, prefix='Generating Trajectories:', suffix='Finished', length=50)

        self.last_result = all_paths
        return all_paths
        
    # Zustands- und Verlaufsabhängige Prozesse
    def run_adaptive(self)-> list:
        pass

#-------------------------------------------------------------------------
# Hilfsmethoden

    def check_if_complete(self)-> bool:
        if self.transition_function  is None:
            show_error(True, "DataError", "No Transitional Function loaded.")
            return False

        if self.n_steps is None:
            show_error(True, "DataError", "No Number of steps defined.")
            return False
        
        if self.n_paths is None:
            show_error(True, "DataError", "No Number of paths defined.")
            return False
        
        if self.start_state is None:
            show_error(True, "DataError", "No Startstate defined.")
            return False
        
        if self.seed is None:
            show_error(True, "DataError", "No Seed defined.")
            return False
        
        if self.process_type is None:
            show_error(True, "DataError", "No Process type defined.")
            return False
        
        if self.step_size is None:
            show_error(True, "DataError", "No step size defined.")
            return False
        
        return True