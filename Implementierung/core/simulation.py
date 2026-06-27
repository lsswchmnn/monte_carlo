from start_state import fixed_state, random_state               # Startwert auswählen
import random
#=========================================================================
# Methoden für Startzustand in start_state.py; für Transitionsregeln in 
# transition_rule.py. Sim darf nicht wissen, welche Regeln sie nutzt
#=========================================================================
class MonteCarloSim:
    def __init__(self):
        self.n_steps : int      = 10000                      # Schritte eines Pfades
        self.n_paths : int      = 50                      # Anzahl an simulierten Pfaden
        self.start_state        = fixed_state               # Startbedingung
        self.seed : int         = 12                        
        self.rng                = random.Random(self.seed)  # Eigener Random-Numbers-Generator mit Seed
        self.step_size : float  = 1.0                       # Paramter für die Übergangsfunktionen

        # Höchstgrenzen für Datenpunkte (Performance)
        self.markov_max_datapoints : int        = 100_000_000
        self.variational_max_datapoints : int   = 50_000_000
        self.adaptive_max_datapoints : int      = 50_000_000

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

            # nichts in cli zu suchen
            # printProgressBar(
            #     i+1, self.n_paths, 
            #     prefix='Generating Trajectories:', 
            #     suffix='Finished', length=520)

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

            # nichts in backend zu suchen
            # printProgressBar(
            #     i, self.n_paths, 
            #     prefix='Generating Variational Trajectories:', 
            #     suffix='Finished', length=50)

        self.last_result = all_paths
        return all_paths
        
    # Zustands- und Verlaufsabhängige Prozesse
    def run_adaptive(self)-> list:
        self.last_result =  None
        self.last_erg_data = None

        all_paths = []
        all_adaptive_states = []

        for i in range(self.n_paths):
            path = []
            x = self.start_state(self.rng)

            adaptive_state = {}

            for t in range(self.n_steps):
                path.append(x)

                x, adaptive_state = self.transition_function(
                    x_t=x,
                    t=t,
                    path=path,
                    adaptive_state = adaptive_state,
                    rng=self.rng,
                    step_size=self.step_size
                )
            
            all_paths.append(path)
            all_adaptive_states.append(adaptive_state)

            # Nichts in Backend zu suchen
            # printProgressBar(
            #     i + 1, self.n_paths, 
            #     prefix="Generating Adaptive Trajectories",
            #     suffix="Finished", length=50
            # )

        self.last_result = all_paths
        self.last_adaptive_state = all_adaptive_states

        return all_paths

#-------------------------------------------------------------------------
# Hilfsmethoden

    # Prüft ob konfiguration vollständig ist -> auslagern in controller
    def check_if_complete(self)-> bool:

        # ShowError entfernen, hat nichts in Backend zu suchen

        if self.transition_function  is None:
            #show_error(True, "DataError", "No Transitional Function loaded.")
            return False

        if self.n_steps is None:
            #show_error(True, "DataError", "No Number of steps defined.")
            return False

        if self.n_paths is None:
            #show_error(True, "DataError", "No Number of paths defined.")
            return False

        if self.start_state is None:
            #show_error(True, "DataError", "No Startstate defined.")
            return False

        if self.seed is None:
            #show_error(True, "DataError", "No Seed defined.")
            return False

        if self.process_type is None:
            #show_error(True, "DataError", "No Process type defined.")
            return False

        if self.step_size is None:
            #show_error(True, "DataError", "No step size defined.")
            return False

        return True