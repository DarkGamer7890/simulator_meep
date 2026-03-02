"""gui/app_controller.py"""
from PyQt5.QtCore import QObject, pyqtSignal
from core.simulation.simulation_controller import SimulationController
from core.simulation.simulation_data import SimulationData


class AppController(QObject):
    simulation_finished = pyqtSignal()

    def __init__(self, cad_builder):
        super().__init__()
        self.builder = cad_builder
        self.simulation_controller = SimulationController(cad_builder)
        self.plot_panel = None
        self.last_sim_data: SimulationData = None

    def run_simulation(self, config):
        sim_data: SimulationData = self.simulation_controller.run_simulation(config)
        self.last_sim_data = sim_data
        if self.plot_panel is not None:
            self.plot_panel.set_simulation_data(sim_data)
        self.simulation_finished.emit()