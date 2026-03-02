from PyQt5.QtWidgets import QWidget
from core.simulation.simulation_data import SimulationData
from .pg_line import PGLineGraphPlotter
from .pg_mag import PGMagGraphPlotter
from .pg_phase import PGPhaseGraphPlotter
from .pg_contour import PGContourPlotter


class PGPlotter:
    def __init__(self, sim_data: SimulationData):
        self.line = PGLineGraphPlotter(sim_data)
        self.mag = PGMagGraphPlotter(sim_data)
        self.phase = PGPhaseGraphPlotter(sim_data)
        self.contour = PGContourPlotter(sim_data)

        self.capabilities = {
            "line_origin_x": True,
            "line_focus_x": True,
            "line_origin_y": True,
            "line_focus_y": True,
            "line_origin_z": sim_data.is_3D,
            "line_focus_z": sim_data.is_3D,
            "mag_plane_origin_xy": True,
            "mag_plane_focus_xy": sim_data.is_3D,
            "mag_plane_origin_yz": sim_data.is_3D,
            "mag_plane_focus_yz": sim_data.is_3D,
            "mag_plane_origin_xz": sim_data.is_3D,
            "mag_plane_focus_xz": sim_data.is_3D,
            "phase_plane_origin_xy": True,
            "phase_plane_focus_xy": sim_data.is_3D,
            "phase_plane_origin_yz": sim_data.is_3D,
            "phase_plane_focus_yz": sim_data.is_3D,
            "phase_plane_origin_xz": sim_data.is_3D,
            "phase_plane_focus_xz": sim_data.is_3D,
            "contour_origin_xy": True,
            "contour_focus_xy": sim_data.is_3D,
            "contour_origin_yz": sim_data.is_3D,
            "contour_focus_yz": sim_data.is_3D,
            "contour_origin_xz": sim_data.is_3D,
            "contour_focus_xz": sim_data.is_3D,
        }

        self._method_map = {
            "line_origin_x": self.line.origin_x,
            "line_focus_x": self.line.focus_x,
            "line_origin_y": self.line.origin_y,
            "line_focus_y": self.line.focus_y,
            "line_origin_z": self.line.origin_z,
            "line_focus_z": self.line.focus_z,
            "mag_plane_origin_xy": self.mag.origin_xy,
            "mag_plane_focus_xy": self.mag.focus_xy,
            "mag_plane_origin_yz": self.mag.origin_yz,
            "mag_plane_focus_yz": self.mag.focus_yz,
            "mag_plane_origin_xz": self.mag.origin_xz,
            "mag_plane_focus_xz": self.mag.focus_xz,
            "phase_plane_origin_xy": self.phase.origin_xy,
            "phase_plane_focus_xy": self.phase.focus_xy,
            "phase_plane_origin_yz": self.phase.origin_yz,
            "phase_plane_focus_yz": self.phase.focus_yz,
            "phase_plane_origin_xz": self.phase.origin_xz,
            "phase_plane_focus_xz": self.phase.focus_xz,
            "contour_origin_xy": self.contour.origin_xy,
            "contour_focus_xy": self.contour.focus_xy,
            "contour_origin_yz": self.contour.origin_yz,
            "contour_focus_yz": self.contour.focus_yz,
            "contour_origin_xz": self.contour.origin_xz,
            "contour_focus_xz": self.contour.focus_xz,
        }

    def plot(self, method_name: str, **kwargs) -> QWidget:
        if not self.capabilities.get(method_name, False):
            return None
        method = self._method_map.get(method_name)
        if method is None:
            return None
        if "contour" in method_name:
            return method(**kwargs)
        return method()