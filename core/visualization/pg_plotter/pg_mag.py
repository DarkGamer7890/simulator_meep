import pyqtgraph as pg
from core.simulation.simulation_data import SimulationData
from .pg_base import heatmap_widget

_JET = pg.colormap.get("jet", source="matplotlib")


class PGMagGraphPlotter:
    def __init__(self, sim_data: SimulationData):
        self.data = sim_data
        self.is_3D = sim_data.is_3D
        self.mag = sim_data.magnitude
        self.center = sim_data.center
        self.coords = sim_data.coords
        self.axis = sim_data.axis

    def origin_xy(self):
        z = self.mag[:, :, self.center] if self.is_3D else self.mag
        return heatmap_widget(z, self.axis, "Magnitude |Ez| (XY plane, z=0)", "X", "Y", _JET)

    def focus_xy(self):
        if not self.is_3D:
            return None
        z = self.mag[:, :, self.coords[2]]
        return heatmap_widget(z, self.axis, f"Magnitude |Ez| (XY plane, z={self.coords[2] - self.center})", "X", "Y", _JET)

    def origin_yz(self):
        if not self.is_3D:
            return None
        z = self.mag[self.center, :, :]
        return heatmap_widget(z, self.axis, "Magnitude |Ez| (YZ plane, x=0)", "Y", "Z", _JET)

    def focus_yz(self):
        if not self.is_3D:
            return None
        z = self.mag[self.coords[0], :, :]
        return heatmap_widget(z, self.axis, f"Magnitude |Ez| (YZ plane, x={self.coords[0] - self.center})", "Y", "Z", _JET)

    def origin_xz(self):
        if not self.is_3D:
            return None
        z = self.mag[:, self.center, :]
        return heatmap_widget(z, self.axis, "Magnitude |Ez| (XZ plane, y=0)", "X", "Z", _JET)

    def focus_xz(self):
        if not self.is_3D:
            return None
        z = self.mag[:, self.coords[1], :]
        return heatmap_widget(z, self.axis, f"Magnitude |Ez| (XZ plane, y={self.coords[1] - self.center})", "X", "Z", _JET)