"""
Created on Fri Sep 28 12:26:45 2018

Last Modified:  1/31/2019 4:50PM
Eric Allen, University of Delaware
@author: allenea

These are alternatives to MET: Model Evaluation Toolkit - supported by NCAR/DTC

Slow version that carefully tracks each calculation and builds that up to create
    a time series analysis of model performance.

Lead-lag analysis
Saves to CSV file
Accounts for land-mask
Hourly/Case/IV Analysis and plots as time-series
    - Overall numbers may vary slightly since it becomes an average of the cases
        for the stat/iv in question. Need to include formula in thesis for both.
Excluded CMLF data in validation because it's moving and iffy data.

DO NOT DO LEAD-LAG on the time-series version  -- DON'T RELEASE
"""
## IMPORTS
import os
import sys
import warnings
from datetime import timedelta
import pandas as pd
import numpy as np
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src_sfc_stats.getmetrics import getmetrics
from src_sfc_stats.get_land_value import get_land_value
from src_sfc_stats.get_values_loc import get_values_loc
from src_sfc_stats.get_substeps import get_substeps
from src_sfc_stats.print_info import print_table, print_bad_output
from src_sfc_stats.plot_timeseries import make_plot
from commonclass.ModelData import ModelData
import src_sfc_stats.alt_stats as astat

def model_analysis_timeseries(stats, obs):
    """ Calculated each statistic individually and builds up over the analysis"""
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
            leadlagstr = "_LLp"+str(lead_num)

        elif "-" in leadlag_str:
            lead_num = -1 * int("".join(leadlag_str.split("-")))
            lead_time = timedelta(minutes=(obs.observation_interval_min*lead_num))
            leadlagstr = "_LLn"+str(lead_num)

        else:
            sys.exit("NO LEAD LAG. NEEDS TO BE INDICATED BY a + or a -... Exiting")
        print("Lead Lag Analysis Step: ", lead_num, "as", lead_time.total_seconds()/60, "Minutes")
    else:
        lead_num = 0
        lead_time = timedelta(minutes=0)
        leadlagstr = ""
        print("No Lead Lag Analysis: ", lead_num, "as", lead_time.total_seconds()/60, "Minutes")

    #Make directory to store CSV's if it doesn't already exist
    if not os.path.exists(stats.csv_out_dir) and stats.save_results:
        os.makedirs(stats.csv_out_dir)


    ##########################DO NOT EDIT BELOW#####################################################
    ## FILL WITH TIME STEPS DURING ANALYSIS FOR PLOTTING
    header = ["Station", "AVERAGE"]
    header_iv = ["RunType", "AVERAGE"]
    header_case = ["CaseStudy", "AVERAGE"]

    #Constants
    fillHeaders = False
    analysis_hour = stats.analysis_start_hour
    ###################################################3########################################
    stats.get_analysis_window(stats.casestudy_times[0])

    wrf_substeps, _analysis_substeps =  get_substeps(stats.wrf_interval_min,\
                                                    stats.analysis_interval_min)
    if _analysis_substeps != 1:
        sys.exit("Current configuration does not allow multiple substeps in the analysis data for one wrf_step")

    stats.print_info()


    for variable in stats.variables:

        #Create the table to hold the final statistics
        create_stats_table = np.empty((len(stats.independent_variables),\
                                       len(stats.stats_table)))
        table = pd.DataFrame(create_stats_table, columns=stats.stats_table,\
                             index=stats.independent_variables)
        table["VAR."] = stats.independent_variables

        iv_analysis = np.zeros((len(stats.alt_stats_list), len(stats.independent_variables),\
                                int(((stats.analysis_end+lead_time -\
                                stats.analysis_start+lead_time).total_seconds()/\
                                (stats.analysis_interval_min * 60.0))+2))).astype(object)

        count_ivNum = 0
        # For each WRF configuration
        for ind_var in stats.independent_variables:
            all_obs_array = []
            all_pres_array = []
            case_analysis = np.zeros((len(stats.alt_stats_list), len(stats.casestudy_times),\
                                      int((((stats.analysis_end+lead_time -\
                                            stats.analysis_start+lead_time).total_seconds()/\
                                            (stats.analysis_interval_min * 60.0))+2)))).astype(object)
            count_caseNum = 0
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
                #data.loc[data['Wind_Speed (m/s)'] < 0.44704,\
                        #['Wind_Speed (m/s)', 'Wind_Direction (deg)']] = np.nan

                IDS = list(set(obs.id_string))
                IDS.sort()

                                #Calculate the expected length of observations/forecasted values extracted
                #sec = 60.0
                length_count = len(IDS)*int(((stats.analysis_end+lead_time -\
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



                # Plus two because extra first and extra last when all are averaged.
                half_hourly_analysis = np.zeros((len(stats.alt_stats_list), len(IDS),\
                                                 int(((stats.analysis_end+lead_time -\
                                    stats.analysis_start+lead_time).total_seconds()/\
                                    (stats.analysis_interval_min * 60.0))+2))).astype(object)

                hha_idx = 0
                hha_idx_lst = np.zeros((len(stats.alt_stats_list), len(IDS), 1)).astype(int)

                #Each statistical measure will have it's own position in this matrix
                #in the 0th column of each it will contain the station ID's
                for k in range(len(stats.alt_stats_list)):
                    half_hourly_analysis[k, :, 0] = IDS


                ## FOCUS ON 8am to 8pm so 12UTC to 0UTC
                ## CHANGED TO 6am to midnight that way it captures sunrise and sunset and after SB.
                lastJ = 0
                for j in range(0, len(wrf_data.wrf_dt), wrf_substeps):
                    #Checks every half hour and 30 minutes
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

                            if not fillHeaders and wrf_data.wrf_dt[j] != lastJ:
                                hha_idx += 1
                                # NAME ..... # AVERAGE
                                header.insert(hha_idx, wrf_data.wrf_dt[j].strftime("%d_%H:%M"))
                                header_iv.insert(hha_idx, analysis_hour)
                                header_case.insert(hha_idx, analysis_hour)
                                lastJ = wrf_data.wrf_dt[j]
                                analysis_hour += 1

                            for k in range(len(stats.alt_stats_list)):
                                which_row = np.where(half_hourly_analysis[k, :, 0]\
                                                     == obs.id_string[i])[0][0]
                                hha_idx_lst[k, which_row] = hha_idx_lst[k, which_row] + 1
                                half_hourly_analysis[k, which_row, hha_idx_lst[k, which_row]] = np.nan

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

                            if not fillHeaders and wrf_data.wrf_dt[j] != lastJ:
                                hha_idx += 1
                                # NAME ..... # AVERAGE
                                header.insert(hha_idx, wrf_data.wrf_dt[j].strftime("%d_%H:%M"))
                                header_iv.insert(hha_idx, analysis_hour)
                                header_case.insert(hha_idx, analysis_hour)
                                lastJ = wrf_data.wrf_dt[j]
                                analysis_hour += 1

                            # Observation Data is Missing Value
                            if np.isnan(obs.variable_data[i]):
                                for k in range(len(stats.alt_stats_list)):
                                    which_row = np.where(half_hourly_analysis[k, :, 0]\
                                                         == obs.id_string[i])[0][0]
                                    hha_idx_lst[k, which_row] = hha_idx_lst[k, which_row] +1
                                    half_hourly_analysis[k, which_row, hha_idx_lst[k,\
                                                                                   which_row]] = np.nan

                                obs_array[count] = np.nan
                                preds_array[count] = np.nan
                                count += 1

                            # WRF Data is Missing Value
                            elif trim_wrf_var is None or np.isnan(trim_wrf_var):
                                for k in range(len(stats.alt_stats_list)):
                                    which_row = np.where(half_hourly_analysis[k, :, 0]\
                                                                 == obs.id_string[i])[0][0]
                                    hha_idx_lst[k, which_row] = hha_idx_lst[k, which_row] +1
                                    half_hourly_analysis[k, which_row, hha_idx_lst[k,\
                                                                   which_row]] = np.nan

                                obs_array[count] = np.nan
                                preds_array[count] = np.nan
                                count += 1

                            else:
                                obs_array[count] = obs.variable_data[i]
                                preds_array[count] = trim_wrf_var
                                count += 1

                                for k in range(len(stats.alt_stats_list)):
                                    which_row = np.where(half_hourly_analysis[k, :, 0]\
                                                                     == obs.id_string[i])[0][0]
                                    hha_idx_lst[k, which_row] = hha_idx_lst[k, which_row] +1
                                    if stats.alt_stats_list[k] == "MAE":
                                        stat_value = astat.absolute_error(trim_wrf_var,\
                                                                         obs.variable_data[i])
                                    elif stats.alt_stats_list[k] == "MAPE":
                                        stat_value = astat.relative_error(trim_wrf_var,\
                                                                 obs.variable_data[i]) * 100.0
                                    elif stats.alt_stats_list[k] == "BIAS":
                                        stat_value = astat.forecast_error(trim_wrf_var,\
                                                                          obs.variable_data[i])

                                    elif stats.alt_stats_list[k] == "RMSE":
                                        stat_value = (astat.forecast_error(trim_wrf_var,\
                                                           obs.variable_data[i])  ** 2) ** 0.5
                                    #ADD MORE STATS HERE
                                    else:
                                        sys.exit("UNKNOWN STAT")

                                    half_hourly_analysis[k, which_row, hha_idx_lst[k,\
                                                                   which_row]] = stat_value

                        #This will always happen even if there is no wrf match to the t_time.
                        elif obs.t_time[i] != wrf_data.wrf_dt[j]+lead_time and\
                                        wrf_data.wrf_dt[j]+lead_time == wrf_data.wrf_dt[-1]+lead_time:
                            continue

                        #This will always happen at the end of the iteration or if no match.
                        elif obs.t_time[i]+lead_time == obs.t_time[-1]+lead_time:
                            continue
                        #WRF Data outside analysis window

                # MAKE TRUE TO PREVENT HEADERS FROM BEING REFILLED EACH TIME
                fillHeaders = True

                #Single WRF run (case) analyzed
                all_obs_array.extend(obs_array[:count])
                all_pres_array.extend(preds_array[:count])

                #Stats for each WRF Output by observation location - Case and Variation and Variable
                for k in range(len(stats.alt_stats_list)):
                    ### AVERAGE BY LOCATION - TAKE THE MEAN OF ALL CHECKS (OR SQ MEAN FOR RMSE)
                    ### FOR EACH HOUR.... THEN FOR EACH STATION AND APPEND
                    hr_stations_stat = pd.DataFrame(half_hourly_analysis[k, :, :], index=None)
                    hr_stations_stat[hr_stations_stat == 0] = np.nan

                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore", category=RuntimeWarning)
                        horAvg = np.nanmean(hr_stations_stat.drop(columns=0).astype(float), axis=1)

                    complete_station_stats = pd.concat((pd.DataFrame(half_hourly_analysis[k, :, :],\
                                             index=None), pd.DataFrame(horAvg, index=None)), axis=1)
                    per_hhour_stats = np.array(complete_station_stats)
                    per_hhour_stats[per_hhour_stats == 0] = np.nan
                    #vertically (DEFAULT: axis=0),
                    vertAvg = np.nanmean((np.array(per_hhour_stats)[:, 1:]).astype(float), axis=0)
                    tmp1 = np.zeros(len(vertAvg)+1).astype(object)
                    tmp1[0] = "CaseAvg"
                    tmp1[1:] = vertAvg
                    half_hourly_analysis2 = pd.concat((pd.DataFrame(per_hhour_stats,\
                                        index=None), pd.DataFrame(tmp1, index=None).T))
                    half_hourly_analysis2.columns = header
                    half_hourly_analysis2 = half_hourly_analysis2.reset_index(drop=True)

                    # WRITE TO CSV - 4 files per case subdir (so about 16 files per variable)
                    new_dir = stats.csv_out_dir+"/csv/Case_"+ wrf_data.case_time.replace("-", "_").strip()+"/"
                    #Make directory to store CSV's if it doesn't already exist
                    if not os.path.exists(new_dir):
                        os.makedirs(new_dir)
                    half_hourly_analysis2.to_csv(new_dir+ind_var+"_"+\
                                                 stats.alt_stats_list[k]+"_"+stats.domain+"_"+\
                                                 variable[:10].strip()+"_s"+\
                                                 str(stats.analysis_start_hour)+"_len"+\
                                                 str(stats.analysis_length_hrs)+"_freq"+\
                                                 str(stats.analysis_interval_min)+leadlagstr+".csv",\
                                                 index=False, float_format='%.3f')
                    case_type_check = np.array(half_hourly_analysis2)[len(half_hourly_analysis2)-1][:-1]
                    case_type_check[0] = case_time
                    case_analysis[k, count_caseNum] = case_type_check

                count_caseNum += 1

            #Statistics for a single "independent variable"
            statlist = getmetrics(np.array(all_obs_array),\
                                  np.array(all_pres_array), stats.stats_table)
            table.loc[ind_var, 1:] = statlist

            #Stats for each case for an IV type (and stat): WRF Output - Variation and Variable
            for k in range(len(stats.alt_stats_list)):
                vertAvgCase = np.nanmean((case_analysis[k, :, 1:]).astype(float), axis=0)
                tmp4 = np.zeros(len(vertAvgCase)+1).astype(object)
                tmp4[0] = "TypeAvg"
                tmp4[1:] = vertAvgCase
                caseAnaly2 = pd.concat((pd.DataFrame(case_analysis[k, :, :]), pd.DataFrame(tmp4).T))
                caseAnaly2[caseAnaly2 == 0] = np.nan
                ivAnaly2 = caseAnaly2
                caseAnaly2 = np.array(caseAnaly2)
                horAvgCase = np.nanmean(caseAnaly2[:, 1:].astype(float), axis=1)#horizontally (axis=1)
                case22 = pd.concat((pd.DataFrame(caseAnaly2), pd.DataFrame(horAvgCase)), axis=1)
                case22.columns = header_case
                case22.to_csv(stats.csv_out_dir+"/csv/"+ind_var+"_"+stats.alt_stats_list[k]+"_s"+\
                              str(stats.analysis_start_hour)+"_len"+\
                              str(stats.analysis_length_hrs)+"_freq"+str(stats.analysis_interval_min)+\
                              "_"+variable[:10]+leadlagstr+".csv", index=False, float_format='%.3f')

                iv_check222 = np.array(case22)[len(case22)-1][:-1]
                iv_check222[0] = ind_var
                iv_analysis[k, count_ivNum] = iv_check222
            count_ivNum += 1

        ### For each variable (and stat) overall stats by model variation (Independent Variable)
        for k in range(len(stats.alt_stats_list)):
            vertAvgIV = np.nanmean((iv_analysis[k, :, 1:]).astype(float), axis=0)
            tmp5 = np.zeros(len(vertAvgIV)+1).astype(object)
            tmp5[0] = "Average"
            tmp5[1:] = vertAvgIV
            ivAnaly2 = pd.concat((pd.DataFrame(iv_analysis[k, :, :]), pd.DataFrame(tmp5).T))
            ivAnaly2[ivAnaly2 == 0] = np.nan
            ivAnaly2 = np.array(ivAnaly2)
            horAvgIV = np.nanmean(ivAnaly2[:, 1:].astype(float), axis=1)
            df = pd.concat((pd.DataFrame(ivAnaly2), pd.DataFrame(horAvgIV)), axis=1)
            df.columns = header_iv
            df.to_csv(stats.csv_out_dir+"/csv/All_Assimilation_Types_"+stats.alt_stats_list[k]+\
                      "_s"+str(stats.analysis_start_hour)+"_len"+\
                    str(stats.analysis_length_hrs)+"_freq"+str(stats.analysis_interval_min)+\
                      "_"+variable[:10]+leadlagstr+".csv", index=False, float_format='%.3f')

            #COMPARE ALL_ASSIMILATION_TYPES TO FINAL WRF_VALIDATE NUMBERS

            #Create figure for each stat as a time series
            if stats.save_results:
                stat_name = stats.alt_stats_list[k]
                if len(stats.casestudy_times) == 1:
                    stats.set_plot_out_dir(os.path.join(stats.graph_out_dir,\
                                        wrf_data.case_time.replace("-", "_").strip()))
                    if not os.path.exists(stats.graph_out_dir):
                        os.mkdir(stats.graph_out_dir)
                    
                    outfile = stats.graph_out_dir+"/"+stats.alt_stats_list[k]+"_s"+\
                        str(stats.analysis_start_hour)+"_len"+\
                        str(stats.analysis_length_hrs)+"_freq"+str(stats.analysis_interval_min)+"_"+\
                        variable[:10]+leadlagstr+"_iv"+\
                        str(len(stats.independent_variables))+"_single_case.png"
                else:
                    outfile = stats.graph_out_dir+"/"+stats.alt_stats_list[k]+"_s"+str(stats.analysis_start_hour)+"_len"+\
                        str(stats.analysis_length_hrs)+"_freq"+str(stats.analysis_interval_min)+"_"+\
                        variable[:10]+leadlagstr+"_All_Cases.png"

                make_plot(outfile, variable, df, stat_name, header_iv)

        #Statistics for a single meteorological variable
        table.reset_index(drop=True)

        #Round the data to the thousandth place
        decimals = pd.Series(([3]*len(stats.stats_table)), index=stats.stats_table)
        print_table(table, variable, decimals)

        if stats.save_results:

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
