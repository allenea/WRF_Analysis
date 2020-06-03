"""Copyright (C) 2018-Present E. Allen, D. Veron - University of Delaware"""
#
# You may use, distribute and modify this code under the
# terms of the GNU Lesser General Public License v3.0 license.
#
# https://www.gnu.org/licenses/lgpl-3.0.en.html
#
# Imports
from __future__ import print_function
import wrf


def get_values_loc(ncfile, wrf_var, landmask, land_type, latitude, longitude, analysis_type=True):
    """WRF VARIABLE FULL TIME SLICE AT ONE LOCATION"""
    #analysis_type (True) = x_y[1], x_y[0]
    #analysis_type (False) =
    #x_y[1], x_y[0]
    #x_y[1]+1, x_y[0]
    #x_y[1]-1, x_y[0]
    #x_y[1], x_y[0]+1
    #x_y[1], x_y[0]-1
    #x_y[1]+1,  x_y[0]+1
    #x_y[1]-1,  x_y[0]-1
    #x_y[1]+1,  x_y[0]-1
    #x_y[1]-1,  x_y[0]+1

    x_y = wrf.ll_to_xy(ncfile, latitude, longitude, meta=False)
    try:
        valid_loc = wrf_var[int(x_y[1]), int(x_y[0])]
    except ValueError:
        return None
    if analysis_type:
        #Value at the point
        return valid_loc
    else:
        sum_values = 0.0
        num_values = 0
        #Value at the point 0 = west-east and 1 = north-south
        for i in range(-1, 1+1):
            for j in range(-1, 1+1):
                #print("X+", j, "Y+",i)
                try:
                    temp = wrf_var[int(x_y[1]+j), int(x_y[0]+i)]
                    ltype = landmask[int(x_y[1]+j), int(x_y[0]+i)]
                except ValueError:
                    continue

                if land_type == ltype:
                    sum_values += temp
                    num_values += 1
                else:
                    pass
                #print(land_type, ltype, temp, num_values)
        #print(sum_values, num_values)
        if num_values == 0:
            return None
        return sum_values/num_values
