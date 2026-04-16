import numpy as np

class Transform:
    def __init__(
        self,
        translation=(0, 0, 0),
        rotation=(0, 0, 0),   # radians, XYZ
        scale=(1, 1, 1)
    ):
        self.translation = np.array(translation, float)
        self.rotation = np.array(rotation, float)
        self.scale = np.array(scale, float)



    def matrix(self):
        tx, ty, tz = self.translation
        rx, ry, rz = self.rotation
        sx, sy, sz = self.scale

        # scale
        S = np.array([
            [sx, 0,  0,  0],
            [0,  sy, 0,  0],
            [0,  0,  sz, 0],
            [0,  0,  0,  1],
        ])

        # rotation (local axis)
        cx, cy, cz = np.cos([rx, ry, rz])
        sx_, sy_, sz_ = np.sin([rx, ry, rz])

        Rx = np.array([
            [1, 0,   0,    0],
            [0, cx, -sx_,  0],
            [0, sx_, cx,   0],
            [0, 0,   0,    1],
        ])

        Ry = np.array([
            [cy, 0, sy_, 0],
            [0,  1, 0,   0],
            [-sy_, 0, cy, 0],
            [0,  0, 0,   1],
        ])

        Rz = np.array([
            [cz, -sz_, 0, 0],
            [sz_, cz,  0, 0],
            [0,   0,   1, 0],
            [0,   0,   0, 1],
        ])

        R = Rz @ Ry @ Rx

        # translation
        T = np.array([
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0, 1],
        ])

        return T @ R @ S



    def combined_with(self, parent: "Transform") -> "Transform":
        return Transform(
            translation=parent.translation + self.translation,
            rotation=parent.rotation + self.rotation,
            scale=parent.scale * self.scale,
        )

    


    # def local_axes(self):
    #     R = self.matrix()[:3, :3]   # rotation+scale
    #     x = R[:, 0]
    #     y = R[:, 1]
    #     z = R[:, 2]
    #     return x, y, z


    
    # def translate(self, dx, dy, dz):
    #     self.translation += np.array([dx, dy, dz])



    # def rotate(self, rx, ry, rz):
    #     self.rotation += np.array([rx, ry, rz])



    # def scale_by(self, sx, sy, sz):
    #     self.scale *= np.array([sx, sy, sz])



    def clone(self):
        return Transform(
            translation=self.translation.copy(),
            rotation=self.rotation.copy(),
            scale=self.scale.copy()
        )
