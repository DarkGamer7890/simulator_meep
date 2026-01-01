import numpy as np
import plotly.graph_objects as go
from .layout import apply_common_layout


class ContourPlotter:
    def __init__(self, self_data):
        self.data = self_data
        self.is_3D = self_data.is_3D
        self.mag = self_data.magnitude
        self.center = self_data.center
        self.coords = self_data.coords
        self.limit = self_data.limit
        self.axis = self_data.axis



    def origin_xy(self, **kwargs):

        z = (
            self.mag[:, :, self.center]
            if self.is_3D
            else self.mag[:, :]
        )

        levels = kwargs.get("contour_levels", None)
        norm = kwargs.get("normalize", None)

        if levels is not None:
            denominator = (levels - 1)

            if norm:
                ticks = np.linspace(z.min(), z.max(), levels)
                ticktext = np.linspace(0, 1, levels).round(2)
                colorbar_title = "Normalized |Ez|"
            else:
                ticks = np.linspace(z.min(), z.max(), levels)
                ticktext = ticks.round(3)
                colorbar_title = "|Ez|"

        else:
            denominator = 14

        fig = go.Figure(
            go.Contour(
                z=z.T,
                x=self.axis,
                y=self.axis,
                contours=dict(
                    start=z.min(),
                    end=z.max(),
                    size=(z.max()-z.min())/denominator,
                    coloring="lines"
                ),
                colorscale="Jet",
                colorbar=dict(
                    title=colorbar_title,
                    tickvals=ticks,
                    ticktext=ticktext
                ),
            )
        )

        apply_common_layout(
            fig,
            title="Contour |Ez| (XY plane, z=0)",
            xlabel="X",
            ylabel="Y",
            spatial=True,
        )

        return fig



    def focus_xy(self, **kwargs):
        if not self.is_3D:
            return None
        
        z = self.mag[:, :, self.coords[2]]
        
        levels = kwargs.get("contour_levels", None)
        norm = kwargs.get("normalize", None)

        if levels is not None:
            denominator = (levels - 1)

            if norm:
                ticks = np.linspace(z.min(), z.max(), levels)
                ticktext = np.linspace(0, 1, levels).round(2)
                colorbar_title = "Normalized |Ez|"
            else:
                ticks = np.linspace(z.min(), z.max(), levels)
                ticktext = ticks.round(3)
                colorbar_title = "|Ez|"

        else:
            denominator = 14

        fig = go.Figure(
            go.Contour(
                z=z.T,
                x=self.axis,
                y=self.axis,
                contours=dict(
                    start=z.min(),
                    end=z.max(),
                    size=(z.max()-z.min())/denominator,
                    coloring="lines"
                ),
                colorscale="Jet",
                colorbar=dict(
                    title=colorbar_title,
                    tickvals=ticks,
                    ticktext=ticktext
                ),
            )
        )

        apply_common_layout(
            fig,
            title=f"Contour |Ez| (XY plane, z={self.coords[2]-self.center})",
            xlabel="X",
            ylabel="Y",
            spatial=True,
        )

        return fig



    def origin_yz(self, **kwargs):
        if not self.is_3D:
            return None
        
        z = self.mag[self.center, :, :]

        levels = kwargs.get("contour_levels", None)
        norm = kwargs.get("normalize", None)

        if levels is not None:
            denominator = (levels - 1)

            if norm:
                ticks = np.linspace(z.min(), z.max(), levels)
                ticktext = np.linspace(0, 1, levels).round(2)
                colorbar_title = "Normalized |Ez|"
            else:
                ticks = np.linspace(z.min(), z.max(), levels)
                ticktext = ticks.round(3)
                colorbar_title = "|Ez|"

        else:
            denominator = 14

        fig = go.Figure(
            go.Contour(
                z=z.T,
                x=self.axis,
                y=self.axis,
                contours=dict(
                    start=z.min(),
                    end=z.max(),
                    size=(z.max()-z.min())/denominator,
                    coloring="lines"
                ),
                colorscale="Jet",
                colorbar=dict(
                    title=colorbar_title,
                    tickvals=ticks,
                    ticktext=ticktext
                ),
            )
        )

        apply_common_layout(
            fig,
            title="Contour |Ez| (YZ plane, x=0)",
            xlabel="Y",
            ylabel="Z",
            spatial=True,
        )

        return fig



    def focus_yz(self, **kwargs):
        if not self.is_3D:
            return None
        
        z = self.mag[self.coords[0], :, :]
        
        levels = kwargs.get("contour_levels", None)
        norm = kwargs.get("normalize", None)

        if levels is not None:
            denominator = (levels - 1)

            if norm:
                ticks = np.linspace(z.min(), z.max(), levels)
                ticktext = np.linspace(0, 1, levels).round(2)
                colorbar_title = "Normalized |Ez|"
            else:
                ticks = np.linspace(z.min(), z.max(), levels)
                ticktext = ticks.round(3)
                colorbar_title = "|Ez|"

        else:
            denominator = 14

        fig = go.Figure(
            go.Contour(
                z=z.T,
                x=self.axis,
                y=self.axis,
                contours=dict(
                    start=z.min(),
                    end=z.max(),
                    size=(z.max()-z.min())/denominator,
                    coloring="lines"
                ),
                colorscale="Jet",
                colorbar=dict(
                    title=colorbar_title,
                    tickvals=ticks,
                    ticktext=ticktext
                ),
            )
        )

        apply_common_layout(
            fig,
            title=f"Contour |Ez| (YZ plane, x={self.coords[0]-self.center})",
            xlabel="Y",
            ylabel="Z",
            spatial=True,
        )

        return fig
    


    def origin_xz(self, **kwargs):
        if not self.is_3D:
            return None
        
        z = self.mag[:, self.center, :]
        
        levels = kwargs.get("contour_levels", None)
        norm = kwargs.get("normalize", None)

        if levels is not None:
            denominator = (levels - 1)

            if norm:
                ticks = np.linspace(z.min(), z.max(), levels)
                ticktext = np.linspace(0, 1, levels).round(2)
                colorbar_title = "Normalized |Ez|"
            else:
                ticks = np.linspace(z.min(), z.max(), levels)
                ticktext = ticks.round(3)
                colorbar_title = "|Ez|"

        else:
            denominator = 14

        fig = go.Figure(
            go.Contour(
                z=z.T,
                x=self.axis,
                y=self.axis,
                contours=dict(
                    start=z.min(),
                    end=z.max(),
                    size=(z.max()-z.min())/denominator,
                    coloring="lines"
                ),
                colorscale="Jet",
                colorbar=dict(
                    title=colorbar_title,
                    tickvals=ticks,
                    ticktext=ticktext
                ),
            )
        )

        apply_common_layout(
            fig,
            title="Contour |Ez| (XZ plane, y=0)",
            xlabel="X",
            ylabel="Z",
            spatial=True,
        )

        return fig



    def focus_xz(self, **kwargs):
        if not self.is_3D:
            return None
        
        z = self.mag[:, self.coords[1], :]

        levels = kwargs.get("contour_levels", None)
        norm = kwargs.get("normalize", None)

        if levels is not None:
            denominator = (levels - 1)

            if norm:
                ticks = np.linspace(z.min(), z.max(), levels)
                ticktext = np.linspace(0, 1, levels).round(2)
                colorbar_title = "Normalized |Ez|"
            else:
                ticks = np.linspace(z.min(), z.max(), levels)
                ticktext = ticks.round(3)
                colorbar_title = "|Ez|"

        else:
            denominator = 14

        fig = go.Figure(
            go.Contour(
                z=z.T,
                x=self.axis,
                y=self.axis,
                contours=dict(
                    start=z.min(),
                    end=z.max(),
                    size=(z.max()-z.min())/denominator,
                    coloring="lines"
                ),
                colorscale="Jet",
                colorbar=dict(
                    title=colorbar_title,
                    tickvals=ticks,
                    ticktext=ticktext
                ),
            )
        )

        apply_common_layout(
            fig,
            title=f"Contour |Ez| (XZ plane, y={self.coords[1]-self.center})",
            xlabel="X",
            ylabel="Z",
            spatial=True,
        )

        return fig