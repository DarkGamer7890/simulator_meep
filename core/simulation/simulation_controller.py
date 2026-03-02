from core.cad.cad_builder import CADBuilder
from core.simulation.simulation_config import SimulationConfig
from core.simulation.simulation_data import SimulationData
from core.solver.meep_solver import MeepSolver
import numpy as np


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

    def run_simulation(self, config: SimulationConfig) -> SimulationData:
        raw_geometry = self.cad_builder.build()
        geometry = []

        for _, obj, transform in raw_geometry:
            R = self._pure_rotation_matrix(transform)

            # Apply world position
            obj.center = transform.translation.copy()

            # Apply rotation to direction vectors
            if hasattr(obj, 'axis'):
                obj.axis = np.round(R @ np.array(obj.axis))
            if hasattr(obj, 'e1'):
                obj.e1 = R @ np.round(np.array(obj.e1))
                obj.e2 = R @ np.round(np.array(obj.e2))
                obj.e3 = R @ np.round(np.array(obj.e3))

            geometry.append(obj)

        solver = MeepSolver(
            geometry=geometry,
            cell_size=config.cell_size,
            resolution=config.resolution,
            pml=config.pml,
            source_center=config.source_center,
            source_size=config.source_size,
            frequency=config.frequency,
            time=config.time,
        )

        eps_sim, ez_dft = solver.run()

        return SimulationData(
            eps_sim=eps_sim,
            ez_dft=ez_dft,
            pml=config.pml,
            resolution=config.resolution,
        )
