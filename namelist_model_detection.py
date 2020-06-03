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
import warnings
import matplotlib as mpl
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from commonclass.AnalysisGrid import AnalysisGrid
from commonclass.DetectionInfo import DetectionInfo
from src_model.driver import driver

if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')

def main():
    """Set configuration of Front Detection Domain and Simulations to Analyze"""
    warning_input = True    # True ignores warnings / false tracks warnings
    if warning_input:
        warnings.filterwarnings("ignore")
# =============================================================================
#   Analysis Grid Information
# =============================================================================
    level = 2                       # Model level
    horizontal_resolution = 1.0     # Resolution of domain being analyzed
    west_start = 125
    east_end = 315
    south_start = 125
    north_end = 325

    cell_size = 2                   # Number of grid cells on each side -- upscale/avg
    gradient_distance = 10          # dx for gradient

    threshold = 0.1                 # Frontal Strength values below 0.125 are removed
    min_pixel_area = 500            # Connected features must have a size of 500 pixels

    grid = AnalysisGrid(level, horizontal_resolution, cell_size, gradient_distance, west_start,\
                         east_end, south_start, north_end, threshold, min_pixel_area)

# =============================================================================
#   Detection and Model Run Information
#
#   POTENTIAL TEMPERATURE (I.E, PERTURBATION + REFERENCE TEMPERATURE)
# =============================================================================
    variable = "Potential Temperature"          # This shouldn't change
    domain = 3                                  # Int value 3 --> "03"
    save_results = True                        # Should be True
    namelist_wps_file = os.path.join(os.getcwd(), 'namelist_FRONT.wps') #Set valid path

# =============================================================================
# Set location of parent directory for model data.
# =============================================================================
    #DATA_DIRECTORY = os.path.join("/", "home", "work", "clouds_wind_climate",\
    #                               "WRF4", "DelWRF", "SAVE_OUTPUTS")
    data_directory = os.path.join("/", "Volumes", "Seagate_Expansion",\
                                  "SAVE_OUTPUTS", "DELAWARE_OUTPUTS")
# =============================================================================
# =============================================================================
# #  Cases and Sensitivity Tests - Naming scheme crafted by fmt_run_path
# #     All model runs located within data_directory
# =============================================================================
# =============================================================================
    casestudy_time = ['2014-06-03_12:00', '2014-06-07_12:00',\
                      '2015-07-19_12:00', '2015-08-13_12:00']

    independent_var = ["FTIME", "GEOG", "PLAIN", "FERRY", "DEOS", "BOTH", "ALL",\
                       "NDA", "FERRY_SST", "DEOS_SST", "BOTH_SST", "ALL_SST"]

# =============================================================================
# =============================================================================
# # Setup Detection Info Class
# =============================================================================
# =============================================================================
    # First Location of model data (all EXCEPT BUOY and BUOY_SST runs)
    detect = DetectionInfo(cases_times=casestudy_time, case_versions=independent_var,\
                           variable=variable, domain_number=domain, save_results=save_results)
    detect.set_data_dir(data_directory)
    detect.set_namelistwps(namelist_wps_file)

# =============================================================================
#   Check to make sure valid information is being passed
# =============================================================================
    if detect.data_directory is None or not os.path.exists(detect.data_directory):
        sys.exit("INVALID DIRECTORY FOR MODEL DATA")

    if len(detect.casestudy_times) == 0 and len(detect.independent_variables) == 0:
        sys.exit("No cases and/or versions of the model were provided (naming purposes)")
# =============================================================================
#   Start detecting fronts
# =============================================================================
    driver(grid, detect)

# =============================================================================
# =============================================================================
# # EXCLUSIVE FOR ERIC'S THESIS SINCE 8TB DRIVE FAILED
# =============================================================================
# =============================================================================
    # Second Location of model data (BUOY and BUOY_SST runs)
    data_directory = os.path.join("/", "Volumes", "Allen_Data2",\
                                  "SAVE_OUTPUTS", "DELAWARE_OUTPUTS")

    #Set the new set of case versions
    detect.set_data_dir(data_directory)

    #Remove all case versions
    detect.clear_case_versions()

    #Set the new case versions
    independent_var = ['BUOY', "BUOY_SST"]
    detect.add_case_versions(independent_var)
# =============================================================================
# =============================================================================
# # END EXCLUSIVE FOR ERIC'S THESIS
# =============================================================================
# =============================================================================
    if detect.data_directory is None or not os.path.exists(detect.data_directory):
        sys.exit("INVALID DIRECTORY FOR MODEL DATA")

    if len(detect.casestudy_times) == 0 and len(detect.independent_variables) == 0:
        sys.exit("No cases and/or versions of the model were provided (naming purposes)")
# =============================================================================
#   Start detecting fronts
# =============================================================================
    driver(grid, detect)

if __name__ == '__main__':
    main()
    print("Completed Front Detection")
