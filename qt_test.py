import os
os.environ["QT_QPA_PLATFORM"] = "xcb"
os.environ["QTWEBENGINE_DISABLE_GPU"] = "1"
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu"
os.environ["QT_OPENGL"] = "software"

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView

app = QApplication(sys.argv)
w = QWebEngineView()
w.setHtml("<h1>Hello</h1>")
w.show()
sys.exit(app.exec_())
