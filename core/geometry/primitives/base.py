from abc import ABC, abstractmethod
import numpy as np

class GeometryPrimitive(ABC):
    def __init__(self, center, epsilon):
        self.epsilon = epsilon
        self.center = np.array(center)

    @abstractmethod
    def to_meep(self):
        pass

    @abstractmethod
    def to_mesh(self):
        pass

    @abstractmethod
    def to_plot(self):
        pass
    
    def apply_transform(self, transform):
        print("transform called")
        tx, ty, tz = np.array(transform.translation)
        self.center[0] += tx
        self.center[1] += ty
        self.center[2] += tz
