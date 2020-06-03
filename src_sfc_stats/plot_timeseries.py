"""Copyright (C) 2018-Present E. Allen, D. Veron - University of Delaware"""
#
# You may use, distribute and modify this code under the
# terms of the GNU Lesser General Public License v3.0 license.
#
# https://www.gnu.org/licenses/lgpl-3.0.en.html
#
# Imports
from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np

def make_plot(fig_outfile, variable, df1, stat_type, header):
    """Make a time-series plot of the given statistic over time"""
    ## PLOT ERROR BY CASE BY HOUR
    _, ax1 = plt.subplots(figsize=(14, 8))
    colors = ['black', "gray", 'orange', 'green', 'blue', 'purple', 'magenta',\
              'red', 'green', 'blue', 'purple', 'magenta', 'teal']
                # Put new color at the front if including NARR run
    colorcount = 0
    for row in np.array(df1):
        if "SST" in row[0] or "NDA" in row[0]:
            ax1.plot(header[1:-1], row[1:-1], color=colors[colorcount], marker="o",\
                     markeredgecolor='black', label=row[0])
        elif "Average" in row[0]:
            ax1.plot(header[1:-1], row[1:-1], color=colors[colorcount], label=row[0])
        else:
            ax1.plot(header[1:-1], row[1:-1], color=colors[colorcount],\
                     marker="d", label=row[0])
        colorcount += 1
    ax1.set_title(stat_type+" for All Configurations\n"+\
                  variable.replace("_", " "), fontsize=18, fontweight='bold')

    ax1.legend(loc='center left', bbox_to_anchor=(1, 0.65), numpoints=1, fontsize=14)
    ax1.set_xticks(header[1:-1][::2])
    ax1.minorticks_on()
    y_ticklst = ["%.1f"%item for item in ax1.get_yticks()]
    ax1.set_yticklabels(y_ticklst, fontsize=16, fontweight='bold')
    ax1.set_xticklabels(header[1:-1:2], fontsize=16, fontweight='bold')
    ax1.set_ylabel(stat_type +" ("+stat_type+")", fontsize=16, fontweight='bold')
    ax1.set_xlabel('Model Hour', fontsize=16, fontweight='bold')
    #plt.gcf().autofmt_xdate()
    plt.savefig(fig_outfile, bbox_inches='tight')
    #plt.show()
    plt.close()
