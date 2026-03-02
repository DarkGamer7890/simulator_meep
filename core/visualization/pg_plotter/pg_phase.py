import pyqtgraph as pg
from core.simulation.simulation_data import SimulationData
from .pg_base import heatmap_widget

_BLUES = pg.colormap.get("Blues", source="matplotlib")


class PGPhaseGraphPlotter:
    def __init__(self, sim_data: SimulationData):
        self.data = sim_data
        self.is_3D = sim_data.is_3D
        self.phase = sim_data.phase
        self.center = sim_data.center
        self.coords = sim_data.coords
        self.axis = sim_data.axis

    def origin_xy(self):
        z = self.phase[:, :, self.center] if self.is_3D else self.phase
        return heatmap_widget(z, self.axis, "Phase (XY plane, z=0)", "X", "Y", _BLUES)

    def focus_xy(self):
        if not self.is_3D:
            return None
        z = self.phase[:, :, self.coords[2]]
        return heatmap_widget(z, self.axis, f"Phase (XY plane, z={self.coords[2] - self.center})", "X", "Y", _BLUES)

    def origin_yz(self):
        if not self.is_3D:
            return None
        z = self.phase[self.center, :, :]
        return heatmap_widget(z, self.axis, "Phase (YZ plane, x=0)", "Y", "Z", _BLUES)

    def focus_yz(self):
        if not self.is_3D:
            return None
        z = self.phase[self.coords[0], :, :]
        return heatmap_widget(z, self.axis, f"Phase (YZ plane, x={self.coords[0] - self.center})", "Y", "Z", _BLUES)

    def origin_xz(self):
        if not self.is_3D:
            return None
        z = self.phase[:, self.center, :]
        return heatmap_widget(z, self.axis, "Phase (XZ plane, y=0)", "X", "Z", _BLUES)

    def focus_xz(self):
        if not self.is_3D:
            return None
        z = self.phase[:, self.coords[1], :]
        return heatmap_widget(z, self.axis, f"Phase (XZ plane, y={self.coords[1] - self.center})", "X", "Z", _BLUES)