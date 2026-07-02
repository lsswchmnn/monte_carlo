from   core.config   import SimConfig
from   pathlib      import Path
from   datetime     import datetime
import numpy        as     np
import json
import csv
#=========================================================================
# Exporter
# Verantwortlichkeit: Simulationsergebnisse in verschiedene Formate
# exportieren. Wird lazy vom Controller gehalten.
#=========================================================================

class Exporter:

    DEFAULT_DIR = Path.home() / "Downloads"

#-------------------------------------------------------------------------
# Entry-Point

    def export(self, result: list, config: SimConfig,
               fmt: str = "json", output_dir: Path | None = None) -> Path:
        '''
        Exportiert ein Simulationsergebnis im gewählten Format.
        Gibt den Pfad der erzeugten Datei zurück.
        Unterstützte Formate: 'json', 'csv'
        '''
        exporters = {
            "json": self._export_json,
            "csv":  self._export_csv,
        }

        fn = exporters.get(fmt.lower())
        if fn is None:
            raise ValueError(
                f"Unknown export format: '{fmt}'. "
                f"Supported: {list(exporters.keys())}"
            )

        out_dir = Path(output_dir) if output_dir else self.DEFAULT_DIR
        out_dir.mkdir(parents=True, exist_ok=True)

        filename = self._build_filename(config, fmt)
        filepath = out_dir / filename

        fn(result, config, filepath)
        return filepath

    @staticmethod
    def supported_formats() -> list[str]:
        return ["json", "csv"]

#-------------------------------------------------------------------------
# Private Export-Funktionen

    def _export_json(self, result: list, config: SimConfig, filepath: Path) -> None:
        '''
        Exportiert Rohdaten und Metadaten als JSON.
        np.ndarray-Werte werden zu Listen konvertiert.
        '''
        data = {
            "meta": self._build_meta(config),
            "paths": [
                [v.tolist() if isinstance(v, np.ndarray) else v for v in path]
                for path in result
            ],
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _export_csv(self, result: list, config: SimConfig, filepath: Path) -> None:
        '''
        Exportiert Rohdaten als CSV.
        1D: eine Spalte pro Pfad, eine Zeile pro Schritt.
        ND: eine Spaltengruppe pro Pfad (path_N_dim_M), eine Zeile pro Schritt.
        Metadaten als Kommentar-Header.
        '''
        meta = self._build_meta(config)
        is_nd = config.dimensionality == "nd"
        n_paths = len(result)
        n_steps = len(result[0]) if result else 0

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # Metadaten als Kommentar-Header
            for key, value in meta.items():
                writer.writerow([f"# {key}: {value}"])
            writer.writerow([])

            # Spaltenheader
            if is_nd:
                n_dim = config.n_dimensions
                header = [
                    f"path_{p}_dim_{d}"
                    for p in range(n_paths)
                    for d in range(n_dim)
                ]
            else:
                header = [f"path_{p}" for p in range(n_paths)]
            writer.writerow(header)

            # Datenpunkte
            for step in range(n_steps):
                if is_nd:
                    row = [
                        result[p][step][d]
                        for p in range(n_paths)
                        for d in range(config.n_dimensions)
                    ]
                else:
                    row = [result[p][step] for p in range(n_paths)]
                writer.writerow(row)

#-------------------------------------------------------------------------
# Hilfsmethoden

    @staticmethod
    def _build_meta(config: SimConfig) -> dict:
        return {
            "transition":       config.transition_name,
            "process_type":     config.process_type,
            "dimensionality":   config.dimensionality,
            "n_dimensions":     config.n_dimensions,
            "seed":             config.seed,
            "n_paths":          config.n_paths,
            "n_steps":          config.n_steps,
            "step_size":        config.step_size,
            "exported_at":      datetime.now().isoformat(timespec="seconds"),
        }

    @staticmethod
    def _build_filename(config: SimConfig, format: str) -> str:
        '''Generiert einen Dateinamen aus Config-Daten.'''
        transition = (config.transition_name or "unknown").lower().replace(" ", "_")
        dim = f"{config.n_dimensions}d" if config.dimensionality == "nd" else "1d"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{transition}_{dim}_seed{config.seed}_{config.n_paths}p_{config.n_steps}s_{timestamp}.{format}"
    
#-------------------------------------------------------------------------
# Import

    def import_result(self, filepath) -> tuple:
        '''
        Liest eine exportierte JSON-Datei und rekonstruiert result und config.
        Funktionsreferenzen (transition_fn, start_state_fn) werden nicht
        wiederhergestellt — der Eintrag ist für Anzeige und Analyse gedacht,
        nicht für Re-Simulation.
        '''
        filepath = Path(filepath)
 
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
 
        if filepath.suffix.lower() != ".json":
            raise ValueError(f"Only JSON import is supported, got: '{filepath.suffix}'")
 
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
 
        if "meta" not in data or "paths" not in data:
            raise ValueError("Invalid file format: missing 'meta' or 'paths' key.")
 
        meta   = data["meta"]
        result = self._restore_result(data["paths"], meta)
        config = self._restore_config(meta)
 
        return result, config
 
    @staticmethod
    def _restore_result(paths: list, meta: dict) -> list:
        '''ND-Einträge (Listen) werden zu np.ndarray konvertiert.'''
        if meta.get("dimensionality") == "nd":
            return [[np.array(step) for step in path] for path in paths]
        return paths
 
    @staticmethod
    def _restore_config(meta: dict):
        '''Rekonstruiert SimConfig-Snapshot. Funktionsreferenzen bleiben None.''' 
        SC = SimConfig
        cfg = SC(
            seed      = meta.get("seed", 42),
            n_steps   = meta.get("n_steps", 0),
            n_paths   = meta.get("n_paths", 0),
            step_size = meta.get("step_size", 1.0),
        )
        cfg.dimensionality   = meta.get("dimensionality", "1d")
        cfg.n_dimensions     = meta.get("n_dimensions", 1)
        cfg.process_type     = meta.get("process_type")
        cfg.transition_name  = meta.get("transition")
        cfg.start_state_name = None
        cfg.transition_fn    = None
        cfg.start_state_fn   = None
        return cfg