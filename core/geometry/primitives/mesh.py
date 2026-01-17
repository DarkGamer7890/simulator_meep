from core.geometry.primitives.base import GeometryPrimitive

class GeometryMesh(GeometryPrimitive):

    def __init__(self, mesh, center, epsilon, pitch=0.1):  #removed offset
        super().__init__(center, epsilon)  #sending center instead of center = offset
        self.mesh = mesh
        self.pitch = pitch  



    def to_meep(self):
        import meep as mp

        """
        Convert mesh into Meep geometry via voxelization
        """
        # 1. Voxelize the mesh
        voxelized = self.mesh.voxelized(self.pitch)

        # 2. Get voxel centers
        points = voxelized.points

        geometry = []

        for x, y, z in points:
            geometry.append(
                mp.Block(
                    size=mp.Vector3(self.pitch, self.pitch, self.pitch),
                    center=mp.Vector3(
                        x + self.center[0],
                        y + self.center[1],
                        z + self.center[2],
                    ),
                    material=mp.Medium(epsilon=self.epsilon)
                )
            )

        return geometry



    def to_mesh(self):
        return self.mesh



    def to_plot(self):
        import pyvista as pv
        return pv.wrap(self.mesh)



    def apply_transform(self, transform):
        # move center
        print('mesh transform called')
        super().apply_transform(transform)

        # ALSO move the mesh itself
        M = transform.matrix()
        self.mesh = self.mesh.copy()
        self.mesh.apply_transform(M)

    def bounding_volume(self):
        dx, dy, dz = self.mesh.bounding_box.extents
        return dx * dy * dz