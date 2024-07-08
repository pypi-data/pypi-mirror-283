#!/usr/bin/env python

"""
Handler of the {compute,co} action.
"""

import sys
import argparse
import signal

from multiprocessing import Pool
#from multiprocessing.pool import ThreadPool as Pool -> GIL inhibits real thread-based parallelism
from pathlib import Path

from climdex import indices, utils
from climdex.bindings import cdobnd as ccdo, cibnd as cci
from climdex.constants import *
from climdex.utils import DebugLevels, MODULE_PATH
from climdex.nc import NETCDF_RGX, NETCDF_EXT
from climdex.workers import registry as wrk_reg
from climdex.workers.cdowrk import CDOWorkerFactory, CDOWorker
from climdex.workers.ciwrk import CIWorkerFactory, CIWorker


#
# register the workers
#
wrk_reg.register_worker(CDOWorkerFactory(), CDOWorker.INDICES)
wrk_reg.register_worker(CIWorkerFactory(),  CIWorker.INDICES)

# tmp files
tmp_files=[]
tmp_dirs=[]

def log_header():
    LOGGER = utils.get_logger(__name__)

    LOGGER.info("             ____ _    _ _  _ ___  ____ _  _             ")
    LOGGER.info("########     |    |    | |\/| |  \ |___  \/      ########")
    LOGGER.info("########     |___ |___ | |  | |__/ |___ _/\_     ########")
    LOGGER.info("                                                         ")

# signals
# (unused)
def __interrupt_handler__(sign, frame):
    LOGGER = utils.get_logger(__name__)
    LOGGER.error(f"[!] INTERRUPTION SIGNAL {sign}:{signal.strsignal(sign)}")
    __cleanup()
    for cdowr in ccdo.__cdos__.values():
        LOGGER.debug(f"{cdowr} : interrupt handler")
        cdowr.__catch__(sign, frame)

    sys.exit(-sign)

# by default: interrupt -> KeyboardInterrupt/SystemExit try/except flow
#signal.signal(signal.SIGTERM, __interrupt_handler__)
#signal.signal(signal.SIGINT,  __interrupt_handler__)
#signal.signal(signal.SIGSEGV, __interrupt_handler__)

# SIGPIPE: when redirecting output to file + CTRL-C (KeyboardInterrupt),
# then logging will raise a BrokenPipeError.
# Workaround: ignore the broken pipes, though logging does not
# happen in the KeyboardInterrupt exception handler. FIXME
signal.signal(signal.SIGPIPE, signal.SIG_DFL)


# ------------------------------------------------------------------------------
#
def validate_args(args) -> bool:
    """
    Arguments validation for the {compute,co} action.
    """

    # CSV string to list
    args.index = args.index.split(',')

    LOGGER = utils.get_logger(__name__)
    LOGGER.debug("To compute %d indices: %s", len(args.index), args.index)

    # check 'all' keyword is not mixed with actual indices
    if INDICES_ALL in args.index:
        if len(args.index) > 1:
            raise ValueError("'{}' keyword among indices: please select either '{}' or valid indices."
                    .format(INDICES_ALL, INDICES_ALL))
            return False # or raise Exception?
        else:
            LOGGER.debug("Replacing '%s' with actual indices.", INDICES_ALL)
            args.index = indices.list_indices()

    # parallelism
    if args.multiprocessing not in PARALLELISM_KWDS:
        try:
            args.multiprocessing = int(args.multiprocessing)
        except ValueError:
            raise ValueError("'%s' not recognized as multiprocessing option.")

    # check input dir
    idir = Path(args.idir)
    if not idir.exists():
        raise ValueError("'{}' does not exist.".format(args.idir))

    # check scenario exists
    # TODO find -type d -maxdepth 2 -name $scenario
    LOGGER.debug("Scenarios: %s", args.scenario)

    # check output dir
    odir = Path(args.odir)
    if not odir.exists():
        if odir.parent.exists():
            LOGGER.info("Creating output folder: '%s'")
            try:
                odir.mkdir(parents=False, exist_ok=False)
            except:
                raise ValueError("Cannot create output folder '%s'. Check your permissions on the file system and retry.", odir)
        else:
            raise ValueError("'%s' does not exist.", args.odir)

    return True


# ------------------------------------------------------------------------------
#
def run(args) -> bool:
    """
    Executes the configured {compute,co} action.
    """
    # to dict: >>> vars(args)

    # reload logger (level might have changed) # FIXME debug option setting should be done before logger is loaded
    LOGGER = utils.get_logger(__name__)

    # print header with all configuration
    LOGGER.debug("Executing indices calculation now.")

    # PRINT HEADER with all input conditions
    log_header()


    return compute_indexes(
            args.index, args.idir, args.odir, args.scenario,
            cpus=args.multiprocessing,
            regex=args.regex,
            metadata_only = args.metadata_only,
            dry_run=args.dry_run,
            force=args.force)


# import climdex.cdo as ccdo
# import climdex.main as cmdx
# indexes  = ['eca_fd']
# idir     = "/mnt/CEPH_PROJECTS/FACT_CLIMAX/CORDEX-Adjust/QDM/"
# odir     = "/mnt/CEPH_PROJECTS/FACT_CLIMAX/CORDEX-Adjust/INDICES/"
# tsteps   = range(1990,1993)
# scenario = "rcp45"

# cmdx.cdowr.get_years(idir + "tasmin_EUR-11_CNRM-CERFACS-CNRM-CM5_CNRM-ALADIN63_r1i1p1_v2_day_19702100_rcp45.nc")
# cmdx.compute_indexes(indexes, idir, odir, scenario, cpus='all_but_one', regex="*REMO2009*.nc", time_range=tsteps, dry_run=True, force=False)
# ------------------------------------------------------------------------------
def compute_indexes(indexes:list, idir, odir, scenarios, cpus=1, regex=NETCDF_RGX, time_range=None, metadata_only=False, dry_run=False, force=False) -> int :
    """
    Computes then given (list of) indexes on the provided input data.

    Parameters
    ----------
    indexes : str or list
        The 1+ climate indexes to be computed on the input data
    idir : str or Path
        The directory containing the input data
    odir : str or Path
        The root directory where to store the output files (climate indices)
        The actual index files will be stored in "odir/index/scenario/*.nc"
    scenarios : str
        The name of the scenario(s) of the input datasets: this will affect the
        name of the folder containing the indexes (see odir)
    cpus : int or str
        The level of CPU parallelism by either the number of CPU cores to use
        or by means of keyword (see PARALLELISM_KWDS).
        If set to 1/'one' the execution of the program will be synchronous.
    regex : str
        The regular expression to filter files from the input directory idir
    time_range : list or range [not implemented yet]
        Time filter for the input time steps, eg. range(2000, 2005)
    dry_run : bool
        Print the index computation calls without executing them
    force : bool
        Forse overwriting of existing indexes and tmp folders (otherwise execution is stopped).

    Returns
    -------
    The number of new climate index files that were created and stored in the odir.
    """
    # - - - - - - - - - -

    # pdb.set_trace() ########################################################################################
    LOGGER = utils.get_logger(__name__)

    if time_range is not None:
        raise NotImplementedError("'time_range' option not implemented.")

    if type(scenarios) is str:
        scenarios = [scenarios]

    if type(indexes) is str:
        indexes = [indexes]

    all_indices = indices.list_indices()
    indices.load_indices()

    if INDICES_ALL in indexes:
        if len(indexes) != 1:
            LOGGER.error(f"[{INDICES_ALL}] keyword shall be used as only input index argument.")
            sys.exit(1)
        else:
            indexes = [ index for index in all_indices ]
    else:
        for index in indexes:
            if index not in all_indices:
                LOGGER.error(f"[{index}] is not recognized. Available indices: {all_indices}")
                #raise ValueError(f"{index} unknown. Please see `climdex --list\' for a full list of supported operators.")
                sys.exit(1)

    idir = Path(idir) if type(idir) is str else idir
    odir = Path(odir) if type(odir) is str else odir

    for fld in [idir, odir]:
        if not fld.exists():
            raise ValueError(f"Invalid folder: {fld}")

    if type(cpus) is int:
        if cpus > MAX_CPUS:
            cpus = MAX_CPUS
            LOGGER.warning("Too many CPUs requested. Trimming to %s.", MAX_CPUS)
        ncpus = cpus
    else:
        if type(cpus) is str and cpus not in PARALLELISM_KWDS:
            raise ValueError(f"Invalid cpus argument: {cpus}. Please put either a number or one among: {PARALLELISM_KWDS}.")
        ncpus = utils.ncpus_of(cpus)

    synchronous = (ncpus == 1)

    if type(time_range) is int:
        time_range = [time_range]

    # - - - - - - - - - -

    # TODO report input params

    LOGGER.info("Calculating %s from %s with %d CPUs.",indexes, idir, ncpus)
    if time_range is not None:
        LOGGER.info("Selected time range: %s", time_range)

    __cleanup() # jic (spurious)
    index_pool = None

    try:
        for scenario in scenarios:
            LOGGER.info("")
            LOGGER.info(":::::::: SCENARIO :  %s", scenario)
            LOGGER.info("")

            tasks_ok = tasks_error = 0 # stats
            workers = []

            if not synchronous:
                sigint_handler            = signal.signal(signal.SIGINT, signal.SIG_IGN)
                index_pool, index_results = Pool(ncpus, __pool_worker_initializer), dict()
                signal.signal(signal.SIGINT, sigint_handler)

            to_merge_files = dict()

            # launch computation of all indexes
            for index in indexes:

                # parse index configuration
                index_conf  = indices.indices_conf[index]

                # identify worker type hand pass on
                w_factory = wrk_reg.get_worker_factory(index)
                if w_factory is None:
                    raise RuntimeError(f"No workers found for index '{index}'")

                LOGGER.debug("Workers factory for '%s': %s", index, w_factory)

                # pack params
                kwparams = {
                        'scenario': scenario,
                        'regex' : regex,
                        'metadata_only': metadata_only,
                        'dry_run': dry_run,
                        'force': force,
                        'to_merge_files': to_merge_files }

                ## delegate to worker ######################################################
                worker = w_factory.get_worker()
                LOGGER.debug("Worker found for index %s: %s", index, worker)
                worker.compute_all(index, index_conf, index_pool, idir, odir, **kwparams)
                workers.append( worker )
                ############################################################################

            LOGGER.info("|---------------------------------------------|")

            if not synchronous:
                LOGGER.info("Waiting for operators tasks to join... ")
                index_pool.close()
                index_pool.join()
                LOGGER.info("All operators tasks terminated.")

            for worker in workers:
                tasks_ok    += worker.tasks_ok
                tasks_error += worker.tasks_error

            # ok/error stats
            __print_report(tasks_ok, tasks_error)

            if len(to_merge_files) > 0:
                # merge all yearly indexes onto single datasets
                LOGGER.debug("To be merged: %s", to_merge_files.keys())
                merge_pool, merge_results = Pool(ncpus, __pool_worker_initializer), dict()

                try:
                    for model, index in to_merge_files:
                        # input / output
                        tmp_odir  = to_merge_files[ (model, index) ]
                        cdo_ofile = tmp_odir.parent / f'{index}_{scenario}_{model}'

                        if cdo_ofile.exists() and not force:
                            LOGGER.warning("Time-merged file already exists: %s", cdo_ofile)
                            cdo_ofile = cdo_ofile.with_stem(f'{cdo_ofile.stem}_new')

                        time_regex = _tmp_file_regex(scenario, index)
                        cdo_ifiles = list(tmp_odir.glob(time_regex))

                        if len(cdo_ifiles) == 0 and not dry_run:
                            # TODO exact number of expected yearly files
                            LOGGER.critical("No input files found in folder: %s", tmp_odir)

                        if dry_run:
                            LOGGER.info("(dry-run) cdowr.mergetime(%s, %s, dry_run=%s)", cdo_ifiles, cdo_ofile, dry_run)
                        else:
                            cdowr.mergetime(cdo_ifiles, cdo_ofile, dry_run=dry_run)
                            #merge_results[index] = merge_pool.apply_async(cdowr.mergetime, (cdo_ifiles, cdo_ofile), dry_run=dry_run, no_history=True

                    LOGGER.debug("Waiting for time-merge tasks to join... ")
                    merge_pool.close()
                    merge_pool.join()
                    LOGGER.debug("All time-merge tasks terminated.")

                except (KeyboardInterrupt, SystemExit) as err:
                    if (utils.debug_level() > DebugLevels.NO_DEBUG):
                        LOGGER.exception("Interruption caught: terminating yearly indices time merging...", err)
                    else:
                        LOGGER.error("Interruption caught (%s). Terminating yearly indices time merging...", err)
                    merge_pool.terminate()
                    merge_pool.join()

                merge_pool.close()
                merge_pool.join()

    except KeyboardInterrupt as err:
        if utils.debug_level() > DebugLevels.NO_DEBUG:
            LOGGER.exception("Interruption caught!")
        else:
            LOGGER.error("Interruption caught (%s)", err)
        if not synchronous:
            LOGGER.error("Terminating indices calculation...")
            index_pool.terminate()
            index_pool.join()
            LOGGER.info("All subprocesses terminated.")

    except Exception as err:
        if utils.debug_level() > DebugLevels.NO_DEBUG:
            LOGGER.exception("ERROR: %s", err)
        else:
            LOGGER.error("ERROR: %s", err)

    finally:
        __cleanup()

    LOGGER.info("Bye.")

    return # TODO return N indices computed

# ------------------------------------------------------------------------------
# misc

def __pool_worker_initializer():
    """Ignore SIGINT handler for forked processes, so that SIGINT handler is inherited from parent."""
    #signal.signal(signal.SIGINT, signal.SIG_IGN)

# ------------------------------------------------------------------------------

def __print_report(n_ok, n_error):
    LOGGER = utils.get_logger(__name__)
    LOGGER.info("|")
    LOGGER.info("| Total indices calculated : {0} ".format(n_ok))
    LOGGER.info("! Total indices aborted    : {0} ".format(n_error))
    LOGGER.info("|__")

# ------------------------------------------------------------------------------

def __cleanup():
    LOGGER = utils.get_logger(__name__)
    #LOGGER.debug("compute CLEANUP")
    for f in tmp_files:
        if f.exists():
            LOGGER.debug(f"Deleting tmp file: {f}")
            f.unlink(missing_ok=True)
    tmp_files.clear()
    for d in tmp_dirs:
        if d.exists():
            LOGGER.debug(f"Deleting tmp folder: {d}")
            d.rmdir()
    tmp_dirs.clear()

