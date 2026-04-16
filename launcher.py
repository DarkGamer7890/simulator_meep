import sys
import multiprocessing
from pathlib import Path

# add project root to PYTHONPATH
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from gui.app import MainWindow
from PySide6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    win.plotter.render()
    sys.exit(app.exec())



if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
