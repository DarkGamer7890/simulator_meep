import os
os.environ["QT_QPA_PLATFORM"] = "xcb"

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

app = QApplication(sys.argv)

view = QWebEngineView()
view.load(QUrl.fromLocalFile(sys.argv[1]))
view.resize(1000, 700)
view.show()

sys.exit(app.exec_())
