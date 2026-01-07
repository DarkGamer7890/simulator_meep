import numpy as np
from core.geometry.geometry_builder import GeometryBuilder
from core.geometry.registry import register_geometry
from .primitives.sphere import Sphere
from .primitives.cylinder import Cylinder

@register_geometry("Luneburg Lens")
class LuneburgLens(GeometryBuilder):
    def __init__(self, radius, layers, cell_z):
        self.radius = radius
        self.layers = layers
        self.cell_z = cell_z

    def build(self):
        geometry = []
        radii = np.linspace(self.radius / self.layers, self.radius, self.layers)

        if self.cell_z > 0:

            for r in radii[::-1]:
                eps = 2 - (r / self.radius) ** 2
                geometry.append(
                    Sphere(
                        radius=r,
                        center=(0, 0, 0),
                        epsilon=eps
                    )
                )

        else:
            
            for r in radii[::-1]:
                eps = 2 - (r / self.radius) ** 2
                geometry.append(
                    Cylinder(
                        radius=r,
                        height=self.cell_z,
                        center=(0, 0, 0),
                        epsilon=eps
                    )
                )


        return geometry