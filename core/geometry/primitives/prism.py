import meep as mp
from .base import GeometryPrimitive

class Prism(GeometryPrimitive):
    def __init__(self, vertices, height, axis=(0, 0, 1), sidewall_angle=0, **kwargs):
        super().__init__(self, **kwargs)
        self.vertices = vertices
        self.height = height
        self.axis = axis
        self.sidewall_angle = sidewall_angle

    def to_meep(self):
        return mp.Prism(
            center=self.center,
            vertices=self.vertices,
            height=self.height,
            axis=self.axis,
            sidewall_angle=self.sidewall_angle,
            material=mp.Medium(epsilon=self.epsilon)
        )
    
    def to_mesh(self):
        return NotImplementedError
    
    def to_plot(self):
        return NotImplementedError