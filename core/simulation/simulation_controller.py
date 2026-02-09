from core.cad.cad_builder import CADBuilder
from core.simulation.simulation_config import SimulationConfig
from core.simulation.simulation_data import SimulationData
from core.solver.meep_solver import MeepSolver


class SimulationController:
    def __init__(self, cad_builder: CADBuilder):
        self.cad_builder = cad_builder

    def run_simulation(self, config: SimulationConfig) -> SimulationData:
        raw_geometry = self.cad_builder.build()
        geometry = []

        for _, obj in raw_geometry:
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
