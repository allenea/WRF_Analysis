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
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import cartopy.feature as cfeature
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from commonclass.namelist_plot import wps_info

def plot_data(pwrf, pgrid, gridded_data, lon_pts, lat_pts):
    """plot_data: Plot the data

    Input:
        pwrf -- (class) ModelData
        pgrid -- class AnalysisGrid
        gridded_data -- (masked-array) frontal strength values
        lon_pts -- (list) Longitude points of front
        lat_pts -- (list) Latitude points of front
    Output:
        Optional: Save Figure
        None
    """
    ## Get/Store WPS Data - recreate the domain
    wps = wps_info(pwrf.wpsfile)

    ## SET UP PLOT
    fig1 = plt.figure(figsize=[8, 8], dpi=100)
    ax1 = plt.axes(projection=wps.calc_wps_domain_info()[0]) #wpsproj - namelist.wps

    ax1.set_title("WRFv4 "+ pwrf.version +" Frontal Strength\nTime: "+\
                  pwrf.wrf_dt[pwrf.time_idx].strftime("%Y-%m-%d %H:%M")+"Z",\
                  size=20)

    #Plot the front threshold data (after it's been cleaned)
    plt1 = plt.pcolormesh(pwrf.lons[pgrid.south_start:pgrid.north_end,\
                                  pgrid.west_start:pgrid.east_end-pgrid.gradient_distance],\
                        pwrf.lats[pgrid.south_start:pgrid.north_end,\
                                  pgrid.west_start:pgrid.east_end-pgrid.gradient_distance],\
                        gridded_data[pgrid.south_start:pgrid.north_end,\
                                     pgrid.west_start:pgrid.east_end-pgrid.gradient_distance],\
                        cmap='jet', vmin=pgrid.threshold, vmax=3, transform=ccrs.PlateCarree())

    plt1.cmap.set_under("white")

    #plot the front points
    for ijk in range(len(lon_pts)):
        ax1.plot(lon_pts[ijk], lat_pts[ijk], 'rp', markersize=4, transform=ccrs.PlateCarree())

    #Add map layers for counties/states/coastlines/etc.
    try:
        reader = shpreader.Reader(os.getcwd()+'/countyl010g_shp_nt00964/countyl010g.shp')
        counties = list(reader.geometries())
        obj_counties = cfeature.ShapelyFeature(counties, ccrs.PlateCarree())
        ax1.add_feature(obj_counties, facecolor='none', edgecolor='darkslategray')
    except ImportError:
        ax1.add_feature(cartopy.feature.STATES.with_scale('10m'),\
                          edgecolor='darkslategray', linewidth=1)
        ax1.coastlines('10m', 'darkslategray', linewidth=1)

    # Set/Add colorbar
    cbar_ax = fig1.add_axes([0, 0, 0.1, 0.1])
    posn = ax1.get_position()
    cbar_ax.set_position([posn.x0 + posn.width + 0.01, posn.y0, 0.04, posn.height])
    plt.colorbar(plt1, cax=cbar_ax, extend='min')

    if pwrf.save:
        plt.savefig(pwrf.mappath+"/Frontal_Strength_Analysis_"+\
                    pwrf.wrf_dt[pwrf.time_idx].strftime("%Y_%m_%d_%H%M")+\
                    "_"+pwrf.version+".png", transparent=True, dpi=600)
    else:
        plt.show()

    plt.close()
