import numpy as np
import plotly.graph_objects as go
from .layout import apply_common_layout

class MagGraphPlotter:
    def __init__(self, sim_data):
        self.data = sim_data
        self.is_3D = sim_data.is_3D
        self.mag = sim_data.magnitude
        self.center = sim_data.center
        self.coords = sim_data.coords
        self.limit = sim_data.limit
        self.axis = sim_data.axis

    

    def origin_xy(self):
        if self.is_3D:
            z_slice = self.mag[:, :, self.center]
        else:
            z_slice = self.mag

        fig = go.Figure(
            go.Heatmap(
                z=z_slice,
                x=self.axis,
                y=self.axis,
                colorscale="Jet",
                colorbar=dict(title="|Ez|"),
            )
        )

        apply_common_layout(
            fig,
            title="Magnitude |Ez| (XY plane, z=0)",
            xlabel="X",
            ylabel="Y",
            spatial=True
        )

        return fig
    


    def focus_xy(self):
        if not self.is_3D:
            return None

        fig = go.Figure(
            go.Heatmap(
                z=self.mag[:, :, self.coords[2]],
                x=self.axis,
                y=self.axis,
                colorscale="Jet",
                colorbar=dict(title="|Ez|"),
            )
        )

        apply_common_layout(
            fig,
            title=f"Magnitude |Ez| (XY plane, z={self.coords[2] - self.center})",
            xlabel="X",
            ylabel="Y",
            spatial=True
        )

        return fig
    


    def origin_yz(self):
        if not self.is_3D:
            return None

        fig = go.Figure(
            go.Heatmap(
                z=self.mag[self.center, :, :],
                x=self.axis,
                y=self.axis,
                colorscale="Jet",
                colorbar=dict(title="|Ez|"),
            )
        )

        apply_common_layout(
            fig,
            title="Magnitude |Ez| (YZ plane, x=0)",
            xlabel="Y",
            ylabel="Z",
            spatial=True
        )

        return fig
    


    def focus_yz(self):
        if not self.is_3D:
            return None

        fig = go.Figure(
            go.Heatmap(
                z=self.mag[self.coords[0], :, :],
                x=self.axis,
                y=self.axis,
                colorscale="Jet",
                colorbar=dict(title="|Ez|"),
            )
        )

        apply_common_layout(
            fig,
            title=f"Magnitude |Ez| (YZ plane, x={self.coords[0] - self.center})",
            xlabel="Y",
            ylabel="Z",
            spatial=True
        )

        return fig

    

    def origin_xz(self):
        if not self.is_3D:
            return None

        fig = go.Figure(
            go.Heatmap(
                z=self.mag[:, self.center, :],
                x=self.axis,
                y=self.axis,
                colorscale="Jet",
                colorbar=dict(title="|Ez|"),
            )
        )

        apply_common_layout(
            fig,
            title="Magnitude |Ez| (XZ plane, y=0)",
            xlabel="X",
            ylabel="Z",
            spatial=True
        )

        return fig



    def focus_xz(self):
        if not self.is_3D:
            return None

        fig = go.Figure(
            go.Heatmap(
                z=self.mag[:, self.coords[1], :],
                x=self.axis,
                y=self.axis,
                colorscale="Jet",
                colorbar=dict(title="|Ez|"),
            )
        )

        apply_common_layout(
            fig,
            title=f"Magnitude |Ez| (XZ plane, y={self.coords[1] - self.center})",
            xlabel="X",
            ylabel="Z",
            spatial=True
        )
        
        return fig