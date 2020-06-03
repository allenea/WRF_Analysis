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

def get_land_value(ncfile, wrf_var, latitude, longitude):
    """WRF LANDMAKS VALUE AT ONE LOCATION"""
    try:
        # LAT LON to X Y
        x_y = wrf.ll_to_xy(ncfile, latitude, longitude, meta=False)
        #Longitude, Latitude, # TIME -- ignore
        return wrf_var[int(x_y[1]), int(x_y[0])]
    #OUTSIDE DOMAIN
    except ValueError:
        return None
