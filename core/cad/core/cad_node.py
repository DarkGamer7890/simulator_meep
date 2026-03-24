from typing import List, Optional, Tuple
from core.cad.cad_primitives.primitive import CADPrimitive
# from core.geometry.primitives.base import GeometryPrimitive
from core.cad.core.geometry_build_result import GeometryBuildResult
from core.cad.core.transform import Transform

class CADNode:

    def __init__(
        self,
        name: str = "Node",
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



    # def to_geometry(self, parent_transform: Optional[Transform] = None) -> List[Tuple["CADNode", GeometryPrimitive, Transform]]:

    #     if parent_transform is None:
    #         world = self.transform.clone()
    #     else:
    #         world = self.transform.combined_with(parent_transform)

    #     geometries = []

    #     if self.cad_primitive is not None:
    #         geom_list = self.cad_primitive.to_geometry()
    #         for geom in geom_list:
    #             full_world_transform = Transform(
    #                 # translation=world_translation,
    #                 # rotation=world_rotation,
    #                 # scale=self.transform.scale

    #                 translation=world.translation,
    #                 rotation=world.rotation,
    #                 scale=world.scale
    #             )
    #             geometries.append((self, geom, full_world_transform))

    #     for child in self.children:
    #         world_transform = Transform(
    #             translation=world.translation,
    #             rotation=world.rotation,
    #             scale=world.scale
    #         )
    #         geometries.extend(child.to_geometry(world_transform))

    #     return geometries



    def get_world_transform(self, parent_transform):
        if parent_transform is None:
            return self.transform.clone()
        return self.transform.combined_with(parent_transform)



    def to_geometry(self, parent_transform=None):
        world_transform = self.get_world_transform(parent_transform)
    
        result = GeometryBuildResult()
    
        if self.cad_primitive:
            geometry_list = self.cad_primitive.to_geometry()
    
            for geom in geometry_list:
                result.additions.append((self, geom, world_transform))
    
        for child in self.children:
            child_result = child.to_geometry(world_transform)
            result.merge(child_result)
    
        return result



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
    

    def to_dict(self):
        return {
            "type": "cad",
            "name": self.name,
            "transform": {
                "translation": list(self.transform.translation),
                "rotation": list(self.transform.rotation),
                "scale": list(self.transform.scale)
            },
            "primitive": self.cad_primitive.to_dict() if self.cad_primitive else None,
            "children": [child.to_dict() for child in self.children]
        }