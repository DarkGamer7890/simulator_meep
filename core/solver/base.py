from abc import ABC, abstractmethod

class BaseSolver(ABC):
    def __init__(self, cell_size, resolution, pml, source_center, source_size, frequency, geometry, time):
        self.cell_size = cell_size
        self.resolution = resolution
        self.pml = pml
        self.source_center = source_center
        self.source_size = source_size
        self.frequency = frequency
        self.geometry = geometry
        self.time = time

    @abstractmethod
    def run(self):
        pass


