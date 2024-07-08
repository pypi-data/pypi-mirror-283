#!/usr/bin/env python

"""
Worker that handles climate indices calculated
via 1+ calls to the climate_indices Python package.

See also: https://climate-indices.readthedocs.io/en/latest/
"""

import re

from datetime import datetime
from pathlib import Path

from climate_indices.compute import Periodicity
from climate_indices.indices import Distribution

from climdex import utils
from climdex.bindings.cibnd import CIWrapper, Coord, MP
from climdex.bindings.cdobnd import CDOWrapper
from climdex.constants import *
from climdex.nc import (NETCDF_RGX, NETCDF_EXT)
from climdex.workers import registry, iworker
from climdex.workers.iworker import IWorker, IWorkerFactory

# ------------------------------------------------------------------------------
#
class CIWorker(IWorker):

    ID = 'ci'

    INDICES = [
            'spi12', 'spei12'
    ]

    # mapping of input to input types
    __precipitation_vars = ['$pr']
    __temperature_vars   = ['$tas', '$tasmin', '$tasmax']
    __pet_vars           = ['$pet']

    accepted_vars = [ *__precipitation_vars, *__temperature_vars, *__pet_vars ]


    def __init__(self):
        self.LOGGER = utils.get_logger(__name__)

    def __repr__(self):
        return f'CIWorker[{ID}]'

    def __str__(self):
        return "CIWorker"

    def __callback_ok(self, res):
        self.LOGGER.debug("%s done : %s", self, res) # TODO add index to params for tracing?
        self.tasks_ok += 1 # TODO lock

    def __callback_fail(self, exception):
        self.LOGGER.exception("Exception while executing a task.", exc_info=exception)
        self.tasks_error += 1 # TODO lock

    def compute_all(self, index, index_conf, pool,
            idir=None,
            odir=None,
            scenario=None,
            regex=NETCDF_RGX,
            time_range=None,
            metadata_only=False,
            dry_run=False,
            force=False, **kwargs) -> int:
        """
        Computes the given index on all input data (filtered model x scenario).
        """
        ci_index     = index_conf['ci.index']
        input_vars   = index_conf['ci.input']
        periodicity  = index_conf['ci.periodicity']
        scale        = int(index_conf['ci.scales'])
        distribution = index_conf['ci.distribution']
        calibration  = index_conf['ci.calibration']

        if (dry_run):
            self.LOGGER.info("~ ~ ~ ~ ~ ~ ~ ~ ((   DRY RUN  )) ~ ~ ~ ~ ~ ~ ~ ~")

        self.LOGGER.info("|------------------- [%s] -------------------|", index)
        self.LOGGER.info("|--+ pool         : %s", pool)
        self.LOGGER.info("|--+ idir         : %s", idir)
        self.LOGGER.info("|--+ odir         : %s", odir)
        self.LOGGER.info("|--+ scenario     : %s", scenario)
        self.LOGGER.info("|--+ regex        : %s", regex)
        self.LOGGER.info("|--+ periodicity  : %s", periodicity)
        self.LOGGER.info("|--+ scale        : %s", scale)
        self.LOGGER.info("|--+ inputs       : %s", input_vars)
        self.LOGGER.info("|--+ baseline     : %s", calibration)
        self.LOGGER.info("|--+ distr        : %s", distribution)
        self.LOGGER.info("|--+ md-only      : %s", metadata_only)
        self.LOGGER.info("|--+ force        : %s", force)
        self.LOGGER.info("|-------------------")

        # ok / errors
        self.__setup__() # reset stats

        # sync/async execution of slave workers?
        synchronous = (pool is None)

        # unpack calibration years
        calib_range = calibration.split('/')
        for idx, year in enumerate(calib_range):
            try:
                calib_range[idx] = int(year)
            except ValueError:
                raise ValueError("Non-integer calibration year found: %s", year)

        # unpack vars
        input_vars = input_vars.split(' ')

        # find input files
        modelname2paths, constvar2file = utils.search_files(idir, input_vars, scenario, regex)
        models_names = modelname2paths.keys()
        self.LOGGER.info("Found %d model(s) [regex:%s] among input variables: %s", len(models_names), regex, input_vars)

        if 0 == len(modelname2paths):
            self.LOGGER.warning("No input models found in %s with regex %s", idir, regex)

        if 0 > len(constvar2file):
            self.LOGGER.warning("Ignoring constant input file(s): %s", constvar2file)

        # set output index folder
        index_odir = utils._index_odir(odir, index, scenario)
        index_odir.mkdir(parents=True, exist_ok=True)

        if len(list(index_odir.glob(NETCDF_RGX))) > 0:
            self.LOGGER.warning("Output dir for index [%s] (%s) is not empty.", index, scenario)

        for idx, model_name in enumerate(models_names):
            self.LOGGER.info("___(%s)___ %s ...", idx, model_name)

            if time_range is not None:
                self.LOGGER.warning("Ignoring time_range option: to be implemented.")

            index_ofile = index_odir / utils._index_ofile(index, scenario, model_name)

            # input paths
            varname2path = modelname2paths[model_name]
            self.LOGGER.debug("%s -> %s", model_name, varname2path)

            # parallelism (TODO map ncpus to MP)
            multiprocessing = MP.SINGLE if synchronous else MP.ALL

            # climate_indices CALL-BEGIN #######################################################################
            # NOTE: no async call here, climate_indices raises 'daemonic processes are not allowed to have children'
            #       we lose parallelism as all preprocessing and postprocessing is not asynced TODO
            try:
                index_result = self.compute(
                       index, varname2path, scenario, model_name,
                       periodicity, scale,
                       distribution,
                       calib_range[0], calib_range[1],
                       index_ofile,
                       index_conf,
                       metadata_only = metadata_only,
                       multiprocessing = multiprocessing,
                       dry_run = dry_run,
                       force   = force )
            except Exception as ex:
                self.__callback_fail(ex)
            else:
                self.__callback_ok(RET_OK)
            # ASYNC CALL-END ####################################################################################

        return RET_OK


    def compute(self, index, inputs, scenario, model_name,
            periodicity, scale, distribution, calibration_start, calibration_end,
            ofile, index_conf, metadata_only=False, multiprocessing=MP.ALL_BUT_ONE,
            dry_run=False, force=False):
        """
        Computes a climate index for the specific scenario/model case.

        Parameters
        ----------
        index : str
            Identifier of the index (it shall be tracked in the supported indices in INDICES).
        inputs
            The list of input files (dictionary of varname-->paths)
        scenario : str
            The name of the scenario (just a tag, for naming purposes)
        model_name : str
            The name of the input model used (just a tag, for naming purposes)
        periodicity : Periodicity
            Either 'daily' or 'monthly': determines the time unit.
        scale : int
            The scale of the output index (whether the numeber is intepreted as
            days or month will depend on the 'periodicity' argument).
        distribution : Distribution
            The distribution to be used for the calculation of the indices.
        calibration_start : int
            Initial year of calibration.
        calibration_end : int
            Final year (inclusive) of the calibration.
        ofile : str or Path
            The name of the output index file.
        index_conf : dict
            The complete configuration of the index.
        metadata_only : bool
            True to skip the calculation of the index, and just re-write the metadata fields
            found in index_conf attributed.
            Use force flag to compute the index anyway in case ofile is missing.
        multiprocessing : MP
            Level of parallelism for the underlying computations.
        dry_run : bool
            Print actions only.
        force : bool
            Either force overwrite of existing output files, or force calculation of index in case
            output file does not exist and the metadata_only flag is set.

        Returns
        -------
        The path to the output index file.
        """
        # - - - - - - - - - -
        if type(ofile) is str:
            ofile = Path(ofile)

        if len(inputs) == 0:
            raise ValueError("No inputs provided.")

        if type(periodicity) == Periodicity:
            periodicity = periodicity.value

        if type(ofile) is str:
            ofile = Path(ofile)

        if not ofile.exists() and metadata_only:
            self.LOGGER.warning("metadata_only flag on uncomputed [%s] index file (%s) for model %s.",
                    index, ofile, model_name)
            if force:
                metadata_only = False
            else:
                raise ValueError(f"Cannot set metadata only for inexisting [{index}] index file")

        if ofile.exists() and not metadata_only and not force:
            ofile = ofile.with_stem('{}_{}'.format(ofile.stem, datetime.now().strftime(COMPACT_TIME_FMT)))
            self.LOGGER.warning("[%s] index file for model %s already exists. Use --force to overwrite.", index, model_name)
            self.LOGGER.warning("Storing index to: %s", ofile)

        # - - - - - - - - - -

        # unpack inputs
        temp_dict = self.__get_temperature(inputs)
        prec_dict = self.__get_precipitation(inputs)
        pet_dict  = self.__get_pet(inputs)

        self.LOGGER.debug("%s -> temp:%s, pr:%s, pet:%s", inputs, temp_dict, prec_dict, pet_dict)

        # integrity checks
        if len(temp_dict)+len(prec_dict)+len(pet_dict) == 0:
            raise ValueError(f"No acceptable inputs found. Accepted input vars: {self.accepted_vars}")

        for input_dict in temp_dict, prec_dict, pet_dict:
            if len(input_dict) > 1:
                raise ValueError(f"Ambiguous input variables: {input_dict}")

        # CDO setup
        cdo_logs_dir = Path(DEFAULT_CDO_LOGS_DIR)
        if not cdo_logs_dir.exists():
            self.LOGGER.debug("Creating %s folder.", cdo_logs_dir)
            cdo_logs_dir.mkdir(parents=False, exist_ok=False)

        uid = '{}_{}_{}_{}{}_{}'.format(
                scenario, model_name, index,
                scale, periodicity[:1], distribution)
        tempDir = '{}/{}'.format(DEFAULT_CDO_TMP_DIR, uid)
        logFile = Path(cdo_logs_dir, 'cdo_commands_{}.log'.format(uid))

        # unfold inputs
        temp_var = list(temp_dict.keys())[0][1:] if len(temp_dict) > 0 else None
        prec_var = list(prec_dict.keys())[0][1:] if len(prec_dict) > 0 else None
        pet_var  = list(pet_dict.keys())[0][1:]  if len(pet_dict)  > 0 else None

        # monthly aggregation operators:
        var2cdo_op = {
                prec_var:'monsum',
                temp_var:'monavg', # [!] not monsum -> "Unable to calculate Pearson Type III parameters due to invalid L-moments"
                pet_var: 'monavg'  #                    for illegal temperature (you do not SUM daily temperatures of course)
        }
        cdo_preproc_dict = {
                prec_var:'',
                temp_var:'-setunit,"celsius"', # climate_indices do not like '°c' unit
                pet_var: ''
        }

        # FIXME no fixed paths, but conf.ini
        grids_dir = Path(list(inputs.values())[0]).parent.parent.parent / 'hgrids'
        latlon_grid = grids_dir / 'southtyrol_wgs84.grid'
        laea_grid   = grids_dir / 'southtyrol_laea.grid'

        for path in grids_dir, latlon_grid, laea_grid:
            if not grids_dir.exists():
                raise RuntimeError("Missing required: %s", path)

        with CDOWrapper(uid, tempdir=tempDir, logging=True, logFile=str(logFile)) as cdowr:
            if not metadata_only or not ofile.exists():
                #
                # pre-processing:
                # dims labels/order, time resolution, etc
                #

                # var->cdo_preproc
                var2cdo_preproc = {}

                for input_dict in temp_dict, prec_dict, pet_dict:
                    if len(input_dict) > 0:
                        var_name    = list(input_dict.keys())[0]
                        ifile       = input_dict[var_name]
                        cdo_expr    = cdo_preproc_dict[var_name[1:]]
                        cdo_preproc = '{} "{}"'.format(cdo_expr, ifile)

                        # daily to monthly input
                        # TODO if (input_res = daily):
                        if Periodicity.monthly == Periodicity[periodicity]:
                            cdo_op = var2cdo_op[var_name[1:]]
                            #self.LOGGER.debug("%s -> %s            (%s)", var_name[1:], cdo_op, var2cdo_op)
                            cdo_preproc = '-{} {}'.format(cdo_op, cdo_preproc)
                            self.LOGGER.debug("Monthly '%s' aggregation operation pre-appended to chain for input file '%s'.", cdo_op, ifile)

                        # rename / legal UoMs / latlongrid month sum: (TODO read dimensions -- now assume xy)
                        # FIXME do *not* assume xy input coords
                        #cdo_preproc = '-chname,x,lon,y,lat' # setgrid is enough
                        otmp_latlon = cdowr.compute('setgrid', latlon_grid, iexpr=cdo_preproc, dry_run=dry_run, history=False)
                        self.LOGGER.debug("XY coordinates regridded to lat/lon -> '%s'", ofile)
                        input_dict[var_name] = otmp_latlon

                # extract actual input file paths
                temp_file = list(temp_dict.values())[0] if len(temp_dict) > 0 else None
                prec_file = list(prec_dict.values())[0] if len(prec_dict) > 0 else None
                pet_file  = list(pet_dict.values())[0]  if len(pet_dict)  > 0 else None

                #
                # compute index
                #
                self.LOGGER.debug("Computing %s,%d/%d (%d%s / %s) on %s/%s...", index,
                        calibration_start, calibration_end, scale, periodicity[:1],
                        distribution, scenario, model_name)

                ci_index = index_conf['ci.index']
                ciwr = CIWrapper(uid)
                ofile_base = Path(tempDir) / uid

                tmp_ofile = ciwr.compute(
                    ci_index,
                    calibration_start, calibration_end,
                    ofile_base, # it can be a path (not only filename base)
                    itemp=temp_file, itemp_var=temp_var,
                    iprec=prec_file, iprec_var=prec_var,
                    ipet =pet_file,  ipet_var =pet_var,
                    periodicity=periodicity, scale=scale,
                    distribution=distribution,
                    # eq=?
                    multiprocessing=multiprocessing,
                    dry_run=dry_run,
                    history=False)

                self.LOGGER.debug("[%s] successfully computed. Now revert to original horizontal grid.", ci_index)

                #
                # post-processing:
                # revert pre-processing: horizontal grid, labels, etc
                #
                cdo_preproc = '-setgrid,"{}" "{}"'.format(laea_grid, tmp_ofile)
                tmp_ofile_xy = cdowr.compute('setname', index, iexpr=cdo_preproc, dry_run=dry_run, history=False)
                self.LOGGER.debug("Lat/lon coordinates regridded to Lambert Azimuthal Equal Area grid -> '%s'", tmp_ofile_xy)
                # cleanup
                self.LOGGER.debug("Deleting tmp file \"%s\"..", tmp_ofile)
                tmp_ofile = Path(tmp_ofile)
                tmp_ofile.unlink(missing_ok=dry_run)
                tmp_ofile = tmp_ofile_xy
            else:
                # metadata only: make a copy of the index file before setting the new metadata:
                created_on = "\"Created on\"=\"{}\"".format(datetime.now().strftime(CREATED_ON_FMT))
                tmp_ofile = cdowr.compute('setattribute', op_args=created_on, ifile=ofile, dry_run=dry_run, history=False)

            # craft the CDO call to set all NetCDF metadata attributes:
            index_metadata = utils.build_metadata_cdo_chain(index_conf)
            keywords       = utils.build_kw_dict(index_conf, ofile.name)
            index_metadata = utils.replace_keywords(index_metadata, keywords, camelcase='nc.long_name')
            # CDO call:
            iexpr = ' '.join([index_metadata, tmp_ofile])
            created_on = "\"Created on\"=\"{}\"".format(datetime.now().strftime(CREATED_ON_FMT))
            cdowr.compute('setattribute', op_args=created_on, iexpr=iexpr, ofile=ofile, dry_run=dry_run, history=False) # FIXME

            # cleanup
            self.LOGGER.debug("Deleting tmp file \"%s\"..", tmp_ofile)
            tmp_ofile = Path(tmp_ofile)
            tmp_ofile.unlink(missing_ok=dry_run)

        return RET_OK

    def __get_temperature(self, input_dict):
        """Euristic to extract temperature input from available dictionary (it can return empy dict)."""
        return utils._subdict(input_dict, self.__temperature_vars)

    def __get_precipitation(self, input_dict):
        """Euristic to extract precipitation input from available dictionary (it can return empy dict)."""
        return utils._subdict(input_dict, self.__precipitation_vars)

    def __get_pet(self, input_dict):
        """Euristic to extract PET input from available dictionary (it can return empy dict)."""
        return utils._subdict(input_dict, self.__pet_vars)


# ------------------------------------------------------------------------------
#
class CIWorkerFactory(IWorkerFactory):

    def get_worker(self) -> CIWorker:
        return CIWorker()

