import trimesh
import meep as mp
import numpy as np

class Importer():
    def __init__(self, path, pitch):
        self.path = path
        self.pitch = pitch

    def voxelize_mesh(path, pitch, epsilon):
        mesh = trimesh.load_mesh(path)
        vox = mesh.voxelized(pitch)

        geometry = []

        for center in vox.points:
            geometry.append(
                mp.Block(
                    size=mp.Vector3(pitch, pitch, pitch),
                    center=mp.Vector3(*center),
                    material=mp.Medium(epsilon=epsilon)
                )
            )

        return geometry
    
    # def voxalization(self):

    #     mesh = trimesh.load_mesh(self.path)

    #     voxelized = mesh.voxelized(self.pitch)

    #     filled = voxelized.points

    #     print(len(filled))

    #     return filled