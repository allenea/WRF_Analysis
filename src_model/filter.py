"""Copyright (C) 2018-Present E. Allen, D. Moore, D. Veron - University of Delaware"""
#
# You may use, distribute and modify this code under the
# terms of the GNU Lesser General Public License v3.0 license.
#
# https://www.gnu.org/licenses/lgpl-3.0.en.html
#
# Imports
from __future__ import print_function
import numpy as np
from scipy import ndimage
from skimage.measure import regionprops

def filter_data(data, grid):
    """filter_data: Remove small clusters of possible frontal value

    Input:
        data (2D array) Front Threshold Values
        grid (class) AnalysisGrid
    Output:
        data (2D array) Front Threshold Values - Cleaned
    """
    #Pre-processing data so that the rest of the function will work.
    data[np.isnan(data)] = 0

    #See 'ndimage' for more information.
    simg = ndimage.generate_binary_structure(2, 2) #Create structure

    #labeled: each connected feature is given a number to then be
    #analyzed individually.
    #ncomponents: number of individual connected features in data.
    labeled, ncomponents = ndimage.measurements.label(data, structure=simg)

    #Statistics
    #These build arrays of statistics where each element represents
    #the statistics for the given labeled feature.
    #In other words, the area for labeled feature #5 in 'labeled' is
    #the fifth element in the 'areas' array below.

    #means = ndimage.mean(data, labeled, range(1, ncomponents + 1))
    #maxs = ndimage.maximum(data, labeled, range(1, ncomponents + 1))
    #locs = [r.centroid for r in regionprops(labeled)]#center of mass (x/y)
    areas = [r.filled_area for r in regionprops(labeled)]#in pixels
    labels = [r.label for r in regionprops(labeled)]#number of feature
    maj_ax_len = [r.major_axis_length for r in regionprops(labeled)]

    #Iterate through connected features.
    len_area = len(areas)
    for i in range(len_area):
        idx = labeled == labels[i]
        if maj_ax_len[i] == 0.0:
            labeled[idx] = 0
            data[idx] = np.nan
            continue

        #Too small:
        if areas[i] < grid.filter_area:
            labeled[idx] = 0
            data[idx] = np.nan
        #Or else just continue on to next if statement.
        else:
            #print(areas[i])
            pass

    data[data == 0] = np.nan

    return data
