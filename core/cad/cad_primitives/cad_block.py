from .primitive import CADPrimitive
from core.geometry.primitives.block import Block

class CADBlock(CADPrimitive):
    def __init__(self, size, epsilon, **kwargs):
        super().__init__(**kwargs)
        self.size = size
        self.epsilon = epsilon

    def to_geometry(self):
        return [
            Block(
                size=self.size,
                center=self.center,
                epsilon=self.epsilon
            )
        ]
    
    def get_properties(self):
        return {
            "type": "block",
            "size_x": self.size[0],
            "size_y": self.size[1],
            "size_z": self.size[2],
            "epsilon": self.epsilon,
        }
    
    def set_property(self, name, value):
        if name == "size_x":
            self.size[0] = value
        elif name == "size_y":
            self.size[1] = value
        elif name == "size_z":
            self.size[2] = value
        elif name == "epsilon":
            self.epsilon = value
        else:
            raise AttributeError(f"No property {name}")
        

    def to_dict(self):
        return {
            "type": "block",
            "size": list(self.size),
            "epsilon": float(self.epsilon),
            "center": list(self.center),
        }

