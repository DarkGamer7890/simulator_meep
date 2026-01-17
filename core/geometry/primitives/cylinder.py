from .base import GeometryPrimitive

class Cylinder(GeometryPrimitive):
    def __init__(self, radius, height=1e+20, axis=(0, 0, 1), **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.height = height
        self.axis = axis

    def to_meep(self):
        import meep as mp
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
        import pyvista as pv
        import numpy as np

        direction = np.array(self.axis, dtype=float)
        direction = direction / np.linalg.norm(direction)

        return pv.Cylinder(
            center=self.center,
            direction=direction,
            radius=self.radius,
            height=self.height
        )
    
    def bounding_volume(self):
        import numpy as np

        r = self.radius
        h = self.height
        return np.pi * r**2 * h