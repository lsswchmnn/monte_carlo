import time
import threading
import sys
#=========================================================================
# Spinner-Klasse
class Spinner:
    def __init__(self, symbols="|/—\\", delay=0.15):
        self.symbols    = symbols
        self.delay      = delay
        self.running    = False
        self.thread     = None

    def start(self, message="Loading"):
        self.running = True
        self.thread = threading.Thread(target=self._spin, args=(message,), daemon=True)
        self.thread.start()

    def _spin(self, message):
        idx = 0
        while self.running:
            sys.stdout.write(f"\r{message} {self.symbols[idx % len(self.symbols)]}")
            sys.stdout.flush()
            idx += 1
            time.sleep(self.delay)
        sys.stdout.write("\r" + " " * (len(message) + 2) + "\r")  # Clear line

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

#-------------------------------------------------------------------------

# Fortschritts-Iterator mit tqdm; funktioniert bei for-Schleifen
def printProgressBar(iteration, 
                     total, 
                     prefix = '', 
                     suffix = '', 
                     decimals = 1, 
                     length = 100, 
                     fill = '█',
                     printEnd = "\r"):
    '''
    Ein Iterator, der über einen iterierbaren Prozess läuft,
    dabei eine Fortschrittsleiste anzeigt und optional eine Callback-Funktion
    auf jedes Element anwenden kann.

    Parameter:
    - iterable: Ein iterierbares Objekt (z.B. range, Liste, Generator).
    - desc: Beschreibung, die links von der Leiste angezeigt wird.
    - unit: Einheit für die Leiste (standard: "it" für Iterationen).
    - total: Gesamtzahl der Schritte (falls tqdm sie nicht automatisch bestimmen kann).
    - callback: Optionale Funktion, die auf jedes Element angewendet wird.

    Rückgabe:
    - Liste mit Ergebnissen der Callback-Verarbeitung (falls callback gesetzt),
    sonst eine Liste der Elemente selbst.
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    '''

    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    
    sys.stdout.write(
        f"\r{prefix} |{bar}| {percent}% {suffix}"
    )
    sys.stdout.flush()

    if iteration == total:
        sys.stdout.write("\n")
        sys.stdout.flush()

def finishProgressBar():
    sys.stdout.write("\r\033[2K\n")
    sys.stdout.flush()