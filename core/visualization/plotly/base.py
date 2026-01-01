from .line_graph import LineGraphPlotter
from .mag_graph import MagGraphPlotter
from .phase_graph import PhaseGraphPlotter
from .contour import ContourPlotter


class PlotlyPlotter:
    def __init__(self, plotter):
        self.plotter = plotter
        self.line = LineGraphPlotter(plotter)
        self.mag = MagGraphPlotter(plotter)
        self.phase = PhaseGraphPlotter(plotter)
        self.contour = ContourPlotter(plotter)

        self.capabilities = {
            "line_origin_x": True,
            "line_focus_x": True,

            "line_origin_y": True,
            "line_focus_y": True,

            "line_origin_z": plotter.is_3D,
            "line_focus_z": plotter.is_3D,

            "mag_plane_origin_xy": True,
            "mag_plane_focus_xy": plotter.is_3D,

            "mag_plane_origin_yz": plotter.is_3D,
            "mag_plane_focus_yz": plotter.is_3D,
            
            "mag_plane_origin_xz": plotter.is_3D,
            "mag_plane_focus_xz": plotter.is_3D,

            "phase_plane_origin_xy": True,
            "phase_plane_focus_xy": plotter.is_3D,

            "phase_plane_origin_yz": plotter.is_3D,
            "phase_plane_focus_yz": plotter.is_3D,
            
            "phase_plane_origin_xz": plotter.is_3D,
            "phase_plane_focus_xz": plotter.is_3D,

            "contour_origin_xy": True,
            "contour_focus_xy": plotter.is_3D,

            "contour_origin_yz": plotter.is_3D,
            "contour_focus_yz": plotter.is_3D,
            
            "contour_origin_xz": plotter.is_3D,
            "contour_focus_xz": plotter.is_3D,
        }

    def plot(self, method_name, **kwargs):

        if not self.capabilities.get(method_name, False):
            return None


        method_map = {
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
            "mag_plane_focus_xz": self.mag.origin_xz,

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

        method = method_map.get(method_name)
        if method is None:
            return None
        
        elif "contour" in method_name.lower():
            return method(**kwargs)


        return method()
