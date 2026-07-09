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
    pass

@dataclass
class HurstExponentResult:
    pass

@dataclass
class VarianceGrowthResult:
    pass