from .cad_node import CADNode
from .boolean_node import BooleanNode
from core.cad.cad_primitives.cad_block import CADBlock
from core.cad.cad_primitives.cad_cylinder import CADCylinder
from core.cad.cad_primitives.cad_sphere import CADSphere
from core.cad.cad_primitives.cad_prism import CADPrism

from core.geometry.primitives.base import GeometryPrimitive
import json


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

        node = CADNode(name=name, cad_primitive=primitive)

        if parent is None:
            self.root.add_child(node)
        else:
            parent.add_child(node)

        return node

    def get_root(self) -> CADNode:
        return self.root

    def set_root(self, root: CADNode):
        self.root = root

    # save

    def save_scene(self, filepath):
        data = self.root.to_dict()
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

    # load

    @staticmethod
    def load_scene(filepath):
        with open(filepath, "r") as f:
            data = json.load(f)

        root = CADScene.from_dict(data)

        scene = CADScene()
        scene.set_root(root)

        return scene

    

    @staticmethod
    def from_dict(data):

        if data["type"] == "cad":
            node = CADNode(name=data["name"])

            # Transform (translation + rotation + scale)
            node.transform.translation = tuple(data["transform"]["translation"])
            node.transform.rotation = tuple(data["transform"]["rotation"])
            node.transform.scale = tuple(data["transform"]["scale"])

            # Primitive
            if data["primitive"]:
                node.cad_primitive = CADScene.primitive_from_dict(data["primitive"])

            # Children
            for child_data in data["children"]:
                child = CADScene.from_dict(child_data)
                node.add_child(child)

            return node

        elif data["type"] == "boolean":
            node = BooleanNode(data["operation"])

            for child_data in data["children"]:
                child = CADScene.from_dict(child_data)
                node.add_child(child)

            return node

    

    @staticmethod
    def primitive_from_dict(data):

        if data["type"] == "block":
            return CADBlock(
                size=list(data["size"]),
                epsilon=data["epsilon"],
                # center=list(data["center"])
            )

        elif data["type"] == "cylinder":
            return CADCylinder(
                radius=data["radius"],
                height=data["height"],
                epsilon=data["epsilon"],
                axis=list(data["axis"]),
                # center=list(data["center"]),
            )
        
        elif data["type"] == "sphere":
            return CADSphere(
                radius=data["radius"],
                epsilon=data["epsilon"],
                # center=list(data["center"]),
            )
        
        elif data["type"] == "prism":
            return CADPrism(
                height=data["height"],
                epsilon=data["epsilon"],
                vertices=list(data["vertices"]),
                axis=list(data["axis"]),
                # center=list(data["center"]),
            )

        else:
            raise ValueError(f"Unknown primitive type: {data['type']}")