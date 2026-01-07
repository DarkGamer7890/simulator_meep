import meep as mp
from .base import GeometryPrimitive

class Block(GeometryPrimitive):
    def __init__(self, size, e1=(1, 0, 0), e2=(0, 1, 0), e3=(0, 0, 1), **kwargs):
        super().__init__(**kwargs)
        self.size=size
        self.e1=e1
        self.e2=e2
        self.e3=e3

    def to_meep(self):
        return mp.Block(
            size=mp.Vector3(*self.size),
            e1=self.e1,
            e2=self.e2,
            e3=self.e3,
            center=mp.Vector3(*self.center),
            material=mp.Medium(epsilon=self.epsilon)
        )
    
    def to_mesh(self):
        return NotImplementedError
    
    def to_plot(self):
        return NotImplementedError
