#!/usr/bin/env python

"""
Wrapper of all climate-indices's [1] related operators.

[1] https://climate-indices.readthedocs.io/en/latest/
"""
# install
# > conda install -c conda-forge nco
# > pip install climate-indices

import tempfile

from enum import Enum
from multiprocessing import Lock
from nco import Nco
from nco import custom as c
from pathlib import Path

import climate_indices.__main__ as ci
import climate_indices.indices as ci_indices

from climate_indices.__main__ import InputType
from climate_indices.compute import Periodicity
from climate_indices.indices import Distribution

from climdex import utils
from climdex.utils import MyEnumMeta
from climdex.bindings.cdobnd import CDOWrapper
from climdex.constants import *

__lock__   = Lock()
__serial__ = 0

# coordinates
class Coord(Enum, metaclass=MyEnumMeta):
    """Enumeration of standard coordinates variables."""
    lat = 'lat'
    lon = 'lon'
    time = 'time'
    x = 'x'
    y = 'y'

# ------------------------------------------------------------------------------
#
class PETEq(Enum, metaclass=MyEnumMeta):
    """
    Enumeration of types of equations to be used fot the Potential Evapotranspiration (PET) index.
    """
    thornthwaite = 'thornthwaite'
    hargreaves = 'hargreaves'

# ------------------------------------------------------------------------------
#
class MP(Enum, metaclass=MyEnumMeta):
    """Enumeration of ci Multi-Processing (MP) configurations."""
    SINGLE = 'single'
    ALL_BUT_ONE = 'all_but_one'
    ALL = 'all'

# ------------------------------------------------------------------------------
#
class CIWrapper:
    """
    Wrapper of the climate_indices (CI) Python package.
    """

    __xy2latlon = {
        Coord.x.value: Coord.lon.value,
        Coord.y.value: Coord.lat.value
    }
    __latlon2xy = {
        Coord.lon.value: Coord.x.value,
        Coord.lat.value: Coord.y.value
    }

    def __init__(self, uid):
        self.LOGGER = utils.get_logger(__name__)
        self.uid = uid

        # nco
        self.__nco__ = Nco(debug=utils.debug_level().value)
        self.NCO_OVWRITE = self.__nco__.OverwriteOperatorsPattern[0] # avoid user-input hanging execution
        self.NCO_NO_HIST = '--hst'

        # cdo
        cdo_logs_dir = Path(DEFAULT_CDO_LOGS_DIR)
        if not cdo_logs_dir.exists():
            self.LOGGER.debug("Creating %s folder.", cdo_logs_dir)
            cdo_logs_dir.mkdir(parents=False, exist_ok=False)
        #
        tempDir = '{}/{}'.format(DEFAULT_CDO_TMP_DIR, uid)
        logFile = Path(cdo_logs_dir, 'cdo_commands_{}.log'.format(uid))
        self.__cdowr__ = CDOWrapper(uid, tempdir=tempDir, logging=True, logFile=str(logFile))

    def __exit__(self, exc_type, exc_value, traceback):
        __lock__.acquire()
        self.LOGGER.debug(f"[{self}] EXIT")
        self.LOGGER.debug(f"[{self}] clean tmp dir")
        # nco
        # clean tmp files TODO
        # cdo
        cdo = self.__cdowr__.__exit__(exc_type, exc_value, traceback)
        __lock__.release()

    def __catch__(self, signum, frame):
        self.LOGGER.debug(f"[{self}] CAUGHT SIGINT")
        # nco
        # clean files? TODO
        # cdo
        self.__cdowr__.__catch__(signum, frame)
        # ...

    def list_all(self):
        """List all avaiable indices."""
        return ci_indices.__all__

    def compute(self,
            index:str, calib_start:int, calib_end:int, ofile_base,
            itemp=None, itemp_var=None,
            iprec=None, iprec_var=None,
            ipet=None,  ipet_var=None,
            scale:int=None, periodicity:Periodicity=None,
            distribution:Distribution=None, eq:PETEq=None,
            multiprocessing:MP=MP.ALL_BUT_ONE,
            dry_run=False, history=False):
        """
        Computes a climate given on an input file.

        Parameters
        ----------
        index : str
            The index to be calculated (see list_all() for a complete list)
        calib_start : int
            Initial year of the calibration period
        calib_end : int
            Final year of the calibration period (inclusive)
        ofile_base : str or Path
            The base name for the output file: index's abbreviation plus a
            month scale (if applicable), connected with underscores, plus the
            '.nc' NetCDF extension (eg. <ofile_base>_spei_12.nc)
        itemp : str or Path
            The input file containing the temperature dataset
        itemp_var : str
            The name of the temperature variable inside the itemp dataset
        iprec : str or Path
            The input file containing the precipitation dataset
        iprec_var : str
            The name of the temperature variable inside the ipr dataset
        ipet : str or Path
            The input file containing the PET dataset (note:
            PET is required by SPEI and Palmers indices, but will be
            automatically computed if not provided)
        ipet_var : str
            The name of the temperature variable inside the ipet dataset
        scale : int
            Time step scales over which the PNP, SPI, and SPEI values are to be computed.
            Required when the index argument is 'spi', 'spei', 'pnp', or 'scaled'
        periodicity : str or Periodicity
            The periodicity of the input dataset files. Valid values are 'monthly' and 'daily'.
            NOTE: Only SPI and PNP support daily inputs
        distribution : str or Distribution
            The distribution used for either the SPI or SPEI indices
        equation : str or PETEq
            The equation used for the PET index calculation
        multiprocessing : str
            Control the parallelism of the computations (either 'single', 'all' or 'all_but_one' CPUs)
        dry_run : bool
            Only show execution flow; do not run.
        history : bool
            whether to include the `history' attribute in the output NetCDF

        Returns
        -------
        The name of the output index file.
        """
        # - - - - - - - - - -
        if index is None or len(index) == 0:
            raise ValueError("A valid index input is mandatory.")

        if index not in self.list_all():
            raise ValueError(f"{index} not valid. Available indices: {self.list_all()}")

        if calib_start > calib_end:
            raise ValueError(f"Calibration start year {calib_start} must be prior to end year {calib_end}.")

        if ofile_base is None or len(str(ofile_base)) == 0:
            raise ValueError("ofile_base argument shall not be empty.")

        # input files dict
        ifiles = {itemp:itemp_var,iprec:iprec_var, ipet:iprec_var}

        if all(ifile is None for ifile in ifiles):
            raise ValueError("Please provide at least 1 input file.")

        if any(ifile is not None and var_name is None for ifile, var_name in ifiles.items()):
            raise ValueError("Please provide variable name for given input file(s).")

        if type(periodicity) == str:
            try:
                periodicity = Periodicity.from_string(periodicity)
            except:
                raise ValueError("Illegal periodicity '%s'. Allowed values: %s",
                        periodicity, Periodicity._member_names_)

        if type(distribution) == str:
            try:
                distribution = Distribution[distribution]
            except:
                raise ValueError("Illegal distribution '%s'. Allowed values: %s",
                        distribution, Distribution._member_names_)

        if type(eq) == str:
            try:
                eq = PETEq[eq]
            except:
                raise ValueError("Illegal equation '%s'. Allowed values: %s",
                        eq, PETEq._member_names_)

        if not multiprocessing in MP:
            raise ValueError("Invalid multiprocessing parameter '{}'. Valid values: {}"
                    .format(multiprocessing, MP.values()))
        # - - - - - - - - - -

        tmp_files = list()

        try:
            #
            # prepare all inputs (xyt dimensions order)
            #
            self.LOGGER.debug("Preparing input file(s)...")

            # discard None input files
            ifiles = {ifile:var_name for (ifile,var_name) in ifiles.items() if ifile is not None}
            # var:ifile dictionaries
            ifiles_ok = dict.fromkeys([itemp_var, iprec_var, ipet_var])

            dims_rearranged = False

            # convert to mandatory dimensions order to (lat, lon, time) :
            for ifile, var_name in ifiles.items():
                if dry_run:
                    self.LOGGER.info("Preparing input file '%s'...", ifile)
                    ifiles_ok[var_name] = ifile
                else:
                    self.LOGGER.debug("Preparing input file '%s'...", ifile)
                    ## prepare ifile ######################
                    #ifile_ok = ci._prepare_file(ifile, var_name) -> I can control more NCO options:
                    ifile_ok = self.__nco__.ncpdq(input=ifile, options=[f'-a "lat,lon,time"', self.NCO_OVWRITE, self.NCO_NO_HIST])
                    dims_rearranged     = (ifile_ok != ifile)
                    ifiles_ok[var_name] = ifile_ok
                    #######################################
                    if dims_rearranged:
                        self.LOGGER.debug("Input file re-arranged for index calculation: '%s'", ifile_ok)
                        tmp_files.append(ifile_ok)

            # layout input args
            #    [!] NOTE
            #    'None' input arg triggers error! It searches for None input and fails.
            #    Absent input shall be absent from kwargs!
            ci_input_dict = {}
            for var_name, ifile in ifiles_ok.items():
                if var_name is None:
                    continue
                if var_name == iprec_var:
                    ci_input_dict['netcdf_precip']   = ifile
                    ci_input_dict['var_name_precip'] = var_name
                elif var_name == itemp_var:
                    ci_input_dict['netcdf_temp']     = ifile
                    ci_input_dict['var_name_temp']   = var_name
                elif var_name == ipet_var:
                    ci_input_dict['netcdf_pet']      = ifile
                    ci_input_dict['var_name_pet']    = var_name
                else:
                    raise RuntimeError("Unrecognized variable: %s", var_name)

            # compute PET on SPEI if missing:
            if index == 'spei' and ipet is None:
                kwargs = {
                     **ci_input_dict,
                     "index": 'pet', # <<<<<<<< PET index
                     "input_type":  InputType.grid,
                     "scale": scale,
                     "distribution": distribution,
                     "periodicity": periodicity,
                     "calibration_start_year": calib_start,
                     "calibration_end_year": calib_end,
                     "output_file_base": '{}_pet'.format(str(ofile_base)),
                     'multiprocessing': multiprocessing
                }
                if dry_run:
                    self.LOGGER.info("ci._compute_write_index(%s)", kwargs)
                    ci_input_dict['netcdf_pet']   = 'tmp_pet.nc'
                    ci_input_dict['var_name_pet'] = 'pet'
                else:
                    ## compute PET ########################
                    self.LOGGER.debug("Spawn %s PET computation (%s)", index, kwargs)
                    pet_ifile, pet_var_name = ci._compute_write_index(kwargs)
                    #######################################
                    ci_input_dict['netcdf_pet']   = pet_ifile
                    ci_input_dict['var_name_pet'] = pet_var_name
                    tmp_files.append(pet_ifile)

            # compute
            kwargs = {
                 **ci_input_dict,
                 "index": index,
                 "input_type":  InputType.grid, # TODO not fixed
                 "scale": scale,
                 "distribution": distribution,
                 "periodicity": periodicity,
                 "calibration_start_year": calib_start,
                 "calibration_end_year": calib_end,
                 "output_file_base": str(ofile_base),
                 'multiprocessing': multiprocessing
            }
            if dry_run:
                self.LOGGER.info("ci._compute_write_index(%s)", kwargs)
                ofile = str(ofile_base)
            else:
                ## compute index ######################
                self.LOGGER.debug("Spawn %s index computation (%s)", index, kwargs)
                ofile, ovar_name = ci._compute_write_index(kwargs)
                #######################################

            if dims_rearranged:
                if dry_run:
                    self.LOGGER.info("nco ncpdq %s %s -a \"time,lat,lon\"", self.NCO_OVWRITE, self.NCO_NO_HIST)
                else:
                    # restore coordinates input dims arrangement
                    ofile_tlatlon = self.__nco__.ncpdq(input=ofile, options=[f'-a "time,lat,lon"',
                        self.NCO_OVWRITE, self.NCO_NO_HIST])
                    self.LOGGER.debug("Input file re-arranged to CF convention: '%s'", ofile_tlatlon)
                    #
                    tmp_files.append(ofile)
                    ofile = ofile_tlatlon

        finally:
            for f in tmp_files:
                f = Path(f)
                if f.exists():
                    self.LOGGER.debug(f"Deleting tmp file: {f}")
                    f.unlink(missing_ok=True)
            tmp_files.clear()

        return ofile


# == SPI ==================================================================================================================

# monthly resolution + reprojection
# > cdo --timestat_date first --no_history -O --timestat_date first monsum pr.nc pr_monthly.nc
# > cdo griddes pr_monthly.nc
#
# gridID 1
#
#    gridtype  = projection
#    gridsize  = 29929
#    xsize     = 173
#    ysize     = 173
#    xname     = x
#    xlongname = "x coordinate of projection"
#    xunits    = "m"
#    yname     = y
#    ylongname = "y coordinate of projection"
#    yunits    = "m"
#    xfirst    = 4344390.93180395
#    xinc      = 1000
#    yfirst    = 2500757.63356769
#    yinc      = 1000
#    grid_mapping = lambert_azimuthal_equal_area
#    grid_mapping_name = lambert_azimuthal_equal_area
#    long_name = "CRS definition"
#    false_easting = 4321000.
#    false_northing = 3210000.
#    latitude_of_projection_origin = 52.
#    longitude_of_projection_origin = 10.
#    longitude_of_prime_meridian = 0.
#    semi_major_axis = 6378137.
#    inverse_flattening = 298.257222101
#    spatial_ref = 'PROJCS["unknown",GEOGCS["unknown",DATUM["Unknown_based_on_GRS80_ellipsoid",SPHEROID["GRS 1980",6378137,298.257222101004,AUTHORITY["EPSG","7019"]]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]]],PROJECTION["Lambert_Azimuthal_Equal_Area"],PARAMETER["latitude_of_center",52],PARAMETER["longitude_of_center",10],PARAMETER["false_easting",4321000],PARAMETER["false_northing",3210000],UNIT["metre",1],AXIS["Easting",EAST],AXIS["Northing",NORTH]]'
#    GeoTransform = "4343891 1000 0 2673258 0 -1000"

# define latlon grid
# > gdalwarp -s_srs '+proj=laea +lat_0=52 +lon_0=10 +x_0=4321000 +y_0=3210000 +ellps=GRS80 +units=m +no_defs' -t_srs epsg:4326 \
#         /mnt/CEPH_PROJECTS/FACT_CLIMAX/CORDEX-Adjust/QDM/land_mask/southtyrol_all_land.nc \
#         /mnt/CEPH_PROJECTS/FACT_CLIMAX/CORDEX-Adjust/QDM/land_mask/southtyrol_all_land_wgs84.nc
# > gdalinfo /mnt/CEPH_PROJECTS/FACT_CLIMAX/CORDEX-Adjust/QDM/land_mask/southtyrol_all_land_wgs84.nc [...]
# > dc <<< '7k 12.5808876 10.2930560 - 173 /p'
# .0132244
# > dc <<< '7k 47.1724653 45.5843104 - 173 /p'
# .0091800
# > cat  /mnt/CEPH_PROJECTS/FACT_CLIMAX/CORDEX-Adjust/QDM/hgrids/southtyrol_wgs84.grid
# gridtype = lonlat
# xsize    = 173
# ysize    = 173
# xfirst   = 10.2930560
# xinc     = 0.0132244
# yfirst   = 45.5843104
# yinc     = 0.0091800

# > cdo --no_history -O setgrid,southtyrol_wgs84.grid pr_monthly.nc pr_monthly_latlongrid.nc
# > process_climate_indices \
#        --index spi \
#        --periodicity monthly --scales 12 \
#        --netcdf_precip pr_monthly_latlongrid.nc \
#        --var_name_precip pr \
#        --output_file_base pr_monthly_latlongrid \
#        --calibration_start_year 1981 --calibration_end_year 2010 \
#        --multiprocessing all_but_one

# cdo/CF compatible order: time,lat,lon:
# > ncpdq -a time,lat,lon -O --output=pr_monthly_latlongrid_spi_gamma_12.nc pr_monthly_latlongrid_spi_gamma_12.nc

# restore original hgrid:
# > cdo --no_history -O setgrid,southtyrol_laea.grid pr_monthly_latlongrid_spi_gamma_12.nc pr_monthly_spi_gamma_12.nc
def compute_spi():

    cdo = Cdo()
    pr  = 'pr_EUR-11_IPSL-IPSL-CM5A-MR_IPSL-WRF381P_r1i1p1_v1_day_19702100_rcp45.nc'
    mon_file = cdo.chname('x,lon,y,lat', input=f'-monsum {pr}', opts=[ '--timestat_date first' ])

    # rearrange dimensions:
    nco = Nco()
    dims='lat,lon,time'
    arr_mon_file = nco.ncpdq(input=netcdf_precip, options=[f'-a "{dims}"', "-O"])

    # keyword arguments used for the SPI function
    netcdf_precip = arr_mon_file
    var_name_precip = 'pr'
    input_type = InputType.grid
    scale = 12
    dist = Distribution.gamma
    periodicity = Periodicity.monthly
    calibration_start_year = 1981
    calibration_end_year = 2010
    output_file_base = 'pr_python_monthly'

    kwargs = {"index": "spi",
             "netcdf_precip": netcdf_precip,
             "var_name_precip": var_name_precip,
             "input_type": input_type,
             "scale": scale,
             "distribution": dist,
             "periodicity": periodicity,
             "calibration_start_year": calibration_start_year,
             "calibration_end_year": calibration_end_year,
             "output_file_base": output_file_base
    }

    # compute and write SPI
    res = ci._compute_write_index(kwargs)

    # re-arrange back to time,x,y
    arr_spi_file = res[0]
    dims='time,lat,lon'
    spi_file = nco.ncpdq(input=arr_spi_file, options=[f'-a "{dims}"', "-O"])
    ofile = '$CLIMAX/CORDEX-Adjust/INDICES/spi12/{scenario}/spi12_EUR-11_IPSL-IPSL-CM5A-MR_IPSL-WRF381P_r1i1p1_v1_day_19702100_rcp45.nc'
    cdo.chname('lon,x,lat,y', input=f'-monsum {spi_file}', output=ofile, opts=[ '--timestat_date first' ])









#== SPEI ==================================================================================================================

# (preprocess SPI [...] plus:)
# cdo --no_history -O --timestat_date first --no_history -O setunit,"degree_celsius" -monavg tas.nc tas_monthly.nc
# cdo --no_history -O setgrid,southtyrol_wgs84.grid tas_monthly.nc tas_monthly_latlongrid.nc

#### FIX INPUT: tas_$MODEL.$SCENARIO.nc have "tasmin" variable
#### > cdo --no_history -O setname,"tas" tas_monthly_latlongrid.nc ofile.nc
#### > mv ofile.nc tas_monthly_latlongrid.nc

# > process_climate_indices \
#        --index spei \
#        --periodicity monthly --scales 12 \
#        --netcdf_temp tas_monthly_latlongrid.nc \
#        --var_name_temp tas \
#        --netcdf_precip pr_monthly_latlongrid.nc \
#        --var_name_precip pr \
#        --output_file_base taspr_monthly_latlongrid \
#        --calibration_start_year 1981 --calibration_end_year 2010 \
#        --multiprocessing all_but_one

def compute_spei():

    cdo = Cdo()
    nco = Nco()

    pr  =  'pr_EUR-11_IPSL-IPSL-CM5A-MR_IPSL-WRF381P_r1i1p1_v1_day_19702100_rcp45.nc'
    tas = 'tas_EUR-11_IPSL-IPSL-CM5A-MR_IPSL-WRF381P_r1i1p1_v1_day_19702100_rcp45.nc'
    units = {pr:'mm', tas:'degree_celsius'}
    arr_ifile = dict()
    dims='lat,lon,time'

    for ifile in (pr, tas):
        # rename vars
        # like ci._prepare_file but renames x/y to lon/lat first.
        ofile = cdo.chname('x,lon,y,lat', input=f'-setunit,{units[ifile]} -monsum {ifile}', opts=[ '--timestat_date first' ])
        # rearrange dimensions:
        arr_ifile[ifile] = nco.ncpdq(input=ofile, options=[f'-a "{dims}"', "-O"])


    # keyword arguments used for the SPI function
    netcdf_temp = arr_ifile[tas]
    var_name_temp = 'tas'
    netcdf_precip = arr_ifile[pr]
    var_name_precip = 'pr'
    input_type = InputType.grid
    scale = 12
    dist = Distribution.gamma
    periodicity = Periodicity.monthly
    calibration_start_year = 1981
    calibration_end_year = 2010
    output_file_base = 'pr_python_EUR-11_IPSL-IPSL-CM5A-MR_IPSL-WRF381P_r1i1p1_v1_day_19702100_rcp45_monthly'

    kwargs = {"index": "spi",
             "netcdf_precip": netcdf_precip,
             "var_name_precip": var_name_precip,
             "netcdf_temp": netcdf_temp,
             "var_name_temp": var_name_temp,
             "input_type": input_type,
             "scale": scale,
             "distribution": dist,
             "periodicity": periodicity,
             "calibration_start_year": calibration_start_year,
             "calibration_end_year": calibration_end_year,
             "output_file_base": output_file_base
    }

    # compute and write SPI
    res = ci._compute_write_index(kwargs)

    # re-arrange back to time,x,y
    arr_spi_file = res[0]
    dims='time,lat,lon'
    spi_file = nco.ncpdq(input=arr_spi_file, options=[f'-a "{dims}"', "-O"])
    ofile = '$CLIMAX/CORDEX-Adjust/INDICES/spi12/{scenario}/spi12_EUR-11_IPSL-IPSL-CM5A-MR_IPSL-WRF381P_r1i1p1_v1_day_19702100_rcp45.nc'
    cdo.chname('lon,x,lat,y', input=f'-monsum {spi_file}', output=ofile, opts=[ '--timestat_date first' ])


#== xarray ==================================================================================================================

def test_xarray():

    import xarray as xr
    import numpy as np

    netcdf_temp='~/tmp/tas_monthly_latlon.nc'
    netcdf_prec='~/tmp/pr_monthly_latlon.nc'

    netcdf_temp='~/tmp/tas_monthly.nc'
    netcdf_prec='~/tmp/pr_monthly.nc'

    dataset_temp = xr.open_dataset(netcdf_temp)
    dataset_prec = xr.open_dataset(netcdf_prec)

    dataset_temp['tas']
    dataset_prec['pr']

    lats_temp = dataset_temp['lat'].values[:]
    lats_prec = dataset_prec['lat'].values[:]

    np.array_equal(lats_prec, lats_temp)
    np.allclose(lats_prec, lats_temp, atol=0.01)


    # working SPEI
    # monsum [...]
    latlon_grid='/mnt/CEPH_PROJECTS/FACT_CLIMAX/CORDEX-Adjust/QDM/hgrids/southtyrol_wgs84.grid'
    #cdo --timestat_date first -O -setgrid,"$latlon_grid" -chname,x,lon,y,lat ~/tmp/pr_monthly.nc ~/tmp/pr_monthly_latlon.nc
    #cdo --timestat_date first -O -setgrid,"$latlon_grid" -setunit,'celsius' -chname,x,lon,y,lat ~/tmp/tas_monthly.nc ~/tmp/tas_monthly_latlon.nc


