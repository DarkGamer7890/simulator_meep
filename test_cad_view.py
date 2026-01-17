import os

# Force X11, NOT Wayland
os.environ["QT_QPA_PLATFORM"] = "xcb"

# Disable GPU for QWebEngine
os.environ["QTWEBENGINE_DISABLE_GPU"] = "1"
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --disable-software-rasterizer"

# Avoid shared GL context crashes
os.environ["QT_OPENGL"] = "software"



import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter, QDockWidget
from PyQt5.QtCore import Qt
# from PyQt5.QtWebEngineWidgets import QWebEngineView

from core.cad.cad_scene import CADScene
# from core.cad.cad_node import CADNode
from core.cad.cad_builder import CADBuilder
from core.cad.cad_primitives import *
# from core.cad.transform import Transform
from core.cad.cad_controller import CADController
from gui.properties.property_panel import PropertyPanel
from gui.viewer import PyVistaViewer
# from core.simulation.simulation_controller import SimulationController
from gui.simulation.simulation_panel import SimulationPanel
from gui.app_controller import AppController
# from gui.plots.plot_panel import PlotPanel

# Create scene
scene = CADScene()
builder = CADBuilder(scene.root)

# Create QApplication
app = QApplication(sys.argv)

# Set application attributes for better compatibility
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

# Create property panel
property_panel = PropertyPanel(controller=controller, model=controller.property_model)

# Create app controller
app_controller = AppController(builder)

# Create plot panel as a dock widget
# plot_dock = QDockWidget("Plots", main_window)
# plot_panel = PlotPanel()
# plot_dock.setWidget(plot_panel)
# plot_dock.setMinimumHeight(200)

# Create simulation panel (NOT as dock widget, just in splitter)
sim_panel = SimulationPanel(app_controller)
# sim_panel = SimulationPanel(app_controller, plot_panel)

# Connect viewer selection to property panel
def on_selection_changed(node):
    print(f"Selection changed to: {node}")
    controller.property_model.node = node
    property_panel.refresh()

viewer.signals.selection_changed.connect(on_selection_changed)

# Create right side splitter with both panels
right_splitter = QSplitter(Qt.Vertical)
right_splitter.addWidget(property_panel)
right_splitter.addWidget(sim_panel)
right_splitter.setMinimumWidth(250)
right_splitter.setMaximumWidth(350)
right_splitter.setSizes([400, 200])

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