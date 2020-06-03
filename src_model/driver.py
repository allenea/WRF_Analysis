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
#import time
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src_model.find_front import find_front
from commonclass.ModelData import ModelData

def driver(grid, detection_info):
    """driver: Run the detection algorithm by looping through cases/versions and analyzing

    Input:
        grid (class)  instance of DetectionInfo
        detection_info (class) instance of DetectionInfo
    Output:
        None
        csv file containing the time, lat, long of the frontal locations.
    """
    grid.print_info()

    detection_info.print_info()

    for case in detection_info.casestudy_times:
        for ivar in detection_info.independent_variables:

            wrf_data = ModelData(case=case, version=ivar, var=detection_info.variable,\
                                 domain=detection_info.domain,\
                                 path=detection_info.data_directory)

            wrf_data.set_datapath(os.path.join(os.getcwd(), 'Data', "Model_Data", "Fronts",\
                                    wrf_data.case_time.replace("-", "_"), wrf_data.version))

            wrf_data.set_mappath(os.path.join(os.getcwd(), 'Plots', 'ModelFronts',\
                                   wrf_data.case_time.replace("-", "_"), wrf_data.version))

            wrf_data.set_namelistwps(detection_info.wpsfile)
            wrf_data.set_save(detection_info.save_results)

            #FOR DEBUG ONLY
            #wrf_data.print_info()

            #Loop through times in the model output
            first_df = True
            for time_step in range(len(wrf_data.wrf_dt)):
                #start_time = time.time()
                #Update timestep
                wrf_data.set_timestep(time_step)

                #Find Front - Single Time Step
                out_lon, out_lat, front_info = find_front(wrf_data, grid)

                #Store data for one time step, each time step
                if first_df:
                    master_list = np.zeros((len(out_lat), len(wrf_data.wrf_dt)+1))
                    header = ["LATITUDE",\
                              wrf_data.wrf_dt[wrf_data.time_idx].strftime("%m%d%Y_%H%M")]
                    master_list[:, 0] = out_lat
                    master_list[:, time_step+1] = out_lon
                    first_df = False
                else:
                    header.append(wrf_data.wrf_dt[wrf_data.time_idx].strftime("%m%d%Y_%H%M"))
                    master_list[:, time_step+1] = out_lon

                #end_time = time.time()
                print(ivar, time_step, ":: Front Found: ", front_info[0], "  |||  Percentage: ",\
                      front_info[1], "  |||  Length: ", front_info[2])
                      #, "  |||  ", end_time - start_time)
                sys.stdout.flush()

            sbf_df = pd.DataFrame(master_list, columns=header)

            #Save data
            if detection_info.save_results:
                outstring = os.path.join(wrf_data.datapath, "SBF_"+\
                           wrf_data.case_time.replace("-", "_")+\
                           "_"+wrf_data.version+".csv")

                sbf_df.to_csv(outstring, index=False)
