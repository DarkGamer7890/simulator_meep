from dataclasses import dataclass
from typing import Tuple

@dataclass
class SimulationConfig:
    cell_size: Tuple[float, float, float]
    resolution: int
    pml: float
    frequency: float
    time: float

    source_center: Tuple[float, float, float]
    source_size: Tuple[float, float, float]
