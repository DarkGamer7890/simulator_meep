from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView


class PlotPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.view = QWebEngineView()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)

    def show_figure(self, fig):
        html = fig.to_html(include_plotlyjs="cdn")
        self.view.setHtml(html)
