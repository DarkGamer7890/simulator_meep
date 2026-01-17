from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from core.simulation.simulation_config import SimulationConfig



class SimulationPanel(QWidget):
    def __init__(self, app_controller):
        super().__init__()
        self.app = app_controller
        # self.plot_panel = plot_panel

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Simulation Panel"))

        run_btn = QPushButton("Run Simulation")
        run_btn.clicked.connect(self.run_simulation)
        layout.addWidget(run_btn)

    def run_simulation(self):
        config = SimulationConfig(
            cell_size=(10, 10, 0),
            resolution=20,
            pml=1.0,
            frequency=1.0,
            time=200,
            source_center=(-4, 0, 0),
            source_size=(10, 10, 0),
        )

        self.app.run_simulation(config)
        # self.plot_panel.show_figure(fig)
