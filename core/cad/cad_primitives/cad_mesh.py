from .primitive import CADPrimitive
from core.geometry.primitives.mesh import GeometryMesh

class CADMesh(CADPrimitive):   # removed offset

    def __init__(self, mesh, pitch, epsilon, **kwargs):
        super().__init__(**kwargs)
        self.mesh = mesh
        self.pitch = pitch
        self.epsilon = epsilon



    def to_geometry(self):
        return [
            GeometryMesh(
                mesh=self.mesh,
                center=self.center,
                epsilon=self.epsilon,
                pitch=self.pitch
            )
        ]
    
    def get_properties(self):
        raise NotImplementedError
    

    def to_dict(self):
        raise NotImplementedError
        
