from .primitive import CADPrimitive
from core.geometry.primitives.prism import Prism

class CADPrism(CADPrimitive):
    def __init__(self, vertices, height, epsilon, axis=(0,0,1), **kwargs):
        super().__init__(**kwargs)
        self.vertices = vertices
        self.height = height
        self.axis = axis
        self.epsilon = epsilon

    def to_geometry(self):
        return [
            Prism(
                vertices=self.vertices,
                height=self.height,
                axis=self.axis,
                center=self.center,
                epsilon=self.epsilon
            )
        ]
    
    def get_properties(self):
        return {
            "type": "prism",
            "height": self.height,
            "epsilon": self.epsilon,
            "num_vertices": len(self.vertices),
        }
    
    def to_dict(self):
        return {
            "type": "prism",
            "height": float(self.height),
            "epsilon": float(self.epsilon),
            "axis": list(self.axis),
            "vertices": list(self.vertices),
            "center": list(self.center),
        }

