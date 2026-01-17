from .base import GeometryPrimitive

class Block(GeometryPrimitive):
    def __init__(self, size, e1=(1, 0, 0), e2=(0, 1, 0), e3=(0, 0, 1), **kwargs):
        super().__init__(**kwargs)
        self.size=size
        self.e1=e1
        self.e2=e2
        self.e3=e3

    def to_meep(self):
        import meep as mp
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
        import pyvista as pv
        sx, sy, sz = self.size

        return pv.Box(
            bounds=(
                self.center[0] - sx/2, self.center[0] + sx/2,
                self.center[1] - sy/2, self.center[1] + sy/2,
                self.center[2] - sz/2, self.center[2] + sz/2,
            )
        )
    
    def bounding_volume(self):
        sx, sy, sz = self.size  
        return sx * sy * sz