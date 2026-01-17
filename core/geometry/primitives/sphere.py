from .base import GeometryPrimitive


class Sphere(GeometryPrimitive):
    def __init__(self, radius, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius

    def to_meep(self):
        import meep as mp

        return mp.Sphere(
            radius=self.radius,
            center=mp.Vector3(*self.center),
            material=mp.Medium(epsilon=self.epsilon)
        )
    
    def to_mesh(self):
        raise NotImplementedError
    
    def to_plot(self):
        import pyvista as pv

        sphere = pv.Sphere(
            radius=self.radius,
            center=self.center.tolist()
        )
        return sphere
    
    def bounding_volume(self):
        import numpy as np
        return (4/3) * np.pi * self.radius**3