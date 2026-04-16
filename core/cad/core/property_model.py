from .cad_node import CADNode


class PropertyModel:
    def __init__(self):
        self.node = None

    def set_node(self, node: CADNode):
        self.node = node

    def clear(self):
        self.node = None

    def get_properties(self):
        if self.node is None:
            return {}
        
        import numpy as np

        t = self.node.transform
        props = {
            # **self.node.cad_primitive.get_properties(),

            "pos_x": float(t.translation[0]),
            "pos_y": float(t.translation[1]),
            "pos_z": float(t.translation[2]),

            "rot_x": np.degrees(t.rotation[0]),
            "rot_y": np.degrees(t.rotation[1]),
            "rot_z": np.degrees(t.rotation[2]),
        }


        if self.node.cad_primitive is not None:
            props.update(self.node.cad_primitive.get_properties())

        return props

    
    def set_property(self, name, value):
        node = self.node
        if not node:
            return
    
        import numpy as np
        
        transform = node.transform
    

        if name == "pos_x":
            transform.translation[0] = value
        elif name == "pos_y":
            transform.translation[1] = value
        elif name == "pos_z":
            transform.translation[2] = value
    

        elif name == "rot_x":
            transform.rotation[0] = np.radians(value)
        elif name == "rot_y":
            transform.rotation[1] = np.radians(value)
        elif name == "rot_z":
            transform.rotation[2] = np.radians(value)
    

        else:
            if node.cad_primitive is not None:
                node.cad_primitive.set_property(name, value)
