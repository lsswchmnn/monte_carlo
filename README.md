# Monte Carlo Simulation
Implementierung für abstrakte Monte-Carlo Versuche

---

## Fragen und Probleme

- wie implementiere ich "Typ B"?
- wie sorge ich für saubere Auswahl aus A und B in der CLI?
- wie grenze ich die Übergangsfunktionen von einander ab? Evtl. Dict?
- Die maximal erlaubte Pfad- und stepanzahl muss für Typ B und C reduziert werden

---

## Übersicht der Typen

| Typ | Name / Paradigma | Run-Methode | Übergangsfunktionen | Zustand | Pfadbewertung | Interaktion zwischen Pfaden | Typische Anwendungen / Analogie | Besonderheiten |
|-----|-----------------|------------|-------------------|--------|---------------|----------------------------|-------------------------------|----------------|
| A   | Lokale stochastische Prozesse | `run` | lokal, additiv, Markov | Skalar | implizit / keine | nein | Random Walk, Drift, Finanz-Zeitreihen | Einfach, schnell, klassischer stochastischer Prozess |
| B   | Pfadbasierte Variationsprozesse | `run_variational` | global, kann Pfadkontext sehen | Vektor / Objekt | global, nach Pfadabschluss | nein | Path Integral, Action-Weighted Sampling, Large-Deviation-Sampling | Pfadgewichtung entscheidet Relevanz, globale Struktur entsteht |
| C   | Adaptive / interaktive Pfadprozesse | `run_adaptive` (hypothetisch) | adaptiv, reagiert auf Meta-Informationen und andere Pfade | Vektor / Objekt + Meta | global, dynamisch während Pfad | ja | Diffusion Monte Carlo, adaptive Optimierung, evolutionäre Trajektorien | Pfade beeinflussen sich gegenseitig, adaptive Steuerung, komplex, ressourcenintensiv |
