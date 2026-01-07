from .base import GeometryPrimitive
import meep as mp

class Sphere(GeometryPrimitive):
    def __init__(self, radius, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius

    def to_meep(self):
        return mp.Sphere(
            radius=self.radius,
            center=mp.Vector3(*self.center),
            material=mp.Medium(epsilon=self.epsilon)
        )
    
    def to_mesh(self):
        raise NotImplementedError
    
    def to_plot(self):
        raise NotImplementedError