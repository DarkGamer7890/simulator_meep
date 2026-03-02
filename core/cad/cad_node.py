from typing import List, Optional, Tuple
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



    # def to_geometry(          
    #     self,
    #     parent_transform: Optional[Transform] = None
    # ) -> List[Tuple["CADNode", GeometryPrimitive]]:
        
    #     # --- WORLD translation ---
    #     if parent_transform is None:
    #         world_translation = self.transform.translation.copy()
    #         world_rotation = self.transform.rotation.copy()
    #     else:
    #         world_translation = (
    #             parent_transform.translation + self.transform.translation
    #         )
    #         world_rotation = (
    #             parent_transform.rotation + self.transform.rotation
    #         )
    
    #     # build a NEW transform (NO matrices)
    #     current = Transform(
    #         translation=world_translation,
    #         rotation=world_rotation,
    #         scale=self.transform.scale
    #     )
    
    #     geometries = []
    
    #     if self.cad_primitive is not None:
    #         geom_list = self.cad_primitive.to_geometry()
    #         for geom in geom_list:
    #             geom.apply_transform(current)
    #             geometries.append((self, geom))
    
    #     for child in self.children:
    #         geometries.extend(
    #             child.to_geometry(current)
    #         )
    
    #     return geometries




    def to_geometry(self, parent_transform: Optional[Transform] = None) -> List[Tuple["CADNode", GeometryPrimitive, Transform]]:

        import numpy as np

        if parent_transform is None:
            world_translation = self.transform.translation.copy()
            world_rotation = self.transform.rotation.copy()
        else:
            world_translation = parent_transform.translation + self.transform.translation
            world_rotation = parent_transform.rotation + self.transform.rotation

        geometries = []

        if self.cad_primitive is not None:
            geom_list = self.cad_primitive.to_geometry()
            for geom in geom_list:
                full_world_transform = Transform(
                    translation=world_translation,
                    rotation=world_rotation,
                    scale=self.transform.scale
                )
                geometries.append((self, geom, full_world_transform))

        for child in self.children:
            world_transform = Transform(
                translation=world_translation,
                rotation=world_rotation,
                scale=self.transform.scale
            )
            geometries.extend(child.to_geometry(world_transform))

        return geometries




    def clone_recursive(self):
        new_node = CADNode(
            name=f"{self.name}_copy",
            cad_primitive=self.cad_primitive.clone() if self.cad_primitive else None,
            transform=self.transform.clone()
        )

        for child in self.children:
            new_child = child.clone_recursive()
            new_node.add_child(new_child)

        return new_node