from core.cad.core.cad_node import CADNode
from core.cad.core.boolean_node import BooleanNode
from core.cad.cad_primitives.cad_block import CADBlock
from core.cad.cad_primitives.cad_cylinder import CADCylinder
from core.cad.cad_builder import CADBuilder
from core.cad.core.cad_scene import CADScene


def print_build_result(build_result):
    print("\n=== BUILD RESULT ===")
    print(f"Additions: {len(build_result.additions)}")
    for i, obj in enumerate(build_result.additions):
        print(f"  [{i}] {type(obj).__name__}")

    print(f"Subtractions: {len(build_result.subtractions)}")
    for i, obj in enumerate(build_result.subtractions):
        print(f"  [{i}] {type(obj).__name__}")
    print("====================\n")


def main():
    print("Starting CAD CSG Test...")

    scene = CADScene()

    subtract_node = BooleanNode("subtract")

    box_node = CADNode(
        name="box",
        cad_primitive=CADBlock(size=(2, 2, 2), epsilon=2)
    )

    cylinder_node = CADNode(
        name="cyl",
        cad_primitive=CADCylinder(radius=0.5, height=3, epsilon=2)
    )

    subtract_node.add_child(box_node)
    subtract_node.add_child(cylinder_node)

    scene.get_root().add_child(subtract_node)

    builder = CADBuilder(scene)
    build_result = builder.build()

    print_build_result(build_result)

    if len(build_result.additions) == 1 and len(build_result.subtractions) == 1:
        print("✅ CSG subtract appears to be working correctly.")
    else:
        print("❌ Something is wrong with CSG logic.")


if __name__ == "__main__":
    main()