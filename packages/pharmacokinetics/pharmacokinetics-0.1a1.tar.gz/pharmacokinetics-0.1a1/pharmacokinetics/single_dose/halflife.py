import math

__all__ = [
    "halflifeFromDoses",
]

def halflifeFromDoses(initial_dose, remaining_dose, time_elapsed) -> float:
    """Calculates the half-life based on the dose remaining after a specific time.

    :param initial_dose: the initial dose administered
    :param remaining_dose: the remaining dose at the specified time
    :param time_elapsed: the time elapsed since the drug has reached peak concentrations"""
    halfLivesPassed = math.log10(remaining_dose/initial_dose) / math.log10(0.5)
    return time_elapsed / halfLivesPassed
