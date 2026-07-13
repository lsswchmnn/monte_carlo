# Monte Carlo Simulation

Ein Python-Tool zur Simulation und Analyse stochastischer Prozesse in 1D und ND. Simuliert Trajektorien nach wählbaren Übergangsregeln, visualisiert sie und untersucht statistische Eigenschaften wie Ergodizität, Autokorrelation und Langzeitgedächtnis.

## Architektur

Das Projekt ist strikt in unabhängige Schichten getrennt — jede kennt nur, was sie unbedingt braucht:

```
main.py
  └── ui/cli.py          (Benutzerinteraktion)
        └── core/controller.py   (einzige Vermittlung UI <-> Backend)
              ├── core/config.py        (Simulationsparameter)
              ├── core/simulation.py    (Pfadberechnung)
              ├── core/history.py       (Ergebnisse zur Laufzeit)
              ├── analyze/analyzer.py   (statistische Analyse)
              ├── exporter.py           (JSON/CSV Export/Import)
              └── process/registry.py   (Übergangsfunktionen)
        └── ui/plots.py         (Plotter, unabhängig vom Controller)
```

**Leitprinzip:** Der `Controller` kennt kein Plotting, die `SimConfig` kennt keine Programm-/Anzeigeeinstellungen, der `Plotter` kennt keine Simulationslogik. Anzeige-Einstellungen (Smoothing, Alpha, Grid) leben in `PlotSettings`, gehalten vom `Plotter`, der wiederum von der CLI instanziiert wird — nicht vom Controller.

## Module im Überblick

| Modul | Verantwortlichkeit |
|---|---|
| `core/config.py` | `SimConfig` — Simulationsparameter, Validität, Datapoint-Limits |
| `core/controller.py` | Koordiniert alle Kernkomponenten, einzige Schnittstelle für die UI |
| `core/simulation.py` | `MonteCarloSim` — führt die eigentliche Pfadberechnung aus |
| `core/history.py` | Hält Ergebnisse (`HistoryEntry`) während der Laufzeit |
| `analyze/analyzer.py` | Statistische Analysen auf fertigen Ergebnissen |
| `analyze/results.py` | Dataclasses für Analyseergebnisse |
| `process/registry.py` | Zentrales Register aller Übergangs- und Startzustandsfunktionen |
| `process/transitions_1d/`, `transitions_nd/` | Konkrete Übergangsfunktionen (Markov, Variational, Adaptive) |
| `exporter.py` | Export nach JSON/CSV, Re-Import von JSON |
| `ui/cli.py` | Terminal-Benutzeroberfläche |
| `ui/plots.py` | `Plotter` + `PlotSettings` — alle Visualisierungen |

## Prozesstypen

Drei Kategorien von Übergangsfunktionen, jeweils in 1D und ND verfügbar:

1. **Markov** — nächster Zustand hängt nur vom aktuellen Zustand ab (z. B. Random Walk, Mean Reversion, Lévy Flight)
2. **Variational** — Übergang nutzt den gesamten bisherigen Pfad (z. B. Rückkopplung an Pfadmittelwert)
3. **Adaptive** — Übergangsregel passt sich über die Zeit an (z. B. volatilitätsabhängige Schrittweite)

## Analyse-Features

| Feature | Status | Methode |
|---|---|---|
| Ergodizität | ✅ fertig | Vergleich Zeit- vs. Ensemble-Mittel |
| Autokorrelation | ✅ fertig | ACF pro Pfad, Ensemble-gemittelt, 95%-Konfidenzgrenze |
| Hurst-Exponent | ✅ fertig | Detrended Fluctuation Analysis (DFA) auf Zuwächsen |
| Variance Growth | ⏳ Stub | noch nicht implementiert |

## Ausführen

```bash
python main.py
```

Startet direkt die CLI (`ui/cli.py`). Ein Startmenü für alternative Oberflächen (GUI/Web) ist in `main.py` als Erweiterungspunkt vorgesehen, aber noch nicht aktiv.

## Export/Import

Ergebnisse lassen sich als JSON (vollständig, re-importierbar) oder CSV (Rohdaten) exportieren. JSON-Dateien lassen sich wieder in die History laden — Funktionsreferenzen (Übergangsfunktion etc.) werden dabei nicht rekonstruiert, der Eintrag dient nur der Anzeige/Analyse, nicht der Re-Simulation.

## Stand

~3600 Zeilen Python. Keine automatisierten Tests bisher — Verifikation der statistischen Methoden (ACF, DFA) erfolgte manuell gegen bekannte Referenzfälle (weißes Rauschen, reiner Random Walk, Mean-Reversion).