from .primitive import CADPrimitive
from core.geometry.primitives.sphere import Sphere

class CADSphere(CADPrimitive):
    def __init__(self, radius, epsilon, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.epsilon = epsilon

    def to_geometry(self):
        return [
            Sphere(
                radius=self.radius,
                center=self.center,
                epsilon=self.epsilon
            )
        ]

