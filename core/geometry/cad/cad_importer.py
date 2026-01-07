from core.importer import Importer
from core.geometry.cad.cad_primitives.cad_mesh import CADMesh
from core.geometry.registry import register_geometry

@register_geometry("Import")
class CADImporter:

    def __init__(self, **kwargs):
        self.importer = Importer()
        self.path = kwargs["path"]
        self.pitch = kwargs["pitch"]
        self.epsilon = kwargs["epsilon"]


    def build(self):   #not taking offset=(0,0,0)
        mesh = self.importer.load(self.path)
        return CADMesh(mesh=mesh, pitch=self.pitch, epsilon=self.epsilon) #not sending offset
