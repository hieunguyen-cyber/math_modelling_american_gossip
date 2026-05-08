from typing import Set

def spread_factor(reached: Set[int], victim_degree: int) -> float:
    """Compute spread factor f = nf / k where nf is number of reached friends and k is degree."""
    if victim_degree == 0:
        return 0.0
    nf = len(reached)
    return nf / victim_degree

def spreading_time(history: list) -> int:
    """Compute spreading time tau as minimum timesteps to reach final frontier."""
    if not history:
        return 0
    # history is list of frontiers per timestep; last non-empty frontier index
    last_idx = len(history) - 1
    return last_idx
