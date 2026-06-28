from dataclasses import dataclass, replace
from core.config import SimConfig
#=========================================================================
# HistoryManager
# Verantwortlichkeit: Ergebnisse während runtime halten.
# Jeder Eintrag enthält das Ergebnis und einen eingefroreren Config-Snapshot.
#=========================================================================
@dataclass
class HistoryEntry:
    result : list
    config : SimConfig

#=========================================================================
class HistoryManager:

    def __init__(self):
        self._entries: list[HistoryEntry] = []

    def add(self, result: list, config: SimConfig) -> None:
        snapshot = replace(config)      # flache Kopie der Dataclass
        self._entries.append(HistoryEntry(result=result, config=snapshot))
 
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