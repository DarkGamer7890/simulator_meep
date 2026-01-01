import meep as mp
import numpy as np

class Geometry():
    def __init__(self, radius, layers, cell_z):
        self.radius = radius
        self.layers = layers
        self.cell_z = cell_z

    def luneburg_lens(self):
        geometry = []
        radii = np.linspace(self.radius / self.layers, self.radius, self.layers)

        if self.cell_z > 0:

            for r in radii[::-1]:
                eps = 2 - (r / self.radius) ** 2
                geometry.append(
                    mp.Sphere(
                        radius=r,
                        center=mp.Vector3(),
                        material=mp.Medium(epsilon=eps)
                    )
                )

        else:
            
            for r in radii[::-1]:
                eps = 2 - (r / self.radius) ** 2
                geometry.append(
                    mp.Cylinder(
                        radius=r,
                        height=self.cell_z,
                        center=mp.Vector3(),
                        material=mp.Medium(epsilon=eps)
                    )
                )


        return geometry