from .core.cad_node import CADNode
from .core.transform import Transform
from  .cad_primitives import *
from .core.property_model import PropertyModel




class CADController:
    def __init__(self, builder, viewer):
        self.builder = builder
        self.viewer = viewer
        self.selected_node = None
        self.transform_mode = "translate"  # translate | rotate
        self.axis_mode = "local"           # local | world

        self.property_model = PropertyModel()

        self.viewer.signals.move_requested.connect(self.on_move_requested)
        self.viewer.signals.add_sphere_requested.connect(self.add_sphere)
        self.viewer.signals.add_cylinder_requested.connect(self.add_cylinder)
        self.viewer.signals.add_block_requested.connect(self.add_block)
        self.viewer.signals.add_prism_requested.connect(self.add_prism)
        self.viewer.signals.delete_requested.connect(self.delete_selected)
        self.viewer.signals.selection_changed.connect(self.on_node_selected)
        self.viewer.signals.duplicate_node.connect(self.duplicate_node)
        self.viewer.signals.save_scene.connect(self.save_scene)

        self.rebuild()



    def rebuild(self):
        geometries = self.builder.build()
        self.viewer.show_geometry(geometries)

        if hasattr(self, "hierarchy_panel"):
            self.hierarchy_panel.rebuild()




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
        node = self.selected_node
        if node is None:
            return
        
        # Don't delete the root node
        if node == self.builder.root_node:
            print("Cannot delete root node")
            return


        for parent in self.builder.root_node.flatten():
            if node in parent.children:
                parent.children.remove(node)
                break

        self.selected_node = None
        self.viewer.highlight_node(None)

        if hasattr(self, 'hierarchy_panel'):
            self.hierarchy_panel.select_node(None)

        if hasattr(self, 'properties_panel'):
            self.properties_panel.clear()

        # self.viewer.deselect_all()
        self.rebuild()



    def on_move_requested(self, node, delta):
        import numpy as np

        if node is not self.selected_node:
            return

        dx, dy, dz = delta
        
        node.transform.translation[0] += dx  
        node.transform.translation[1] += dy  
        node.transform.translation[2] += dz 
        self.rebuild()




    def on_node_selected(self, node, source=None):
        """Handle node selection from any source (viewer, hierarchy, etc.)"""
        # Guard against re-selecting the same node
        if self.selected_node is node:
            return

        self.selected_node = node

        if node is None:
            self.property_model.clear()
        else:
            self.property_model.set_node(node)

        # Update viewer highlight (NO callbacks)
        self.viewer.highlight_node(node)

        print(self.property_model.get_properties())

        # Update hierarchy selection (NO callbacks)
        if hasattr(self, 'hierarchy_panel'):
            self.hierarchy_panel.select_node(node)


        # Update properties panel
        if hasattr(self, 'properties_panel'):
            if node is None:
                self.properties_panel.clear()
            else:
                self.properties_panel.refresh()




    def update_property(self, node: CADNode, prop: str, value):
        self.property_model.set_property(prop, value)
        self.rebuild()



    def add_child(self, parent):
        # temporarily added sphere
        child = CADNode(
            name="Child",
            cad_primitive=CADSphere(radius=0.5, epsilon=1.0),
            transform=Transform()
        )
        parent.add_child(child)
        self.rebuild()



    def duplicate_node(self):
        if self.selected_node is None:
            return

        # find parent
        parent = self.builder.root_node
        for n in self.builder.root_node.flatten():
            if self.selected_node in n.children:
                parent = n
                break

        duplicated = self.selected_node.clone_recursive()

        parent.add_child(duplicated)
        self.rebuild()


    def save_scene(self):
        import sys
        from PyQt5.QtWidgets import QApplication, QFileDialog
    
        app = QApplication.instance() or QApplication(sys.argv)
    
        filepath, _ = QFileDialog.getSaveFileName(
            None, "Save Scene", "", "JSON Files (*.json);;All Files (*)"
        )
    
        if not filepath:
            return
    
        if not filepath.endswith(".json"):
            filepath += ".json"
    
        try:
            self.builder.scene.save_scene(filepath)
            print("Saved at:", filepath)
        except Exception as e:
            print("Error saving:", e)
