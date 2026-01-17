from core.geometry.cad.cad_scene import CADScene
from core.geometry.cad.cad_node import CADNode
from core.geometry.cad.cad_primitives.cad_sphere import CADSphere
from core.geometry.cad.cad_primitives.cad_prism import CADPrism
from core.geometry.cad.cad_primitives.cad_mesh import CADMesh
from core.geometry.cad.cad_builder import CADBuilder
from core.geometry.cad.transform import Transform
from core.geometry.cad.cad_importer import CADImporter

prism = CADPrism(
    vertices=[
        [0, 0, 0],
        [1, 0, 0],
        [0, 1, 0]
    ],
    height=2,
    axis=[0,0,1],
    epsilon=2.5,
)

node = CADNode(
    name="prism1",
    cad_primitive=prism,
    transform=Transform(translation=(6, 0, 0))
)

# mesh = CADImporter(path="../pyramid.stl", pitch=0.2, epsilon=3.0)
# mesh = mesh.build()

# node = CADNode(
#     name="mesh1",
#     cad_primitive=mesh,
#     transform=Transform(translation=(3, 0, 0))
# )

builder = CADBuilder(node)
geometry = builder.build()

print(geometry[0].center)
