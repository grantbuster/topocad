# topocad

Welcome to topocad! This repo contains utilities for topography-based 3D
modeling using CAD + python scripting tools. To get started, check out the 
[code](https://github.com/grantbuster/topocad/blob/main/topocad/topocad.py) 
or the 
[example notebook](https://github.com/grantbuster/topocad/blob/main/example/example.ipynb). 

## Gallery

Here's an example of a 3D topo model of Boulder, Colorado. The three spatial axes are to-scale and based on the DEM from USGS. The model is designed to be printed at a footprint of approximately 100mm x 100mm with approximately 7 pixels per mm. The 10m DEM was coarsened by 3x to produce the model. The model took 6 minutes to create on an M1 Macbook Air. 

![alt text](https://github.com/grantbuster/topocad/blob/main/boulder_model_capture.png?raw=true)

## Resources:

1/3 arc-second (approx. 10m) DEM from USGS: https://apps.nationalmap.gov/downloader/

CAD scripting is with CADQuery: https://cadquery.readthedocs.io/en/latest/index.html

Autodesk model viewer web app (free): https://viewer.autodesk.com/

Services for making 3D prints of topo models: https://www.shapeways.com/ | https://craftcloud3d.com/

## Installation

1. `git clone git@github.com:grantbuster/topocad.git`
2. `cd topocad`
3. `pip install -e .`
4. `conda install -c conda-forge cadquery`
