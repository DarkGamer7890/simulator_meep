import trimesh

class importer():
    def __init__(self, path, pitch):
        self.path = path
        self.pitch = pitch
    
    def voxalization(self):

        mesh = trimesh.load_mesh(self.path)

        voxelized = mesh.voxelized(self.pitch)

        filled = voxelized.points

        print(len(filled))

        return filled