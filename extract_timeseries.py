#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 14:50:02 2020

@author: allenea
"""
import os
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src_sfc_stats.get_land_value import get_land_value
from src_sfc_stats.get_values_loc import get_values_loc
from commonclass.ModelData import ModelData
#LWSD1  = -75.11917, 38.78278


loc_id = "LWSD1"
loc_lat = 38.78278
loc_lon = -75.11917

#loc_id = "CMAN4"
#loc_lat = 38.96777778
#loc_lon = -74.96

#loc_id = "44009"
#loc_lat = 38.461
#loc_lon = -74.703

#loc_id = "SJSN4"
#loc_lat = 39.305
#loc_lon = -75.377

# Sussex Inland
#loc_id = "DWAR"
#loc_lat = 38.679167
#loc_lon = -75.247222

#Kent Inland
#loc_id = "DSJR"
#loc_lat = 39.0882
#loc_lon = -75.4373

#Sussex Complex Coastal
#loc_id = "DIRL"
#loc_lat = 38.633056
#loc_lon = -75.066389

# =============================================================================
# Set location of parent directory for model data.
# =============================================================================
data_directory = os.path.join("/", "Volumes", "EA_BACKUP",\
                              "SAVE_OUTPUTS", "DELAWARE_OUTPUTS")
# =============================================================================
# =============================================================================
# #  Cases and Sensitivity Tests - Naming scheme crafted by fmt_run_path
# #     All model runs located within data_directory
# =============================================================================
# =============================================================================
case_time = '2014-06-03_12:00'
domain = "03"


independent_var = ["PLAIN"]#, "NDA"] #, "ALL", "ALL_SST"]
variables = [ "SST", 'Air_Temperature (K)']#, 'Wind_Speed (m/s)',\
             #'Wind_Direction (deg)', 'Dewpoint_Temperature (K)']#,\
             #'Pressure (Pa)']#\
             #,
OUTHEADER = [loc_id+"_SST", loc_id+"_TEMP"]#, loc_id+"_WSPD",\
             #loc_id+"_DIR", loc_id+"_DEW"]#, loc_id+"_PRES"]#\
            # 
wrf_substeps = 1

# For each WRF domain in analysis get that data file and read it. If Empty->EXIT
for ind_var in independent_var:
    #Get landmask values
    wrf_data = ModelData(case=case_time, version=ind_var, var=variables[0],\
             domain=domain, path=data_directory)
    wrf_data.get_landmask()
    lst = np.zeros((43, len(variables)))
    for i, var in enumerate(variables):
        wrf_data.get_wrf_data(var)
        for j in range(0, len(wrf_data.wrf_dt), wrf_substeps):
            #Some type of work around...
            #if "PRES" in var.upper():
            #    wrf.g_slp.get_slp(cls.ncfile, timeidx=wrf.ALL_TIMES,\
            #                            method='cat', squeeze=True, cache=None,\
            #                            meta=False, _key=None, units='Pa')
            
            # When evaluating with an average only use same land-type as station.
            land_val = get_land_value(wrf_data.ncfile,\
                                  wrf_data.landvalues[j, :, :],\
                                  loc_lat, loc_lon)
            #Get the WRF variable's values for this time and location
            trim_wrf_var = get_values_loc(wrf_data.ncfile,\
                                  wrf_data.wrf_var[j, :, :],\
                                  wrf_data.landvalues[j, :, :], land_val, \
                                  loc_lat, loc_lon,\
                                  analysis_type=False)
            if var in ["SST", 'Air_Temperature (K)', 'Dewpoint_Temperature (K)']:
                lst[j, i] = trim_wrf_var - 273.15
            else:
                lst[j, i] = trim_wrf_var
        #sys.exit(0)
    
    df = pd.DataFrame(lst, columns=OUTHEADER, index=None)
    df.to_csv(loc_id+"_"+ind_var+"_output.csv")
    ##ADD THIS TO EXCEL SPREADSHEET
    #del wrf_data
    sys.exit(0)