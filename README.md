# Computational Simulation and Visualization Platform

This project is a Python-based platform for computational simulation, combining electromagnetic modeling with interactive 3D visualization. It is designed to define, simulate, and visually inspect structured systems within a unified workflow.

---

## Overview

The platform integrates numerical simulation and visualization into a single environment. It enables users to construct geometries, run simulations, and analyze results interactively.

It is being developed toward a CAD-like system for structured modeling and simulation-driven design.

---

## Features

* Interactive 3D visualization of geometries
* Electromagnetic simulation support
* Scene and structure management
* Export of simulation data and configurations

---

## Core Components

* **Meep**
  Used for electromagnetic simulations, enabling modeling of wave propagation and interaction with materials.

* **PyVista (VTK backend)**
  Provides 3D visualization of geometries and simulation structures, allowing interactive inspection.

* **PyQtGraph**
  Used for fast plotting and visualization of numerical data generated during simulations.

---

## Usage

```bash
conda env create -f env.yml
conda activate pmp
python launcher.py
```

---

## Current Status

The system supports defining simulation structures, running workflows, and visualizing results. Development is ongoing to improve usability and extend functionality.

---

## Roadmap

* Import functionality for loading saved simulations
* Improved data handling and serialization
* Advanced interaction and editing tools
* Tighter integration between simulation and visualization

---

## License

MIT License
