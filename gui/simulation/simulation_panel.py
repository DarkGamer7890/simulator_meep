from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QLabel, QFormLayout, QLineEdit
)
from core.simulation.simulation_config import SimulationConfig


class SimulationPanel(QWidget):
    def __init__(self, app_controller):
        super().__init__()
        self.app = app_controller

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Simulation Parameters"))

        form = QFormLayout()

        self.cell_x = QLineEdit("10")
        self.cell_y = QLineEdit("10")
        self.cell_z = QLineEdit("10")
        self.pml = QLineEdit("1")
        self.resolution = QLineEdit("20")
        self.frequency = QLineEdit("0.15")
        self.time = QLineEdit("200")

        form.addRow("Cell_X", self.cell_x)
        form.addRow("Cell_Y", self.cell_y)
        form.addRow("Cell_Z", self.cell_z)

        form.addRow("PML", self.pml)

        form.addRow("Resolution", self.resolution)
        form.addRow("Frequency", self.frequency)
        form.addRow("Time", self.time)

        layout.addLayout(form)

        run_btn = QPushButton("Run Simulation")
        run_btn.clicked.connect(self.run_simulation)
        layout.addWidget(run_btn)

    def run_simulation(self):
        config = SimulationConfig(
            cell_size=(
                float(self.cell_x.text()), 
                float(self.cell_y.text()), 
                float(self.cell_z.text())
            ),
            resolution=int(self.resolution.text()),
            pml=float(self.pml.text()),
            frequency=float(self.frequency.text()),
            time=float(self.time.text()),
            source_center=(-float(self.cell_z.text()) / 2 + float(self.pml.text()) + 0.5, 0, 0),
            source_size=(
                float(self.cell_x.text()), 
                float(self.cell_y.text()), 
                0.0
            ),
        )

        self.app.run_simulation(config)
