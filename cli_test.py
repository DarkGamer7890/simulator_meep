from core.geometry.cad.cad_scene import CADScene
from core.geometry.cad.cad_node import CADNode
from core.geometry.cad.cad_primitives.cad_sphere import CADSphere
from core.geometry.cad.cad_primitives.cad_mesh import CADMesh
from core.geometry.cad.cad_builder import CADBuilder
from core.geometry.cad.cad_importer import CADImporter

def main():
    # 1. Create scene
    scene = CADScene("TestScene")

    # 2. Create CAD primitives
    sphere = CADSphere(radius=1.0, epsilon=2.5)
    mesh = CADImporter(path="../pyramid.stl", pitch=0.2, epsilon=3.0)
    mesh = mesh.build()

    # 3. Wrap them in nodes
    sphere_node = CADNode("sphere1", cad_primitive=sphere)
    mesh_node = CADNode("mesh1", cad_primitive=mesh)

    # 4. Add to scene
    scene.root.add_child(sphere_node)
    scene.root.add_child(mesh_node)

    # 5. Build geometry
    builder = CADBuilder(scene.root)
    geometry = builder.build()

    # 6. Inspect result
    print("Built geometry:")
    for g in geometry:
        print(type(g), g)

if __name__ == "__main__":
    main()
