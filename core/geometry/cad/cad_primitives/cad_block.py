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
