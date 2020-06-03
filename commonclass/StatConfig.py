"""Copyright (C) 2018-Present E. Allen, D. Veron - University of Delaware"""
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
from datetime import datetime, timedelta

class StatConfig:
    """
    Developed by Eric Allen, University of Delaware

    Set grid you wish to use here.

    """
    def __init__(self,\
                 cases_times=list(),\
                 case_versions=list(),\
                 variables=list(),\
                 domain_number=int(),\
                 runtime_hours=int(),\
                 wrf_interval_min=int(),\
                 analysis_start_hour=int(),\
                 analysis_length_hrs=int(),\
                 analysis_interval_min=int(),\
                 single_point_analysis=False,\
                 save_results=True,\
                 leadlag=False,\
                 leadlag_str=str("-1")):

        #Set Detection Wishes
        self.initialize_cases(cases_times)
        self.initialize_versions(case_versions)
        self.initialize_variables(variables)
        self.set_domain(domain_number)

        self.set_runtime_hours(runtime_hours)
        self.set_interval_min(wrf_interval_min)

        self.set_analysis_type(single_point_analysis)
        self.set_analysis_start_hour(analysis_start_hour)
        self.set_analysis_length_hrs(analysis_length_hrs)
        self.set_analysis_interval_min(analysis_interval_min)
        self.get_analysis_end_hour()

        self.set_save_results(save_results)
        self._init_timeseries(False)
        self.toggle_leadlag(leadlag)
        self.set_leadlag_str(leadlag_str)

    @classmethod
    def get_analysis_window(cls, case_time):
        """
        Calculates the analysis window. Doesn't go multiple months or years.

        (str) Case_Time: i.e. '2014-06-04_12:00'
        (int) analysis_start_hour:  12 # 00UTC
        (int) analysis_length_hrs: i.e. 24 (00UTC + 1 day)
        """
        if cls.analysis_end_hour > cls.runtime_hours:
            sys.exit("Analysis extends longer than declared runtime. Exiting...")
        else:
            tdelta_analysis = timedelta(hours=cls.analysis_start_hour)
            tdelta_end = timedelta(hours=cls.analysis_end_hour)

            time_object = datetime.strptime(case_time, '%Y-%m-%d_%H:%M')

            cls.analysis_start = time_object + tdelta_analysis
            cls.analysis_end = time_object + tdelta_end

    @classmethod
    def set_domain(cls, number):
        """Set (int) domain number as string"""
        cls.domain = str(number).zfill(2)

    @classmethod
    def initialize_cases(cls, lst):
        """Set list of cases"""
        cls.casestudy_times = lst

    @classmethod
    def initialize_versions(cls, lst):
        """set list of case versions"""
        cls.independent_variables = lst

    @classmethod
    def initialize_variables(cls, lst):
        """Set variables"""
        cls.variables = lst

    @classmethod
    def add_cases(cls, lst):
        """Add case (TIME) e.g. 2014-06-03_12:00"""
        for string in lst:
            cls.casestudy_times.append(string)

    @classmethod
    def add_case_versions(cls, lst):
        """Add sensitivity tests (for all cases there should be a consistent version)
        I used: FTIME, GEOG, PLAIN, NDA, ALL, BUOY, DEOS, etc....."""
        for string in lst:
            cls.independent_variables.append(string)

    @classmethod
    def add_variables(cls, lst):
        """Add sensitivity tests (for all cases there should be a consistent version)
        I used: FTIME, GEOG, PLAIN, NDA, ALL, BUOY, DEOS, etc....."""
        for string in lst:
            cls.variables.append(string)

    @classmethod
    def clear_cases(cls):
        """clear all cases"""
        cls.casestudy_times = list()

    @classmethod
    def clear_case_versions(cls):
        """Clear all versions"""
        cls.independent_variables = list()

    @classmethod
    def clear_variables(cls):
        """Clear all versions"""
        cls.variables = list()

    @classmethod
    def set_save_results(cls, boolean):
        """To save or not to save"""
        cls.save_results = boolean


    @classmethod
    def set_runtime_hours(cls, number):
        """setter"""
        cls.runtime_hours = number

    @classmethod
    def set_interval_min(cls, number):
        """setter"""
        cls.wrf_interval_min = number

    @classmethod
    def set_analysis_type(cls, boool):
        """setter"""
        cls.single_point_analysis = boool

    @classmethod
    def set_analysis_start_hour(cls, number):
        """setter"""
        cls.analysis_start_hour = number


    @classmethod
    def set_analysis_length_hrs(cls, number):
        """setter"""
        cls.analysis_length_hrs = number


    @classmethod
    def get_analysis_end_hour(cls):
        """setter"""
        cls.analysis_end_hour = cls.analysis_start_hour + cls.analysis_length_hrs


    @classmethod
    def change_analysis_end_hour(cls, number):
        """setter"""
        cls.analysis_end_hour = number

    @classmethod
    def set_analysis_interval_min(cls, number):
        """setter"""
        cls.analysis_interval_min = number


    @classmethod
    def set_stats_header(cls, lst):
        """setter"""
        cls.stats_table = ["VAR."] + lst


    @classmethod
    def set_marine_list(cls, lst):
        """setter"""
        cls.marine_list = lst

    @classmethod
    def _init_timeseries(cls, boolean):
        """setter"""
        cls.timeseries = boolean

    @classmethod
    def toggle_timeseries(cls, boolean, alt_stats_list=["MAE"]):
        """setter"""
        cls.timeseries = boolean
        cls.alt_stats_list = alt_stats_list

    @classmethod
    def toggle_leadlag(cls, boolean):
        """setter"""
        cls.leadlag = boolean


    @classmethod
    def set_leadlag_str(cls, string):
        """setter"""
        cls.leadlag_str = string


    @classmethod
    def set_data_dir(cls, string):
        """This should be the parent directory for all model data"""
        cls.data_directory = string
        if not os.path.exists(cls.data_directory):
            sys.exit("Directory containing model data not found. Exiting...")


    @classmethod
    def set_csv_out_dir(cls, string):
        """This should be the parent directory for all model data"""
        cls.csv_out_dir = string
        if not os.path.exists(cls.csv_out_dir):
            os.mkdir(cls.csv_out_dir)

    @classmethod
    def set_plot_out_dir(cls, string):
        """This should be the parent directory for all model data"""
        cls.graph_out_dir = string
        if not os.path.exists(cls.graph_out_dir):
            os.mkdir(cls.graph_out_dir)


    @classmethod
    def print_info(cls):
        """Print the Observation Info from the namelist file"""
        print("Observation Data Information")
        print("----------------")
        print("Do Alternative Time Series Analysis: ", cls.timeseries)
        print("List of Case Studies: ", cls.casestudy_times)
        print("List of Sensitivity Tests: ", cls.independent_variables)
        print("List of Variables: ", cls.variables)

        print("Domain Number: ", cls.domain)
        print("Save Results: ", cls.save_results)
        print("Model Runtime (hours): ", cls.runtime_hours)
        print("Model Output Interval (minutes): ", cls.wrf_interval_min)
        print()
        print("Analysis Starting (hour): ", cls.analysis_start_hour)
        print("Analysis Ending (hour): ", cls.analysis_end_hour)
        print("Analysis Length (hrs): ", cls.analysis_length_hrs)
        print("Analysis Interval (minutes): ", cls.analysis_interval_min)
        print()
        #print("Use Lead-Lag Analysis: ", cls.leadlag)
        #print("Lead-Lag Increment: ", cls.leadlag_str)
        #print("Statistics: ", cls.stats_table)
        #print("Marine FM-CODES: ", cls.marine_list)
        print()
        print()