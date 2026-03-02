from core.simulation.simulation_data import SimulationData
from .pg_base import line_widget


class PGLineGraphPlotter:
    def __init__(self, sim_data: SimulationData):
        self.data = sim_data
        self.mag = sim_data.magnitude
        self.center = sim_data.center
        self.coords = sim_data.coords
        self.axis = sim_data.axis

    def origin_x(self):
        y = self.mag[:, self.center, self.center] if self.data.is_3D else self.mag[:, self.center]
        title = "Line X (y=0)" + (", (z=0)" if self.data.is_3D else "")
        return line_widget(self.axis, y, title, "X")

    def focus_x(self):
        if self.data.is_3D:
            _, yi, zi = self.coords
            y = self.mag[:, yi, zi]
            label = f"y={yi - self.center}, z={zi - self.center}"
        else:
            _, yi = self.coords
            y = self.mag[:, yi]
            label = f"y={yi - self.center}"
        return line_widget(self.axis, y, f"Line X (Focus: {label})", "X")

    def origin_y(self):
        y = self.mag[self.center, :, self.center] if self.data.is_3D else self.mag[self.center, :]
        title = "Line Y (x=0)" + (", (z=0)" if self.data.is_3D else "")
        return line_widget(self.axis, y, title, "Y")

    def focus_y(self):
        if self.data.is_3D:
            xi, _, zi = self.coords
            y = self.mag[xi, :, zi]
            label = f"x={xi - self.center}, z={zi - self.center}"
        else:
            xi, _ = self.coords
            y = self.mag[xi, :]
            label = f"x={xi - self.center}"
        return line_widget(self.axis, y, f"Line Y (Focus: {label})", "Y")

    def origin_z(self):
        y = self.mag[self.center, self.center, :]
        return line_widget(self.axis, y, "Line Z (x=0, y=0)", "Z")

    def focus_z(self):
        xi, yi, _ = self.coords
        y = self.mag[xi, yi, :]
        return line_widget(self.axis, y, f"Line Z (Focus: x={xi - self.center}, y={yi - self.center})", "Z")