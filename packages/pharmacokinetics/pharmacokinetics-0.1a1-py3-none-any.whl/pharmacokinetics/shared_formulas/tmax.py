import math
from pharmacokinetics import _handlers

__all__ = [
    "calculateTmax",
]

def calculateTmax(**kwargs) -> float:
    """Calculates the time to reach maximum concentration (tmax).

    :param **kwargs:
        dose_interval: the interval between dose administration (optional)
        ka: absorption rate constant
        t12abs: absorption half-life (alternative to `ka`)
        ke: elimination rate constant
        t12: elimination half-life (alternative to `ke`)"""
    ka = _handlers._getPkConstantFromKwargs("ka", "t12abs", kwargs)
    ke = _handlers._getPkConstantFromKwargs("ke", "t12", kwargs)
    dose_interval = kwargs.get("dose_interval")
    isMultipleDoses = dose_interval != None
    if isMultipleDoses:
        _numerator = ka * (1 - math.e**(-ke*dose_interval))
        _denominator = ke * (1 - math.e**(-ka*dose_interval))
        return math.log(_numerator/_denominator) / (ka-ke)
    else:
        return 1 / (ka - ke) * math.log(ka/ke)
