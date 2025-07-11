import wx
import matplotlib
matplotlib.use('WXAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np


class plotter():
    def __init__(self, eps_sim, ez_dft, figure, canvas, ax):

        self.canvas = canvas
        self.figure = figure
        self.ax = ax
        self.colorbar = None


        self.data = ez_dft
        self.magnitude = np.abs(ez_dft)
        self.phase = np.angle(ez_dft)

        self.limit = len(self.magnitude) // 2

        self.extent = np.linspace(-self.limit, self.limit, len(self.magnitude))

        max_index = np.argmax(self.magnitude)
        self.coords = np.unravel_index(max_index, self.magnitude.shape)


    def line_graph_origin_x(self):

        self.figure.clf()                    # Clears everything
        self.ax = self.figure.add_subplot(1, 1, 1)

        self.ax.plot(self.extent, self.magnitude[:, self.limit - 1, self.limit - 1].T, color='blue')
        self.ax.grid(True)
        self.ax.set_xlabel('X-axis (y=0, z=0)', fontsize=14, fontweight='bold')
        self.ax.set_ylabel('|Ez|', fontsize=14, fontweight='bold')

        self.ax.figure.tight_layout()
        self.canvas.draw()



    def line_graph_focus_x(self):

        self.figure.clf()                    # Clears everything
        self.ax = self.figure.add_subplot(1, 1, 1)

        self.ax.plot(self.extent, self.magnitude[:, self.coords[1], self.coords[2]].T, color='blue')
        self.ax.grid(True)
        self.ax.set_xlabel(f'X-axis (y={self.coords[1]}, z={self.coords[2]})', fontsize=14, fontweight='bold')
        self.ax.set_ylabel('|Ez|', fontsize=14, fontweight='bold')

        self.ax.figure.tight_layout()
        self.canvas.draw()



    def line_graph_origin_y(self):

        self.figure.clf()                    # Clears everything
        self.ax = self.figure.add_subplot(1, 1, 1)

        self.ax.plot(self.extent, self.magnitude[self.limit - 1, :, self.limit - 1].T, color='blue')
        self.ax.grid(True)
        self.ax.set_xlabel('Y-axis (x=0, z=0)', fontsize=14, fontweight='bold')
        self.ax.set_ylabel('|Ez|', fontsize=14, fontweight='bold')

        self.ax.figure.tight_layout()
        self.canvas.draw()



    def line_graph_focus_y(self):

        self.figure.clf()                    # Clears everything
        self.ax = self.figure.add_subplot(1, 1, 1)

        self.ax.plot(self.extent, self.magnitude[self.coords[0], :, self.coords[2]].T, color='blue')
        self.ax.grid(True)
        self.ax.set_xlabel(f'Y-axis (x={self.coords[0]}, z={self.coords[2]})', fontsize=14, fontweight='bold')
        self.ax.set_ylabel('|Ez|', fontsize=14, fontweight='bold')

        self.ax.figure.tight_layout()
        self.canvas.draw()

        

    def line_graph_origin_z(self):

        self.figure.clf()                    # Clears everything
        self.ax = self.figure.add_subplot(1, 1, 1)

        self.ax.plot(self.extent, self.magnitude[self.limit - 1, self.limit - 1, :].T, color='blue')
        self.ax.grid(True)
        self.ax.set_xlabel('Z-axis (x=0, y=0)', fontsize=14, fontweight='bold')
        self.ax.set_ylabel('|Ez|', fontsize=14, fontweight='bold')

        self.ax.figure.tight_layout()
        self.canvas.draw()

    

    def line_graph_focus_z(self):

        self.figure.clf()                    # Clears everything
        self.ax = self.figure.add_subplot(1, 1, 1)

        self.ax.plot(self.extent, self.magnitude[self.coords[0], self.coords[1], :].T, color='blue')
        self.ax.grid(True)
        self.ax.set_xlabel(f'Z-axis (x={self.coords[0]}, y={self.coords[1]})', fontsize=14, fontweight='bold')
        self.ax.set_ylabel('|Ez|', fontsize=14, fontweight='bold')

        self.ax.figure.tight_layout()
        self.canvas.draw()



    def mag_plane_origin_xy(self):

        self.figure.clf()                    # Clears everything
        self.ax = self.figure.add_subplot(1, 1, 1)

        im = self.ax.imshow(self.magnitude[:, :, self.limit - 1].T, cmap='jet', origin='lower', extent=[-self.limit, self.limit, -self.limit, self.limit])
        self.colorbar = self.ax.figure.colorbar(im, ax=self.ax)
        self.ax.set_xlabel('X (z = 0)', fontsize=14, fontweight='bold')
        self.ax.set_ylabel('Y', fontsize=14, fontweight='bold')

        self.ax.figure.tight_layout()
        self.canvas.draw()



    def mag_plane_focus_xy(self):

        self.figure.clf()                    # Clears everything
        self.ax = self.figure.add_subplot(1, 1, 1)

        im = self.ax.imshow(self.magnitude[:, :, self.coords[2]].T, cmap='jet', origin='lower', extent=[-self.limit, self.limit, -self.limit, self.limit])
        self.colorbar = self.ax.figure.colorbar(im, ax=self.ax)
        self.ax.set_xlabel(f'X (z = {self.coords[2]})', fontsize=14, fontweight='bold')
        self.ax.set_ylabel('Y', fontsize=14, fontweight='bold')

        self.ax.figure.tight_layout()
        self.canvas.draw()

    

    def mag_plane_origin_yz(self):

        self.figure.clf()                    # Clears everything
        self.ax = self.figure.add_subplot(1, 1, 1)

        im = self.ax.imshow(self.magnitude[self.limit - 1, :, :].T, cmap='jet', origin='lower', extent=[-self.limit, self.limit, -self.limit, self.limit])
        self.colorbar = self.ax.figure.colorbar(im, ax=self.ax)
        self.ax.set_xlabel('Y (x = 0)', fontsize=14, fontweight='bold')
        self.ax.set_ylabel('Z', fontsize=14, fontweight='bold')

        self.ax.figure.tight_layout()
        self.canvas.draw()




    def mag_plane_focus_yz(self):

        self.figure.clf()                    # Clears everything
        self.ax = self.figure.add_subplot(1, 1, 1)

        im = self.ax.imshow(self.magnitude[self.coords[0], :, :].T, cmap='jet', origin='lower', extent=[-self.limit, self.limit, -self.limit, self.limit])
        self.colorbar = self.ax.figure.colorbar(im, ax=self.ax)
        self.ax.set_xlabel(f'Y (x = {self.coords[0]})', fontsize=14, fontweight='bold')
        self.ax.set_ylabel('Z', fontsize=14, fontweight='bold')

        self.ax.figure.tight_layout()
        self.canvas.draw()



    def mag_plane_origin_xz(self):

        self.figure.clf()                    # Clears everything
        self.ax = self.figure.add_subplot(1, 1, 1)

        im = self.ax.imshow(self.magnitude[:, self.limit - 1, :].T, cmap='jet', origin='lower', extent=[-self.limit, self.limit, -self.limit, self.limit])
        self.colorbar = self.ax.figure.colorbar(im, ax=self.ax)
        self.ax.set_xlabel('X (y = 0)', fontsize=14, fontweight='bold')
        self.ax.set_ylabel('Z', fontsize=14, fontweight='bold')

        self.ax.figure.tight_layout()
        self.canvas.draw()




    def mag_plane_focus_xz(self):

        self.figure.clf()                    # Clears everything
        self.ax = self.figure.add_subplot(1, 1, 1)

        im = self.ax.imshow(self.magnitude[:, self.coords[1], :].T, cmap='jet', origin='lower', extent=[-self.limit, self.limit, -self.limit, self.limit])
        self.colorbar = self.ax.figure.colorbar(im, ax=self.ax)
        self.ax.set_xlabel(f'X (y = {self.coords[1]})', fontsize=14, fontweight='bold')
        self.ax.set_ylabel('Z', fontsize=14, fontweight='bold')

        self.ax.figure.tight_layout()
        self.canvas.draw()



    def phase_plane_origin_xy(self):

        self.figure.clf()                    # Clears everything
        self.ax = self.figure.add_subplot(1, 1, 1)

        im = self.ax.imshow(self.phase[:, :, self.limit - 1].T, cmap='Blues', origin='lower', extent=[-self.limit, self.limit, -self.limit, self.limit])
        self.colorbar = self.ax.figure.colorbar(im, ax=self.ax)
        self.ax.set_xlabel('X (z = 0)', fontsize=14, fontweight='bold')
        self.ax.set_ylabel('Y', fontsize=14, fontweight='bold')

        self.ax.figure.tight_layout()
        self.canvas.draw()



    def phase_plane_focus_xy(self):

        self.figure.clf()                    # Clears everything
        self.ax = self.figure.add_subplot(1, 1, 1)

        im = self.ax.imshow(self.phase[:, :, self.coords[2]].T, cmap='Blues', origin='lower', extent=[-self.limit, self.limit, -self.limit, self.limit])
        self.colorbar = self.ax.figure.colorbar(im, ax=self.ax)
        self.ax.set_xlabel(f'X (z = {self.coords[2]})', fontsize=14, fontweight='bold')
        self.ax.set_ylabel('Y', fontsize=14, fontweight='bold')

        self.ax.figure.tight_layout()
        self.canvas.draw()

    

    def phase_plane_origin_yz(self):

        self.figure.clf()                    # Clears everything
        self.ax = self.figure.add_subplot(1, 1, 1)

        im = self.ax.imshow(self.phase[self.limit - 1, :, :].T, cmap='Blues', origin='lower', extent=[-self.limit, self.limit, -self.limit, self.limit])
        self.colorbar = self.ax.figure.colorbar(im, ax=self.ax)
        self.ax.set_xlabel('Y (x = 0)', fontsize=14, fontweight='bold')
        self.ax.set_ylabel('Z', fontsize=14, fontweight='bold')

        self.ax.figure.tight_layout()
        self.canvas.draw()




    def phase_plane_focus_yz(self):

        self.figure.clf()                    # Clears everything
        self.ax = self.figure.add_subplot(1, 1, 1)

        im = self.ax.imshow(self.phase[self.coords[0], :, :].T, cmap='Blues', origin='lower', extent=[-self.limit, self.limit, -self.limit, self.limit])
        self.colorbar = self.ax.figure.colorbar(im, ax=self.ax)
        self.ax.set_xlabel(f'Y (x = {self.coords[0]})', fontsize=14, fontweight='bold')
        self.ax.set_ylabel('Z', fontsize=14, fontweight='bold')

        self.ax.figure.tight_layout()
        self.canvas.draw()



    def phase_plane_origin_xz(self):

        self.figure.clf()                    # Clears everything
        self.ax = self.figure.add_subplot(1, 1, 1)

        im = self.ax.imshow(self.phase[:, self.limit - 1, :].T, cmap='Blues', origin='lower', extent=[-self.limit, self.limit, -self.limit, self.limit])
        self.colorbar = self.ax.figure.colorbar(im, ax=self.ax)
        self.ax.set_xlabel('X (y = 0)', fontsize=14, fontweight='bold')
        self.ax.set_ylabel('Z', fontsize=14, fontweight='bold')

        self.ax.figure.tight_layout()
        self.canvas.draw()




    def phase_plane_focus_xz(self):

        self.figure.clf()                    # Clears everything
        self.ax = self.figure.add_subplot(1, 1, 1)

        im = self.ax.imshow(self.phase[:, self.coords[1], :].T, cmap='Blues', origin='lower', extent=[-self.limit, self.limit, -self.limit, self.limit])
        self.colorbar = self.ax.figure.colorbar(im, ax=self.ax)
        self.ax.set_xlabel(f'X (y = {self.coords[1]})', fontsize=14, fontweight='bold')
        self.ax.set_ylabel('Z', fontsize=14, fontweight='bold')

        self.ax.figure.tight_layout()
        self.canvas.draw()