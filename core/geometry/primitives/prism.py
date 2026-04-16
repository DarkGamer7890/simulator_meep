from .base import GeometryPrimitive

class Prism(GeometryPrimitive):
    def __init__(self, vertices, height, axis=(0, 0, 1), sidewall_angle=0, **kwargs):
        super().__init__(**kwargs)
        self.vertices = vertices
        self.height = height
        self.axis = axis
        self.sidewall_angle = sidewall_angle

    def to_meep(self):
        import meep as mp


        meep_vertices = [mp.Vector3(v[0], v[1], v[2]) for v in self.vertices]
    

        meep_axis = mp.Vector3(self.axis[0], self.axis[1], self.axis[2])
        return mp.Prism(
            center=self.center,
            vertices=meep_vertices,
            height=self.height,
            axis=meep_axis,
            sidewall_angle=self.sidewall_angle,
            material=mp.Medium(epsilon=self.epsilon)
        )
    
    def to_mesh(self):
        return NotImplementedError
    
    def to_plot(self):
        import pyvista as pv
        import numpy as np


        base_verts = np.array(self.vertices, dtype=float)
        n = len(base_verts)
    
        # ensure 3d vertices
        if base_verts.shape[1] == 2:
            base_verts = np.c_[base_verts, np.zeros(n)]
        elif base_verts.shape[1] != 3:
            raise ValueError("Prism vertices must be 2D or 3D")
    
        # center base polygon
        centroid = base_verts.mean(axis=0)
        base_verts -= centroid
    
        #axis
        axis = np.array(self.axis, dtype=float)
        axis = axis / np.linalg.norm(axis)
    
        half = axis * (self.height / 2.0)
    
        bottom = base_verts - half
        top = base_verts + half
    
        points = np.vstack([bottom, top])
    
        faces = []
    
        # bottom face (reverse winding)
        faces.append(n)
        faces.extend(range(n - 1, -1, -1))
    
        # top face
        faces.append(n)
        faces.extend(range(n, 2 * n))
    
        # side faces
        for i in range(n):
            j = (i + 1) % n
            faces.extend([4, i, j, j + n, i + n])
    
        mesh = pv.PolyData(points, faces)
    
        # final transform
        mesh.translate(self.center, inplace=True)
    
        return mesh
    
    def bounding_volume(self):
        import numpy as np

        pts = np.array(self.vertices)
        x = pts[:, 0]
        y = pts[:, 1]

        base_area = 0.5 * abs(
            np.dot(x, np.roll(y, -1)) -
            np.dot(y, np.roll(x, -1))
        )

        return base_area * self.height