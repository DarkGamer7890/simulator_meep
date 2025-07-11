import meep as mp
import numpy as np


class sim_in_meep():
    def __init__(self, cell_size, resolution, pml, source_center, source_size, frequency, filled_vox, epsilon, pitch, time):
        self.cell_size = cell_size
        self.resolution = resolution
        self.pml = pml
        self.source_center = source_center
        self.source_size = source_size
        self.frequency = frequency
        self.filled_vox = filled_vox
        self.epsilon = epsilon
        self.pitch = pitch
        self.time = time

    def sim_run(self):
        pml_layer = [mp.PML(self.pml)]

        geometry = []
        xx = []
        yy = []
        zz = []

        for center in self.filled_vox:
        
            xx.append(center[0])
            yy.append(center[1])
            zz.append(center[2])

            geometry.append(
                mp.Block(
                    size=mp.Vector3(self.pitch, self.pitch, self.pitch),  # small voxel approximation
                    center=center,
                    material=mp.Medium(epsilon=self.epsilon)
                )
            )
        
        source = mp.Source(
            src=mp.ContinuousSource(frequency=self.frequency, is_integrated=True),
            center=self.source_center,  # Source at the center
            size=self.source_size,
            component=mp.Ez  # z-directed electric field
        )

        sim = mp.Simulation(
            cell_size=self.cell_size,
            boundary_layers=pml_layer,
            geometry=geometry,
            sources=[source],
            resolution=self.resolution
        )

        dft_monitor = sim.add_dft_fields(
            [mp.Ez],                # Components to monitor
            [self.frequency],             # Central frequency (use a list for compatibility)
            center=mp.Vector3(0, 0, 0),# Monitor center
            size=self.cell_size # Monitor size matching the domain
        )

        sim.init_sim()
        self.eps_data = sim.get_array(center=mp.Vector3(), size=self.cell_size, component=mp.Dielectric)


        sim.run(until=self.time)
        # Get the frequency-domain Ez field
        self.ez_dft = sim.get_dft_array(dft_monitor, mp.Ez, 0)  # Index 0 for first frequency

        # Reshape for visualization
        dim_x = int(self.cell_size.x * self.resolution)
        dim_y = int(self.cell_size.y * self.resolution)
        dim_z = int(self.cell_size.z * self.resolution)

        if dim_z == 0:
            self.ez_dft = np.reshape(self.ez_dft, (dim_x, dim_y))
        else:
            self.ez_dft = np.reshape(self.ez_dft, (dim_x, dim_y, dim_z))  

        return self.eps_data, self.ez_dft

