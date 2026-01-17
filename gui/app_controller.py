from core.simulation.simulation_controller import SimulationController
from core.cad.cad_builder import CADBuilder
from core.simulation.simulation_config import SimulationConfig
from core.simulation.simulation_data import SimulationData
from core.visualization.plotly.base import PlotlyPlotter
import webbrowser
from pathlib import Path



class AppController:
    def __init__(self, cad_builder: CADBuilder):
        self.cad_builder = cad_builder
        self.simulation_controller = SimulationController(cad_builder)

    def run_simulation(self, config: SimulationConfig) -> SimulationData:
        sim_data = self.simulation_controller.run(config)
        plotter = PlotlyPlotter(sim_data)
        # return plotter.plot("mag_plane_origin_xy")
        fig = plotter.plot("mag_plane_origin_xy")

        # Save plot
        plot_path = Path("last_plot.html").resolve()
        fig.write_html(str(plot_path))
        
        webbrowser.open(f"file://{plot_path}")
