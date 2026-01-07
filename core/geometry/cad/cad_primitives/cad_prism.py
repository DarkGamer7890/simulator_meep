from .primitive import CADPrimitive
from core.geometry.primitives.prism import Prism

class CADPrism(CADPrimitive):
    def __init__(self, vertices, height, epsilon, **kwargs):
        super().__init__(**kwargs)
        self.vertices = vertices
        self.height = height
        self.epsilon = epsilon

    def to_geometry(self):
        return [
            Prism(
                vertices=self.vertices,
                height=self.height,
                center=self.center,
                epsilon=self.epsilon
            )
        ]
