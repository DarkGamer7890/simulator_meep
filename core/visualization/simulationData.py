import numpy as np

class SimulationData:
    def __init__(self, eps_sim, ez_dft, pml, resolution):
        # Raw field
        self.ez = ez_dft

        # Metadata
        self.pml = pml
        self.resolution = resolution

        # Dimensionality
        self.is_3D = (ez_dft.ndim == 3)

        # Field quantities
        self.magnitude = np.abs(ez_dft)
        self.phase = np.angle(ez_dft)

        # Remove PML
        self.crop = int(self.pml * self.resolution)
        self._crop_pml()

        # Geometry helpers
        self.center = self.magnitude.shape[0] // 2
        self.limit = self.center
        self.axis = np.arange(-self.limit, self.limit + 1)

        # Focus point
        self._compute_focus_coords()



    def _crop_pml(self):
        c = self.crop
        if self.is_3D:
            self.magnitude = self.magnitude[c:-c, c:-c, c:-c]
            self.phase = self.phase[c:-c, c:-c, c:-c]
        else:
            self.magnitude = self.magnitude[c:-c, c:-c]
            self.phase = self.phase[c:-c, c:-c]



    def _compute_focus_coords(self):
        max_index = np.argmax(self.magnitude)
        self.coords = np.unravel_index(max_index, self.magnitude.shape)

