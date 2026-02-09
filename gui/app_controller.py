from core.visualization.plotly.base import PlotlyPlotter
from core.simulation.simulation_controller import SimulationController
from pathlib import Path
import webbrowser


class AppController:
    def __init__(self, cad_builder):
        self.builder = cad_builder
        self.simulation_controller = SimulationController(cad_builder)

    def run_simulation(self, config):
        sim_data = self.simulation_controller.run_simulation(config)

        plotter = PlotlyPlotter(sim_data)
        fig = plotter.plot("contour_origin_xy")

        plot_path = Path("last_plot.html").resolve()
        fig.write_html(str(plot_path))
        webbrowser.open(f"file://{plot_path}")
