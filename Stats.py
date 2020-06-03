#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 14:48:46 2020

@author: allenea
"""
from __future__ import print_function
import os
import sys
import warnings
import matplotlib as mpl
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from commonclass.StatConfig import StatConfig
from commonclass.ObsData import ObsData
from src_sfc_stats.driver import analyze


if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')

warning_input = False    # True ignores warnings / false tracks warnings
if warning_input:
    warnings.filterwarnings("ignore")
# =============================================================================
# Set location of parent directory for model data.
# =============================================================================
data_directory = os.path.join("/", "Volumes", "Seagate_Expansion",\
                              "SAVE_OUTPUTS", "DELAWARE_OUTPUTS")
# =============================================================================
# =============================================================================
# #  Cases and Sensitivity Tests - Naming scheme crafted by fmt_run_path
# #     All model runs located within data_directory
# =============================================================================
# =============================================================================
casestudy_time = ['2014-06-03_12:00']

#independent_var = ["FTIME", "GEOG", "PLAIN", "FERRY", "DEOS", "BOTH", "ALL",\
#                   "NDA", "FERRY_SST", "DEOS_SST", "BOTH_SST", "ALL_SST"]
independent_var = ["ALL"]
variables = ['Wind_Speed (m/s)', 'Air_Temperature (K)', 'Dewpoint_Temperature (K)']

domain = 3                                  # Int value 3 --> "03"

save_results = True                        # Should be True

runtime_hours = 42
wrf_interval_min = 60                       ### CHANGE BASED ON MODEL-OUTPUT TIMESTEP

analysis_start_hour = 0
analysis_length_hrs = 16                    ### start_hr + length_hrs must not exceed runtime_hrs
analysis_interval_min = 60                  ### CHANGE BASED ON TIME-STEP YOU WANT ANALYZED
                                            ### MUST NOT BE SMALLER THAN WRF interval
single_point_analysis = False

leadlag = False             # Comparing model and observations might be better than this
leadlag_str = "-1"          # + is forward in time, - is backwards in time, # of stemps
                            # + is number of time-steps forward/backward in the observations

init_stats = StatConfig(cases_times=casestudy_time,\
                        case_versions=independent_var,\
                        variables=variables,\
                        domain_number=domain,\
                        runtime_hours=runtime_hours,\
                        wrf_interval_min=wrf_interval_min,\
                        analysis_start_hour=analysis_start_hour,\
                        analysis_length_hrs=analysis_length_hrs,\
                        analysis_interval_min=analysis_interval_min,\
                        single_point_analysis=single_point_analysis,\
                        save_results=save_results,\
                        leadlag=leadlag,leadlag_str=leadlag_str)

init_stats.set_data_dir(data_directory)
init_stats.set_csv_out_dir(os.path.join(os.getcwd(), "Data", "WRF_Analysis"))
init_stats.set_stats_header(["OBS", "PRED", "MAE", "RMSE", "BIAS", "MAD", "NSE"])
init_stats.set_marine_list(["FM-13 SHIP", "FM-18 BUOY", "FM-19 BUOY"])
# ==========================================================================


# =============================================================================
# ## Types of Statistics
# =============================================================================
# THESE ARE THE STATS YOU WANT CALCULATED HOURLY FOR TIME-SERIES ANALYSIS
time_series_analysis = False
alt_stats_list = ["MAE", "BIAS", "MAPE", "RMSE"]
init_stats.toggle_timeseries(time_series_analysis, alt_stats_list=alt_stats_list)
init_stats.set_plot_out_dir(os.path.join(os.getcwd(), "Plots", "WRF_Analysis"))


# =============================================================================
# # Setup Detection Info Class
# =============================================================================
# =============================================================================
# First Location of model data (all EXCEPT BUOY and BUOY_SST runs)


# Where is your observation data located
obs_data_dir = os.path.abspath('../../SeaBreeze_Data/All_Avg/')
# Do you have different types of data - File Naming Scheme
dtype_usage = '10m'         # original ||| highly recommended to always use 10m adjusted wind speed data.
observation_interval_min = 30               ### UNUSED

init_obs = ObsData(obs_data_dir=obs_data_dir,\
                   dtype_usage=dtype_usage,\
                   observation_interval_min=observation_interval_min)

analyze(init_stats, init_obs)
sys.exit(0)
init_stats.clear_cases()
init_stats.add_cases(['2014-06-07_12:00'])
analyze(init_stats, init_obs)

init_stats.clear_cases()
init_stats.add_cases(['2015-07-19_12:00'])

analyze(init_stats, init_obs)

init_stats.clear_cases()
init_stats.add_cases(['2015-08-13_12:00'])

