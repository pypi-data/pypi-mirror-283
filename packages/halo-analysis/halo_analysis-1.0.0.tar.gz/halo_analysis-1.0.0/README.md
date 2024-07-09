# Description

Python package to read and analyze halo/galaxy catalogs (generated from Rockstar or AHF) and merger trees (generated from ConsistentTrees).


---
# Requirements

python 3, numpy, scipy, h5py, matplotlib

This package also requires the [utilities/](https://bitbucket.org/awetzel/utilities) python package for low-level utility functions.


---
# Contents

## halo_analysis

### halo_io.py
* read halo files, convert from text to hdf5 format, assign particle species to dark-matter halos

### halo_plot.py
* analyze and plot halos/galaxies

### halo_select.py
* select halos from large simulations for generating initial conditions for zoom-in

## tutorials

### halo_tutorial.ipynb
* Jupyter notebook tutorial for using this package

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

The easiest way to install the analysis code and all dependencies is by using `pip` or conda.

```
python -m pip install halo_analysis

```

To install from source, clone the latest version of `gizmo_analysis` from `bitbucket` using `git`:

```
git clone git://bitbucket.org/awetzel/halo_analysis.git
``` 

To build and install the project, inside the cloned `halo_analysis` directory:

```
python -m pip install .
```


---
# Using

Once installed, you can use individual modules like this:

```
import halo_analysis
halo_analysis.halo_io
```

or more succinctly like this

```
import halo_analysis as halo
halo.io
```


---
# Citing

If you use this package, please cite it, along the lines of: 'This work used HaloAnalysis (http://ascl.net/2002.014), which first was used in Wetzel et al 2016 (https://ui.adsabs.harvard.edu/abs/2016ApJ...827L..23W).'
