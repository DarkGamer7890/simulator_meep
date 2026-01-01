# 24 Decemeber Phase 0 Part 1
## Fix:
- All Plots for 2D + 3D
- Fix button placements in both 2D and 3D cases
- Fix -> Button now shows after simulation
- Fix -> Plot resets after new simulation


## Architecture Overview (Phase 0)

User Input (UI)

   ↓

Geometry Builder

   ↓

Solver (Meep)

   ↓

Raw Fields (eps, Ez)

   ↓

Plotter

   ↓

Figures (matplotlib / plotly)


# 25 December Phase 0 - Part 2
- 🔍 Understood solver abstraction & imports

## Phase 0 – Part 3: Plot API cleanup

### What was done
- Introduced a unified `Plotter.plot(method_name)` API
- Centralized plot capability checks inside Plotter
- Removed plot-condition logic from GUI
- Made Plotter responsible for:
  - deciding valid plots
  - safely dispatching plot calls
- GUI now only requests plots by name

### Why this was done
- Prevent GUI from inspecting simulation dimensions
- Prepare for future:
  - interactive plots
  - multiple backends (Plotly / VisPy)
  - GPU solvers
- Improve robustness and maintainability

### Result
- Clean separation between GUI and visualization
- Plotter behaves like a plugin-style visualization engine
- No crashes when invalid plots are requested

## Phase 0 – Part 3: Plot API cleanup
### State handling
- Explicitly reset Streamlit session state on "Run":
  - simulation_done → False
  - plotter → None
  - current_fig → None
- Ensures:
  - stale plots are cleared
  - plot buttons disappear during recomputation
  - no accidental access to outdated simulation data


## Phase 0 – Understanding

I now understand:
- Streamlit only handles UI
- Plotter owns all plotting logic
- A class exists to remember data
- Buttons just call methods by name
- 2D vs 3D is a capability, not a special case

## Plotter changed-
- added plot function so UI will now just call plot and not individual function (its now plotter's work)
- added reset function to reset plots so for every new plot i have to write just 1 line
- more bug free and more flexible 

# 27 December
- Refactored visualization architecture

# 28 December 
(Not feeling well)

# 29 December 
Working for HackJNU website

# 30 December Phase 0 - Part 4
### ✅ Plotting system stabilized (Plotly)
- Migrated all plots to Plotly
- Implemented modular visualization architecture
- Added support for 2D/3D automatically
- Fixed contour slicing bugs for YZ/XZ planes
- GUI buttons dynamically adapt to dimensionality

# 31 December, 1st January 
- Happy New Year
- Done nothing as I was having Headache + not in the mood of coding
- Change wallpaper + themes of vs code, zen and ubuntu to match the mood

# 2nd January
- Finally functionable Contour level slider + toggle for normalization