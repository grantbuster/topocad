# topocad

Welcome to topocad! This repo contains utilities for topography-based 3D
modeling using CAD + python scripting tools.

Here's an example of a 3D topo model of Boulder, Colorado. Everything is to scale and based on the 10m DEM from USGS. 

![alt text](https://github.com/grantbuster/topocad/blob/main/boulder_model_capture.png?raw=true)

## Resources:

1/3 arc-second (approx. 10m) DEM from USGS: https://apps.nationalmap.gov/downloader/

CAD scripting is with CADQuery: https://cadquery.readthedocs.io/en/latest/index.html

Autodesk model viewer web app (free): https://viewer.autodesk.com/

Services for making 3D prints of topo models: https://www.shapeways.com/

## Installation

1. `git clone git@github.com:grantbuster/topocad.git`
2. `cd topocad`
3. `pip install -e .`
4. `conda install -c conda-forge cadquery`
