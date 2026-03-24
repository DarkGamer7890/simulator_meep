from core.cad.core.cad_node import CADNode
from core.cad.core.boolean_node import BooleanNode
from core.cad.cad_primitives.cad_block import CADBlock
from core.cad.cad_primitives.cad_cylinder import CADCylinder
from core.cad.core.transform import Transform
from core.cad.cad_builder import CADBuilder
from core.cad.core.cad_scene import CADScene


def print_build_result(build_result):
    print("\n=== BUILD RESULT ===")
    print(f"Additions: {len(build_result.additions)}")
    for i, (geom, transform) in enumerate(build_result.additions):
        print(f"  [+] {i}: {type(geom).__name__}, T={transform.translation}")

    print(f"Subtractions: {len(build_result.subtractions)}")
    for i, (geom, transform) in enumerate(build_result.subtractions):
        print(f"  [-] {i}: {type(geom).__name__}, T={transform.translation}")
    print("====================\n")


def test_single_primitive():
    print("TEST 1: Single Primitive")

    scene = CADScene()
    box = CADNode(
        name="box",
        cad_primitive=CADBlock(size=(2, 2, 2), epsilon=1)
    )
    scene.get_root().add_child(box)

    builder = CADBuilder(scene)
    result = builder.build()

    assert len(result.additions) == 1
    assert len(result.subtractions) == 0
    print("✔ Single primitive OK\n")


def test_transform_propagation():
    print("TEST 2: Transform Propagation")

    scene = CADScene()

    box = CADNode(
        name="box",
        cad_primitive=CADBlock(size=(1, 1, 1), epsilon=1),
        transform=Transform(translation=(5, 0, 0))
    )

    scene.get_root().add_child(box)

    builder = CADBuilder(scene)
    result = builder.build()

    geom, transform = result.additions[0]
    assert tuple(transform.translation) == (5, 0, 0)

    print("✔ Transform propagation OK\n")


def test_simple_subtract():
    print("TEST 3: Simple Subtract")

    scene = CADScene()
    subtract_node = BooleanNode("subtract")

    box = CADNode(
        name="box",
        cad_primitive=CADBlock(size=(2, 2, 2), epsilon=1)
    )

    cyl = CADNode(
        name="cyl",
        cad_primitive=CADCylinder(radius=0.5, height=3, epsilon=1)
    )

    subtract_node.add_child(box)
    subtract_node.add_child(cyl)

    scene.get_root().add_child(subtract_node)

    builder = CADBuilder(scene)
    result = builder.build()

    assert len(result.additions) == 1
    assert len(result.subtractions) == 1

    print("✔ Subtract CSG OK\n")


def test_nested_boolean_with_transform():
    print("TEST 4: Nested Boolean + Transform")

    scene = CADScene()

    parent = CADNode(
        name="parent",
        transform=Transform(translation=(10, 0, 0))
    )

    outer = BooleanNode("subtract")
    inner = BooleanNode("subtract")

    box1 = CADNode(
        name="box1",
        cad_primitive=CADBlock(size=(2, 2, 2), epsilon=1)
    )

    box2 = CADNode(
        name="box2",
        cad_primitive=CADBlock(size=(2, 2, 2), epsilon=1)
    )

    cyl = CADNode(
        name="cyl",
        cad_primitive=CADCylinder(radius=0.5, height=3, epsilon=1)
    )

    outer.add_child(box1)
    outer.add_child(inner)

    inner.add_child(box2)
    inner.add_child(cyl)
    parent.add_child(outer)
    scene.get_root().add_child(parent)

    builder = CADBuilder(scene)
    result = builder.build()

    # Both should inherit parent transform
    for geom, transform in result.additions + result.subtractions:
        assert tuple(transform.translation) == (10, 0, 0)

    print("✔ Nested Boolean + Transform OK\n")


def test_union():
    print("TEST 2: Union")
    scene = CADScene()
    union_node = BooleanNode("union")

    box1 = CADNode(name="box1", cad_primitive=CADBlock(size=(1,1,1), epsilon=1))
    box2 = CADNode(name="box2", cad_primitive=CADBlock(size=(1,1,1), epsilon=1))

    union_node.add_child(box1)
    union_node.add_child(box2)
    scene.get_root().add_child(union_node)

    builder = CADBuilder(scene)
    result = builder.build()

    assert len(result.additions) == 2
    assert len(result.subtractions) == 0

    print("Union worked\n")


def run_all_tests():
    print("\n===== CAD SYSTEM VALIDATION =====\n")

    test_single_primitive()
    test_transform_propagation()
    test_simple_subtract()
    test_nested_boolean_with_transform()
    test_union()

    print("🎉 ALL TESTS PASSED SUCCESSFULLY 🎉\n")


if __name__ == "__main__":
    run_all_tests()