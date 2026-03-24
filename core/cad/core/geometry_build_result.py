class GeometryBuildResult:
    def __init__(self):
        self.additions = []       # (node, geom, transform)
        self.subtractions = []    # (node, geom, transform)

    def merge(self, other):
        self.additions.extend(other.additions)
        self.subtractions.extend(other.subtractions)