from .primitive import CADPrimitive
from core.geometry.primitives.cylinder import Cylinder

class CADCylinder(CADPrimitive):
    def __init__(self, radius, height, axis, epsilon, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.height = height
        self.axis = axis
        self.epsilon = epsilon

    def to_geometry(self):
        return [
            Cylinder(
                radius=self.radius,
                height=self.height,
                axis=self.axis,
                center=self.center,
                epsilon=self.epsilon
            )
        ]

