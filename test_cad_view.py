import os
os.environ["QT_QPA_PLATFORM"] = "xcb"
os.environ["QTWEBENGINE_DISABLE_GPU"] = "1"
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --disable-software-rasterizer"
os.environ["QT_OPENGL"] = "software"

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter, QDockWidget
from PyQt5.QtCore import Qt

from core.cad.core.cad_scene import CADScene
from core.cad.cad_builder import CADBuilder
from core.cad.cad_primitives import *
from core.cad.cad_controller import CADController
from gui.properties.property_panel import PropertyPanel
from gui.viewer import PyVistaViewer
from gui.simulation.simulation_panel import SimulationPanel
from gui.app_controller import AppController
from gui.hierarchy.hierarchy_panel import HierarchyPanel

# Create scene
scene = CADScene()
builder = CADBuilder(scene.root)

# Create QApplication
app = QApplication(sys.argv)
app.setAttribute(Qt.AA_ShareOpenGLContexts, True)

# Create main window
main_window = QMainWindow()
main_window.setWindowTitle("CAD Viewer")
main_window.resize(1400, 800)

# Central widget with layout
central_widget = QWidget()
main_layout = QHBoxLayout(central_widget)

# Create viewer
viewer = PyVistaViewer()
viewer.setMinimumWidth(800)

# Create controller
controller = CADController(builder=builder, viewer=viewer)

# Create panels
property_panel = PropertyPanel(controller=controller, model=controller.property_model)
hierarchy_panel = HierarchyPanel(controller, viewer)

# Connect panels to controller
controller.hierarchy_panel = hierarchy_panel
controller.properties_panel = property_panel

# Rebuild hierarchy
hierarchy_panel.rebuild()

# Create app controller
app_controller = AppController(builder)

# Create simulation panel
sim_panel = SimulationPanel(app_controller)

# Create right side splitter with both panels
right_splitter = QSplitter(Qt.Vertical)
right_splitter.addWidget(hierarchy_panel)
right_splitter.addWidget(property_panel)
right_splitter.addWidget(sim_panel)
right_splitter.setMinimumWidth(250)
right_splitter.setMaximumWidth(350)

# Add widgets to main layout
main_layout.addWidget(viewer, stretch=3)
main_layout.addWidget(right_splitter, stretch=1)

# Set central widget
main_window.setCentralWidget(central_widget)

# Show the window
main_window.show()

# Initial geometry display
geometry = builder.build()
viewer.show_geometry(geometry)

sys.exit(app.exec_())