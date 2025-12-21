# monte_carlo_simulation
Implementierung für abstrakte Monte-Carlo Versuche

---

- Die Simulation weiß nicht, was die FUnktionen für Übergänge und Startzustand genau machen. Sie ruft diese einfach nur auf
- Übergänge und Startzustand sind als Callables definiert und lassen sich nicht über die CLI auswählen (da Overkill)
- Jeder Zustand ist ein Skalar, jeder Pfad eine Reihe von Floats
