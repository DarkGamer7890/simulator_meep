import meep as mp
from .base import GeometryPrimitive

class Cylinder(GeometryPrimitive):
    def __init__(self, radius, height=1e+20, axis=(0, 0, 1), **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.height = height
        self.axis = axis

    def to_meep(self):
        return mp.Cylinder(
            radius=self.radius,
            center = mp.Vector3(*self.center),
            height = self.height,
            axis = mp.Vector3(*self.axis),
            material = mp.Medium(epsilon=self.epsilon)
        )
    
    def to_mesh(self):
        return NotImplementedError
    
    def to_plot(self):
        return NotImplementedError