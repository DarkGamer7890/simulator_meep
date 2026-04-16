from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QLabel, QFormLayout, QLineEdit, QProgressBar, QHBoxLayout
)
from core.simulation.simulation_config import SimulationConfig


class SimulationPanel(QWidget):
    def __init__(self, app_controller):
        super().__init__()
        self.app = app_controller

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Simulation Parameters"))

        form = QFormLayout()
        self.cell_x     = QLineEdit("10")
        self.cell_y     = QLineEdit("10")
        self.cell_z     = QLineEdit("10")
        self.pml        = QLineEdit("1")
        self.resolution = QLineEdit("20")
        self.frequency  = QLineEdit("0.15")
        self.time       = QLineEdit("200")
        form.addRow("Cell_X",      self.cell_x)
        form.addRow("Cell_Y",      self.cell_y)
        form.addRow("Cell_Z",      self.cell_z)
        form.addRow("PML",         self.pml)
        form.addRow("Resolution",  self.resolution)
        form.addRow("Frequency",   self.frequency)
        form.addRow("Time",        self.time)
        layout.addLayout(form)

        self._inputs = [
            self.cell_x, self.cell_y, self.cell_z,
            self.pml, self.resolution, self.frequency, self.time
        ]

        # Run / Cancel buttons side by side
        btn_row = QHBoxLayout()
        self.run_btn    = QPushButton("▶  Run Simulation")
        self.cancel_btn = QPushButton("✕  Cancel")
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.setStyleSheet("color: red;")
        btn_row.addWidget(self.run_btn)
        btn_row.addWidget(self.cancel_btn)
        layout.addLayout(btn_row)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        # Signals
        self.run_btn.clicked.connect(self.run_simulation)
        self.cancel_btn.clicked.connect(self.app.cancel_simulation)

        self.app.simulation_started.connect(self._on_started)
        self.app.simulation_finished.connect(self._on_finished)
        self.app.simulation_error.connect(self._on_error)
        self.app.simulation_progress.connect(self._on_progress)
        self.app.simulation_cancelled.connect(self._on_cancelled)

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
            source_center=(
                -float(self.cell_z.text()) / 2 + float(self.pml.text()) + 0.5, 0, 0
            ),
            source_size=(
                float(self.cell_x.text()),
                float(self.cell_y.text()),
                0.0
            ),
        )
        self.app.run_simulation(config)

    def _on_started(self):
        self.run_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.status_label.setText("⏳ Running...")
        for w in self._inputs:
            w.setEnabled(False)

    def _on_progress(self, pct):
        self.progress_bar.setValue(int(pct * 100))

    def _on_finished(self):
        self._reset_ui("✅ Done")

    def _on_error(self, msg):
        self._reset_ui(f"❌ Error: {msg}")

    def _on_cancelled(self):
        self._reset_ui("🚫 Cancelled")

    def _reset_ui(self, status):
        self.run_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.status_label.setText(status)
        for w in self._inputs:
            w.setEnabled(True)