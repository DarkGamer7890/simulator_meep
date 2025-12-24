import streamlit as st
import sys
from pathlib import Path
import meep as mp
import numpy as np
import matplotlib.pyplot as plt

from core.sim_in_meep import SimInMeep
from core.geometry_factory import build_geometry

from core.plotter import Plotter


BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

st.set_page_config(layout="wide")
st.title("🧪 Meep Simulator")

# -------------------------
# SIDEBAR : PARAMETERS ONLY
# -------------------------
st.sidebar.header("Cell Parameters")

cell_x = st.sidebar.number_input("Cell Size X", value=10.0)
cell_y = st.sidebar.number_input("Cell Size Y", value=10.0)
cell_z = st.sidebar.number_input("Cell Size Z", value=0.0)

pml = st.sidebar.number_input("PML Thickness", value=1.0)

st.sidebar.header("Source Parameters")

src_lx = st.sidebar.number_input("Source Length (X)", value=0.0)
src_ly = st.sidebar.number_input("Source Width (Y)", value=1.0)
src_lz = st.sidebar.number_input("Source Height (Z)", value=0.0)

src_x = st.sidebar.number_input("Source Center X", value=0.0)
src_y = st.sidebar.number_input("Source Center Y", value=0.0)
src_z = st.sidebar.number_input("Source Center Z", value=0.0)

freq = st.sidebar.number_input("Frequency", value=1.0)


st.sidebar.header("Source Parameters")

resolution = st.sidebar.number_input("Resolution", value=2)

sim_time = st.sidebar.number_input("Time", value=200)

# -------------------------
# GEOMETRY SELECTION
# -------------------------
st.header("Geometry")

geometry_type = st.radio(
    "Select Geometry Type",
    ["None", "Import File", "Luneberg Lens"]
)

geometry_path = None
pitch = None
eps = None

geometry = [] 
params = {}

if geometry_type == "Import File":
    geometry_path = st.file_uploader(
        "Upload Geometry File",
        type=["stl", "obj", "ply"]
    )

    pitch = st.number_input("Pitch", value=0.5)
    eps = st.number_input("Epsilon", value=2)

    params = {
        'path': geometry_path,
        'pitch': pitch,
        'epsilon': eps
    }

    

elif geometry_type == "Luneberg Lens":
    radius = st.number_input("Radius", value=3)
    layers = st.number_input("Layers", value=6)

    params = {
        "radius": radius,
        "layers": layers,
        "cell_z": cell_z
    }
        
    

# -------------------------
# RUN BUTTON
# -------------------------
run = st.button("Run Simulation")

st.title("Meep Simulator — Free Space Test")




if "simulation_done" not in st.session_state:
    st.session_state.simulation_done = False

if "plotter" not in st.session_state:
    st.session_state.plotter = None

if "current_fig" not in st.session_state:
    st.session_state.current_fig = None





# ----------------- Geometry -----------------

if run:
    st.session_state.simulation_done = False
    st.session_state.plotter = None
    st.session_state.current_fig = None

    geometry = build_geometry(geometry_type, params)

    # ----------------- Simulation -----------------

    sim = SimInMeep(
        cell_size=mp.Vector3(cell_x, cell_y, cell_z),
        resolution=resolution,
        pml=pml,
        source_center=mp.Vector3(src_x, src_y, src_z),
        source_size=mp.Vector3(src_lx, src_ly, src_lz),
        frequency=freq,
        geometry=geometry,
        time=sim_time
    )

    eps, ez = sim.sim_run()
    st.session_state.simulation_done = True
    st.session_state.ez_ndim = ez.ndim


    # ----------------- Plotter -----------------

    # Create plot area
    plot_area = st.container()


    # Create figure + canvas
    fig, ax = plt.subplots(figsize=(6, 4))
    canvas = fig.canvas


    plotter = Plotter(
        eps_sim = eps,
        ez_dft = ez,
        figure = fig,
        canvas = canvas,
        ax = ax,
        pml = pml,
        resolution = resolution,
    )

    st.session_state.plotter = plotter



if st.session_state.simulation_done:
    is_3d = st.session_state.ez_ndim == 3

    ALL_BUTTONS = {
        "Line Plots": [
            ("Line X (origin)", "line_graph_origin_x", True),
            ("Line X (Focus)", "line_graph_focus_x", True),
            ("Line Y (origin)", "line_graph_origin_y", True),
            ("Line Y (Focus)", "line_graph_focus_y", True),
            ("Line Z (origin)", "line_graph_origin_z", is_3d),
            ("Line Z (Focus)", "line_graph_focus_z", is_3d),
        ],
        "Magnitude Plots": [
            ("Mag XY (Origin)", "mag_plane_origin_xy", True),
            ("Mag XY (Focus)", "mag_plane_focus_xy", is_3d),
            ("Mag YZ (Origin)", "mag_plane_origin_yz", is_3d),
            ("Mag YZ (Focus)", "mag_plane_focus_yz", is_3d),
            ("Mag XZ (Origin)", "mag_plane_origin_xz", is_3d),
            ("Mag XZ (Focus)", "mag_plane_focus_xz", is_3d),
        ],
        "Phase Plots": [
            ("Phase XY (Origin)", "phase_plane_origin_xy", True),
            ("Phase XY (Focus)", "phase_plane_focus_xy", is_3d),
            ("Phase YZ (Origin)", "phase_plane_origin_yz", is_3d),
            ("Phase YZ (Focus)", "phase_plane_focus_yz", is_3d),
            ("Phase XZ (Origin)", "phase_plane_origin_xz", is_3d),
            ("Phase XZ (Focus)", "phase_plane_focus_xz", is_3d),
        ],
        "Contour Plots": [
            ("Contour XY (Origin)", "contour_origin_xy", True),
            ("Contour XY (Focus)", "contour_focus_xy", is_3d),
            ("Contour YZ (Origin)", "contour_origin_yz", is_3d),
            ("Contour YZ (Focus)", "contour_focus_yz", is_3d),
            ("Contour XZ (Origin)", "contour_origin_xz", is_3d),
            ("Contour XZ (Focus)", "contour_focus_xz", is_3d),
        ]
    }



# Placement of Buttons

def render_button_grid(buttons, class_name, plotter):
    cols = st.columns(2)

    for i, (label, method_name) in enumerate(buttons):
        col = cols[i % 2]

        with col:
            clicked = st.button(label, key=f"{class_name}_{label}", disabled=not st.session_state.simulation_done)

            if clicked:
                fig = getattr(plotter, method_name)()
                st.session_state.current_fig = fig


if st.session_state.plotter is not None:
    for class_name, button_list in ALL_BUTTONS.items():
        with st.expander(class_name):
            visible = [
                (label, method)
                for label, method, toggle in button_list
                if toggle
            ]
            render_button_grid(visible, class_name, st.session_state.plotter)




if st.session_state.simulation_done:
    st.markdown("### Plot Output")

    if st.session_state.current_fig:
        st.pyplot(st.session_state.current_fig)
    else:
        st.info("Click a button to generate a plot")





# -------------------------
# DEBUG OUTPUT (IMPORTANT)
# -------------------------
if run:
    st.success("Parameters collected successfully!")

    st.write("### Collected Parameters")
    st.json({
        "cell": [cell_x, cell_y, cell_z],
        "pml": pml,
        "source_size": [src_lx, src_ly, src_lz],
        "source_center": [src_x, src_y, src_z],
        "frequency": freq,
        "resolution": resolution,
        "time": sim_time,
        "geometry_type": geometry_type,
        "geometry_path": str(geometry_path) if geometry_path else None
    })

    st.info("Simulation NOT started yet (by design)")
