#!/usr/bin/env python

"""
Worker that handles climate indices calculated
via 1+ calls to the CDO library.

See also: https://code.mpimet.mpg.de/projects/cdo
"""

import re

from datetime import datetime
from pathlib import Path

from climdex import utils
from climdex.bindings.cdobnd import CDOWrapper
from climdex.constants import *
from climdex.nc import (NETCDF_RGX, NETCDF_EXT)
from climdex.utils import DebugLevels
from climdex.workers import iworker
from climdex.workers.iworker import IWorker, IWorkerFactory


#
# keywords
#
_TMP_VAR_PREFIX  = '$tmp'

# ------------------------------------------------------------------------------
#
class CDOWorker(IWorker):

    ID = 'cdo'

    INDICES = [
        'amt'       , 'jja_mt'    , 'djf_mt'    ,
        'mam_mt'    , 'son_mt'    , 'wsdi'      ,
        'gsl'       , 'su'        , 'hwd'       ,
        'fd'        , 'tr'        , 'apr'       ,
        'djf_pr'    , 'mam_pr'    , 'jja_pr'    ,
        'ondjfm_pr' , 'amjjas_pr' ,
        'son_pr'    , 'cdd'       , 'dd'        ,
        'rx1day'    , 'rx5day'    , 'r99ptot_all',
        'r99ptot'   , 'r95ptot_all', 'r95ptot'   ,
        'r99pfreq_all', 'r99pfreq', 'r95pfreq_all',
        'r95pfreq'  , 'tx90p'     , 'tn90p',
        'cool_dd'   , 'grow_dd'   , 'heat_dd'
    ]
    # > printf "%-12s, %-12s, %-12s,\n" $( grep '^\[' ./conf/indices.ini | tail -n +2 | tr '[' "'" | tr ']' "'" )

    def __init__(self):
        self.LOGGER = utils.get_logger(__name__)
        #self.LOGGER.debug("CDOWRK: %s", self.LOGGER)

    def __repr__(self):
        return f'CDOWorker[{ID}]'

    def __str__(self):
        return "CDOWorker"

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
            force=False,
            to_merge_files=[]) -> int:
        """
        Computes the given index on all input data (filtered model x scenario).

        Returns
        =======
        Exit status.
        The exit status stats can be extracted from the worker object at the fields:
        worker.tasks_ok/tasks_error at the end of the computations.
        """

        if (dry_run):
            self.LOGGER.info("~ ~ ~ ~ ~ ~ ~ ~ ((   DRY RUN  )) ~ ~ ~ ~ ~ ~ ~ ~")

        self.LOGGER.info("|------------------- [%s] -------------------|", index)
        self.LOGGER.info("|--+ pool    : %s", pool)
        self.LOGGER.info("|--+ idir    : %s", idir)
        self.LOGGER.info("|--+ odir    : %s", odir)
        self.LOGGER.info("|--+ scenario: %s", scenario)
        self.LOGGER.info("|--+ regex   : %s", regex)
        self.LOGGER.info("|--+ md-only : %s", metadata_only)
        self.LOGGER.info("|--+ force   : %s", force)
        self.LOGGER.info("|-------------------")

        # ok / errors
        self.__setup__() # reset stats

        # (not implemented)
        is_by_year  = index_conf.getboolean('cdo.by_year')

        # sync/async execution of slave workers?
        synchronous = (pool is None)

        # CDO inputs
        r = re.compile("cdo.input*")
        input_keys = sorted(filter(r.match, dict(index_conf).keys()))
        cdo_inputs = [ index_conf[i] for i in input_keys ]
        self.LOGGER.debug("|--+ CDO inputs: %s", cdo_inputs)

        # CDO operators
        r = re.compile("cdo.operator*")
        oparg_keys = sorted(filter(r.match, dict(index_conf).keys()))
        cdo_opargs = [ index_conf[i] for i in oparg_keys ]
        self.LOGGER.debug("|--+ CDO op,args: %s", cdo_opargs)

        # integrity checks
        if len(cdo_inputs) == 0:
            self.LOGGER.debug([f"{key}: {index_conf[key]}\n" for key in index_conf])
            raise ValueError(f"Misconfigured [{index}]: missing cdo.input param(s).")

        if len(cdo_opargs) == 0:
            raise ValueError(f"Misconfigured [{index}]: missing cdo.operator param(s).")

        if len(cdo_inputs) != len(cdo_opargs):
            raise ValueError(f"Misconfigured [{index}]: inputs and operators cardinalities do not match.")

        # separate operator from its arguments (eg. 'eca_fd,45' -> ('eca_fd', '45'))
        tmp_split = [ el.split(',', 1) for el in cdo_opargs ] # 'op,arg1,arg2,arg3' --> ['op', ['arg1,arg2,arg3'] ]
        cdo_ops   = [ el[0]                                   for el in tmp_split ]
        cdo_args  = [ el[1].split(',') if len(el)>1 else None for el in tmp_split ]
        self.LOGGER.debug("|--+ CDO args: %s", cdo_args)

        # fetch all available models
        cdo_vars = [ re.findall("\$\w+", el) for el in cdo_inputs ]
        cdo_vars = set([ el for subset in cdo_vars for el in subset ]) # flatten
        cdo_vars = [ var for var in cdo_vars if not var.startswith(_TMP_VAR_PREFIX) ] # ignore tmp vars
        self.LOGGER.debug("|--+ CDO vars: %s", cdo_vars)

        # associate input vars with actual files
        #   (model name)  -> { var1:model_path, var2:model_path ... }
        #   (const_var) -> { file.nc }
        modelname2paths, constvar2file = utils.search_files(idir, cdo_vars, scenario, regex)
        models_names = modelname2paths.keys()
        self.LOGGER.info("Found %d model(s) [regex:%s] among input variables: %s", len(models_names), regex, cdo_vars)

        if 0 == len(models_names):
            self.LOGGER.warning("No input model found in %s with regex %s", idir, regex)

        # set output index folder
        index_odir = utils._index_odir(odir, index, scenario)
        index_odir.mkdir(parents=True, exist_ok=True)

        if len(list(index_odir.glob(NETCDF_RGX))) > 0:
            self.LOGGER.warning("Output dir for index [%s] (%s) is not empty.", index, scenario)

        for idx, model_name in enumerate(models_names):
            self.LOGGER.info("___(%s)___ %s ...", idx, model_name)

            if not is_by_year:
                if time_range is not None:
                    # prepend selyear,Y0/Y1 $input for all inputs
                    # ... TODO: cover general case: where is the input (at which level) etc
                    self.LOGGER.warning("Ignoring time_range option: to be implemented.")

                index_ofile = index_odir / utils._index_ofile(index, scenario, model_name)

                # { $pr:/path/to/pr_model.nc, $tmin:/path/to/tmin_model.nc, ...}
                #self.LOGGER.debug(" %s / %s", modelname2paths, constvar2file)
                var2file = { **modelname2paths[model_name], **constvar2file } # merge dictionaries
                self.LOGGER.debug("CDO files mapping: %s", var2file)

                if not synchronous:
                # CDO CALL-BEGIN ###################################################################################
                    self.LOGGER.debug(f"Spawning subtask [{index}]/{model_name} --> ")
                    index_result = pool.apply_async(
                            self.compute, # [!] shall not be private "__func()"
                            args=(
                                index, cdo_inputs, scenario, model_name,
                                cdo_ops, cdo_args, var2file,
                                index_conf, index_ofile),
                            kwds={
                                'metadata_only': metadata_only,
                                'dry_run': dry_run,
                                'force'  : force
                                },
                            callback      = self.__callback_ok,
                            error_callback= self.__callback_fail)
                # --------------------------------------------------------------------------------------------------
                else:
                    try:
                        index_result = self.compute(
                               index, cdo_inputs, scenario, model_name,
                               cdo_ops,
                               cdo_args,
                               var2file,
                               index_conf,
                               index_ofile,
                               metadata_only = metadata_only,
                               dry_run = dry_run,
                               force   = force )
                    except Exception as ex:
                        self.__callback_fail(ex)
                    else:
                        self.__callback_ok(RET_OK)
                # ASYNC CALL-END ####################################################################################
            else:
                raise NotImplementedError("by_year option not implemented yet.")

#                # TODO input: by_year=True AND fetch_years=True then:
#                nc_years = cdowr.get_years(models_path)
#                self.LOGGER.debug("YEARS: %s", nc_years)
#                time_range = nc_years if time_range is None else time_range
#                years = [y for y in nc_years if y in time_range] # intersection
#
#                # manage temporary files:
#                tmp_odir = utils._tmp_odir(odir, index, scenario, model)
#                to_merge_files[ (model, index) ] = tmp_odir
#
#                global tmp_dirs
#                tmp_dirs.append(tmp_odir)
#
#                if tmp_odir.exists() and not force:
#                    self.LOGGER.error(f"Existing tmp folder for the given case already exist: {tmp_odir}. Please either manually remove or call with force=True")
#                    break
#
#                if dry_run:
#                    self.LOGGER.debug("(dry-run) mkdir %s", tmp_odir)
#                else:
#                    tmp_odir.mkdir(parents=True, exist_ok=True)
#
#                self.LOGGER.info("    %s... ", index)
#
#                for year in years: # run once if not by_year
#
#                    self.LOGGER.debug("      %d", year)
#
#                    # add year slicing
#                    if is_by_year:
#                        cdo_preproc += f' -selyear,{year}'
#                        cdo_ofile    = tmp_odir / utils._tmp_filename(scenario, index, year)
#
#                    tmp_files.append(cdo_ofile)
#
#                    if dry_run:
#                        self.LOGGER.info(f"(dry-run) cdo {cdo_ops} {cdo_preproc} {model_path} {cdo_ofile}")
#                    else:
#                        self.LOGGER_warning("TO BE IMPLEMENTED")
#                        # NOTE: method and its params shall be pickleable (ie. serializable). Test with: >>> pickle.dumps(<obj>)
#                        # FIXME what if an index is composed of 2+ CDO calls (eg. percentile).
#                        # (a) tmp_ofiles[i] =  cdowr.compute(cdo_ops[i], op_args=cdo_args[i], iexpr=cdo_iexpr, dry_run=dry_run, history=False)
#                        # (b) cdowr.compute(cdo_osp, model_path, preproc=cdo_preproc, ofile=cdo_ofile, dry_run=dry_run)
#                        #index_results[year] = pool.apply_async( # no-history?
#                        #                          cdowr.compute, (cdo_op, model_path), {
#                        #                              'op_args': cdo_args,
#                        #                              'preproc': cdo_preproc,
#                        #                              'ofile'  : cdo_ofile,
#                        #                              'dry_run': dry_run
#                        #                          },
#                        #                          callback=_callback_ok,
#                        #                          error_callback=_callback_fail)
#                        #COMPUTE LAMBDA:
#                        #TMP[]
#                        #for i in {1..(NCALLS-1)}:
#                        #    PREPROC[i].replace($pr -> pr, $tas -> tas, $tmp, etc.)
#                        #    TMP[i] <- CDO.SYNC_CALL(OP[i], PREPROC[i], INPUT[i])
#                        #done
#                        #PREPROC[i].replace($pr -> pr, $tas -> tas, $tmp, etc.)
#                        #PREPROC[i].prepend($SET_METADATA)
#                        #CDO.ASYNC_CALL(OP[last], PREPROC[last], INPUT[last])

        return RET_OK

    # ------------------------------------------------------------------------------
    def compute(self, index, inputs, scenario, model_name,
            cdo_ops, cdo_args, var2file, index_conf:dict, ofile,
            metadata_only=False, dry_run=False, force=False):
        """
        Computes an index for the given model under a certain scenario.

        Parameters
        ----------
        self : CDOWorker
            Wrapping worker class
        index : str
            The name of the index to be calculated (must be listed in INDICES)
        inputs : list
            The list of inputs (either file(s) of embedded CDO instructions) to be respectively
            assigned to the chain of CDO operators defined in cdo_ops.
        scenario : str
            The name of the scenario (just a tag, for naming purposes)
        model_name : str
            The name of the input model used (just a tag, for naming purposes)
        cdo_ops : list
            The chain of CDO operators to be sequentially called.
        cdo_args : list
            The list of arguments to be respectivey attached to the chain of CDO operators
            defined in cdo_ops.
        var2file : dict
            Mapping of $-signed 'variables' to their actual paths in filesytem, that can be
            found in the inputs.
        index_conf : dict
            The complete configuration of the index.
        ofile : str or Path
            The final unique output file containing the index.
        metadata_only : bool
            True to skip the calculation of the index, and just re-write the metadata fields
            found in index_conf attributed.
            Use force flag to compute the index anyway in case ofile is missing.
        dry_run : bool
            Print actions only.
        force : bool
            Either force overwrite of existing output files, or force calculation of index in case
            output file does not exist and the metadata_only flag is set.

        Return
        ------
        The name of the file containing the index.
        """
        # - - - - - - - - - -
        if len(cdo_ops) != len(cdo_args):
            raise ValueError(f"Mismatch operators and arguments: {cdo_ops} / {cdo_args}")

        if len(cdo_ops) != len(inputs):
            raise ValueError(f"Mismatch operators and inputs: {cdo_ops} / {inputs}")

        if type(ofile) is str:
            ofile = Path(ofile)

        if not ofile.exists() and metadata_only:
            self.LOGGER.warning("metadata_only flag on uncomputed [%s] index file (%s) for model %s.",
                    index, ofile, model_name)
            if force:
                metadata_only = False
            else:
                raise ValueError(f"Cannot set metadata only for inexisting [{index}] index file")

        if not self.can_handle(index):
            raise ValueError("Cannot handle index '%s'", index)
        # - - - - - - - - - -

        if ofile.exists() and not metadata_only and not force:
            ofile = ofile.with_stem('{}_{}'.format(ofile.stem, datetime.now().strftime(COMPACT_TIME_FMT)))
            self.LOGGER.warning("[%s] index file for model %s already exists. Use --force to overwrite.", index, model_name)
            self.LOGGER.warning("Storing index to: %s", ofile)

        N = len(inputs)
        tmp_ofiles = [None] * N

        # logs folder
        cdo_logs_dir = Path(DEFAULT_CDO_LOGS_DIR)
        if not cdo_logs_dir.exists():
            self.LOGGER.debug("Creating %s folder.", cdo_logs_dir)
            cdo_logs_dir.mkdir(parents=False, exist_ok=False)

        # CDOWr per each index so tmpdir can be safely cleaned up after every iteration
        uid     = '{}_{}_{}'.format(scenario, index, model_name)
        tempDir = '{}/{}'.format(DEFAULT_CDO_TMP_DIR, uid)
        logFile = Path(cdo_logs_dir, 'cdo_commands_{}.log'.format(uid))

        with CDOWrapper(uid, tempdir=tempDir, logging=True, logFile=str(logFile)) as cdowr:

            # configure CDO
            cdowr.env = {'CDO_FILE_SUFFIX': NETCDF_EXT}
            cdowr.__cdo__().debug =  ( utils.debug_level() >= DebugLevels.NORMAL )

            if not metadata_only or not ofile.exists():
                for i, cdo_iexpr in enumerate(inputs):
                    # replace $var with /path/to/var.nc
                    # [!] replace longest keywords first, to avoid erroneous replacements (eg. $tasmin -> ${TAS_REPLACEMENT}min)
                    for var in sorted(var2file.keys(), key=len, reverse=True):
                        var_path = str(var2file[var])
                        cdo_iexpr = re.sub("\{}".format(var), var_path, cdo_iexpr)

                    # replace $tmpN with /path/to/tmpN.nc
                    for j in range(1,i+1): # tmp files# index is 1-based in configuration file
                        cdo_iexpr = re.sub(f"\$tmp{j}", tmp_ofiles[j-1], cdo_iexpr)

                    # run CDO computation:
                    cdo_args[i] = '' if cdo_args[i] is None else cdo_args[i]
                    tmp_ofiles[i] =  cdowr.compute(cdo_ops[i], op_args=','.join(cdo_args[i]), iexpr=cdo_iexpr, dry_run=dry_run, history=False)
            else:
                # copy index file to some tmp file:
                created_on = "\"Created on\"=\"{}\"".format(datetime.now().strftime(CREATED_ON_FMT))
                tmp_ofiles[N-1] = cdowr.compute('setattribute', op_args=created_on, ifile=ofile, dry_run=dry_run, history=False)

            # craft the CDO call to set all NetCDF metadata attributes:
            index_metadata = utils.build_metadata_cdo_chain(index_conf)
            keywords       = utils.build_kw_dict(index_conf, ofile.name)
            index_metadata = utils.replace_keywords(index_metadata, keywords, camelcase='nc.long_name')
            # CDO call:
            iexpr = ' '.join([index_metadata, tmp_ofiles[N-1]])
            created_on = "\"Created on\"=\"{}\"".format(datetime.now().strftime(CREATED_ON_FMT))
            cdowr.compute('setattribute', op_args=created_on, iexpr=iexpr, ofile=ofile, dry_run=dry_run, history=False) # FIXME

            self.LOGGER.debug("[%s] / %s / %s: done.", index, scenario, model_name)

        return ofile


# ------------------------------------------------------------------------------
#
class CDOWorkerFactory(IWorkerFactory):

    def get_worker(self) -> CDOWorker:
        return CDOWorker()

