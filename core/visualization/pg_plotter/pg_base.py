import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")
pg.setConfigOptions(antialias=True)

_JET = pg.colormap.get("jet", source="matplotlib")
_BLUES = pg.colormap.get("Blues", source="matplotlib")
_PEN = pg.mkPen(color="#1a73e8", width=2)


def _wrap(inner, label_widget=None):
    w = QWidget()
    l = QVBoxLayout(w)
    l.setContentsMargins(0, 0, 0, 0)
    l.setSpacing(0)
    if label_widget:
        l.addWidget(label_widget)
    l.addWidget(inner)
    return w


def line_widget(x: np.ndarray, y: np.ndarray, title: str, xlabel: str) -> QWidget:
    x = np.asarray(x, float)
    y = np.asarray(y, float)

    pw = pg.PlotWidget()
    pw.setTitle(title, size="10pt")
    pw.setLabel("bottom", xlabel)
    pw.setLabel("left", "|Ez|")
    pw.showGrid(x=True, y=True, alpha=0.3)
    pw.plot(x, y, pen=_PEN)

    hover_label = QLabel("Hover over plot")
    hover_label.setAlignment(Qt.AlignLeft)
    hover_label.setStyleSheet("font-size:8pt; color:#555; padding:2px 6px;")

    vline = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen("#aaa", width=1, style=Qt.DashLine))
    pw.addItem(vline, ignoreBounds=True)

    def on_mouse_move(evt):
        pos = evt[0]
        if pw.sceneBoundingRect().contains(pos):
            mp = pw.getPlotItem().vb.mapSceneToView(pos)
            idx = int(np.clip(np.searchsorted(x, mp.x()), 0, len(x) - 1))
            vline.setPos(x[idx])
            hover_label.setText(f"  {xlabel} = {x[idx]:.4f}   |Ez| = {y[idx]:.6f}")

    pw._hover_proxy = pg.SignalProxy(pw.scene().sigMouseMoved, rateLimit=60, slot=on_mouse_move)
    return _wrap(pw, hover_label)


def heatmap_widget(z: np.ndarray, axis: np.ndarray,
                   title: str, xlabel: str, ylabel: str,
                   cmap=None) -> QWidget:
    z = np.asarray(z, float)
    axis = np.asarray(axis, float)
    cmap = cmap or _JET
    x0, x1 = axis[0], axis[-1]
    y0, y1 = axis[0], axis[-1]

    glw = pg.GraphicsLayoutWidget()
    plot = glw.addPlot()
    plot.setTitle(title, size="10pt")
    plot.setLabel("bottom", xlabel)
    plot.setLabel("left", ylabel)
    plot.setAspectLocked(True)

    img = pg.ImageItem(z)
    nx, ny = z.shape

    transform = pg.QtGui.QTransform()
    transform.translate(x0, y0)
    transform.scale((x1 - x0) / nx, (y1 - y0) / ny)
    img.setTransform(transform)

    img.setColorMap(cmap)
    plot.addItem(img)

    cb = pg.ColorBarItem(values=(z.min(), z.max()), colorMap=cmap, interactive=True)
    cb.setImageItem(img, insert_in=plot)

    hover_label = QLabel("Hover over plot")
    hover_label.setAlignment(Qt.AlignLeft)
    hover_label.setStyleSheet("font-size:8pt; color:#555; padding:2px 6px;")

    def on_mouse_move(evt):
        pos = evt[0]
        if plot.sceneBoundingRect().contains(pos):
            mp = plot.vb.mapSceneToView(pos)
            px, py = mp.x(), mp.y()
            xi = int(np.clip(np.interp(px, [x0, x1], [0, z.shape[0] - 1]), 0, z.shape[0] - 1))
            yi = int(np.clip(np.interp(py, [y0, y1], [0, z.shape[1] - 1]), 0, z.shape[1] - 1))
            hover_label.setText(f"  {xlabel} = {px:.4f}   {ylabel} = {py:.4f}   |Ez| = {z[xi, yi]:.6f}")

    glw._hover_proxy = pg.SignalProxy(glw.scene().sigMouseMoved, rateLimit=60, slot=on_mouse_move)
    return _wrap(glw, hover_label)


def contour_widget(z: np.ndarray, axis: np.ndarray,
                   title: str, xlabel: str, ylabel: str,
                   levels: int = 15) -> QWidget:
    z = np.asarray(z, float)
    axis = np.asarray(axis, float)
    x0, x1 = axis[0], axis[-1]
    y0, y1 = axis[0], axis[-1]
    zmin, zmax = z.min(), z.max()

    glw = pg.GraphicsLayoutWidget()
    plot = glw.addPlot()
    plot.setTitle(title, size="10pt")
    plot.setLabel("bottom", xlabel)
    plot.setLabel("left", ylabel)
    plot.setAspectLocked(True)

    # img = pg.ImageItem(z)
    # nx, ny = z.shape

    # transform = pg.QtGui.QTransform()
    # transform.translate(x0, y0)
    # transform.scale((x1 - x0) / nx, (y1 - y0) / ny)
    # img.setTransform(transform)
    
    # img.setColorMap(_JET)
    # img.setOpacity(0.4)
    # plot.addItem(img)

    for level in np.linspace(zmin, zmax, levels):
        t = (level - zmin) / (zmax - zmin + 1e-12)
        iso = pg.IsocurveItem(data=z, level=level, pen=pg.mkPen(_JET.map(t, mode="qcolor")))
        # iso.setParentItem(img)
        plot.addItem(iso)

    # cb = pg.ColorBarItem(values=(zmin, zmax), colorMap=_JET, interactive=False)
    # cb.setImageItem(img, insert_in=plot)

    hover_label = QLabel("Hover over plot")
    hover_label.setAlignment(Qt.AlignLeft)
    hover_label.setStyleSheet("font-size:8pt; color:#555; padding:2px 6px;")

    def on_mouse_move(evt):
        pos = evt[0]
        if plot.sceneBoundingRect().contains(pos):
            mp = plot.vb.mapSceneToView(pos)
            px, py = mp.x(), mp.y()
            xi = int(np.clip(np.interp(px, [x0, x1], [0, z.shape[0] - 1]), 0, z.shape[0] - 1))
            yi = int(np.clip(np.interp(py, [y0, y1], [0, z.shape[1] - 1]), 0, z.shape[1] - 1))
            hover_label.setText(f"  {xlabel} = {px:.4f}   {ylabel} = {py:.4f}   |Ez| = {z[xi, yi]:.6f}")

    glw._hover_proxy = pg.SignalProxy(glw.scene().sigMouseMoved, rateLimit=60, slot=on_mouse_move)
    return _wrap(glw, hover_label)