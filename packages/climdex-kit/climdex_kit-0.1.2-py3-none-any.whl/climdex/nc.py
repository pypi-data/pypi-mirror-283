#!/usr/bin/env python

"""
Constants and utils related to NetCDF file format.
"""

# constants
NETCDF_EXT=".nc"
NETCDF_RGX="*.nc"

# naming scheme of input NetCDFs file names
NETCDF_NAMING_SCHEME= '^({0})_({1})_({2})_({3})({4})_({5})_?({6}).nc$'
#                         |     |     |     |    |     |      |-extra txt (optional)
#                         |     |     |     |    |     |-scenario
#                         |     |     |     |    |-year end
#                         |     |     |     |-year start
#                         |     |     |-time res
#                         |     |-model name
#                         |-var name
