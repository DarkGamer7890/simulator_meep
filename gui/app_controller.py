import multiprocessing
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from core.simulation.simulation_controller import SimulationController, _simulation_worker
from core.simulation.simulation_data import SimulationData


class SimulationWatcher(QObject):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    progress = pyqtSignal(float)   # 0.0 – 1.0
    cancelled = pyqtSignal()

    def __init__(self, queue, process):
        super().__init__()
        self.queue = queue
        self.process = process
        self._cancel_requested = False

    def request_cancel(self):
        self._cancel_requested = True

    def watch(self):
        while True:
            result = self.queue.get()   # blocks only this QThread

            kind = result[0]

            if kind == "progress":
                self.progress.emit(result[1])

            elif kind == "success":
                self.process.join()
                self.finished.emit((result[1], result[2]))
                return

            elif kind == "error":
                self.process.join()
                self.error.emit(result[1])
                return
            
            elif kind == "cancelled":
                self.cancelled.emit()
                return


class AppController(QObject):
    simulation_started  = pyqtSignal()
    simulation_finished = pyqtSignal()
    simulation_error    = pyqtSignal(str)
    simulation_progress = pyqtSignal(float)
    simulation_cancelled = pyqtSignal()

    def __init__(self, cad_builder):
        super().__init__()
        self.builder = cad_builder
        self.simulation_controller = SimulationController(cad_builder)
        self.plot_panel = None
        self.last_sim_data: SimulationData = None
        self._process = None
        self._watcher_thread = None
        self._watcher = None
        self._pending_pml = 1.0
        self._pending_resolution = 20

    def run_simulation(self, config):
        if self._process is not None and self._process.is_alive():
            print("Simulation already running")
            return

        self._pending_pml = config.pml
        self._pending_resolution = config.resolution

        geometry = self.simulation_controller.prepare_geometry()
        config_dict = {
            "cell_size":     config.cell_size,
            "resolution":    config.resolution,
            "pml":           config.pml,
            "source_center": config.source_center,
            "source_size":   config.source_size,
            "frequency":     config.frequency,
            "time":          config.time,
        }

        queue = multiprocessing.Queue()
        self._process = multiprocessing.Process(
            target=_simulation_worker,
            args=(queue, geometry, config_dict),
            daemon=True
        )
        self._process.start()

        self._watcher_thread = QThread()
        self._watcher = SimulationWatcher(queue, self._process)
        self._watcher.moveToThread(self._watcher_thread)

        self._watcher_thread.started.connect(self._watcher.watch)
        self._watcher.finished.connect(self._on_finished)
        self._watcher.error.connect(self._on_error)
        self._watcher.progress.connect(self.simulation_progress)
        self._watcher.cancelled.connect(self._on_cancelled)

        self._watcher.finished.connect(self._watcher_thread.quit)
        self._watcher.error.connect(self._watcher_thread.quit)
        self._watcher.cancelled.connect(self._watcher_thread.quit)
        self._watcher_thread.finished.connect(self._watcher.deleteLater)
        self._watcher_thread.finished.connect(self._watcher_thread.deleteLater)

        self._watcher_thread.start()
        self.simulation_started.emit()

    def cancel_simulation(self):
        if self._process is not None and self._process.is_alive():
            self._process.terminate()
            self._process.join()

        # unblock queue.get() in the watcher thread
        if self._watcher is not None:
            self._watcher.queue.put(("cancelled",))

    def _on_finished(self, result):
        eps_sim, ez_dft = result
        self.last_sim_data = SimulationData(
            eps_sim=eps_sim,
            ez_dft=ez_dft,
            pml=self._pending_pml,
            resolution=self._pending_resolution,
        )
        if self.plot_panel is not None:
            self.plot_panel.set_simulation_data(self.last_sim_data)
        self.simulation_finished.emit()

    def _on_error(self, error_msg):
        print("Simulation error:", error_msg)
        self.simulation_error.emit(error_msg)

    def _on_cancelled(self):
        print("Simulation cancelled")
        self.simulation_cancelled.emit()