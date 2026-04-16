import numpy as np
from .base import BaseSolver
from ..geometry.primitives import *


class MeepSolver(BaseSolver):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build_geometry(self):
        def volume_key(obj):
            return obj.bounding_volume()
        objs = sorted(self.geometry, key=volume_key, reverse=True)
        return [obj.to_meep() for obj in objs]

    def run(self, progress_queue=None):
        import meep as mp

        pml_layer = [mp.PML(self.pml)]
        source = mp.Source(
            src=mp.ContinuousSource(frequency=self.frequency, is_integrated=True),
            center=mp.Vector3(*self.source_center),
            size=mp.Vector3(*self.source_size),
            component=mp.Ez
        )
        sim = mp.Simulation(
            cell_size=mp.Vector3(*self.cell_size),
            boundary_layers=pml_layer,
            geometry=self.build_geometry(),
            sources=[source],
            resolution=self.resolution
        )
        dft_monitor = sim.add_dft_fields(
            [mp.Ez],
            [self.frequency],
            center=mp.Vector3(0, 0, 0),
            size=mp.Vector3(*self.cell_size)
        )
        sim.init_sim()
        self.eps_data = sim.get_array(
            center=mp.Vector3(),
            size=mp.Vector3(*self.cell_size),
            component=mp.Dielectric
        )

        step_interval = max(self.time / 100.0, 1.0)

        def _report_progress(sim):
            if progress_queue is not None:
                pct = min(sim.meep_time() / self.time, 1.0)
                progress_queue.put(("progress", pct))

        sim.run(
            mp.at_every(step_interval, _report_progress),
            until=self.time
        )

        self.ez_dft = sim.get_dft_array(dft_monitor, mp.Ez, 0)

        dim_x = int(self.cell_size[0] * self.resolution)
        dim_y = int(self.cell_size[1] * self.resolution)
        dim_z = int(self.cell_size[2] * self.resolution)

        if dim_z == 0:
            self.ez_dft = np.reshape(self.ez_dft, (dim_x, dim_y))
        else:
            self.ez_dft = np.reshape(self.ez_dft, (dim_x, dim_y, dim_z))

        return self.eps_data, self.ez_dft