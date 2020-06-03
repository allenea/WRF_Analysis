#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 14:48:46 2020

@author: allenea
"""
from __future__ import print_function
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src_sfc_stats.model_analysis_simple import model_analysis
from src_sfc_stats.time_series_stats import model_analysis_timeseries

def analyze(stats, obs):
    """Select which program should be used"""
    if stats.timeseries == True:
        print("Time-Series Statistics")
        model_analysis_timeseries(stats, obs)
    else:
        print("Traditional Statistics")
        model_analysis(stats, obs)
