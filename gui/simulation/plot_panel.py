from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QLabel, QScrollArea, QFrame, QSizePolicy, QStackedWidget
)
from PyQt5.QtCore import Qt

from core.simulation.simulation_data import SimulationData
from core.visualization.pg_plotter import PGPlotter, PLOT_LABELS, SECTIONS

BTN_STYLE = """
    QPushButton {
        background: #f0f4ff; border: 1px solid #c5d8fc;
        border-radius: 4px; padding: 5px 10px;
        font-size: 8pt; color: #222; text-align: left;
    }
    QPushButton:hover { background: #e8f0fe; border-color: #1a73e8; }
    QPushButton:pressed { background: #c5d8fc; }
    QPushButton:disabled { background: #f5f5f5; color: #aaa; border-color: #ddd; }
    QPushButton:checked { background: #1a73e8; color: white; border-color: #1a73e8; }
"""


class PlotPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._plotter: PGPlotter = None
        self._buttons = {}
        self._active_btn = None
        self._build_ui()

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Sidebar ───────────────────────────────
        sidebar = QWidget()
        sidebar.setFixedWidth(195)
        sidebar.setStyleSheet("background:#fafafa; border-right:1px solid #e0e0e0;")
        sb = QVBoxLayout(sidebar)
        sb.setContentsMargins(0, 0, 0, 0)
        sb.setSpacing(0)

        self.status_label = QLabel("Run simulation first.")
        self.status_label.setWordWrap(True)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(
            "background:#fff8e1; color:#795548; font-size:8pt;"
            "padding:6px; border-bottom:1px solid #ffe082;"
        )
        sb.addWidget(self.status_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        container = QWidget()
        btn_layout = QVBoxLayout(container)
        btn_layout.setContentsMargins(8, 6, 8, 10)
        btn_layout.setSpacing(2)

        for section, keys in SECTIONS.items():
            lbl = QLabel(section)
            lbl.setStyleSheet("font-weight:bold; font-size:9pt; color:#1a73e8; padding:8px 0 2px 0;")
            btn_layout.addWidget(lbl)
            for key in keys:
                btn = QPushButton(PLOT_LABELS[key])
                btn.setStyleSheet(BTN_STYLE)
                btn.setCheckable(True)
                btn.setEnabled(False)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                btn.clicked.connect(lambda _, k=key: self._on_plot(k))
                btn_layout.addWidget(btn)
                self._buttons[key] = btn

        btn_layout.addStretch()
        scroll.setWidget(container)
        sb.addWidget(scroll, stretch=1)

        # ── Canvas ────────────────────────────────
        self.canvas = QStackedWidget()
        placeholder = QLabel("Select a plot from the list.")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet("color:#bbb; font-size:12pt;")
        self.canvas.addWidget(placeholder)  # idx 0

        root.addWidget(sidebar)
        root.addWidget(self.canvas, stretch=1)

    def set_simulation_data(self, sim_data: SimulationData):
        self._plotter = PGPlotter(sim_data)
        self.status_label.setText("Select a plot →")
        self.status_label.setStyleSheet(
            "background:#e8f5e9; color:#2e7d32; font-size:8pt;"
            "padding:6px; border-bottom:1px solid #a5d6a7;"
        )
        for key, btn in self._buttons.items():
            btn.setEnabled(self._plotter.capabilities.get(key, False))

    def _on_plot(self, key: str):
        if self._plotter is None:
            return

        if self._active_btn and self._active_btn is not self._buttons[key]:
            self._active_btn.setChecked(False)
        self._active_btn = self._buttons[key]
        self._active_btn.setChecked(True)

        try:
            widget = self._plotter.plot(key)
            if widget is None:
                return

            while self.canvas.count() > 1:
                w = self.canvas.widget(1)
                self.canvas.removeWidget(w)
                w.deleteLater()

            self.canvas.addWidget(widget)
            self.canvas.setCurrentIndex(1)

        except Exception as e:
            self.canvas.widget(0).setText(f"Error:\n{e}")
            self.canvas.setCurrentIndex(0)