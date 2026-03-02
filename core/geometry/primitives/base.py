from abc import ABC, abstractmethod
import numpy as np

class GeometryPrimitive(ABC):
    def __init__(self, epsilon, center=(0,0,0)):
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
        # # Apply translation to center (world space)
        # self.center = np.array(self.center) + np.array(transform.translation)
        
        # # Store rotation for reference (will be applied by VTK actor)
        # if not hasattr(self, 'rotation'):
        #     self.rotation = transform.rotation
        
        # # Store the world transform (will be used by viewer)
        # self.world_transform = transform
        
        # # Apply scale
        # if hasattr(self, 'radius'):
        #     self.radius *= transform.scale[0]
        # if hasattr(self, 'size'):
        #     self.size = tuple(s * scale for s, scale in zip(self.size, transform.scale))
        pass

    @abstractmethod
    def bounding_volume(self) -> float:
        pass
