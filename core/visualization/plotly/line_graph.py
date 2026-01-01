import numpy as np
import plotly.graph_objects as go
from .layout import apply_common_layout


class LineGraphPlotter:
    def __init__(self, sim_data):
        self.data = sim_data
        self.mag = sim_data.magnitude
        self.center = sim_data.center
        self.coords = sim_data.coords
        self.axis = sim_data.axis


    #-------------------X-axis----------------------#

    def origin_x(self):
        mag = self.mag
        center = self.center

        if self.data.is_3D:
            y = mag[:, center, center]
        else:
            y = mag[:, center]

        x = self.axis

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                name="|Ez|",
                hovertemplate="x=%{x}<br>|Ez|=%{y}<extra></extra>"
            )
        )

        apply_common_layout(
            fig,
            title="Line X (y=0)" + (", (z=0)" if self.data.is_3D else ""),
            xlabel="X",
            ylabel="|Ez|",
            spatial=False
        )

        return fig
    


    def focus_x(self):
        mag = self.mag
        coords = self.coords
        center = self.center

        if self.data.is_3D:
            _, y_idx, z_idx = coords
            y = mag[:, y_idx, z_idx]
            label = f"y={y_idx - center}, z={z_idx - center}"
        else:
            _, y_idx = coords
            y = mag[:, y_idx]
            label = f"y={y_idx - center}"

        x = self.axis

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                name="|Ez|",
                hovertemplate="x=%{x}<br>|Ez|=%{y}<extra></extra>"
            )
        )

        apply_common_layout(
            fig,
            title=f"Line X (Focus: {label})",
            xlabel="X",
            ylabel="|Ez|",
            spatial=False
        )

        return fig


    #-------------------Y-axis----------------------#

    def origin_y(self):
        mag = self.mag
        center = self.center

        if self.data.is_3D:
            y = mag[center, :, center]
        else:
            y = mag[center, :]

        x = self.axis

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                name="|Ez|",
                hovertemplate="x=%{x}<br>|Ez|=%{y}<extra></extra>"
            )
        )

        apply_common_layout(
            fig,
            title="Line Y (x=0)" + (", (z=0)" if self.data.is_3D else ""),
            xlabel="Y",
            ylabel="|Ez|",
            spatial=False
        )

        return fig
    
    

    def focus_y(self):
        mag = self.mag
        coords = self.coords
        center = self.center

        if self.data.is_3D:
            x_idx, _, z_idx = coords
            y = mag[x_idx, :, z_idx]
            label = f"x={x_idx - center}, z={z_idx - center}"
        else:
            x_idx, _ = coords
            y = mag[x_idx, :]
            label = f"x={x_idx - center}"

        x = self.axis

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                name="|Ez|",
                hovertemplate="x=%{x}<br>|Ez|=%{y}<extra></extra>"
            )
        )

        apply_common_layout(
            fig,
            title=f"Line Y (Focus: {label})",
            xlabel="Y",
            ylabel="|Ez|",
            spatial=False
        )

        return fig
    

    #-------------------Z-axis----------------------#

    def origin_z(self):
        if not self.data.is_3D:
            return None
        
        mag = self.mag
        center = self.center

        y = mag[center, center, :]

        x = self.axis

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                name="|Ez|",
                hovertemplate="x=%{x}<br>|Ez|=%{y}<extra></extra>"
            )
        )

        apply_common_layout(
            fig,
            title="Line Z (x=0, y=0)",
            xlabel="Z",
            ylabel="|Ez|",
            spatial=False
        )

        return fig
    
    

    def focus_z(self):
        if not self.data.is_3D:
            return None
         
        mag = self.mag
        coords = self.coords
        center = self.center

        x_idx, y_idx, _ = coords
        y = mag[x_idx, y_idx, :]
        label = f"x={x_idx - center}, y={y_idx - center}"

        x = self.axis

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                name="|Ez|",
                hovertemplate="x=%{x}<br>|Ez|=%{y}<extra></extra>"
            )
        )

        apply_common_layout(
            fig,
            title=f"Line Z (Focus: {label})",
            xlabel="Z",
            ylabel="|Ez|",
            spatial=False
        )

        return fig
