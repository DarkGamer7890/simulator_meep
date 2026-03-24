class SolverAdapter:
    def __init__(self, solver):
        self.solver = solver

    def build(self, build_result):
        for obj in build_result.additions:
            self.solver.add(obj)

        for obj in build_result.subtractions:
            self.solver.subtract(obj)