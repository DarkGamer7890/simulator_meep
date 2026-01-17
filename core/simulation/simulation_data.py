import numpy as np

class SimulationData:
    def __init__(self, eps_sim, ez_dft, pml, resolution):
        self.ez = ez_dft
        self.pml = pml
        self.resolution = resolution
        self.is_3D = (ez_dft.ndim == 3)

        self.magnitude = np.abs(ez_dft)
        self.phase = np.angle(ez_dft)

        self.crop = int(self.pml * self.resolution)
        self._crop_pml()

        # Axis (physical coordinates)
        n = self.magnitude.shape[0]
        physical_size = n / self.resolution
        half_size = physical_size / 2
        self.axis = np.linspace(-half_size, half_size, n)

        self.center = n // 2
        self.limit = half_size

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

