import os
os.environ["QT_QPA_PLATFORM"] = "xcb"
os.environ["QTWEBENGINE_DISABLE_GPU"] = "1"
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --disable-software-rasterizer"
os.environ["QT_OPENGL"] = "software"
os.environ["QTWEBENGINE_SANDBOX"] = "0"

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QSplitter, QLabel, QToolButton, QMenu, QAction, QFrame, QStackedWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

QApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)
app = QApplication(sys.argv)
app.setFont(QFont("Segoe UI", 9))

from core.cad.core.cad_scene import CADScene
from core.cad.cad_builder import CADBuilder
from core.cad.cad_primitives import *
from core.cad.cad_controller import CADController
from gui.properties.property_panel import PropertyPanel
from gui.viewer import PyVistaViewer
from gui.simulation.simulation_panel import SimulationPanel
from gui.app_controller import AppController
from gui.hierarchy.hierarchy_panel import HierarchyPanel
from gui.simulation.plot_panel import PlotPanel


# ribbon helpers

_BTN_STYLE = """
    QToolButton {
        border: none; border-radius: 4px; background: transparent;
        color: #222; font-size: 8pt; min-width: 52px; padding: 4px 2px 2px 2px;
    }
    QToolButton:hover { background: #e8f0fe; }
    QToolButton:pressed { background: #c5d8fc; }
    QToolButton::menu-indicator { image: none; }
"""

_TAB_STYLE = """
    QToolButton {
        border: none; border-bottom: 2px solid transparent;
        background: transparent; color: #444; padding: 0 18px; font-size: 9pt;
    }
    QToolButton:checked {
        color: #1a73e8; border-bottom: 2px solid #1a73e8;
        font-weight: bold; background: #f5f5f5;
    }
    QToolButton:hover:!checked { background: #e0e0e0; }
    QToolButton:disabled { color: #bbb; }
"""

_MENU_STYLE = """
    QMenu {
        background: #fff; border: 1px solid #ccc;
        border-radius: 6px; padding: 4px; font-size: 9pt;
    }
    QMenu::item { padding: 7px 24px; border-radius: 3px; }
    QMenu::item:selected { background: #e8f0fe; color: #1a73e8; }
"""


def _ribbon_btn(icon, label):
    btn = QToolButton()
    btn.setText(f"{icon}\n{label}")
    btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
    btn.setFixedSize(64, 48)
    btn.setFont(QFont("Segoe UI", 8))
    btn.setStyleSheet(_BTN_STYLE)
    return btn


class RibbonSection(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(6, 2, 6, 0)
        outer.setSpacing(0)
        self.row = QHBoxLayout()
        self.row.setContentsMargins(0, 0, 0, 0)
        self.row.setSpacing(2)
        outer.addLayout(self.row)
        lbl = QLabel(title)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("color:#888; font-size:8pt;")
        outer.addWidget(lbl)

    def add_btn(self, icon, label, cb, tip=None):
        btn = _ribbon_btn(icon, label)
        if tip:
            btn.setToolTip(tip)
        btn.clicked.connect(cb)
        self.row.addWidget(btn)
        return btn

    def add_dropdown(self, icon, label, items, tip=None):
        btn = _ribbon_btn(icon, label)
        btn.setPopupMode(QToolButton.InstantPopup)
        if tip:
            btn.setToolTip(tip)
        menu = QMenu(btn)
        menu.setStyleSheet(_MENU_STYLE)
        for item_label, cb in items:
            act = QAction(item_label, menu)
            act.triggered.connect(cb)
            menu.addAction(act)
        btn.setMenu(menu)
        self.row.addWidget(btn)
        return btn


class HomePanel(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 2, 8, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        insert = RibbonSection("Insert")
        insert.add_dropdown("◈", "Shape", [
            ("⬤   Sphere",   controller.add_sphere),
            ("⬭   Cylinder", controller.add_cylinder),
            ("⬛   Block",    controller.add_block),
            ("▲   Prism",    controller.add_prism),
        ])
        layout.addWidget(insert)

        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setFixedWidth(1)
        sep.setStyleSheet("color:#ddd;")
        layout.addWidget(sep)

        edit = RibbonSection("Edit")
        edit.add_btn("🗑", "Delete", controller.delete_selected, "Delete selected (Del)")
        edit.add_btn("⧉", "Duplicate", controller.duplicate_node, "Duplicate selected")
        edit.add_btn("💾", "Save", controller.save_scene, "Scene Saved")
        layout.addWidget(edit)

        layout.addStretch()


#  ribbon bar — tab buttons switch the body

class RibbonBar(QWidget):
    def __init__(self, body_stack: QStackedWidget, parent=None):
        super().__init__(parent)
        self.body_stack = body_stack
        self._tab_btns = []

        self.setFixedHeight(78)
        self.setStyleSheet("background:#f5f5f5;")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Tab button row
        tab_row = QWidget()
        tab_row.setFixedHeight(28)
        tab_row.setStyleSheet("background:#ebebeb; border-bottom:1px solid #ccc;")
        self._tab_row = QHBoxLayout(tab_row)
        self._tab_row.setContentsMargins(4, 0, 0, 0)
        self._tab_row.setSpacing(0)
        self._tab_row.addStretch()
        root.addWidget(tab_row)

        # Ribbon content (buttons for active tab)
        self._content_stack = QStackedWidget()
        self._content_stack.setFixedHeight(48)
        self._content_stack.setStyleSheet("background:#f5f5f5;")
        root.addWidget(self._content_stack)

        # Blue accent line
        accent = QFrame()
        accent.setFixedHeight(2)
        accent.setStyleSheet("background:#1a73e8;")
        root.addWidget(accent)

    def add_tab(self, ribbon_content: QWidget, body_widget: QWidget, label: str, enabled=True):
        idx = len(self._tab_btns)

        btn = QToolButton()
        btn.setText(label)
        btn.setCheckable(True)
        btn.setEnabled(enabled)
        btn.setFont(QFont("Segoe UI", 9))
        btn.setFixedHeight(28)
        btn.setStyleSheet(_TAB_STYLE)
        btn.clicked.connect(lambda _, i=idx: self._switch(i))

        pos = self._tab_row.count() - 1
        self._tab_row.insertWidget(pos, btn)
        self._tab_btns.append(btn)
        self._content_stack.addWidget(ribbon_content)
        self.body_stack.addWidget(body_widget)

        if idx == 0:
            btn.setChecked(True)

        return idx

    def _switch(self, idx):
        self._content_stack.setCurrentIndex(idx)
        self.body_stack.setCurrentIndex(idx)
        for i, btn in enumerate(self._tab_btns):
            btn.setChecked(i == idx)

    def set_tab_enabled(self, idx, enabled):
        self._tab_btns[idx].setEnabled(enabled)


#  status bar

class StatusBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(22)
        self.setStyleSheet("background:#1a73e8;")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        self.label = QLabel("Ready")
        self.label.setStyleSheet("color:white; font-size:8pt;")
        layout.addWidget(self.label)
        layout.addStretch()
        hint = QLabel("Del=Delete  R=Deselect  X/Y/Z=Move+  A/B/C=Move−")
        hint.setStyleSheet("color:rgba(255,255,255,0.7); font-size:8pt;")
        layout.addWidget(hint)

    def set_status(self, text):
        self.label.setText(text)


#  main window

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAD Sim")
        self.resize(1500, 900)

        scene = CADScene()
        builder = CADBuilder(scene)
        viewer = PyVistaViewer()
        viewer.setMinimumWidth(700)

        controller = CADController(builder=builder, viewer=viewer)
        # controller.duplicate_node_selected = lambda: controller.duplicate_node(controller.selected_node)

        property_panel = PropertyPanel(controller=controller, model=controller.property_model)
        hierarchy_panel = HierarchyPanel(controller, viewer)
        app_controller = AppController(builder)
        sim_panel = SimulationPanel(app_controller)
        plot_panel = PlotPanel()

        app_controller.plot_panel = plot_panel

        controller.hierarchy_panel = hierarchy_panel
        controller.properties_panel = property_panel
        hierarchy_panel.rebuild()

        # CAD body: viewer + right sidebar
        right_sidebar = QSplitter(Qt.Vertical)
        right_sidebar.addWidget(hierarchy_panel)
        right_sidebar.addWidget(property_panel)
        right_sidebar.addWidget(sim_panel)
        right_sidebar.setMinimumWidth(240)
        right_sidebar.setMaximumWidth(340)
        right_sidebar.setSizes([220, 220, 180])

        cad_body = QSplitter(Qt.Horizontal)
        cad_body.addWidget(viewer)
        cad_body.addWidget(right_sidebar)
        cad_body.setSizes([1150, 300])

        # Body stack switched by ribbon tabs
        body_stack = QStackedWidget()

        ribbon = RibbonBar(body_stack)
        ribbon.add_tab(HomePanel(controller), cad_body, "Home")
        plot_idx = ribbon.add_tab(QWidget(), plot_panel, "Plot", enabled=False)

        app_controller.simulation_finished.connect(
            lambda: ribbon.set_tab_enabled(plot_idx, True)
        )

        status_bar = StatusBar()
        controller._status_bar = status_bar


        # Simulation freeze/unfreeze
        def _freeze_ui(panels, ribbon_widget):
            for p in panels:
                p.setEnabled(False)
            ribbon_widget.setEnabled(False)
            viewer.simulation_running = True



        def _unfreeze_ui(panels, ribbon_widget):
            for p in panels:
                p.setEnabled(True)
            ribbon_widget.setEnabled(True)
            viewer.simulation_running = False


        panels_to_freeze = [hierarchy_panel, property_panel]


        app_controller.simulation_started.connect(
            lambda: _freeze_ui(panels_to_freeze, ribbon)
        )


        app_controller.simulation_finished.connect(
            lambda: _unfreeze_ui(panels_to_freeze, ribbon)
        )


        app_controller.simulation_error.connect(
            lambda _: _unfreeze_ui(panels_to_freeze, ribbon)
        )


        app_controller.simulation_cancelled.connect(
            lambda: _unfreeze_ui(panels_to_freeze, ribbon)
        )


        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(ribbon)
        layout.addWidget(body_stack, stretch=1)
        layout.addWidget(status_bar)

        self.setCentralWidget(root)
        viewer.show_geometry(builder.build())


window = MainWindow()
window.show()
sys.exit(app.exec_())