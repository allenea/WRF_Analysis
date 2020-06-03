"""Copyright (C) 2018-Present E. Allen, D. Veron - University of Delaware"""
#
# You may use, distribute and modify this code under the
# terms of the GNU Lesser General Public License v3.0 license.
#
# https://www.gnu.org/licenses/lgpl-3.0.en.html
#
# Imports
from __future__ import print_function
import sys

def get_substeps(wrf_interval_min, analysis_interval_min):
    """
    Calculates the analysis window. Doesn't go multiple months or years.

    (int) wrf_interval_min:  30
    (int) analysis_interval_min: i.e. 30
    """

    if analysis_interval_min % wrf_interval_min == 0:
        #opposite
        wrf_substeps = analysis_interval_min//wrf_interval_min
        analysis_substeps = 1
    elif wrf_interval_min % analysis_interval_min == 0:
        #opposite
        analysis_substeps = wrf_interval_min//analysis_interval_min
        wrf_substeps = 1
    else:
        sys.exit("Not an even time-step between the data and the model. Exiting get_substep")

    if analysis_interval_min < wrf_interval_min:
        sys.exit("Analysis cannot be more frequent than the WRF interval. Exiting get_substep")

    return wrf_substeps, analysis_substeps
