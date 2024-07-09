# Description

Python package for reading and analyzing simulations generated using the Gizmo code, in particular, the FIRE cosmological simulations.


---
# Requirements

python 3, numpy, scipy, h5py, matplotlib

This package also requires the [utilities/](https://bitbucket.org/awetzel/utilities) Python package for low-level utility functions.


---
# Contents

## gizmo_analysis

### gizmo_io.py
* read particles from Gizmo snapshot files

### gizmo_plot.py
* analyze and plot particle data

### gizmo_track.py
* track star particles and gas cells across snapshots
### gizmo_file.py
* clean, compress, delete, or transfer Gizmo snapshot files

### gizmo_diagnostic.py
* run diagnostics on Gizmo simulations

### gizmo_ic.py
* generate cosmological zoom-in initial conditions from existing snapshot files

### gizmo_star.py
* models of stellar evolution as implemented in FIRE-2 and FIRE-3: rates and yields from supernovae (core-collapse and white-dwarf) and stellar winds

### gizmo_elementtracer.py
* generate elemental abundances in star particles and gas cells in post-processing, using the element-tracer module


## tutorials

### gizmo_tutorial_read.ipynb
* Jupyter notebook tutorial for reading particle data, understanding its data structure and units

### gizmo_tutorial_analysis.ipynb
* Jupyter notebook tutorial for analyzing and plotting particle data

### transcript.txt
* Transcript of Zach Hafen's video tutorial (https://www.youtube.com/watch?v=bl-rpzE8hrU) on using this package to read FIRE simulations.


## data

### snapshot_times.txt
* example file for storing information about snapshots: scale-factors, redshifts, times, etc


---
# Units

Unless otherwise noted, this package stores all quantities in (combinations of) these base units
* mass [M_sun]
* position [kpc comoving]
* distance, radius [kpc physical]
* time [Gyr]
* temperature [K]
* magnetic field [Gauss]
* elemental abundance [linear mass fraction]

These are the common exceptions to those standards
* velocity [km/s]
* acceleration [km/s / Gyr]
* gravitational potential [km^2 / s^2]
* rates (star formation, cooling, accretion) [M_sun / yr]
* metallicity (if converted from stored massfraction) [log10(mass_fraction / mass_fraction_solar)], using Asplund et al 2009 for Solar


---
# Installing

The easiest way to install this packages and all its dependencies is by using `pip` or conda.

```
python -m pip install gizmo_analysis

```

To install from source, you can clone the latest version of `gizmo_analysis` from `bitbucket` using `git`:

```
git clone git://bitbucket.org/awetzel/gizmo_analysis.git
```

To build and install the project, inside the cloned `gizmo_analysis` directory:

```
python -m pip install .
```


---
# Using

Once installed, you can call individual modules like this:

```
import gizmo_analysis
gizmo_analysis.gizmo_io
```

or more succinctly like this

```
import gizmo_analysis as gizmo
gizmo.io
```


---
# Citing

If you use this package, please cite it, along the lines of: 'This work used GizmoAnalysis (http://ascl.net/2002.015), which first was used in Wetzel et al 2016 (https://ui.adsabs.harvard.edu/abs/2016ApJ...827L..23W).'
