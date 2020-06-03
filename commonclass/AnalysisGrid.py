"""Copyright (C) 2018-Present E. Allen, D. Moore, D. Veron - University of Delaware"""
#
# You may use, distribute and modify this code under the
# terms of the GNU Lesser General Public License v3.0 license.
#
# https://www.gnu.org/licenses/lgpl-3.0.en.html
#
# Imports
from __future__ import print_function

class AnalysisGrid:
    """
    Developed by Eric Allen, University of Delaware

    Set grid you wish to use here.

    """
    def __init__(self,\
                 vertlvl,\
                 resolution,\
                 cellsize,\
                 gradientdx,\
                 westpt,\
                 eastpt,\
                 southpt,\
                 northpt,\
                 threshold_value,\
                 min_pixel_area):

        """
        grid.level = vertlvl
        grid.dx_1 = resolution
        grid.cell_size = cellsize
        grid.gradient_distance = gradientdx
        grid.west_start = westpt
        grid.east_end = eastpt
        grid.south_start = southpt
        grid.north_end = northpt
        grid.threshold = threshold_value
        grid.filter_area = min_pixel_area
        """
        self.set_level(vertlvl)
        self.set_horizontal_resolution(resolution)
        self.set_cell_size(cellsize)
        self.set_nuggetsize()
        self.set_gradient_distance(gradientdx)
        self.set_westpt(westpt)
        self.set_eastpt(eastpt)
        self.set_southpt(southpt)
        self.set_northpt(northpt)
        self.set_threshold(threshold_value)
        self.set_filterarea(min_pixel_area)

    @classmethod
    def set_level(cls, number):
        """setter"""
        cls.level = number

    @classmethod
    def set_horizontal_resolution(cls, number):
        """setter"""
        cls.dx_1 = number

    @classmethod
    def set_cell_size(cls, number):
        """setter"""
        cls.cell_size = number

    @classmethod
    def set_nuggetsize(cls):
        """setter"""
        cls.nugget = (cls.cell_size* 2) + 1

    @classmethod
    def set_gradient_distance(cls, number):
        """setter"""
        cls.gradient_distance = number

    @classmethod
    def set_westpt(cls, number):
        """setter"""
        cls.west_start = number

    @classmethod
    def set_eastpt(cls, number):
        """setter"""
        cls.east_end = number

    @classmethod
    def set_southpt(cls, number):
        """setter"""
        cls.south_start = number

    @classmethod
    def set_northpt(cls, number):
        """setter"""
        cls.north_end = number

    @classmethod
    def set_threshold(cls, number):
        """setter"""
        cls.threshold = number

    @classmethod
    def set_filterarea(cls, number):
        """setter"""
        cls.filter_area = number

    @classmethod
    def print_info(cls):
        """Print the Detection Info from the namelist file"""
        print("Grid Information")
        print("----------------")
        print("Model Level: ", cls.level)
        print("Model Resolution: ", cls.dx_1)
        print("Cell Size: ", cls.cell_size)
        print("Nugget Size: ", cls.nugget, " by ", cls.nugget)
        print("Gradient Distance: ", cls.gradient_distance)
        print()
        print("West-Starting Grid Point: ", cls.west_start)
        print("East-Ending Grid Point: ", cls.east_end)
        print("South-Starting Grid Point: ", cls.south_start)
        print("North-Ending Grid Point: ", cls.north_end)
        print()
        print("Minimum Threshold Value: ", cls.threshold)
        print("Minimum Pixel Area - per Cluster: ", cls.filter_area)
        print()
        print()
