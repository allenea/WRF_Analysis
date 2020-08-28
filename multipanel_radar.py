"""Copyright (C) 2018-Present D. Moore, E. Allen, D. Veron - University of Delaware"""
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
import pyart
import nexradaws
import numpy as np
import matplotlib.pyplot as plt
import cartopy
import matplotlib as mpl

def datetime_range(start, finish, minute_interval=60):
    """Loop through a range of dates including first time
    Input:
        start (datetime object) -- Starting time
        finish (datetime object) -- End of analysis
        minute_interval (int) - minutes between analysis time
    Output:
        yield datetime object - analysis time
    """
    yield start
    while finish > start:
        start = start + timedelta(minutes=minute_interval)
        yield start

def get_closest(aim, scan_options):
    """Get closest radar scan to analysis time
    Input:
        aim (datetime object) target time
        scan_options (iterable) radar scans
    Output:
        scan (radar object) closest to target time
    """
    lst = []
    for opt in scan_options:
        newdt = opt.scan_time.replace(tzinfo=None)
        diff = abs(newdt - aim)
        lst.append(diff)
    return scan_options[lst.index(min(lst))]


panels = 9

#Radar Tilt (lowest is 0)
tilt = 0

radar_id = "KDOX"

year_input = "2014"
month_input = "06"
day_input = "07"
hour_input = "18"
minute_input = "00"


datetime_input = datetime(int(year_input), int(month_input), int(day_input),\
                                           int(hour_input), int(minute_input))
#IF single_scan is False THESE NEED TO BE FILLED CORRECTLY
analysis_window_hr = int(panels-1)  # Number of hours to do analysis when doing multiple scans

temporal_frequency = int(60) # Number of minutes

root_dir = os.getcwd()
#Temp location for scans to download then be deleted
#REMINDER TO CREATE A FOLDER WITHIN THE WORKING DIRECTORY
temp_dir = os.path.join(root_dir, "Data", "Radar_Scans")

#Check if temp_scans folder exists.
if not os.path.isdir(temp_dir):
    os.mkdir(temp_dir)

conn = nexradaws.NexradAwsInterface()
#Establish location of radar
loc = pyart.io.nexrad_common.get_nexrad_location(radar_id)

#Coordinates of radar system used
lon0 = loc[1]
lat0 = loc[0]

earlier = datetime_input - timedelta(minutes=15)
end_time_window = datetime_input + timedelta(hours=analysis_window_hr)
later = end_time_window + timedelta(minutes=15)

scan = []
#Get scans for day
try:
    scans = conn.get_avail_scans_in_range(earlier, later, radar_id)
except:
    sys.exit("No Scans Found On This Day")

#For analyzing until 23:59UTC ~sundown.
target_dates = list(datetime_range(datetime_input, end_time_window, temporal_frequency))
print("Target Dates: ", target_dates)

for time in target_dates:
    scan.append(get_closest(time, scans))

#Download Files:
results = conn.download(scan, temp_dir)

#If no scans are found for the given date:
if len(results.success) == 0:
    sys.exit("No data found for selected date.")

#set up the plotting settings
cmap = "pyart_NWSRef"
levs = np.linspace(0, 80, 41, endpoint=True)
ticks = np.linspace(0, 80, 9, endpoint=True)

#normalize the colormap based on the LEVELs provided above
norm = mpl.colors.BoundaryNorm(levs, 256)


for i, scan in enumerate(results.iter_success(), start=1):
    try:
        radar = scan.open_pyart()
        lats = radar.gate_latitude
        lons = radar.gate_longitude

        min_lat = lats['data'].min()
        max_lat = lats['data'].max()
        #print(max_lat, min_lat)

    except:
        print("FAILED SCAN: ", i, scan)
        continue

    print(i)
    if i == 1:
        timestamp1 = radar.time['units'].split(' ')[-1].split('T')
        timestamp1 = timestamp1[0] + ' ' + timestamp1[1][:-1]
        display1 = pyart.graph.RadarMapDisplay(radar)
    elif i == 2:
        timestamp2 = radar.time['units'].split(' ')[-1].split('T')
        timestamp2 = timestamp2[0] + ' ' + timestamp2[1][:-1]
        display2 = pyart.graph.RadarMapDisplay(radar)
    elif i == 3:
        timestamp3 = radar.time['units'].split(' ')[-1].split('T')
        timestamp3 = timestamp3[0] + ' ' + timestamp3[1][:-1]
        display3 = pyart.graph.RadarMapDisplay(radar)
    elif i == 4:
        timestamp4 = radar.time['units'].split(' ')[-1].split('T')
        timestamp4 = timestamp4[0] + ' ' + timestamp4[1][:-1]
        display4 = pyart.graph.RadarMapDisplay(radar)
    elif i == 5:
        timestamp5 = radar.time['units'].split(' ')[-1].split('T')
        timestamp5 = timestamp5[0] + ' ' + timestamp5[1][:-1]
        display5 = pyart.graph.RadarMapDisplay(radar)
    elif i == 6:
        timestamp6 = radar.time['units'].split(' ')[-1].split('T')
        timestamp6 = timestamp6[0] + ' ' + timestamp6[1][:-1]
        display6 = pyart.graph.RadarMapDisplay(radar)
    elif i == 7:
        timestamp7 = radar.time['units'].split(' ')[-1].split('T')
        timestamp7 = timestamp7[0] + ' ' + timestamp7[1][:-1]
        display7 = pyart.graph.RadarMapDisplay(radar)
    elif i == 8:
        timestamp8 = radar.time['units'].split(' ')[-1].split('T')
        timestamp8 = timestamp8[0] + ' ' + timestamp8[1][:-1]
        display8 = pyart.graph.RadarMapDisplay(radar)
    elif i == 9:
        timestamp9 = radar.time['units'].split(' ')[-1].split('T')
        timestamp9 = timestamp9[0] + ' ' + timestamp9[1][:-1]
        display9 = pyart.graph.RadarMapDisplay(radar)
    elif i == 10:
        timestamp10 = radar.time['units'].split(' ')[-1].split('T')
        timestamp10 = timestamp10[0] + ' ' + timestamp10[1][:-1]
        display10 = pyart.graph.RadarMapDisplay(radar)
    elif i == 11:
        timestamp11 = radar.time['units'].split(' ')[-1].split('T')
        timestamp11 = timestamp11[0] + ' ' + timestamp11[1][:-1]
        display11 = pyart.graph.RadarMapDisplay(radar)
    elif i == 12:
        timestamp12 = radar.time['units'].split(' ')[-1].split('T')
        timestamp12 = timestamp12[0] + ' ' + timestamp12[1][:-1]
        display12 = pyart.graph.RadarMapDisplay(radar)
    else:
        timestamp13 = radar.time['units'].split(' ')[-1].split('T')
        timestamp13 = timestamp13[0] + ' ' + timestamp13[1][:-1]
        display13 = pyart.graph.RadarMapDisplay(radar)

projection = cartopy.crs.Mercator(
                central_longitude=lon0,
                min_latitude=min_lat, max_latitude=max_lat)

if panels == 6:
     myfig, ((ax1, ax2, ax3), (ax4, ax5, ax6))  = plt.subplots(2, 3,
                                 figsize=[20,20],
                                 subplot_kw = {'projection':projection})

elif panels == 9:
    myfig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9))  = plt.subplots(3, 3,
                                 figsize=[20,20],
                                 subplot_kw = {'projection':projection})

elif panels == 12:
    myfig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9), (ax10, ax11, ax12))  = plt.subplots(4, 3,
                                 figsize=[20,20],
                                 subplot_kw = {'projection':projection})

else:
    myfig, ((ax1, ax2, ax3), (ax4, ax5, ax6))  = plt.subplots(2, 3,
                                 figsize=[20,20],
                                 subplot_kw = {'projection':projection})
# Display Data
display1.plot_ppi_map('reflectivity', tilt, vmin=0, vmax=60,\
                     min_lon=-77, max_lon=-73.8, min_lat=37, max_lat=40.25,\
                     lon_lines=np.arange(-180, 0, 1), resolution='10m',\
                     lat_lines=np.arange(0, 90, 1), projection=projection,\
                     lat_0=radar.latitude['data'][0],\
                     lon_0=radar.longitude['data'][0],\
                     title_flag=True,\
                     title=timestamp1,
                     colorbar_flag=True, ticks=ticks,\
                     colorbar_label="",\
                     cmap=cmap, norm=norm, ax=ax1)

# Display Data
display2.plot_ppi_map('reflectivity', tilt, vmin=0, vmax=60,\
                     min_lon=-77, max_lon=-73.8, min_lat=37, max_lat=40.25,\
                     lon_lines=np.arange(-180, 0, 1), resolution='10m',\
                     lat_lines=np.arange(0, 90, 1), projection=projection,\
                     lat_0=radar.latitude['data'][0],\
                     lon_0=radar.longitude['data'][0],\
                     title_flag=True,\
                     title=timestamp2,
                     colorbar_flag=True, ticks=ticks,\
                     colorbar_label="",\
                     cmap=cmap, norm=norm, ax=ax2)

# Display Data
display3.plot_ppi_map('reflectivity', tilt, vmin=0, vmax=60,\
                     min_lon=-77, max_lon=-73.8, min_lat=37, max_lat=40.25,\
                     lon_lines=np.arange(-180, 0, 1), resolution='10m',\
                     lat_lines=np.arange(0, 90, 1), projection=projection,\
                     lat_0=radar.latitude['data'][0],\
                     lon_0=radar.longitude['data'][0],\
                     title_flag=True,\
                     title=timestamp3,
                     colorbar_flag=True, ticks=ticks,\
                     colorbar_label="",\
                     cmap=cmap, norm=norm, ax=ax3)

# Display Data
display4.plot_ppi_map('reflectivity', tilt, vmin=0, vmax=60,\
                     min_lon=-77, max_lon=-73.8, min_lat=37, max_lat=40.25,\
                     lon_lines=np.arange(-180, 0, 1), resolution='10m',\
                     lat_lines=np.arange(0, 90, 1), projection=projection,\
                     lat_0=radar.latitude['data'][0],\
                     lon_0=radar.longitude['data'][0],\
                     title_flag=True,\
                     title=timestamp4,
                     colorbar_flag=True, ticks=ticks,\
                     colorbar_label="",\
                     cmap=cmap, norm=norm, ax=ax4)

# Display Data
display5.plot_ppi_map('reflectivity', tilt, vmin=0, vmax=60,\
                     min_lon=-77, max_lon=-73.8, min_lat=37, max_lat=40.25,\
                     lon_lines=np.arange(-180, 0, 1), resolution='10m',\
                     lat_lines=np.arange(0, 90, 1), projection=projection,\
                     lat_0=radar.latitude['data'][0],\
                     lon_0=radar.longitude['data'][0],\
                     title_flag=True,\
                     title=timestamp5,
                     colorbar_flag=True, ticks=ticks,\
                     colorbar_label="",\
                     cmap=cmap, norm=norm, ax=ax5)

# Display Data
display6.plot_ppi_map('reflectivity', tilt, vmin=0, vmax=60,\
                     min_lon=-77, max_lon=-73.8, min_lat=37, max_lat=40.25,\
                     lon_lines=np.arange(-180, 0, 1), resolution='10m',\
                     lat_lines=np.arange(0, 90, 1), projection=projection,\
                     lat_0=radar.latitude['data'][0],\
                     lon_0=radar.longitude['data'][0],\
                     title_flag=True,\
                     title=timestamp6,
                     colorbar_flag=True, ticks=ticks,\
                     colorbar_label="",\
                     cmap=cmap, norm=norm, ax=ax6)
if panels > 6:
    # Display Data
    display7.plot_ppi_map('reflectivity', tilt, vmin=0, vmax=60,\
                         min_lon=-77, max_lon=-73.8, min_lat=37, max_lat=40.25,\
                         lon_lines=np.arange(-180, 0, 1), resolution='10m',\
                         lat_lines=np.arange(0, 90, 1), projection=projection,\
                         lat_0=radar.latitude['data'][0],\
                         lon_0=radar.longitude['data'][0],\
                         title_flag=True,\
                         title=timestamp7,
                         colorbar_flag=True, ticks=ticks,\
                         colorbar_label="",\
                         cmap=cmap, norm=norm, ax=ax7)

    # Display Data
    display8.plot_ppi_map('reflectivity', tilt, vmin=0, vmax=60,\
                         min_lon=-77, max_lon=-73.8, min_lat=37, max_lat=40.25,\
                         lon_lines=np.arange(-180, 0, 1), resolution='10m',\
                         lat_lines=np.arange(0, 90, 1), projection=projection,\
                         lat_0=radar.latitude['data'][0],\
                         lon_0=radar.longitude['data'][0],\
                         title_flag=True,\
                         title=timestamp8,
                         colorbar_flag=True, ticks=ticks,\
                         colorbar_label="",\
                         cmap=cmap, norm=norm, ax=ax8)

    # Display Data
    display9.plot_ppi_map('reflectivity', tilt, vmin=0, vmax=60,\
                         min_lon=-77, max_lon=-73.8, min_lat=37, max_lat=40.25,\
                         lon_lines=np.arange(-180, 0, 1), resolution='10m',\
                         lat_lines=np.arange(0, 90, 1), projection=projection,\
                         lat_0=radar.latitude['data'][0],\
                         lon_0=radar.longitude['data'][0],\
                         title_flag=True,\
                         title=timestamp9,
                         colorbar_flag=True, ticks=ticks,\
                         colorbar_label="",\
                         cmap=cmap, norm=norm, ax=ax9)


if panels > 9:
    # Display Data
    display10.plot_ppi_map('reflectivity', tilt, vmin=0, vmax=60,\
                         min_lon=-77, max_lon=-73.8, min_lat=37, max_lat=40.25,\
                         lon_lines=np.arange(-180, 0, 1), resolution='10m',\
                         lat_lines=np.arange(0, 90, 1), projection=projection,\
                         lat_0=radar.latitude['data'][0],\
                         lon_0=radar.longitude['data'][0],\
                         title_flag=True,\
                         title=timestamp10,
                         colorbar_flag=True, ticks=ticks,\
                         colorbar_label="",\
                         cmap=cmap, norm=norm, ax=ax10)

    # Display Data
    display11.plot_ppi_map('reflectivity', tilt, vmin=0, vmax=60,\
                         min_lon=-77, max_lon=-73.8, min_lat=37, max_lat=40.25,\
                         lon_lines=np.arange(-180, 0, 1), resolution='10m',\
                         lat_lines=np.arange(0, 90, 1), projection=projection,\
                         lat_0=radar.latitude['data'][0],\
                         lon_0=radar.longitude['data'][0],\
                         title_flag=True,\
                         title=timestamp11,
                         colorbar_flag=True, ticks=ticks,\
                         colorbar_label="",\
                         cmap=cmap, norm=norm, ax=ax11)

    # Display Data
    display12.plot_ppi_map('reflectivity', tilt, vmin=0, vmax=60,\
                         min_lon=-77, max_lon=-73.8, min_lat=37, max_lat=40.25,\
                         lon_lines=np.arange(-180, 0, 1), resolution='10m',\
                         lat_lines=np.arange(0, 90, 1), projection=projection,\
                         lat_0=radar.latitude['data'][0],\
                         lon_0=radar.longitude['data'][0],\
                         title_flag=True,\
                         title=timestamp12,
                         colorbar_flag=True, ticks=ticks,\
                         colorbar_label="",\
                         cmap=cmap, norm=norm, ax=ax12)
if panels >= 9:
    plt.subplots_adjust(wspace=-0.25, hspace=0.25)

#Save File
plt.savefig('Radar_'+str(panels)+'P_'+radar_id+'_'+timestamp1.replace(" ", "_")+'_'+str(i)+'.png', dpi=100)
plt.close()
#plt.show()


"""
reader = shpreader.Reader(os.path.abspath("")+'/countyl010g_shp_nt00964/countyl010g.shp')
counties = list(reader.geometries())
obj_counties = cfeature.ShapelyFeature(counties, projection)

#ADD PROJECTIONS
ax = fig.add_subplot(224, projection=projection)

fig = plt.figure(figsize=(10, 10))

ax = fig.add_subplot(221)
display1.plot('reflectivity', tilt, vmin=0, vmax=60,\
                             title_flag=True,\
                             title=timestamp1,\
                             axislabels=('W-E (km)', ' S-N (km)'),\
                             colorbar_flag=True, ticks=ticks,\
                             colorbar_label="",\
                             cmap=cmap, norm=norm, ax=ax)


display1.set_limits((-100, 100), (-100, 100), ax=ax)

ax = fig.add_subplot(222)
display2.plot('reflectivity', tilt, vmin=0, vmax=60,\
                             title_flag=True,\
                             title=timestamp2,\
                             axislabels=('W-E (km)', ' S-N (km)'),\
                             colorbar_flag=True, ticks=ticks,\
                             colorbar_label="",\
                             cmap=cmap, norm=norm, ax=ax)
display2.set_limits((-100, 100), (-100, 100), ax=ax)

ax = fig.add_subplot(223)
display3.plot('reflectivity', tilt, vmin=0, vmax=60,\
                             title_flag=True,\
                             title=timestamp3,\
                             axislabels=('W-E (km)', ' S-N (km)'),\
                             colorbar_flag=True, ticks=ticks,\
                             colorbar_label="",\
                             cmap=cmap, norm=norm, ax=ax)
display3.set_limits((-100, 100), (-100, 100), ax=ax)

ax = fig.add_subplot(224)
display4.plot('reflectivity', tilt, vmin=0, vmax=60,\
                             title_flag=True,\
                             title=timestamp4,\
                             axislabels=('W-E (km)', ' S-N (km)'),\
                             colorbar_flag=True, ticks=ticks,\
                             colorbar_label="",\
                             cmap=cmap, norm=norm, ax=ax)
display4.set_limits((-100, 100), (-100, 100), ax=ax)

plt.show()
sys.exit(0)
"""