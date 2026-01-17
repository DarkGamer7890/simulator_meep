from .cad_node import CADNode
from .transform import Transform
from .cad_primitives.cad_sphere import CADSphere
from .cad_primitives.cad_cylinder import CADCylinder
from .cad_primitives.cad_block import CADBlock
from .cad_primitives.cad_prism import CADPrism
from .property_model import PropertyModel




class CADController:
    def __init__(self, builder, viewer):
        self.builder = builder
        self.viewer = viewer

        self.property_model = PropertyModel()

        self.viewer.signals.move_requested.connect(self.on_move_requested)
        self.viewer.signals.add_sphere_requested.connect(self.add_sphere)
        self.viewer.signals.add_cylinder_requested.connect(self.add_cylinder)
        self.viewer.signals.add_block_requested.connect(self.add_block)
        self.viewer.signals.add_prism_requested.connect(self.add_prism)
        self.viewer.signals.delete_requested.connect(self.delete_selected)
        self.viewer.signals.selection_changed.connect(self.on_node_selected)

        self.rebuild()



    def rebuild(self):
        geometries = self.builder.build()
        self.viewer.show_geometry(geometries)



    def add_sphere(self):
        node = CADNode(
            name="Sphere",
            cad_primitive=CADSphere(radius=1.0, epsilon=1.0),
            transform=Transform(translation=(0, 0, 0))
        )
        self.builder.root_node.children.append(node)
        self.rebuild()



    def add_cylinder(self):
        node = CADNode(
            name="Cylinder",
            cad_primitive=CADCylinder(radius=1.0, height=2.0, epsilon=1.0),
            transform=Transform(translation=(0, 0, 0))
        )
        self.builder.root_node.children.append(node)
        self.rebuild()



    def add_block(self):
        node = CADNode(
            name="Block",
            cad_primitive=CADBlock(size=(1, 1, 1), epsilon=1.0),
            transform=Transform(translation=(0, 0, 0))
        )
        self.builder.root_node.children.append(node)
        self.rebuild()



    def add_prism(self):
        node = CADNode(
            name="Prism",
            cad_primitive=CADPrism(
                vertices=[(0,0,0), (1,0,0), (1,1,0)],
                height=1.0,
                epsilon=1.0
            ),
            transform=Transform(translation=(0, 0, 0))
        )
        self.builder.root_node.children.append(node)
        self.rebuild()



    def delete_selected(self):
        node = self.viewer.selected_node
        if node is None:
            return

        parent = self.builder.root_node
        parent.children = [c for c in parent.children if c is not node]

        self.viewer.deselect_all()
        self.rebuild()



    def on_move_requested(self, node, delta):
        import numpy as np
        node.transform.translation += np.array(delta)
        self.rebuild()



    def on_node_selected(self, node:CADNode):
        if node is None:
            return 
        self.property_model.set_node(node)
        print(node.cad_primitive.get_properties())
        print(self.property_model.get_properties())



    def update_property(self, node: CADNode, prop: str, value):
        self.property_model.set_property(prop, value)
        self.rebuild()
