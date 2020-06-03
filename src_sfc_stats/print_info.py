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
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src_sfc_stats.split_list import split_list

def print_table(table, variable, decimals):
    """Nicely print the statistics table"""
    blank_index = [''] * len(table)
    table.index = blank_index
    rounded_table = table.round(decimals)

    print()
    print()
    print('VARIABLE: ', variable)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        pd.set_option('display.max_rows', 15)
        pd.set_option('display.max_columns', 15)
        pd.set_option('display.width', 1000)
        print(rounded_table)
    print()
    print()

def print_bad_output(badlist):
    """Nicely print the list of bad observation stations - by land type"""
    #All statistics for a single meteorological variable
    print("The following station(s) model-adjacent location(s) are opposite of their"+\
          " true\nland types (water/land). If single_point_analysis is False, "+\
          "then these are\ncorrected and the "+\
          "average consists of only neighboring grid cells that\nshare the same true land type.")
    print()
    bad_split = split_list(badlist, 5)
    for eric, allen in enumerate(bad_split):
        bad_split[eric] = str(allen).replace("[", " ")
        bad_split[eric] = str(allen).replace("]", " ")
        print("\t", allen)
