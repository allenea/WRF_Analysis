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

class DetectionInfo:
    """
    Developed by Eric Allen, University of Delaware

    Set cases and models you wish to run here.
    """
    def __init__(self,\
                 cases_times=list(),\
                 case_versions=list(),\
                 variable="Potential Temperature",\
                 domain_number=1,\
                 save_results=True):

        #Set Detection Wishes
        self.set_domain(domain_number)
        self.initialize_cases(cases_times)
        self.initialize_versions(case_versions)
        self.set_save(save_results)
        self.set_variable(variable)

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
    def set_save(cls, boolean):
        """To save or not to save"""
        cls.save_results = boolean

    @classmethod
    def set_variable(cls, string):
        """Set variable"""
        cls.variable = string

    @classmethod
    def set_data_dir(cls, string):
        """This should be the parent directory for all model data"""
        cls.data_directory = string
        if not os.path.exists(cls.data_directory):
            sys.exit("Directory containing model data not found. Exiting...")

    @classmethod
    def set_namelistwps(cls, string):
        """Add the namelist.wps file"""
        cls.wpsfile = string

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
    def clear_cases(cls):
        """clear all cases"""
        cls.casestudy_times = list()

    @classmethod
    def clear_case_versions(cls):
        """Clear all versions"""
        cls.independent_variables = list()

    @classmethod
    def print_info(cls):
        """Print the Detection Info from the namelist file"""
        print("Detection Information:")
        print("----------------------")
        print("Model Data Location: ", cls.data_directory)
        print("Namelist.wps File: ", cls.wpsfile)
        print("List of Case Studies: ", cls.casestudy_times)
        print("List of Sensitivity Tests: ", cls.independent_variables)
        print("Domain Number: ", cls.domain)
        print("Variable: ", cls.variable)
        print("Save Results: ", cls.save_results)
        print()
        print()
