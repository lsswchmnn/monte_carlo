from   dataclasses       import dataclass, replace
from   core.config       import SimConfig
from   analyze.analyzer  import ErgodicityResult, AutoCorrelationResult
import numpy             as     np
#=========================================================================
# HistoryManager
# Verantwortlichkeit: Ergebnisse während runtime halten.
# Jeder Eintrag enthält das Ergebnis und einen eingefroreren Config-Snapshot.
#=========================================================================
@dataclass
class HistoryEntry:
    result      : list                                 # Trajektorien
    config      : SimConfig                            # Einstellungen
    erg_result  : ErgodicityResult      | None = None  # Ergodizität     (optoinal)
    acf_result  : AutoCorrelationResult | None = None  # Autokorrelation (optional)
    calc_time   : float                 | None = None  # Berechnungszeit (optional)

#=========================================================================
class HistoryManager:

    def __init__(self):
        self._entries: list[HistoryEntry] = []

    def add(self, result: list, config: SimConfig, calc_time: float | None = None) -> None:
        snapshot = replace(config)
        snapshot.rng = np.random.default_rng(config.seed)                                         # saubere Kopie der Konfiguration
        self._entries.append(HistoryEntry(result=result, config=snapshot, calc_time=calc_time))   # dataclass zu Historie hinzufügen
 
    def get(self, index: int) -> HistoryEntry:
        return self._entries[index]
 
    def all(self) -> list[HistoryEntry]:
        return list(self._entries)
 
    def clear(self) -> None:
        self._entries.clear()
 
    def delete(self, index: int) -> None:
        self._entries.pop(index)

    def is_empty(self) -> bool:
        return len(self._entries) == 0
 
    def __len__(self) -> int:
        return len(self._entries)