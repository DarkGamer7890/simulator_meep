from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from gui.viewer import PyVistaViewer
import pyvista as pv


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAD Viewer")
        self.resize(800, 600)

        frame = QWidget()
        layout = QVBoxLayout(frame)
        self.setCentralWidget(frame)

        self.viewer = PyVistaViewer(frame)
        layout.addWidget(self.viewer.interactor)

