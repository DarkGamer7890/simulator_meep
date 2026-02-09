import pyvista as pv
from pyvistaqt import QtInteractor
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import vtk


class PyVistaViewerSignals(QObject):
    move_requested = pyqtSignal(object, tuple)
    add_sphere_requested = pyqtSignal()
    add_cylinder_requested = pyqtSignal()
    add_block_requested = pyqtSignal()
    add_prism_requested = pyqtSignal()
    delete_requested = pyqtSignal()
    selection_changed = pyqtSignal(object)


class PyVistaViewer(QtInteractor):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create signals object
        self.signals = PyVistaViewerSignals()
        
        # Scene setup
        self.set_background("white")
        self.show_axes()
        
        self.geometry_actors = []
        self.actor_to_node = {}
        self.node_to_actor = {}  # ADD THIS - reverse mapping
        self.selected_actor = None
        self.selected_node = None
        
        self._add_xy_grid()
        
        self.enable_cell_picking(
            callback=self._on_pick,
            show=False,
            left_clicking=True,  # CHANGED: Enable left click
            through=False
        )

    # -------------------------------------------------
    # Scene control
    # -------------------------------------------------
    
    def clear(self):
        for actor in self.geometry_actors:
            self.remove_actor(actor)
        self.geometry_actors.clear()
        self.actor_to_node.clear()
        self.node_to_actor.clear()  # ADD THIS

    def show_geometry(self, geometries):
        # Save camera position before clearing
        saved_camera_position = None
        if self.geometry_actors:
            saved_camera_position = self.camera_position
        
        # Keep track of which node was selected to re-select it
        previously_selected_node = self.selected_node
        
        self.clear()
        
        for node, geom in geometries:
            mesh = geom.to_plot()
            if mesh is None:
                continue
            
            pv_mesh = pv.wrap(mesh)
            actor = self.add_mesh(
                pv_mesh,
                color="lightblue",
                opacity=0.5,
                show_edges=True,
                style="surface",
                pickable=True,
                reset_camera=False
            )
            
            self._apply_transform_to_actor(actor, node.transform)
            
            self.geometry_actors.append(actor)
            self.actor_to_node[actor] = node
            self.node_to_actor[node] = actor  # ADD THIS
            
            # Re-select the previously selected node
            if previously_selected_node is not None and node is previously_selected_node:
                self.selected_actor = actor
                self.selected_node = node
                actor.GetProperty().SetColor(1.0, 0.2, 0.2)
                actor.GetProperty().SetOpacity(0.8)
        
        # Handle camera positioning
        if self.geometry_actors:
            if saved_camera_position is None:
                self.reset_camera(bounds=self._get_geometry_bounds())
            else:
                self.camera_position = saved_camera_position
        
        self.render()

    def _get_geometry_bounds(self):
        if not self.geometry_actors:
            return None
        
        bounds = None
        for actor in self.geometry_actors:
            b = actor.GetBounds()
            if bounds is None:
                bounds = list(b)
            else:
                bounds = [
                    min(bounds[0], b[0]), max(bounds[1], b[1]),
                    min(bounds[2], b[2]), max(bounds[3], b[3]),
                    min(bounds[4], b[4]), max(bounds[5], b[5]),
                ]
        return bounds

    # -------------------------------------------------
    # Grid
    # -------------------------------------------------
    
    def _add_xy_grid(self):
        grid_size = 200
        spacing = 1.0
        plane = pv.Plane(
            center=(0, 0, 0),
            direction=(0, 0, 1),
            i_size=grid_size,
            j_size=grid_size,
            i_resolution=int(grid_size / spacing),
            j_resolution=int(grid_size / spacing),
        )
        self.add_mesh(
            plane,
            style="wireframe",
            color="lightgray",
            opacity=0.4,
            pickable=False,
            reset_camera=False,
        )

    # -------------------------------------------------
    # Camera
    # -------------------------------------------------
    
    def reset_camera_to_geometry(self):
        if not self.geometry_actors:
            return
        
        bounds = self._get_geometry_bounds()
        if bounds:
            self.reset_camera(bounds=bounds)
            self.render()

    # -------------------------------------------------
    # Picking callback
    # -------------------------------------------------
    
    def _on_pick(self, *args, **kwargs):
        """
        Picking callback - handle different callback signatures.
        PyVista's callback can pass different arguments.
        """
        # Get the actor from the picker object
        if not hasattr(self, 'picker') or self.picker is None:
            return

        actor = self.picker.GetActor()

        if actor is None:
            return

        # Only process if it's one of our geometry actors
        if actor not in self.actor_to_node:
            return

        node = self.actor_to_node[actor]
        if node:
            # Emit signal for controller to handle
            self.signals.selection_changed.emit(node)

    # -------------------------------------------------
    # Keyboard movement
    # -------------------------------------------------
    
    def keyPressEvent(self, event):
        key = event.key()
        
        # Shape addition shortcuts
        if key == Qt.Key_1:
            self.signals.add_sphere_requested.emit()
            return
        elif key == Qt.Key_2:
            self.signals.add_cylinder_requested.emit()
            return
        elif key == Qt.Key_3:
            self.signals.add_block_requested.emit()
            return
        elif key == Qt.Key_4:
            self.signals.add_prism_requested.emit()
            return
        elif key == Qt.Key_Delete:
            self.signals.delete_requested.emit()
            return
        
        # Deselect
        if key == Qt.Key_R:
            if self.selected_node is not None:
                self.deselect_all()
                return
            else:
                super().keyPressEvent(event)
                return
        
        # Movement requires selection
        if self.selected_node is None:
            super().keyPressEvent(event)
            return
        
        step = 0.5
        dx = dy = dz = 0.0
        
        if key == Qt.Key_X:
            dx = step
        elif key == Qt.Key_Y:
            dy = step
        elif key == Qt.Key_Z:
            dz = step
        elif key == Qt.Key_A:
            dx = -step
        elif key == Qt.Key_B:
            dy = -step
        elif key == Qt.Key_C:
            dz = -step
        else:
            super().keyPressEvent(event)
            return
        
        if not event.isAutoRepeat():
            self.signals.move_requested.emit(self.selected_node, (dx, dy, dz))

    # -------------------------------------------------
    # Selection management
    # -------------------------------------------------
    
    def deselect_all(self):
        """Clear selection and emit signal."""
        self.clear_highlight()
        self.selected_actor = None
        self.selected_node = None
        self.signals.selection_changed.emit(None)
        self.render()

    def highlight_node(self, node):
        """Pure visual highlight. NO callbacks."""
        self.clear_highlight()
        
        if node is None:
            self.selected_node = None
            self.selected_actor = None
            return
        
        actor = self.node_to_actor.get(node)
        if actor is not None:
            self.selected_actor = actor
            self.selected_node = node
            actor.GetProperty().SetColor(1.0, 0.2, 0.2)
            actor.GetProperty().SetOpacity(0.8)
            self.render()

    def clear_highlight(self):
        """Remove visual highlight only."""
        if self.selected_actor is not None:
            self.selected_actor.GetProperty().SetColor(0.678, 0.847, 0.902)
            self.selected_actor.GetProperty().SetOpacity(0.5)

    # -------------------------------------------------
    # Transform
    # -------------------------------------------------
    
    def _apply_transform_to_actor(self, actor, transform):
        M = transform.matrix()  # 4x4 numpy
        vtk_t = vtk.vtkTransform()
        vtk_t.SetMatrix(M.flatten())
        actor.SetUserTransform(vtk_t)