import numpy as np
from core.cad.cad_builder import CADBuilder
from core.simulation.simulation_config import SimulationConfig
from core.simulation.simulation_data import SimulationData
from core.solver.meep_solver import MeepSolver



def _simulation_worker(queue, geometry, config_dict):
    try:
        solver = MeepSolver(
            geometry=geometry,
            cell_size=config_dict["cell_size"],
            resolution=config_dict["resolution"],
            pml=config_dict["pml"],
            source_center=config_dict["source_center"],
            source_size=config_dict["source_size"],
            frequency=config_dict["frequency"],
            time=config_dict["time"],
        )

        eps_sim, ez_dft = solver.run(progress_queue=queue)
        queue.put(("success", eps_sim, ez_dft))
        
    except Exception as e:
        queue.put(("error", str(e)))



class SimulationController:

    def __init__(self, cad_builder: CADBuilder):
        self.cad_builder = cad_builder



    @staticmethod
    def _pure_rotation_matrix(transform):
        rx, ry, rz = transform.rotation
        cx, cy, cz = np.cos([rx, ry, rz])
        sx, sy, sz = np.sin([rx, ry, rz])

        Rx = np.array([[1,0,0],[0,cx,-sx],[0,sx,cx]])
        Ry = np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]])
        Rz = np.array([[cz,-sz,0],[sz,cz,0],[0,0,1]])

        return Rz @ Ry @ Rx



    def prepare_geometry(self):
        raw_geometry = self.cad_builder.build()
        geometry = []

        for _, obj, transform in raw_geometry:
            R = self._pure_rotation_matrix(transform)
            obj.center = transform.translation.copy()

            if hasattr(obj, 'axis'):
                obj.axis = np.round(R @ np.array(obj.axis))

            if hasattr(obj, 'e1'):
                obj.e1 = R @ np.round(np.array(obj.e1))
                obj.e2 = R @ np.round(np.array(obj.e2))
                obj.e3 = R @ np.round(np.array(obj.e3))

            geometry.append(obj)

        return geometry