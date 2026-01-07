from typing import List
from core.geometry.primitives.base import GeometryPrimitive
from .cad_node import CADNode
from core.geometry.registry import register_geometry

@register_geometry("CAD")
class CADBuilder:

    def __init__(self, root_node: CADNode):
        self.root_node = root_node

    def build(self) -> List[GeometryPrimitive]:
        return self.root_node.to_geometry()
