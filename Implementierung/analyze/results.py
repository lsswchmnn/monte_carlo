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
    pass

@dataclass
class VarianceGrowthResult:
    pass