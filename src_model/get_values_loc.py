"""Copyright (C) 2018-Present E. Allen, D. Moore, D. Veron - University of Delaware"""
#
# You may use, distribute and modify this code under the
# terms of the GNU Lesser General Public License v3.0 license.
#
# https://www.gnu.org/licenses/lgpl-3.0.en.html
#
# Imports
from __future__ import print_function

def get_values_loc2(data_in, size_in, latitude, longitude):
    """get_values_loc2: WRF VARIABLE FULL TIME SLICE AT ONE LOCATION

    Input:
        data_in -- (2D-array) theta values for a single model level
        size_in -- (int) an attribute of wrf_data class [cell_size]
        longitude -- (2D-array) longitude values for a single model level
        latitude -- (2D-array) latitude values for a single model level
    Output:
        (float) Average theta value for the "nugget" or None (no data)
    """
    sum_values = 0.0
    num_values = 0
    #Value at the point 0 = west-east and 1 = north-south
    for i in range(-size_in, size_in+1):
        for j in range(-size_in, size_in+1):
            try:
                temp = data_in[int(latitude+j), int(longitude+i)]
            except ValueError:
                continue
            sum_values += temp
            num_values += 1

    if num_values == 0:
        return None

    return sum_values/num_values
