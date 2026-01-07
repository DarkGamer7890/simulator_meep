from typing import List, Optional
from .cad_primitives.primitive import CADPrimitive
from core.geometry.primitives.base import GeometryPrimitive
from .transform import Transform

class CADNode:

    def __init__(
        self,
        name: str,
        cad_primitive: Optional["CADPrimitive"] = None,
        transform: Optional[Transform] = None
    ):
        self.name = name
        self.cad_primitive = cad_primitive   
        self.transform = transform or Transform() 
        self.children: List["CADNode"] = []



    def add_child(self, node: "CADNode"):
        self.children.append(node)



    def flatten(self) -> List["CADNode"]:

        nodes = [self]
        for child in self.children:
            nodes.extend(child.flatten())
        return nodes



    def to_geometry(          
        self,
        parent_transform: Optional[Transform] = None
    ) -> List[GeometryPrimitive]:

        current = self.transform
        if parent_transform is not None:
            current = parent_transform @ self.transform

        geometries: List[GeometryPrimitive] = []

        if self.cad_primitive is not None:
            geom_list = self.cad_primitive.to_geometry()

            for geom in geom_list:
                geom.apply_transform(current)
                geometries.append(geom)

        for child in self.children:
            geometries.extend(
                child.to_geometry(current)
            )

        return geometries
