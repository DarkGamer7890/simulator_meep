import trimesh

class Importer:

    def load(self, path: str) -> trimesh.Trimesh:
        print(f"path name: {path}")
        
        mesh = trimesh.load_mesh(path)
        if not isinstance(mesh, trimesh.Trimesh):
            raise ValueError("Only single-mesh files supported")
        return mesh
