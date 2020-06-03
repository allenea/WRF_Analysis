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

def detect_front(masked_array, grid_in, wrf):
    """detect_front: Detect Leading Edge of Horizontal Front (Potential Temperature Gradient)

    Input:
        masked_array (masked array) Front Threshold Values
        grid_in (class) AnalysisGrid
        wrf (class) ModelData

    Output:
        sbflon (list) Longitudes of front locations
        sbflat (list) Latitude of front locations
    """
    sbflon = []
    sbflat = []
    spacer = int(grid_in.gradient_distance*0.5)
    eastern_point = (grid_in.east_end-grid_in.gradient_distance)-spacer
    for row in range(grid_in.south_start, grid_in.north_end):
        if not masked_array[row, :].mask.all():
            maxchange = 0.0
            #West = low numbers, East = High Numbers # -1 is to ensure it's the 0 idx
            #for idx in range(grid_in.west_start, grid_in.east_end-grid_in.gradient_distance):
            for idx in range(eastern_point, grid_in.west_start+spacer, -1):
                #If it is the largest gradient value, above threshold
                # and has a valid point above the threshold at 1/2 the
                # gradient distance on either side.
                if masked_array[row, idx] > maxchange\
                        and masked_array[row, idx] > grid_in.threshold\
                        and (masked_array[row, idx-spacer] > grid_in.threshold or\
                             masked_array[row, idx+spacer] > grid_in.threshold):

                    maxchange = masked_array[row, idx]
                    foundidx = idx

            if maxchange > 0:
                sbflon.append(wrf.lons[row, foundidx])
                sbflat.append(wrf.lats[row, foundidx])
            else:
                sbflon.append(np.nan)
                sbflat.append(wrf.lats[row, 0])
        else:
            sbflon.append(np.nan)
            sbflat.append(wrf.lats[row, 0])

    return sbflon, sbflat
