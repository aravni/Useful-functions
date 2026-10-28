#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Functions for interactive measurments on images.
"""

__author__ = "Aljaž Ravnikar"
__date__ = "26.10.2024"

import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.widgets import Cursor

def MeasureLength(filename):
    '''
    Measure distance between two selected points on image.
    Points are selected using right click on mouse.
    
    Parameters
    ----------
    filename: str
        File location and name. Must be readable with `matplotlib.pyplot.imread`

    Returns
    -------
    points: array
        Picked points coordinates in pixels.
    '''
    # Load the image
    data = plt.imread(filename)
    fig, ax = plt.subplots()
    ax.imshow(data)
    plt.axis('off')

    # Interactive point selection
    points = []

    # Initialize the cursor and keep track of the last limits
    cursor = Cursor(ax, useblit=True, color='red', linewidth=0.5)
    last_xlim, last_ylim = ax.get_xlim(), ax.get_ylim()

    def onclick(event):
        '''Check if the click is a right-click to select points'''
        if event.button == 3:  # Use right-click to add two points
            if len(points) < 2: # Add point
                points.append((event.xdata, event.ydata))
                plt.plot(event.xdata, event.ydata, 'r+')  # Mark point
                fig.canvas.draw()
                print(f'Point {len(points):n} [{points[-1][0]:>7.5g},{points[-1][1]:>7.5g}]')
                if len(points) == 2: # Calculate Euclidean distance in pixels
                    p1, p2 = points
                    pixel_distance = np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
                    px_horizontal = abs(p2[0] - p1[0])
                    px_vertical = abs(p2[1] - p1[1])
                    print(f"Length horizontal:  {px_horizontal:>10.3f} px")
                    print(f"Length vertical:    {px_vertical:>10.3f} px")
                    print(f"Length total:       {pixel_distance:>10.3f} px")
                    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'r-')

                    cursor.visible = False # Hide cursor
                    fig.canvas.draw()
                    fig.canvas.mpl_disconnect(cid) # Disconnect further clicks
    def update_cursor(event):
        '''Function to reinitialize the cursor after zoom/pan'''
        nonlocal last_xlim, last_ylim
        # Check if the limits have changed
        current_xlim, current_ylim = ax.get_xlim(), ax.get_ylim()
        if current_xlim != last_xlim or current_ylim != last_ylim:
            cursor.visible = True
            last_xlim, last_ylim = current_xlim, current_ylim
            fig.canvas.draw_idle()

    # Connect the click event to the figure
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    fig.canvas.mpl_connect('draw_event', update_cursor)
    
    plt.show()
    return np.array(points)

def MeasureAngle(filename):
    '''
    Measure angle between two lines selected by three points on image, where
    first selected point is so called corner point. Points are selected using
    right click on mouse.
    
    Parameters
    ----------
    filename: str
        File location and name. Must be readable with `matplotlib.pyplot.imread`

    Returns
    -------
    alpha: float
        Angle between lines in `rad`. Clockwise direction is positive.
    points: array
        Picked points coordinates in pixels.
    '''
    # Load the image
    data = plt.imread(filename)
    fig, ax = plt.subplots()
    ax.imshow(data)
    plt.axis('off')

    # Interactive point selection
    points = []

    # Initialize the cursor and keep track of the last limits
    cursor = Cursor(ax, useblit=True, color='red', linewidth=0.5)
    last_xlim, last_ylim = ax.get_xlim(), ax.get_ylim()
    line, = ax.plot([], [], 'r--')  # Initialize a line object for preview
    x = np.linspace(0, data.shape[1], 3)

    # Initialize variables
    alpha = None
    k1 = None
    k2 = None

    def onclick(event):
        '''Check if the click is a right-click to select points'''
        nonlocal alpha, k1, k2
        if event.button == 3:  # Use right-click to add two points
            if len(points) < 2: # Add point
                points.append((event.xdata, event.ydata))
                plt.plot(event.xdata, event.ydata, 'r+')  # Mark point
                fig.canvas.draw()
                print(f'Point {len(points):n} [{points[-1][0]:>7.5g},{points[-1][1]:>7.5g}]')
                if len(points) == 2: # Line is defined
                    p1, p2 = points
                    k1 = (p2[1]-p1[1]) / (p2[0]-p1[0])
                    n1 = p1[1] - k1*p1[0]
                    line1 = lambda x: k1*x + n1
                    plt.plot(x, line1(x), 'r-', lw=0.75)
                    ax.set_xlim(last_xlim)
                    ax.set_ylim(last_ylim)
                    fig.canvas.draw()
            elif len(points) == 2: # Add third point, fit line and find angle
                points.append((event.xdata, event.ydata))
                plt.plot(event.xdata, event.ydata, 'r+')  # Mark point
                print(f'Point {len(points):n} [{points[-1][0]:>7.5g},{points[-1][1]:>7.5g}]')

                p1, p2, p3 = points
                k2 = (p3[1]-p1[1]) / (p3[0]-p1[0])
                n2 = p1[1] - k2*p1[0]
                line2 = lambda x: k2*x + n2
                plt.plot(x, line2(x), 'r-', lw=0.75)
                ax.set_xlim(last_xlim)
                ax.set_ylim(last_ylim)

                # alpha = np.arctan((k2-k1) / (1+k1*k2)) #smallest angle
                alpha = np.arctan2(p3[1]-p1[1], p3[0]-p1[0]) - np.arctan2(p2[1]-p1[1], p2[0]-p1[0])
                print(f'Angle between lines = {np.rad2deg(alpha):.3f}°')

                cursor.visible = False # Hide cursor
                fig.canvas.draw()
                fig.canvas.mpl_disconnect(cid) # Disconnect further clicks
    def update_cursor(event):
        '''Function to reinitialize the cursor after zoom/pan'''
        nonlocal last_xlim, last_ylim
        # Check if the limits have changed
        current_xlim, current_ylim = ax.get_xlim(), ax.get_ylim()
        if current_xlim != last_xlim or current_ylim != last_ylim:
            cursor.visible = True
            last_xlim, last_ylim = current_xlim, current_ylim
            fig.canvas.draw_idle()
    def onmove(event):
        '''Update the preview line as the cursor moves'''
        if len(points) == 2:  # Only update if the first two point are selected
            x1, y1 = points[0]
            line.set_data([x1, event.xdata], [y1, event.ydata])  # Update line endpoint
            fig.canvas.draw_idle()

    # Connect the click event to the figure
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    fig.canvas.mpl_connect('draw_event', update_cursor)
    fig.canvas.mpl_connect('motion_notify_event', onmove) # Slowing down plotting -> comment for faster plotting

    plt.show()
    return alpha, np.array(points)

if __name__ == '__main__':
    a,p=MeasureAngle("G:/FS/Vecfazni_sistemi/vaje/v3_Skupina_1_2.jpg")