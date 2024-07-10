import math
from pharmacokinetics import _handlers

__all__ = [
    "concentrationAtTime",
]

def concentrationAtTime(dose: float, **kwargs) -> float:
    """Calculates the concentration at a specific time (oral administration).

    :param dose: the dosage administered
    :param **kwargs:
        vd: volume of distribution (default 1)
        bioavailability: fraction of drug absorbed into the systemic circulation (default 1)
        ke: elimination rate constant
        t12: elimination half-life (alternative to `ke`)
        ka: absorption rate constant
        t12abs: absorption half-life
        time_elapsed: time since drug administration
        dose_interval: interval between doses (optional)"""
    ke = _handlers._getPkConstantFromKwargs("ke", "t12", kwargs)
    ka = _handlers._getPkConstantFromKwargs("ka", "t12abs", kwargs)
    vd = kwargs.get("vd", 1)
    bioavailability = kwargs.get("bioavailability", 1)
    time_elapsed = kwargs.get("time_elapsed")
    dose_interval = kwargs.get("dose_interval")
    _lFrac = (bioavailability * dose * ka) / (vd * (ka - ke))
    if dose_interval != None:
        _rFrac1 = math.e**(-ke * time_elapsed) / (1 - math.e**(-ke * dose_interval))
        _rFrac2 = math.e**(-ka * time_elapsed) / (1 - math.e**(-ka * dose_interval))
        return _lFrac * (_rFrac1 - _rFrac2)
    return _lFrac * (math.e**(-ke*time_elapsed) - math.e**(-ka * time_elapsed))
