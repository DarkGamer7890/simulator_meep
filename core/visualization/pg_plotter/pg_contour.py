from core.simulation.simulation_data import SimulationData
from .pg_base import contour_widget


class PGContourPlotter:
    def __init__(self, sim_data: SimulationData):
        self.data = sim_data
        self.is_3D = sim_data.is_3D
        self.mag = sim_data.magnitude
        self.center = sim_data.center
        self.coords = sim_data.coords
        self.axis = sim_data.axis

    def _levels(self, kwargs):
        return kwargs.get("contour_levels", 15)

    def origin_xy(self, **kwargs):
        z = self.mag[:, :, self.center] if self.is_3D else self.mag
        return contour_widget(z, self.axis, "Contour |Ez| (XY plane, z=0)", "X", "Y", self._levels(kwargs))

    def focus_xy(self, **kwargs):
        if not self.is_3D:
            return None
        z = self.mag[:, :, self.coords[2]]
        return contour_widget(z, self.axis, f"Contour |Ez| (XY plane, z={self.coords[2] - self.center})", "X", "Y", self._levels(kwargs))

    def origin_yz(self, **kwargs):
        if not self.is_3D:
            return None
        z = self.mag[self.center, :, :].T
        return contour_widget(z, self.axis, "Contour |Ez| (YZ plane, x=0)", "Y", "Z", self._levels(kwargs))

    def focus_yz(self, **kwargs):
        if not self.is_3D:
            return None
        z = self.mag[self.coords[0], :, :].T
        return contour_widget(z, self.axis, f"Contour |Ez| (YZ plane, x={self.coords[0] - self.center})", "Y", "Z", self._levels(kwargs))

    def origin_xz(self, **kwargs):
        if not self.is_3D:
            return None
        z = self.mag[:, self.center, :].T
        return contour_widget(z, self.axis, "Contour |Ez| (XZ plane, y=0)", "X", "Z", self._levels(kwargs))

    def focus_xz(self, **kwargs):
        if not self.is_3D:
            return None
        z = self.mag[:, self.coords[1], :].T
        return contour_widget(z, self.axis, f"Contour |Ez| (XZ plane, y={self.coords[1] - self.center})", "X", "Z", self._levels(kwargs))