from   core.config      import SimConfig
from   core.history     import HistoryEntry
from   analyze.results  import ErgodicityResult, AutoCorrelationResult, HurstExponentResult, VarianceGrowthResult
import numbers
#=========================================================================
# Textgenerator
# Verantwortlichkeit: reine Formatierungs-Funktionen für Simulations- und
# Analyseergebnisse. Kein Drucken, kein UI-Bezug (kein print_heading, kein
# enter_continue) -- nur fertige Strings, die von einer beliebigen Ober-
# fläche (CLI, später Web, PDF-Export) konsumiert werden können.
# Analog zu HELP_REGISTRY/print_help, nur für dynamische statt statische
# Inhalte.
#=========================================================================
# Simulationseinstellungen

def format_simulation_settings(config: SimConfig) -> str:
    '''Formatiert die aktuellen SimConfig-Einstellungen.'''
    return (
        f"  Dimensions:   {config.n_dimensions}\n"
        f"  Start State:  {config.start_state_name}\n"
        f"  Transition:   {config.transition_name}\n"
        f"  Process Type: {config.process_type}\n"
        f"  Paths:        {config.n_paths}\n"
        f"  Steps:        {config.n_steps}\n"
        f"  Step Size:    {config.step_size}\n"
        f"  Seed:         {config.seed}\n"
        f"  Datapoints:   {config.datapoint_count():_}"
    )

def format_transition_details(config: SimConfig, desc: str, params: dict) -> str:
    '''Formatiert Name, Beschreibung und Parameter der aktuellen Übergangsfunktion.'''
    lines = [
        f"Transition: {config.transition_name}",
        f"\n{desc}",
        format_params(params),
    ]
    return "\n".join(lines)

def format_params(params: dict) -> str:
    '''Formatiert eine params-Dict (Typ/Default/Range/Beschreibung pro Parameter).'''
    if not params:
        return "No parameters defined."

    lines = ["\nParams:"]
    for name, spec in params.items():
        p_type  = spec.get("type", "unknown")
        default = spec.get("default", "n/a")
        min_v   = spec.get("min", "n/a")
        max_v   = spec.get("max", "n/a")
        desc    = spec.get("desc", "")

        lines.append(f"\n {name.capitalize()}")
        lines.append(f"  Type    : {p_type}")
        lines.append(f"  Default : {default}")
        if min_v is not None and max_v is not None:
            lines.append(f"  Range   : [{min_v}, {max_v}]")
        lines.append(f"  Desc    : {desc}")

    return "\n".join(lines)

#-------------------------------------------------------------------------
# Ergebnisse

def format_result_summary(entry: HistoryEntry) -> str:
    '''Formatiert eine Zusammenfassung eines History-Eintrags (Settings, Dauer, erste Werte).'''
    lines = [format_simulation_settings(entry.config)]

    if entry.calc_time:
        lines.append(f"  Duration:     {entry.calc_time:.4f}s")

    lines.append("")
    if entry.result:
        values_rounded = _round_nested(entry.result[0][:10])
        lines.append(f"  First path (first 10 values): {values_rounded}")
    else:
        lines.append("  First path (first 10 values): —")

    return "\n".join(lines)

def format_result_name(config: SimConfig) -> str:
    '''Einzeiliger Name eines Ergebnisses, z.B. für Auswahllisten.'''
    return f"{config.transition_name} | {config.n_paths} paths × {config.n_steps} steps | seed {config.seed}"

#-------------------------------------------------------------------------
# Ergodizität

def format_ergodicity(result: ErgodicityResult) -> str:
    return (
        f"Ensemble Mean:       {result.ensemble_mean:.4f}\n"
        f"Mean of Time Means:  {result.time_mean_mean:.4f}\n"
        f"Std of Time Means:   {result.time_mean_std:.4f}\n"
        f"Number of Paths:     {len(result.time_means)}"
    )

def format_ergodicity_heuristic(result: ErgodicityResult) -> str:
    result_str = "ergodic" if result.ergodic_heuristic else "not ergodic"
    return f"\nProcess is {result_str} (heuristic)."

#-------------------------------------------------------------------------
# Autokorrelation

def format_autocorrelation(result: AutoCorrelationResult) -> str:
    lines = []
    for lag, val in zip(result.lags, result.acf_mean):
        marker = " *" if lag > 0 and abs(val) > result.confidence_bound else ""
        lines.append(f"  Lag {lag:>3}: {val:+.4f}{marker}")
    lines.append(f"\n  95% Confidence Bound: ±{result.confidence_bound:.4f}")
    return "\n".join(lines)

def format_autocorrelation_significance(result: AutoCorrelationResult) -> str:
    n_sig = int(result.significant_lags.sum())
    if n_sig == 0:
        return "\nNo significant autocorrelation detected (consistent with white noise)."
    sig_lags = result.lags[result.significant_lags]
    return f"\nSignificant autocorrelation at {n_sig} lag(s): {list(sig_lags)}"

#-------------------------------------------------------------------------
# Hurst-Exponent (DFA)

def format_hurst_exponent(result: HurstExponentResult) -> str:
    lines = []
    for s, f in zip(result.scales, result.fluctuation_mean):
        lines.append(f"  Window {s:>5}: F(s) = {f:.4f}")
    lines.append(f"\n  Hurst Exponent (path-mean): {result.hurst_mean:.4f}")
    lines.append(f"  Std across paths:           {result.hurst_std:.4f}")
    lines.append(f"  Fit quality (mean R²):      {result.r_squared_mean:.4f}")
    lines.append(f"  Computed on:                {'increments' if result.on_increments else 'raw levels'}")
    return "\n".join(lines)

def format_hurst_interpretation(result: HurstExponentResult) -> str:
    H = result.hurst_mean
    if H < 0.45:
        interpretation = "Anti-persistent (mean-reverting): increments tend to reverse direction."
    elif H > 0.55:
        interpretation = "Persistent (trending): increments tend to continue in the same direction."
    else:
        interpretation = "Close to 0.5: consistent with uncorrelated increments (random walk)."

    lines = [f"\n  H ≈ {H:.4f}  ->  {interpretation}"]
    if result.r_squared_mean < 0.95:
        lines.append(f"  Note: R² = {result.r_squared_mean:.4f} is relatively low — "
                      f"the scaling may not be well-described by a single exponent.")
    return "\n".join(lines)

#-------------------------------------------------------------------------
# Varianzwachstum

def format_variance_growth(result: VarianceGrowthResult) -> str:
    lines = []
    for t, v in zip(result.times, result.variance):
        lines.append(f"  t = {t:>5}: Var(t) = {v:.4f}")
    lines.append(f"\n  Growth Exponent (γ): {result.growth_exponent:.4f}")
    lines.append(f"  Fit quality (R²):     {result.r_squared:.4f}")
    lines.append(f"  Classification:        {result.diffusive_type}")
    return "\n".join(lines)

def format_variance_growth_interpretation(result: VarianceGrowthResult) -> str:
    gamma = result.growth_exponent
    lines = [f"\n  γ ≈ {gamma:.4f}  ->  {result.diffusive_type.capitalize()}"]

    if result.diffusive_type == "diffusive":
        lines.append("  Variance grows approximately linearly — consistent with "
                      "normal (Fickian) diffusion, e.g. an uncorrelated random walk.")
    elif result.diffusive_type == "subdiffusive":
        lines.append("  Variance grows slower than linear — consistent with a "
                      "restoring force (e.g. mean reversion) limiting long-term spread.")
    else:
        lines.append("  Variance grows faster than linear — consistent with rare, "
                      "large jumps (e.g. heavy-tailed transitions) or persistent trending.")

    if result.r_squared < 0.8:
        lines.append(f"  Note: R² = {result.r_squared:.4f} is low — the growth "
                      f"likely doesn't follow a single power law over this range.")
    return "\n".join(lines)

#-------------------------------------------------------------------------
# Hilfsfunktionen (privat)

def _round_nested(value, digits: int = 4):
    '''Rundet verschachtelte Ergebnisse auf n Nachkommastellen.'''
    if isinstance(value, numbers.Number):
        return round(value, digits)
    return [_round_nested(v, digits) for v in value]