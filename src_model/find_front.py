"""Copyright (C) 2018-Present E. Allen, D. Moore, D. Veron - University of Delaware"""
#
# You may use, distribute and modify this code under the
# terms of the GNU Lesser General Public License v3.0 license.
#
# https://www.gnu.org/licenses/lgpl-3.0.en.html
#
# Imports
from __future__ import print_function
import os
import sys
import numpy as np
import numpy.ma as ma
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src_model.get_values_loc import get_values_loc2
from src_model.detect_front import detect_front
from src_model.plot_data import plot_data
from src_model.filter import filter_data

def find_front(wrf1, grid1):
    """find_front: Calculate and Find the Front

    May need to change criteria for what is/isn't a front.

    Input:
        wrf1 (class) ModelData
        grid1 (class) AnalysisGrid
    Output:
        lon_pts -- (list) Longitude points of front
        lat_pts -- (list) Latitude points of front
        found -- (Boolean) True/False: Front Found
    """
    # Set the dimensions of the WRF domain
    south_north = wrf1.lat_dim
    west_east = wrf1.lon_dim
    #levels = wrf1.vert_dim
                        # MIN:must be greater than 0
                        # MAX:one less than the unstaggered dimension #

    data_fill = np.empty((south_north, west_east))

    #Fill the array with calculations of theta
    for ilat in range(grid1.south_start, grid1.north_end, grid1.cell_size):
        for jlon in range(grid1.west_start, grid1.east_end, grid1.cell_size):
            theta = get_values_loc2(wrf1.wrf_var[wrf1.time_idx, grid1.level, :, :],\
                                    grid1.cell_size, ilat, jlon)
            for idx2 in range(-grid1.cell_size, grid1.cell_size+1):
                for jdx2 in range(-grid1.cell_size, grid1.cell_size+1):
                    data_fill[ilat+idx2, jlon+jdx2] = theta

    #Frontal strength calculations - ALL
    front_threshold = np.empty((south_north, west_east-grid1.gradient_distance))

    #Frontal strength calculation - Filter low values
    front_threshold2 = np.empty((south_north, west_east-grid1.gradient_distance))

    for row in range(grid1.south_start, grid1.north_end):
        for col in range(grid1.west_start, grid1.east_end-grid1.gradient_distance):

            front_threshold[row, col] = (data_fill[row, col] -\
                           data_fill[row, col + grid1.gradient_distance]) /\
                           grid1.gradient_distance*grid1.dx_1

            if front_threshold[row, col] >= grid1.threshold:
                front_threshold2[row, col] = front_threshold[row, col]
            else:
                front_threshold2[row, col] = np.nan


    #Remove low pixels and small clusters of pixels
    filtered_data = filter_data(front_threshold2, grid1)
    masked_array = ma.masked_where(filtered_data < grid1.threshold, filtered_data)
    lon_pts, lat_pts = detect_front(masked_array, grid1, wrf1)

    #Determine front characteristics
    tmp_df = pd.DataFrame(lon_pts, index=None)
    ratio_pts = round(float((1-(tmp_df.isnull().sum()/len(tmp_df))) * 100), 2)
    sequence = np.array(tmp_df.dropna(how='any').index)
    longest_seq = max(np.split(sequence, np.where(np.diff(sequence) != 1)[0]+1), key=len)
    len_long_seq = len(tmp_df.iloc[longest_seq])

    #TODO Check if it meets the characteristics
    if (ratio_pts > 50.00 and len_long_seq > 20) or (ratio_pts > 30.00 and len_long_seq > 45):
        found = True
    else:
        found = False
        lon_pts[:] = [np.nan] * len(lon_pts)

    if wrf1.save:
        np.savetxt(wrf1.datapath+"/2D_front_"+wrf1.case_time.replace("-", "_")+"_"+\
                   wrf1.version+"_"+str(wrf1.time_idx)+".csv", front_threshold,\
                   delimiter=',', fmt='%f')

        np.savetxt(wrf1.datapath+"/2D_theta_"+wrf1.case_time.replace("-", "_")+"_"+\
                   wrf1.version+"_"+str(wrf1.time_idx)+".csv", data_fill,\
                   delimiter=',', fmt='%f')

    plot_data(wrf1, grid1, front_threshold2, lon_pts, lat_pts)

    return lon_pts, lat_pts, [found, ratio_pts, len_long_seq]
