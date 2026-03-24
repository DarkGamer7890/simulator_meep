from core.cad.core.geometry_build_result import GeometryBuildResult
from .core.cad_scene import CADScene
from .core.transform import Transform
from core.geometry.registry import register_geometry

@register_geometry("CAD")
class CADBuilder:

    def __init__(self, scene: CADScene):
        self.scene = scene
        self.root_node = scene.get_root()

    def build(self):
        result = self.root_node.to_geometry()

        geometries = []

        # Add additions
        for node, geom, transform in result.additions:
            geometries.append((node, geom, transform))

        # Add subtractions (for Meep overwrite behavior)
        for node, geom, transform in result.subtractions:
            geometries.append((node, geom, transform))

        return geometries
