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

    def matrix(self) -> np.ndarray:
        """4x4 homogeneous transform"""
        tx, ty, tz = self.translation
        sx, sy, sz = self.scale
        rx, ry, rz = self.rotation

        # scale
        S = np.diag([sx, sy, sz, 1])

        # rotation (XYZ order)
        cx, cy, cz = np.cos([rx, ry, rz])
        sx_, sy_, sz_ = np.sin([rx, ry, rz])

        Rx = np.array([
            [1, 0, 0, 0],
            [0, cx, -sx_, 0],
            [0, sx_, cx, 0],
            [0, 0, 0, 1]
        ])

        Ry = np.array([
            [cy, 0, sy_, 0],
            [0, 1, 0, 0],
            [-sy_, 0, cy, 0],
            [0, 0, 0, 1]
        ])

        Rz = np.array([
            [cz, -sz_, 0, 0],
            [sz_, cz, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        R = Rz @ Ry @ Rx

        T = np.eye(4)
        T[:3, 3] = [tx, ty, tz]

        return T @ R @ S

    def __matmul__(self, other: "Transform") -> "Transform":
        """Compose transforms"""
        M = self.matrix() @ other.matrix()
        return Transform.from_matrix(M)

    @staticmethod
    def from_matrix(M: np.ndarray) -> "Transform":
        t = M[:3, 3]
        s = np.linalg.norm(M[:3, :3], axis=0)
        return Transform(translation=t, scale=s)
    
    def translate(self, dx, dy, dz):
        self.translation += np.array([dx, dy, dz])

    def rotate(self, rx, ry, rz):
        self.rotation += np.array([rx, ry, rz])

    def scale_by(self, sx, sy, sz):
        self.scale *= np.array([sx, sy, sz])

    def clone(self):
        return Transform(
            translation=self.translation.copy(),
            rotation=self.rotation.copy(),
            scale=self.scale.copy()
        )
