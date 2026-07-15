from   dataclasses import dataclass
import numpy       as     np
#=========================================================================
@dataclass
class ErgodicityResult:
    ensemble_mean       : float
    time_mean_mean      : float
    time_mean_std       : float
    time_means          : np.ndarray
    ergodic_heuristic   : bool
 
@dataclass
class AutoCorrelationResult:
    lags                : np.ndarray
    acf_mean            : np.ndarray
    acf_std             : np.ndarray
    significant_lags    : np.ndarray
    confidence_bound    : float

@dataclass
class HurstExponentResult:
    scales            : np.ndarray
    fluctuation_mean  : np.ndarray
    hurst_per_path    : np.ndarray
    hurst_mean        : float
    hurst_std         : float
    r_squared_mean    : float
    on_increments     : bool

@dataclass
class VarianceGrowthResult:
    times            : np.ndarray
    variance         : np.ndarray
    growth_exponent  : float
    r_squared        : float
    diffusive_type   : str