import math
from pharmacokinetics import _handlers

__all__ = [
    "calculateCmax",
]

def calculateCmax(initial_concentration: float, dose_interval: float, **kwargs) -> float:
    """Calculates the maximum concentration (cmax).

    :param initial_concentration: initial administered concentration
    :param dose_interval: interval between administered doses
    :param **kwargs:
        ke: elimination rate constant
        t12: elimination half-life (alternative to `ke`)"""
    ke = _handlers._getPkConstantFromKwargs("ke", "t12", kwargs)
    return initial_concentration / (1 - math.e**(-ke * dose_interval))
