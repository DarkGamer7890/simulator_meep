from core.geometry.cad.cad_node import CADNode
from core.geometry.primitives.base import GeometryPrimitive


class CADScene:

    def __init__(self, name: str = "Scene"):
        self.name = name
        self.root = CADNode(name="root")



    def add_primitive(
        self,
        name: str,
        primitive: GeometryPrimitive,
        parent: CADNode | None = None
    ) -> CADNode:
        """
        Returns:
            CADNode created for this primitive
        """
        node = CADNode(name=name, geometry=primitive)

        if parent is None:
            self.root.add_child(node)
        else:
            parent.add_child(node)

        return node



    def get_root(self) -> CADNode:
        return self.root
