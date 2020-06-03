"""
Created on Fri Sep 28 12:26:45 2018

Last Modified:  1/31/2019 4:50PM
Eric Allen, University of Delaware
@author: allenea

This is an alternative to MET: Model Evaluation Toolkit - supported by NCAR/DTC

Fast version that doesn't worry about making a time-series

Lead-lag analysis
Saves to CSV file
Accounts for land-mask
Excluded CMLF data in validation because it's moving and iffy data.
"""
## IMPORTS
import os
import sys
from datetime import timedelta
import pandas as pd
import numpy as np
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src_sfc_stats.getmetrics import getmetrics
from src_sfc_stats.get_land_value import get_land_value
from src_sfc_stats.get_values_loc import get_values_loc
from src_sfc_stats.get_substeps import get_substeps
from src_sfc_stats.print_info import print_table, print_bad_output
from commonclass.ModelData import ModelData

def model_analysis(stats, obs):
    """Using an instance of the analysis instructions, perform the analysis"""
    # =============================================================================
    # ## Unacceptable land mask value locations based on FM Codes for marine observing systems
    # =============================================================================
    marine_list = stats.marine_list
    badlist = []
    #Gather the necessary information for lead-lag analysis
    if stats.leadlag:
        leadlag_str = "".join(stats.leadlag_str.split())
        if "+" in leadlag_str:
            lead_num = int("".join(leadlag_str.split("+")))
            lead_time = timedelta(minutes=(obs.observation_interval_min*lead_num))

        elif "-" in leadlag_str:
            lead_num = -1 * int("".join(leadlag_str.split("-")))
            lead_time = timedelta(minutes=(obs.observation_interval_min*lead_num))
        else:
            sys.exit("NO LEAD LAG. NEEDS TO BE INDICATED BY a + or a -... Exiting")
        print("Lead Lag Analysis Step: ", lead_num, "as", lead_time.total_seconds()/60, "Minutes")
    else:
        lead_num = 0
        lead_time = timedelta(minutes=0)
        print("No Lead Lag Analysis: ", lead_num, "as", lead_time.total_seconds()/60, "Minutes")

    #Make directory to store CSV's if it doesn't already exist
    if not os.path.exists(stats.csv_out_dir) and stats.save_results:
        os.makedirs(stats.csv_out_dir)

    wrf_substeps, _analysis_substeps = get_substeps(stats.wrf_interval_min,\
                                                    stats.analysis_interval_min)

    stats.print_info()

    for variable in stats.variables:
        #Create the table to hold the final statistics
        create_stats_table = np.empty((len(stats.independent_variables),\
                                       len(stats.stats_table)))
        table = pd.DataFrame(create_stats_table, columns=stats.stats_table,\
                             index=stats.independent_variables)
        table["VAR."] = stats.independent_variables

        for ind_var in stats.independent_variables:
            all_obs_array = []
            all_pres_array = []

            # For each case study
            for case_time in stats.casestudy_times:
                stats.get_analysis_window(case_time)

                # Read in observation data  - Verification
                obs.set_data_file(case_time)
                obs.read_in_obs()
                obs.get_obs_data(variable)
                obs.get_obs_metadata()
                obs.get_obs_datetime_obj()

                ## IF LESS THAN 1 MPH as M/S then make it missing
                #obs.obs_data.loc[obs.obs_data['Wind_Speed (m/s)'] < 0.44704,\
                        #['Wind_Speed (m/s)', 'Wind_Direction (deg)']] = np.nan

                #Calculate the expected length of observations/forecasted values extracted
                #sec = 60.0
                length_count = len(list(set(obs.id_string)))*int(((stats.analysis_end+lead_time -\
                               stats.analysis_start+lead_time).total_seconds()/\
                                (stats.wrf_interval_min * 60.0))+1)

                #Initialize the arrays and the indexer for storing values
                count = 0
                obs_array = np.empty(length_count)
                preds_array = np.empty(length_count)

                # For each WRF domain in analysis get that data file and read it. If Empty->EXIT
                wrf_data = ModelData(case=case_time, version=ind_var, var=variable,\
                                 domain=stats.domain, path=stats.data_directory)

                #Remove any observations outside of the domain
                obs.remove_data_outside(wrf_data.ncfile)

                #Extract the WRF variable for analysis
                #wrf_var = get_wrf_data(ncfile, variable)

                #Get landmask values
                wrf_data.get_landmask()

                #Get observation data
                obs.get_obs_data(variable)

                #Match up the data and the observations
                for j in range(0, len(wrf_data.wrf_dt), wrf_substeps):
                    len0 = 0
                    for i in range(len0, len(obs.obs_data)):
                        #Observation Data outside analysis window
                        if obs.t_time[i] < stats.analysis_start+lead_time or\
                                    obs.t_time[i] > stats.analysis_end+lead_time:
                            len0 = i
                        #WRF Data outside analysis window
                        elif wrf_data.wrf_dt[j] < stats.analysis_start or\
                                wrf_data.wrf_dt[j] > stats.analysis_end:
                            continue

                        elif (np.isnan(obs.obs_lat_list[i]) or np.isnan(obs.obs_lon_list[i])) and\
                                obs.t_time[i] == wrf_data.wrf_dt[j]+lead_time:
                            # For Eric's purposes the CMLF is often missing lat and long
                            # Nothing else should. So let me know if there is....
                            if obs.id_string[i] != "CMLF":
                                print("OUTSIDE OF MODEL DOMAIN - ERROR",\
                                     obs.id_string[i], obs.obs_lat_list[i], obs.obs_lon_list[i])
                            obs_array[count] = np.nan
                            preds_array[count] = np.nan
                            count += 1
                            continue

                        ## Correct obs.t_time - MATCH!
                        elif obs.t_time[i] == wrf_data.wrf_dt[j]+lead_time:
                            # When evaluating with an average only use same land-type as station.
                            land_val = get_land_value(wrf_data.ncfile,\
                                                      wrf_data.landvalues[j, :, :],\
                                                      obs.obs_lat_list[i], obs.obs_lon_list[i])

                            #These conditional handle if the wrf land type is wrong
                            if land_val == 0.0 and obs.fm_string_list[i] not in marine_list:
                                # NOT IN --- Limits the badlist to only higher resolution geography
                                # but makes the change even if it's from the low-res cases
                                if obs.id_string[i] not in badlist and ind_var not\
                                                    in ("NARR", "FTIME", "GEOG"):
                                    badlist.append(obs.id_string[i])
                                land_val = 1.0

                            elif land_val == 1.0 and obs.fm_string_list[i] in marine_list:
                                if obs.id_string[i] not in badlist and ind_var not\
                                                    in ("NARR", "FTIME", "GEOG"):
                                    badlist.append(obs.id_string[i])
                                land_val = 0.0

                            #Get the WRF variable's values for this time and location
                            trim_wrf_var = get_values_loc(wrf_data.ncfile,\
                                                  wrf_data.wrf_var[j, :, :],\
                                                  wrf_data.landvalues[j, :, :], land_val, \
                                                  obs.obs_lat_list[i], obs.obs_lon_list[i],\
                                                  analysis_type=stats.single_point_analysis)
                            # Observation data has a missing value
                            if np.isnan(obs.variable_data[i]):
                                obs_array[count] = np.nan
                                preds_array[count] = np.nan
                                count += 1

                            # WRF data has a missing value
                            elif trim_wrf_var is None or np.isnan(trim_wrf_var):
                                obs_array[count] = np.nan
                                preds_array[count] = np.nan
                                count += 1

                            # Good Data - MATCHES!
                            else:
                                obs_array[count] = obs.variable_data[i]
                                preds_array[count] = trim_wrf_var
                                count += 1

                        #This will always happen even if there is no wrf match to the obs.t_time.
                        elif obs.t_time[i] != wrf_data.wrf_dt[j]+lead_time and\
                                wrf_data.wrf_dt[j]+lead_time == wrf_data.wrf_dt[-1]+lead_time:
                            continue

                        #This will always happen at the end of the iteration or if no match.
                        elif obs.t_time[i]+lead_time == obs.t_time[-1]+lead_time:
                            continue

                #Single WRF run (case) analyzed
                all_obs_array.extend(obs_array[:count])
                all_pres_array.extend(preds_array[:count])

            #Statistics for a single "independent variable"
            statlist = getmetrics(np.array(all_obs_array),\
                                  np.array(all_pres_array), stats.stats_table)

            table.loc[ind_var, 1:] = statlist

        #Statistics for a single meteorological variable
        table.reset_index(drop=True)

        #Round the data to the thousandth place
        decimals = pd.Series(([3]*len(stats.stats_table)), index=stats.stats_table)
        print_table(table, variable, decimals)

        if stats.save_results:
            if stats.leadlag:
                if lead_num > 0:
                    leadlagstr = "_LLp"+str(lead_num)
                elif lead_num < 0:
                    leadlagstr = "_LLn"+str(lead_num)
                else:
                    leadlagstr = ""
            else:
                leadlagstr = ""

            if len(stats.casestudy_times) > 1:
                strcase = str(len(stats.casestudy_times))
            else:
                strcase = wrf_data.case_time.replace("-", "_")

            csv_outfile = stats.csv_out_dir + "/WRF_Validate_"+variable.split()[0]+\
                "_nc"+strcase+\
                "_niv"+str(len(stats.independent_variables))+"_s"+\
                str(stats.analysis_start_hour)+"_len"+\
                str(stats.analysis_length_hrs)+"_freq"+\
                str(stats.analysis_interval_min)+leadlagstr+".csv"

            table.to_csv(csv_outfile, index=False, float_format='%.3f')

    #List any locations with the wrong land type in WRF from what was expected
    if len(badlist) > 0:
        print_bad_output(badlist)
