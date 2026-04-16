import matplotlib
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np


class Plotter():
    def __init__(self, eps_sim, ez_dft, figure, canvas, ax, pml, resolution):

        
        self.canvas = canvas
        self.figure = figure
        self.ax = ax
        self.ax = self.figure.add_subplot(1, 1, 1)
        
        self.colorbar = None
        self.pml = pml
        self.resolution = resolution

        self.data = ez_dft
        self.magnitude = np.abs(ez_dft)
        self.phase = np.angle(ez_dft)


        self.crop = int(self.pml * self.resolution)
        self.is_3D = (ez_dft.ndim == 3)

        if self.is_3D: 
            self.magnitude = self.magnitude[self.crop - 1: -self.crop, self.crop - 1: -self.crop, self.crop - 1: -self.crop]
        else:
            self.magnitude = self.magnitude[self.crop - 1: -self.crop, self.crop - 1: -self.crop]

        self.center = len(self.magnitude) // 2
        self.limit = int(len(self.magnitude) // 2)
        print(len(self.magnitude))


       

        self.extent = np.linspace(-self.limit, self.limit, len(self.magnitude))

        max_index = np.argmax(self.magnitude)
        self.coords = np.unravel_index(max_index, self.magnitude.shape)

        self.capabilities = {
            "line_graph_origin_x": True,
            "line_graph_origin_y": True,
            "line_graph_origin_z": self.is_3D,

            "line_graph_focus_x": True,
            "line_graph_focus_y": True,
            "line_graph_focus_z": self.is_3D,

            "mag_plane_origin_xy": True,
            "mag_plane_origin_yz": self.is_3D,
            "mag_plane_origin_xz": self.is_3D,

            "mag_plane_focus_xy": self.is_3D,
            "mag_plane_focus_yz": self.is_3D,
            "mag_plane_focus_xz": self.is_3D,

            "phase_plane_origin_xy": True,
            "phase_plane_origin_yz": self.is_3D,
            "phase_plane_origin_xz": self.is_3D,

            "phase_plane_focus_xy": self.is_3D,
            "phase_plane_focus_yz": self.is_3D,
            "phase_plane_focus_xz": self.is_3D,

            "contour_origin_xy": True,
            "contour_origin_yz": self.is_3D,
            "contour_origin_xz": self.is_3D,

            "contour_focus_xy": self.is_3D,
            "contour_focus_yz": self.is_3D,
            "contour_focus_xz": self.is_3D,
        }




    def plot(self, method_name: str):
        """
        Safely call a plotting method by name.
        """
        if not self.capabilities.get(method_name, False):
            return None
    
        method = getattr(self, method_name, None)
        if method is None:
            return None
    
        return method()
    


    def _reset_axis(self):
        self.figure.clf()
        self.ax = self.figure.add_subplot(1, 1, 1)   



    def line_graph_origin_x(self):
        self._reset_axis()
    
        if self.is_3D:
            ydata = self.magnitude[:, self.center, self.center]
            xlabel = "X-axis (y=0, z=0)"
        else:
            ydata = self.magnitude[:, self.center]
            xlabel = "X-axis (y=0)"
    
        self.ax.plot(self.extent, ydata.T)
        self.ax.grid(True)
    
        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel("|Ez|", fontsize=14, fontweight="bold")
        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
    
        self.figure.tight_layout()
        return self.figure




    def line_graph_focus_x(self):

        self.figure.clf()                   
        self.ax = self.figure.add_subplot(1, 1, 1)

        if self.is_3D:
            ydata = self.magnitude[:, self.coords[1], self.coords[2]]
            xlabel = f"X-axis (y={self.coords[1] - self.center}, z={self.coords[2] - self.center})"
        else:
            ydata = self.magnitude[:, self.coords[1]]
            xlabel = f"X-axis (y={self.coords[1] - self.center})"

        self.ax.plot(self.extent, ydata.T)
        self.ax.grid(True)
    
        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel("|Ez|", fontsize=14, fontweight="bold")
        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
    
        self.figure.tight_layout()
        return self.figure



    def line_graph_origin_y(self):

        self._reset_axis()
    
        if self.is_3D:
            ydata = self.magnitude[self.center, :, self.center]
            xlabel = "Y-axis (x=0, z=0)"
        else:
            ydata = self.magnitude[self.center, :]
            xlabel = "Y-axis (x=0)"
    
        self.ax.plot(self.extent, ydata.T)
        self.ax.grid(True)
    
        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel("|Ez|", fontsize=14, fontweight="bold")
        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
    
        self.figure.tight_layout()
        return self.figure



    def line_graph_focus_y(self):

        self.figure.clf()                   
        self.ax = self.figure.add_subplot(1, 1, 1)

        if self.is_3D:
            ydata = self.magnitude[self.coords[0], :, self.coords[2]]
            xlabel = f"Y-axis (x={self.coords[0] - self.center}, z={self.coords[2] - self.center})"
        else:
            ydata = self.magnitude[self.coords[0], :]
            xlabel = f"Y-axis (x={self.coords[0] - self.center})"

        self.ax.plot(self.extent, ydata.T)
        self.ax.grid(True)
    
        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel("|Ez|", fontsize=14, fontweight="bold")
        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
    
        self.figure.tight_layout()
        return self.figure

        

    def line_graph_origin_z(self):

        if not self.is_3D:
            return None
    
        self._reset_axis()
    
        
        ydata = self.magnitude[self.center, self.center, :]
        xlabel = "Z-axis (x=0, y=0)"
    
        self.ax.plot(self.extent, ydata.T)
        self.ax.grid(True)
    
        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel("|Ez|", fontsize=14, fontweight="bold")
        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
    
        self.figure.tight_layout()
        return self.figure

    

    def line_graph_focus_z(self):

        if not self.is_3D:
            return None

        self.figure.clf()                   
        self.ax = self.figure.add_subplot(1, 1, 1)

        
        ydata = self.magnitude[self.coords[0], self.coords[1], :]
        xlabel = f"Z-axis (x={self.coords[0] - self.center}, y={self.coords[1] - self.center})"

        self.ax.plot(self.extent, ydata.T)
        self.ax.grid(True)
    
        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel("|Ez|", fontsize=14, fontweight="bold")
        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
    
        self.figure.tight_layout()
        return self.figure



    def mag_plane_origin_xy(self):

        self.figure.clf()
        self.colorbar = None
        self.ax = self.figure.add_subplot(1, 1, 1)

        if self.is_3D:
            data = self.magnitude[:, :, self.center].T
            xlabel = "X (z = 0)"
            ylabel = "Y"
        else:
            data = self.magnitude.T
            xlabel = "X"
            ylabel = "Y"

        im = self.ax.imshow(
            data,
            cmap="jet",
            origin="lower",
            extent=[-self.limit, self.limit, -self.limit, self.limit],
        )

        self.colorbar = self.figure.colorbar(im, ax=self.ax)

        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel(ylabel, fontsize=14, fontweight="bold")

        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
        self.ax.set_yticks(np.arange(-self.limit, self.limit + 1))

        self.figure.tight_layout()
        return self.figure



    def mag_plane_focus_xy(self):

        if not self.is_3D:
            return None

        self.figure.clf()
        self.colorbar = None
        self.ax = self.figure.add_subplot(1, 1, 1)


        data = self.magnitude[:, :, self.coords[2]].T
        xlabel = f"X (z = {self.coords[2] - self.center})"
        ylabel = "Y"

        im = self.ax.imshow(
            data,
            cmap="jet",
            origin="lower",
            extent=[-self.limit, self.limit, -self.limit, self.limit],
        )

        self.colorbar = self.figure.colorbar(im, ax=self.ax)

        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel(ylabel, fontsize=14, fontweight="bold")

        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
        self.ax.set_yticks(np.arange(-self.limit, self.limit + 1))

        self.figure.tight_layout()
        return self.figure

    

    def mag_plane_origin_yz(self):

        if not self.is_3D:
            return None

        self.figure.clf()
        self.colorbar = None
        self.ax = self.figure.add_subplot(1, 1, 1)

        
        data = self.magnitude[self.center, :, :].T
        xlabel = "Y (x = 0)"
        ylabel = "Z"

        im = self.ax.imshow(
            data,
            cmap="jet",
            origin="lower",
            extent=[-self.limit, self.limit, -self.limit, self.limit],
        )

        self.colorbar = self.figure.colorbar(im, ax=self.ax)

        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel(ylabel, fontsize=14, fontweight="bold")

        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
        self.ax.set_yticks(np.arange(-self.limit, self.limit + 1))

        self.figure.tight_layout()
        return self.figure



    def mag_plane_focus_yz(self):

        if not self.is_3D:
            return None

        self.figure.clf()
        self.colorbar = None
        self.ax = self.figure.add_subplot(1, 1, 1)


        data = self.magnitude[self.coords[0], :, :].T
        xlabel = f"Y (x = {self.coords[0] - self.center})"
        ylabel = "Z"

        im = self.ax.imshow(
            data,
            cmap="jet",
            origin="lower",
            extent=[-self.limit, self.limit, -self.limit, self.limit],
        )

        self.colorbar = self.figure.colorbar(im, ax=self.ax)

        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel(ylabel, fontsize=14, fontweight="bold")

        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
        self.ax.set_yticks(np.arange(-self.limit, self.limit + 1))

        self.figure.tight_layout()
        return self.figure



    def mag_plane_origin_xz(self):

        if not self.is_3D:
            return None

        self.figure.clf()
        self.colorbar = None
        self.ax = self.figure.add_subplot(1, 1, 1)

        
        data = self.magnitude[:, self.center, :].T
        xlabel = "X (y = 0)"
        ylabel = "Z"

        im = self.ax.imshow(
            data,
            cmap="jet",
            origin="lower",
            extent=[-self.limit, self.limit, -self.limit, self.limit],
        )

        self.colorbar = self.figure.colorbar(im, ax=self.ax)

        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel(ylabel, fontsize=14, fontweight="bold")

        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
        self.ax.set_yticks(np.arange(-self.limit, self.limit + 1))

        self.figure.tight_layout()
        return self.figure



    def mag_plane_focus_xz(self):

        if not self.is_3D:
            return None

        self.figure.clf()
        self.colorbar = None
        self.ax = self.figure.add_subplot(1, 1, 1)

        # 3D: take XY slice at z = center
        data = self.magnitude[:, self.coords[1], :].T
        xlabel = f"X (y = {self.coords[1] - self.center})"
        ylabel = "Z"

        im = self.ax.imshow(
            data,
            cmap="jet",
            origin="lower",
            extent=[-self.limit, self.limit, -self.limit, self.limit],
        )

        self.colorbar = self.figure.colorbar(im, ax=self.ax)

        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel(ylabel, fontsize=14, fontweight="bold")

        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
        self.ax.set_yticks(np.arange(-self.limit, self.limit + 1))

        self.figure.tight_layout()
        return self.figure



    def phase_plane_origin_xy(self):

        self.figure.clf()
        self.colorbar = None
        self.ax = self.figure.add_subplot(1, 1, 1)

        if self.is_3D:
            data = self.phase[:, :, self.center].T
            xlabel = "X (z = 0)"
            ylabel = "Y"
        else:
            data = self.magnitude.T
            xlabel = "X"
            ylabel = "Y"

        im = self.ax.imshow(
            data,
            cmap="Blues",
            origin="lower",
            extent=[-self.limit, self.limit, -self.limit, self.limit],
        )

        self.colorbar = self.figure.colorbar(im, ax=self.ax)

        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel(ylabel, fontsize=14, fontweight="bold")

        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
        self.ax.set_yticks(np.arange(-self.limit, self.limit + 1))

        self.figure.tight_layout()
        return self.figure



    def phase_plane_focus_xy(self):

        if not self.is_3D:
            return None

        self.figure.clf()
        self.colorbar = None
        self.ax = self.figure.add_subplot(1, 1, 1)

        # 3D: take XY slice at z = center
        data = self.phase[:, :, self.coords[2]].T
        xlabel = f"X (z = {self.coords[2] - self.center})"
        ylabel = "Y"

        im = self.ax.imshow(
            data,
            cmap="Blues",
            origin="lower",
            extent=[-self.limit, self.limit, -self.limit, self.limit],
        )

        self.colorbar = self.figure.colorbar(im, ax=self.ax)

        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel(ylabel, fontsize=14, fontweight="bold")

        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
        self.ax.set_yticks(np.arange(-self.limit, self.limit + 1))

        self.figure.tight_layout()
        return self.figure

    

    def phase_plane_origin_yz(self):

        if not self.is_3D:
            return None

        self.figure.clf()
        self.colorbar = None
        self.ax = self.figure.add_subplot(1, 1, 1)

        
        data = self.phase[self.center, :, :].T
        xlabel = "Y (x = 0)"
        ylabel = "Z"

        im = self.ax.imshow(
            data,
            cmap="Blues",
            origin="lower",
            extent=[-self.limit, self.limit, -self.limit, self.limit],
        )

        self.colorbar = self.figure.colorbar(im, ax=self.ax)

        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel(ylabel, fontsize=14, fontweight="bold")

        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
        self.ax.set_yticks(np.arange(-self.limit, self.limit + 1))

        self.figure.tight_layout()
        return self.figure



    def phase_plane_focus_yz(self):

        if not self.is_3D:
            return None

        self.figure.clf()
        self.colorbar = None
        self.ax = self.figure.add_subplot(1, 1, 1)

        # 3D: take XY slice at z = center
        data = self.phase[self.coords[0], :, :].T
        xlabel = f"Y (x = {self.coords[0] - self.center})"
        ylabel = "Z"

        im = self.ax.imshow(
            data,
            cmap="Blues",
            origin="lower",
            extent=[-self.limit, self.limit, -self.limit, self.limit],
        )

        self.colorbar = self.figure.colorbar(im, ax=self.ax)

        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel(ylabel, fontsize=14, fontweight="bold")

        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
        self.ax.set_yticks(np.arange(-self.limit, self.limit + 1))

        self.figure.tight_layout()
        return self.figure



    def phase_plane_origin_xz(self):

        if not self.is_3D:
            return None

        self.figure.clf()
        self.colorbar = None
        self.ax = self.figure.add_subplot(1, 1, 1)

        
        data = self.phase[:, self.center, :].T
        xlabel = "X (y = 0)"
        ylabel = "Z"

        im = self.ax.imshow(
            data,
            cmap="Blues",
            origin="lower",
            extent=[-self.limit, self.limit, -self.limit, self.limit],
        )

        self.colorbar = self.figure.colorbar(im, ax=self.ax)

        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel(ylabel, fontsize=14, fontweight="bold")

        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
        self.ax.set_yticks(np.arange(-self.limit, self.limit + 1))

        self.figure.tight_layout()
        return self.figure



    def phase_plane_focus_xz(self):

        if not self.is_3D:
            return None

        self.figure.clf()
        self.colorbar = None
        self.ax = self.figure.add_subplot(1, 1, 1)

        # 3D: take XY slice at z = center
        data = self.phase[:, self.coords[1], :].T
        xlabel = f"X (y = {self.coords[1] - self.center})"
        ylabel = "Z"

        im = self.ax.imshow(
            data,
            cmap="Blues",
            origin="lower",
            extent=[-self.limit, self.limit, -self.limit, self.limit],
        )

        self.colorbar = self.figure.colorbar(im, ax=self.ax)

        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel(ylabel, fontsize=14, fontweight="bold")

        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
        self.ax.set_yticks(np.arange(-self.limit, self.limit + 1))

        self.figure.tight_layout()
        return self.figure



    def contour_origin_xy(self):

        self.figure.clf()
        self.colorbar = None
        self.ax = self.figure.add_subplot(1, 1, 1)

        levels = np.arange(0, 1.01, 0.2)

        # Select data slice
        if self.is_3D:
            data = self.magnitude[:, :, self.center]
            xlabel = "X (z = 0)"
            ylabel = "Y"
        else:
            data = self.magnitude
            xlabel = "X"
            ylabel = "Y"

        # Normalize safely
        norm = data / (np.max(data) + 1e-6)

        cs = self.ax.contour(
            norm.T,
            levels=levels,
            cmap="jet",
            origin="lower",
            linestyles="-",
            extent=[-self.limit, self.limit, -self.limit, self.limit],
        )

        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel(ylabel, fontsize=14, fontweight="bold")

        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
        self.ax.set_yticks(np.arange(-self.limit, self.limit + 1))

        # Safe colorbar creation
        self.colorbar = self.figure.colorbar(cs, ax=self.ax)

        self.ax.grid(True)
        self.figure.tight_layout()

        return self.figure



    def contour_focus_xy(self):

        if not self.is_3D:
            return None

        self.figure.clf()
        self.colorbar = None
        self.ax = self.figure.add_subplot(1, 1, 1)

        levels = np.arange(0, 1.01, 0.2)

        data = self.magnitude[:, :, self.coords[2]]
        xlabel = f"X (z = {self.coords[2] - self.center})"
        ylabel = "Y"

        # Normalize safely
        norm = data / (np.max(data) + 1e-6)

        cs = self.ax.contour(
            norm.T,
            levels=levels,
            cmap="jet",
            origin="lower",
            linestyles="-",
            extent=[-self.limit, self.limit, -self.limit, self.limit],
        )

        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel(ylabel, fontsize=14, fontweight="bold")

        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
        self.ax.set_yticks(np.arange(-self.limit, self.limit + 1))

        # Safe colorbar creation
        self.colorbar = self.figure.colorbar(cs, ax=self.ax)

        self.ax.grid(True)
        self.figure.tight_layout()

        return self.figure



    def contour_origin_yz(self):

        if not self.is_3D:
            return None

        self.figure.clf()
        self.colorbar = None
        self.ax = self.figure.add_subplot(1, 1, 1)

        levels = np.arange(0, 1.01, 0.2)

        data = self.magnitude[self.center, :, :]
        xlabel = "Y (x = 0)"
        ylabel = "Z"

        # Normalize safely
        norm = data / (np.max(data) + 1e-6)

        cs = self.ax.contour(
            norm.T,
            levels=levels,
            cmap="jet",
            origin="lower",
            linestyles="-",
            extent=[-self.limit, self.limit, -self.limit, self.limit],
        )

        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel(ylabel, fontsize=14, fontweight="bold")

        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
        self.ax.set_yticks(np.arange(-self.limit, self.limit + 1))

        # Safe colorbar creation
        self.colorbar = self.figure.colorbar(cs, ax=self.ax)

        self.ax.grid(True)
        self.figure.tight_layout()

        return self.figure



    def contour_focus_yz(self):

        if not self.is_3D:
            return None

        self.figure.clf()
        self.colorbar = None
        self.ax = self.figure.add_subplot(1, 1, 1)

        levels = np.arange(0, 1.01, 0.2)

        data = self.magnitude[self.coords[0], :, :]
        xlabel = f"Y (x = {self.coords[0] - self.center})"
        ylabel = "Z"

        # Normalize safely
        norm = data / (np.max(data) + 1e-6)

        cs = self.ax.contour(
            norm.T,
            levels=levels,
            cmap="jet",
            origin="lower",
            linestyles="-",
            extent=[-self.limit, self.limit, -self.limit, self.limit],
        )

        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel(ylabel, fontsize=14, fontweight="bold")

        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
        self.ax.set_yticks(np.arange(-self.limit, self.limit + 1))

        # Safe colorbar creation
        self.colorbar = self.figure.colorbar(cs, ax=self.ax)

        self.ax.grid(True)
        self.figure.tight_layout()

        return self.figure



    def contour_origin_xz(self):

        if not self.is_3D:
            return None

        self.figure.clf()
        self.colorbar = None
        self.ax = self.figure.add_subplot(1, 1, 1)

        levels = np.arange(0, 1.01, 0.2)

        data = self.magnitude[:, self.center, :]
        xlabel = "X (y = 0)"
        ylabel = "Z"

        # Normalize safely
        norm = data / (np.max(data) + 1e-6)

        cs = self.ax.contour(
            norm.T,
            levels=levels,
            cmap="jet",
            origin="lower",
            linestyles="-",
            extent=[-self.limit, self.limit, -self.limit, self.limit],
        )

        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel(ylabel, fontsize=14, fontweight="bold")

        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
        self.ax.set_yticks(np.arange(-self.limit, self.limit + 1))

        # Safe colorbar creation
        self.colorbar = self.figure.colorbar(cs, ax=self.ax)

        self.ax.grid(True)
        self.figure.tight_layout()

        return self.figure



    def contour_focus_xz(self):

        if not self.is_3D:
            return None

        self.figure.clf()
        self.colorbar = None
        self.ax = self.figure.add_subplot(1, 1, 1)

        levels = np.arange(0, 1.01, 0.2)

        data = self.magnitude[:, self.coords[1], :]
        xlabel = f"X (y = {self.coords[1] - self.center})"
        ylabel = "Z"

        # Normalize safely
        norm = data / (np.max(data) + 1e-6)

        cs = self.ax.contour(
            norm.T,
            levels=levels,
            cmap="jet",
            origin="lower",
            linestyles="-",
            extent=[-self.limit, self.limit, -self.limit, self.limit],
        )

        self.ax.set_xlabel(xlabel, fontsize=14, fontweight="bold")
        self.ax.set_ylabel(ylabel, fontsize=14, fontweight="bold")

        self.ax.set_xticks(np.arange(-self.limit, self.limit + 1))
        self.ax.set_yticks(np.arange(-self.limit, self.limit + 1))

        # Safe colorbar creation
        self.colorbar = self.figure.colorbar(cs, ax=self.ax)

        self.ax.grid(True)
        self.figure.tight_layout()

        return self.figure
