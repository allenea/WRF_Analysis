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
from datetime import datetime
from netCDF4 import Dataset
import wrf
from wrf import getvar

class ModelData:
    """
    Class for Model Data

    Developed by Eric Allen, University of Delaware

    Input:
        case (string) case time
        version (string) Sensitivity test version
        var (string) Variable name
        domain (string) 2-char string domain number "02"
        path (string) path to the model data
    Output:
        class object
    """
    def __init__(self,\
                 case,\
                 version,\
                 var,\
                 domain,\
                 path,\
                 clear_ncfile=False):

        if path is None:
            sys.exit("No Path to Model Data")

        self.fmt_run_path(case, version, domain, path)

        self.set_version(version)

        self.set_open_file()

        self.get_wrf_data(var)

        self.get_wrf_datetime_obj()

        self.lats = getvar(self.ncfile, "XLAT", timeidx=0, method='cat',\
                           squeeze=True, cache=None, meta=False)

        self.lons = getvar(self.ncfile, "XLONG", timeidx=0, method='cat',\
                           squeeze=True, cache=None, meta=False)

        self.set_lat_dimension()
        self.set_lon_dimension()
        self.set_vert_dimension()

        self.set_timestep(0)

        #Likely not the right path.... Will need to be set correctly later
        self.set_namelistwps(os.getcwd()+'/namelist.wps')
        self.set_save(None)

        #Clear from memory
        if clear_ncfile:
            self.clear_ncfile()

    @classmethod
    def set_open_file(cls):
        """set filename and get the data"""
        listing = glob.glob(cls.filelocname)
        if os.path.exists(listing[0]):
            cls.ncfile = Dataset(listing[0])
        else:
            sys.exit("FILE NOT FOUND IN PROVIDED PATH AND/OR FILENAME")

    @classmethod
    def fmt_run_path(cls, case, independent_var, domain, path_pwd):
        """
        SETS FILE FORMAT FOR CASES AND THEIR VARIATIONS
        Files should be arranged and named so you can simply look through.


        # DIRECTORY MAKER: Build Your Own Naming Mechanism
        # - For Example:
            'CaseStudy_6-4-2014/BOTH_6_4_2014'
            'CaseStudy_6-4-2014/DEOS_6_4_2014'
            'CaseStudy_6-4-2014/NDA_6_4_2014'
            'CaseStudy_6-4-2014/FERRY_6_4_2014'
            'CaseStudy_6-8-2014/BOTH_6_8_2014'
            'CaseStudy_6-8-2014/DEOS_6_8_2014'
            'CaseStudy_6-8-2014/FERRY_6_8_2014'
            'CaseStudy_6-8-2014/NDA_6_8_2014'
        """
        filename = "wrfout_d"+domain+"_*"

        prefix_casestudy = "CaseStudy_"
        dtuple = datetime.strptime(case, "%Y-%m-%d_%H:%M")
        short_time = dtuple.strftime('%-m-%-d-%Y')
        simulation = "/"+prefix_casestudy+short_time+"/"+independent_var+"_"+\
                        short_time.replace("-", "_")+"/"

        model_path = path_pwd+simulation+filename

        cls.filelocname = model_path
        cls.case_time = short_time


    @classmethod
    def get_wrf_data(cls, variable):
        """get_wrf_data: Add your data accordingly here.  What variables will you need?

        May need to add to this in the future

        Input:
            ncfile (netCDF4) netcdf file that contains the wrf model output
            variable (string) string with a valid variable name
        Output:
            wrf_var (array) All the data associated with that variable
        """
        if variable == 'Wind_Speed (m/s)':#10m wind speed    UNIT m/s
            data = wrf.g_uvmet.get_uvmet10_wspd_wdir(cls.ncfile, timeidx=wrf.ALL_TIMES,\
                                                    method='cat', squeeze=True, cache=None,\
                                                    meta=False, _key=None, units='m s-1')[0]

        elif variable == 'Wind_Direction (deg)':#10m wind direction UNIT m/s and degrees
            data = wrf.g_uvmet.get_uvmet10_wspd_wdir(cls.ncfile, timeidx=wrf.ALL_TIMES,\
                                                    method='cat', squeeze=True, cache=None,\
                                                    meta=False, _key=None, units='m s-1')[1]

        #2m air temperature KELVIN
        elif variable == 'Air_Temperature (K)':
            data = wrf.getvar(cls.ncfile, "T2", timeidx=wrf.ALL_TIMES, method='cat',\
                                                 squeeze=True, cache=None, meta=False)

        #2m dewpoint temperature KELVIN
        elif variable == 'Dewpoint_Temperature (K)':
            data = wrf.g_dewpoint.get_dp_2m(cls.ncfile, timeidx=wrf.ALL_TIMES,\
                                           method='cat', squeeze=True, cache=None,\
                                           meta=False, _key=None, units='K')
        elif variable in ("Potential Temperature", "th", "theta"):
            data = wrf.g_temp.get_theta(cls.ncfile, timeidx=wrf.ALL_TIMES,\
                                   method='cat', squeeze=True, cache=None,\
                                   meta=False, _key=None, units='K')
        #2m relative humidity   UNIT: %
        elif variable == "Relative Humidity (%)":
            data = wrf.g_rh.get_rh_2m(cls.ncfile, timeidx=wrf.ALL_TIMES,\
                                     method='cat', squeeze=True, cache=None,\
                                     meta=False, _key=None)

        #SLP pressure UNITS: Pa
        elif variable == "Pressure (Pa)":
            #wrf-python is absolute garbage with about 10% usefulness. This will only work
            #one at a time.
            data = wrf.g_slp.get_slp(cls.ncfile, timeidx=wrf.ALL_TIMES,\
                                        method='cat', squeeze=True, cache=None,\
                                        meta=False, _key=None, units='Pa')
        elif variable == "U10":
            data = wrf.g_uvmet.get_uvmet10(cls.ncfile, timeidx=wrf.ALL_TIMES,\
                                              method='cat', squeeze=True, cache=None,\
                                              meta=False, _key=None, units='m s-1')[0]

        elif variable == "V10":
            data = wrf.g_uvmet.get_uvmet10(cls.ncfile, timeidx=wrf.ALL_TIMES,\
                                          method='cat', squeeze=True, cache=None,\
                                          meta=False, _key=None, units='m s-1')[1]

        else:
            try:
                data = wrf.getvar(cls.ncfile, variable, timeidx=wrf.ALL_TIMES,\
                                 method='cat', squeeze=True, cache=None, meta=False)
            except:
                sys.exit("INVALID VARIABLE OPTION")

        cls.wrf_var = data
    
    @classmethod
    def get_landmask(cls):
        cls.landvalues = wrf.getvar(cls.ncfile, "LANDMASK", timeidx=wrf.ALL_TIMES,\
                                 method='cat', squeeze=True, cache=None, meta=False)
    @classmethod
    def set_version(cls, string):
        """set sensitivity test name
        Input:
            string (str)
        """
        cls.version = string

    @classmethod
    def set_timestep(cls, idx):
        """Update the time index
        Input:
            number (int)
        """
        cls.time_idx = idx

    @classmethod
    def set_namelistwps(cls, string):
        """Set the path to the namelist.wps file
        Input:
            string (str)
        """
        cls.wpsfile = string

    @classmethod
    def set_save(cls, boolean):
        """Set the boolean to determine what is saved
        Input:
            boolean (bool)
        """
        cls.save = boolean

    @classmethod
    def set_datapath(cls, string):
        """Update the path to store data. Verify its a valid path.
        Input:
            string (str)
        """
        cls.datapath = string

        if not os.path.exists(cls.datapath):
            os.makedirs(cls.datapath)

    @classmethod
    def set_mappath(cls, string):
        """Update the path to store plots. Verify its a valid path.
        Input:
            string (str)
        """
        cls.mappath = string

        if not os.path.exists(cls.mappath):
            os.makedirs(cls.mappath)

    @classmethod
    def set_lat_dimension(cls):
        """get/set the size of the latitudinal dimension"""
        cls.lat_dim = cls.ncfile.dimensions.get("south_north").size

    @classmethod
    def set_lon_dimension(cls):
        """get/set the size of the longitudinal dimension"""
        cls.lon_dim = cls.ncfile.dimensions.get("west_east").size

    @classmethod
    def set_vert_dimension(cls):
        """get/set the size of the vertical dimension"""
        cls.vert_dim = cls.ncfile.dimensions.get('bottom_top').size

    @classmethod
    def get_wrf_datetime_obj(cls):
        """get_wrf_datetime_obj: Get wrf timesteps as datetime objects

        Input:
            ncfile (netCDF4) netcdf file that contains the wrf model output
        Output:
            wrf_dt (list) List of wrf model time steps as datetime objects
        """
        #Get WRF time-step and reformat
        wrf_times = wrf.extract_times(cls.ncfile, timeidx=wrf.ALL_TIMES,\
                                  method='cat', squeeze=True, cache=None,\
                                  meta=False, do_xtime=False).astype(str)

        time_obj = [""] * len(wrf_times)
        for ijk, time in enumerate(wrf_times):
            # FOR SOME REASON THERE ARE 9 miliseconds precision when there should be 6
            time_obj[ijk] = datetime.strptime(time[:-3], '%Y-%m-%dT%H:%M:%S.%f')

        diff_wrf = time_obj[-1] - time_obj[0]
        wrf_timestep = (time_obj[1] - time_obj[0]).total_seconds()
        tot_sec_wrf = diff_wrf.total_seconds()

        if len(time_obj) != (tot_sec_wrf / wrf_timestep) + 1:
            sys.exit("WRF TIME NOT THE RIGHT LENGTH")

        cls.wrf_dt = time_obj

    @classmethod
    def clear_ncfile(cls):
        """Clear large file from memory"""
        cls.ncfile = None

    @classmethod
    def print_info(cls):
        """Print the Detection Info from the namelist file"""
        print("Model Data:")
        print("-----------")
        print("Model Data Location: ", cls.filelocname)
        print()
        print("Case: ", cls.case_time)
        print("Version: ", cls.version)
        print("Time Index: ", cls.time_idx)
        print()
        print("Namelist.wps File: ", cls.wpsfile)
        print("Output Data Location: ", cls.datapath)
        print("Output Plot Location: ", cls.mappath)
        print()
        print("Netcdf File (should be None): ", cls.ncfile)
        print("Save Results: ", cls.save)
        print("Dimensions(vert-lat-lon): ", cls.vert_dim, cls.lat_dim, cls.lon_dim)
        print()
        print()
