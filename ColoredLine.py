#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Function for plotting colored lines.
'''

__author__ = "Aljaž Ravnikar"
__date__ = "27.8.2024"

import numpy as np
from matplotlib.collections import LineCollection
import warnings

def colored_line(x, y, c, ax, n_mids, cmap, norm, **lc_kwargs):
    """
    Plot a line with a color specified along the line by a third value [1].

    It does this by creating a collection of line segments. Each line segment is
    made up of `n_mids` intermediate points between the (x, y) data points, connected
    with straight lines with interpolated color.

    Parameters
    ----------
    x, y : array-like
        The horizontal and vertical coordinates of the data points.
    c : array-like
        The color values, which should be the same size as x and y.
    ax : Axes
        Axis object on which to plot the colored line.
    n_mids : int
        Number of intermediate points between each pair of original points.
    cmap : matplotlib.colors.Colormap
        The colormap instance used to map color values to RGBA colors.
    **lc_kwargs
        Any additional arguments to pass to matplotlib.collections.LineCollection
        constructor. This should not include the array keyword argument because
        that is set to the color argument. If provided, it will be overridden.

    Returns
    -------
    matplotlib.collections.LineCollection
        The generated line collection representing the colored line.

    References
    ----------
    .. [1] `Multicolored line
            <https://matplotlib.org/stable/gallery/lines_bars_and_markers/multicolored_line.html>`_
            on Matplotlib Examples.
    """
    if "array" in lc_kwargs:
        warnings.warn('The provided "array" keyword argument will be overridden')
    
    if norm is None:
        norm = mpl.colors.Normalize(vmin=np.min(c), vmax=np.max(c))

    # Default the capstyle to butt so that the line segments smoothly line up
    default_kwargs = {"capstyle": "butt"}
    default_kwargs.update(lc_kwargs)            

    # Generate intermediate points between each pair of points and interpolate color values.
    x = np.asarray(x)
    y = np.asarray(y)
    x_midpts = []
    y_midpts = []
    interpolated_colors = []
    for i in range(len(x)-1):
        xi = np.linspace(x[i], x[i+1], n_mids+2)[1:]
        yi = np.linspace(y[i], y[i+1], n_mids+2)[1:]
        l = ((x[i]-x[i+1])**2 + (y[i]-y[i+1])**2)**0.5
        li = np.linspace(0, l, n_mids+2)[1:]
        segment_colors = np.interp(li, [li[0],li[-1]], [c[i],c[i+1]])
        x_midpts.extend(xi)
        y_midpts.extend(yi)
        interpolated_colors.extend(segment_colors)
    x_midpts = np.array([x[0]] + x_midpts)
    y_midpts = np.array([y[0]] + y_midpts)
    interpolated_colors = np.array(interpolated_colors)

    # Determine the start, middle, and end coordinate pair of each line segment.
    # Use the reshape to add an extra dimension so each pair of points is in its
    # own list. Then concatenate them to create:
    # [
    #   [(x1_start, y1_start), (x1_mid, y1_mid), ... (x1_end, y1_end)],
    #   [(x2_start, y2_start), (x2_mid, y2_mid), ... (x2_end, y2_end)],
    #   ...
    # ]
    coord_start = np.column_stack((x_midpts[:-1], y_midpts[:-1]))[:, np.newaxis, :]
    coord_end = np.column_stack((x_midpts[1:], y_midpts[1:]))[:, np.newaxis, :]
    segments = np.concatenate((coord_start, coord_end), axis=1)

    lc = LineCollection(segments, colors=cmap(norm(interpolated_colors)), norm=norm ,**default_kwargs)
    return ax.add_collection(lc)