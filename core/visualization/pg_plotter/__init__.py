from .pg_plotters import PGPlotter

PLOT_LABELS = {
    "line_origin_x": "Line — Origin X",
    "line_focus_x": "Line — Focus X",
    "line_origin_y": "Line — Origin Y",
    "line_focus_y": "Line — Focus Y",
    "line_origin_z": "Line — Origin Z",
    "line_focus_z": "Line — Focus Z",
    "mag_plane_origin_xy": "Magnitude — Origin XY",
    "mag_plane_focus_xy": "Magnitude — Focus XY",
    "mag_plane_origin_yz": "Magnitude — Origin YZ",
    "mag_plane_focus_yz": "Magnitude — Focus YZ",
    "mag_plane_origin_xz": "Magnitude — Origin XZ",
    "mag_plane_focus_xz": "Magnitude — Focus XZ",
    "phase_plane_origin_xy": "Phase — Origin XY",
    "phase_plane_focus_xy": "Phase — Focus XY",
    "phase_plane_origin_yz": "Phase — Origin YZ",
    "phase_plane_focus_yz": "Phase — Focus YZ",
    "phase_plane_origin_xz": "Phase — Origin XZ",
    "phase_plane_focus_xz": "Phase — Focus XZ",
    "contour_origin_xy": "Contour — Origin XY",
    "contour_focus_xy": "Contour — Focus XY",
    "contour_origin_yz": "Contour — Origin YZ",
    "contour_focus_yz": "Contour — Focus YZ",
    "contour_origin_xz": "Contour — Origin XZ",
    "contour_focus_xz": "Contour — Focus XZ",
}

SECTIONS = {
    "Line Plots": [k for k in PLOT_LABELS if k.startswith("line_")],
    "Magnitude": [k for k in PLOT_LABELS if k.startswith("mag_")],
    "Phase": [k for k in PLOT_LABELS if k.startswith("phase_")],
    "Contour": [k for k in PLOT_LABELS if k.startswith("contour_")],
}