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
import glob
import math
from datetime import datetime
import numpy as np
import pandas as pd
import wrf
class ObsData:
    """
    Developed by Eric Allen, University of Delaware

    Set cases and models you wish to run here.
    """
    def __init__(self,\
                 obs_data_dir,\
                 dtype_usage=str(),\
                 observation_interval_min=int(60)):

        self.set_obs_data_dir(obs_data_dir)
        self.set_obs_interval_min(observation_interval_min)
        self.set_obs_dtype(dtype_usage)

    @classmethod
    def set_obs_data_dir(cls, string):
        """This should be the parent directory for all model data"""
        cls.OBS_DATA_DIR = string
        if not os.path.exists(cls.OBS_DATA_DIR):
            sys.exit("Observation Data Directory Not Found")

    @classmethod
    def set_obs_dtype(cls, string):
        """Set (int) domain number as string"""
        cls.DTYPE_USAGE = string

    @classmethod
    def set_obs_interval_min(cls, number):
        """Set list of cases"""
        cls.OBSERVATION_INTERVAL_MIN = number


    @classmethod
    def print_info(cls):
        """Print the Detection Info from the namelist file"""
        print("Detection Information:")
        print("----------------------")
        print("Observation Data Location: ", cls.OBS_DATA_DIR)
        print("Observation Time Interval (minutes): ", cls.OBSERVATION_INTERVAL_MIN)
        print("Data Type (file-naming scheme) ", cls.DTYPE_USAGE)
        print()
        print()


# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# CHANGE FOR A DIFFERENT OBSERVATION DATA SOURCE/FORMAT
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
    @classmethod
    def set_data_file(cls, case_time):
        """Get the file name for the observation data"""
        ### GATHER VALIDATION DATA DIRECTORY FOR CASE
        if cls.DTYPE_USAGE == "10m":
            data_file = cls.OBS_DATA_DIR+"/"+cls.DTYPE_USAGE+"/"+case_time[0:10]+'/'
        elif cls.DTYPE_USAGE == "original":
            data_file = cls.OBS_DATA_DIR+"/"+cls.DTYPE_USAGE+"/"+case_time[0:10]+'/'

        obsdat = glob.glob(data_file+"*")
        if len(obsdat) != 1:
            sys.exit("EXITING. TOO MANY FILES.", obsdat)

        cls.obs_data_file = obsdat[0]

    @classmethod
    def read_in_obs(cls):
        """store array with observation data"""
        data = pd.read_csv(cls.obs_data_file, low_memory=False)
        data.columns.tolist()
        # FOR ALL EXPECTED/POSSIBLE MISSING VALUE FLAGS -- remove
        data[data == " "] = np.nan
        data[data == ""] = np.nan
        data[data == -888888.0] = np.nan
        # Save cleaned data
        cls.obs_data = data


    @classmethod
    def get_obs_data(cls, variable):
        """These variables from your data file should match the variable names above
        You will use those header variable names to get the data from WRF and the
        observation dataset. The user will need to configure to fit their data."""
        # PER VARIABLE - VERIFICATION
        if variable == 'Wind_Speed (m/s)':
            cls.variable_data = np.array(cls.obs_data['Wind_Speed (m/s)'])
        elif variable == 'Wind_Direction (deg)':
            cls.variable_data = np.array(cls.obs_data['Wind_Direction (deg)'])
        elif variable == 'Air_Temperature (K)':
            cls.variable_data = np.array(cls.obs_data['Air_Temperature (K)'])
        elif variable == 'Dewpoint_Temperature (K)':
            cls.variable_data = np.array(cls.obs_data['Dewpoint_Temperature (K)'])
        elif variable == "Relative Humidity (%)":
            cls.variable_data = np.array(cls.obs_data['Relative Humidity (%)'])
        elif variable == "Pressure (Pa)":
            cls.variable_data = np.array(cls.obs_data['Pressure (Pa)'])
        elif variable in ("U10", "V10"):
            u10, v10 = wind_components(np.array(cls.obs_data['Wind_Speed (m/s)']),\
                                       np.array(cls.obs_data['Wind_Direction (deg)']))
            if variable == "U10":
                cls.variable_data = u10
            elif variable == "V10":
                cls.variable_data = v10
            else:
                print("MAJOR ERROR IN U/V10 GATHERING.")
        else:
            try:
                cls.variable_data = np.array(cls.obs_data[variable])
            except:
                sys.exit("INVALID VARIABLE OPTION")
        
    @classmethod
    def get_obs_metadata(cls):
        """Get the observation data metadata"""
        cls.id_string = np.array(cls.obs_data['ID_String'])
        cls.obs_lat_list = np.array(cls.obs_data['Latitude'])
        cls.obs_lon_list = np.array(cls.obs_data['Longitude'])
        cls.fm_string_list = np.array(cls.obs_data['FM_string'])

    @classmethod
    def get_obs_datetime_obj(cls):
        """Get observation date-time data as datetime objects"""
        obs_time = []
        #SAMPLE: '2014-06-04T06:00:00.000000000'
        year = np.array(cls.obs_data['YEAR'], dtype=int)
        month = np.array(cls.obs_data['MONTH'], dtype=int)
        day = np.array(cls.obs_data['DAY'], dtype=int)
        hour = np.array(cls.obs_data['HOUR'], dtype=int)
        minute = np.array(cls.obs_data['MINUTE'], dtype=int)
        for idx in range(len(year)):
            utc_dt = datetime(year[idx], month[idx], day[idx], hour[idx], minute[idx])
            obs_time.append(utc_dt)
        cls.t_time = obs_time

# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
    @classmethod
    def remove_data_outside(cls, ncfile):
        """Identify and remove any observations out of the range of the domain"""
        dom_lat_max = np.max(wrf.g_latlon.get_lat(ncfile, timeidx=0, meta=False))
        dom_lat_min = np.min(wrf.g_latlon.get_lat(ncfile, timeidx=0, meta=False))
        dom_lon_max = np.max(wrf.g_latlon.get_lon(ncfile, timeidx=0, meta=False))
        dom_lon_min = np.min(wrf.g_latlon.get_lon(ncfile, timeidx=0, meta=False))

        # HANDLES LAT/LON OUTSIDE WRF DOMAIN
        out_of_range = cls.obs_data[(cls.obs_data.Latitude > dom_lat_max) |\
                            (cls.obs_data.Latitude < dom_lat_min) &\
                            (cls.obs_data.Longitude > dom_lon_max) |\
                            (cls.obs_data.Longitude < dom_lon_min)].index
        if len(out_of_range) != 0:
            print("out_of_range INDEX", out_of_range)
        cls.obs_data.drop(out_of_range, inplace=True)


def wind_components(wspd, wdir):
    """CALCULATE U and V"""
    degrad = math.pi / 180.0
    wdir_rads = wdir * degrad
    u_wind = -wspd * np.sin(wdir_rads)
    v_wind = -wspd * np.cos(wdir_rads)
    return u_wind, v_wind
