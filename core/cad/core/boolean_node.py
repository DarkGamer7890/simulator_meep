from core.cad.core.cad_node import CADNode
from core.cad.core.geometry_build_result import GeometryBuildResult


class BooleanNode(CADNode):

    def __init__(self, operation: str, name: str = "Boolean", enabled=False):
        super().__init__(name=name)
        self.operation = operation.lower()

        if self.operation not in ("union", "subtract", "intersect"):
            raise ValueError("Boolean operation must be union, subtract, or intersect")
        
        self.enabled = enabled




    # def to_geometry(self, parent_transform=None):
    #     world_transform = self.get_world_transform(parent_transform)

    #     result = GeometryBuildResult()

    #     if not self.children:
    #         return result

    #     # First child is base
    #     base_result = self.children[0].to_geometry(world_transform)

    #     if self.operation == "union":
    #         result.merge(base_result)

    #         for child in self.children[1:]:
    #             child_result = child.to_geometry(world_transform)
    #             result.merge(child_result)

    #     elif self.operation == "subtract":
    #         result.additions.extend(base_result.additions)
    #         result.subtractions.extend(base_result.subtractions)

    #         # All other children become subtractions
    #         for child in self.children[1:]:
    #             child_result = child.to_geometry(world_transform)

    #             # Add child's additions as subtractions
    #             result.subtractions.extend(child_result.additions)

    #             # Child subtractions must flip back to additions
    #             result.additions.extend(child_result.subtractions)

    #     elif self.operation == "intersect":
    #         # result.merge(base_result)

    #         # for child in self.children[1:]:
    #         #     child_result = child.to_geometry(world_transform)
    #         #     result.merge(child_result)

    #         raise NotImplementedError(
    #             "Intersection is not supported in symbolic CSG stage."
    #         )

    #     return result



    def to_geometry(self, parent_transform=None):
        world_transform = self.get_world_transform(parent_transform)

        result = GeometryBuildResult()

        for child in self.children:
            child_result = child.to_geometry(world_transform)
            result.merge(child_result)

        return result
    


    def to_dict(self):
        return {
            "type": "boolean",
            "operation": self.operation,
            "children": [child.to_dict() for child in self.children]
        }