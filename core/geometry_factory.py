from core.geometry import Geometry
from core.importer import Importer

def build_geometry(geom_type, params):
    """
    Returns:
        geometry : list of meep objects
    """

    if geom_type == "Luneberg Lens":
        geom_obj = Geometry(
            radius=params["radius"],
            layers=params["layers"],
            cell_z = params['cell_z']
        )

        return geom_obj.luneburg_lens()

    elif geom_type == "Import File":
        geom_obj = Importer(
            path=params["path"],
            pitch=params["pitch"],
            epsilon=params["epsilon"]
        )

        return geom_obj.voxelize_mesh()

    else:
        return []
