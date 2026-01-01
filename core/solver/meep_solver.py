import meep as mp
from .base import BaseSolver

class MeepSolver(BaseSolver):
    def __init__(self, sim):
        self.sim = sim

    def run(self):
        # WHY: isolate Meep-specific execution here
        eps, ez = self.sim.sim_run()
        return eps, ez
