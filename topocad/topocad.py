# -*- coding: utf-8 -*-
"""
topocad
"""
import cadquery as cq
import time
import numpy as np
from math import radians, cos, sin, asin, sqrt


def haversine(coord1, coord2):
    """Calculate the great circle distance in kilometers between two points on
    the earth (specified in decimal degrees)

    Parameters
    ----------
    coord1 : tuple
        (lat, lon) for point1 in decimal degrees
    coord2 : tuple
        (lat, lon) for point2 in decimal degrees

    Returns
    -------
    dist : float
        Distance between points in km
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles.
    return c * r


def get_xz(arr, idy, dx, subsample=1, x_scale=1, z_exag=1, z_adder=1):
    """Get a tuple of many (x,z) coordinates corresponding to one row (idy) in
    the topo array.

    Parameters
    ----------
    arr : np.ndarray
        2D (y, x) array of elevation values in meters (z)
    idy : int
        Axis=0 index (y-axis)
    dx : float
        Distance in km along the x-axis
    subsample : int
        Interval at which to sample the x-axis (reduce detail for lower compute
        costs)
    x_scale : float
        How to scale the x-axis values in mm. e.g., if this 100, the
        x-coordinates will range from (0, 100) mm
    z_exag : float
        Option to exaggerate the topography (multiplier). 1 makes everthing to
        true scale
    z_adder : float
        This will be the minimum z-value and results in the minimum thickness
        in mm of the work piece.

    Returns
    -------
    xz : tuple
        Tuple of (x, z) points for cadquery to spline. x values are longitude
        points in x_scale units z values are elevation values that are
        appropriately scaled to the x values and the input z_exag.
    """

    x = np.linspace(0, x_scale, arr.shape[1])

    dz = arr.max() - arr.min()
    # dz / (dx*1000) = true_z_exag / x_scale  # maintain aspect ratio
    true_z_scale = x_scale * dz / (dx*1000)
    z = (arr[idy] - arr.min()) / dz
    z = z * true_z_scale * z_exag + z_adder

    xz = tuple(zip(x, z))
    xz = xz[::subsample]
    return xz


def make_topo_cad(arr, dx, dy, x_scale, z_exag, z_adder, subsample=50,
                  spline=False):
    """Make a 3D CAD topography model

    Parameters
    ----------
    arr : np.ndarray
        2D (y, x) array of elevation values in meters (z)
    dx : float
        Distance in km along the x-axis
    dy : float
        Distance in km along the y-axis
    x_scale : float
        How to scale the x-axis values in mm. e.g., if this 100, the
        x-coordinates will range from (0, 100) mm
    z_exag : float
        Option to exaggerate the topography (multiplier). 1 makes everthing to
        true scale
    z_adder : float
        This will be the minimum z-value and results in
        the minimum thickness in mm of the work piece.
    subsample : int
        Interval at which to sample the x and y axes. A larger value reduces
        detail for lower compute costs. Compute estimates for a 10m DEM with
        shape (1729, 2127):
        5 -> 8 hours, 10 -> 37min, 15 -> 3min
    spline : bool
        Connect points with a spline (True) or linearly (False). Spline is more
        computationally expensive.

    Returns
    -------
    wp : cadquery.Workplane
        Cadquery Workplane object with the 3D model. Units are in mm and
        dimensions are specified by the x_scale, z_exag, and z_adder inputs.
    """

    wp = cq.Workplane("XZ")

    irows = range(0, len(arr), subsample)
    y_scale = x_scale * dy / dx
    y_offset = y_scale / len(irows)

    t0 = time.time()
    for i, irow in enumerate(irows):
        if i > 0:
            wp = wp.workplane(offset=y_offset)

        xz = get_xz(arr, irow, dx,
                    subsample=subsample,
                    x_scale=x_scale,
                    z_exag=z_exag,
                    z_adder=z_adder)
        if spline:
            wp = (wp
                  .lineTo(*xz[0])
                  .spline(xz[1:], includeCurrent=True)
                  .lineTo(xz[-1][0], 0)
                  .close()
                 )
        else:
            for ixz in xz:
                wp = wp.lineTo(*ixz)
            wp = wp.lineTo(xz[-1][0], 0).close()

    if spline:
        wp = wp.loft(combine=True, ruled=False)
    else:
        wp = wp.loft(combine=False, ruled=True)

    print('Render took {:.1f} minutes. '
          'Approximately {:.1f} points per mm. '
          'Aspect ratio (x:y) is {:.0f}:{:.0f}'
          .format((time.time() - t0) / 60,
                  arr.shape[1] / subsample / x_scale,
                  x_scale, y_scale))

    return wp
