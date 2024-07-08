#!/usr/bin/env python

"""
Entry point for calculating climate indices over a time-series
of datasets.
"""
# NOTE: zonal average along time point: cdo -outputtab,date,lon,lat,value -remapnn,"lon=151.5683_lat=-32.7427" temp.nc > output.csv

# imports time profile:
# > export PYTHONPATH=$HOME/src/eurac/climax/climdex/src/
# > conda activate cdo
# > python3 -X importtime -m climdex 2> climdex-imports

#import pdb

import logging
import logging.config
import multiprocessing
import sys, errno
import time

from datetime import datetime
from pathlib import Path
from pkg_resources import Requirement, resource_filename

from climdex import utils
from climdex.constants import (
        DEFAULT_LOGLEVEL, LOGGING_CONF,
        DEFAULT_INDEXCONF_PATH)
from climdex.utils import MODULE_PATH, DebugLevels

# setup logging for whole package (do this before any other import using logging)
default_log_conf = Path(MODULE_PATH, LOGGING_CONF)
utils.setup_logging(path=default_log_conf, level=DEFAULT_LOGLEVEL)
#
from climdex import cli, indices
from climdex.cli import climdex_parser
from climdex.utils import DebugLevels

#
# indices configuration
#
indices.set_settings_path(Path(MODULE_PATH, DEFAULT_INDEXCONF_PATH))
#_set_conf_path(DEFAULT_CONF_PATH) TODO


# ------------------------------------------------------------------------------
#
def climdex(args):
    """
    Entry point for the computation of indices from CLI arguments.
    """

    LOGGER = utils.get_logger(__name__)

    try:
        # log some timing info, used later for elapsed time
        start_datetime = datetime.now()

        LOGGER.info("Start time:    %s", start_datetime)

        # validate the arguments and determine the input type
        try:
            cli.validate_climdex_args(args)
         #   LOGGER.debug("Arguments successfully validated and processed.")
        except ValueError as err:
            LOGGER.error("Invalid input argument: %s", err)
            sys.exit(-1) # TODO ret codes

        # process args input
        indices.set_settings_path( args.idx_conf )

        # logging
        if not default_log_conf.samefile( args.log_conf ):
            LOGGER.info("Setting up new logger configuration at \"%s\"", args.log_conf)
            utils.setup_logging(path=args.log_conf, level=LOGGER.level)
            # ``disable_disable_existing_loggers = False'' otherwise this LOGGER is disabled from here on.

        # debug logging
        if args.debug:
            # app-level DEBUG
            LOGGER.info("DEBUG mode on")
            utils.set_debug_level(DebugLevels.NORMAL)
            # TODO -d -d -> DebugLevels.VERBOSE
            if LOGGER.level > logging.DEBUG:
                #logging.getLogger().setLevel(logging.DEBUG) # [!] it does not change children loggers' level
                LOGGER.setLevel(logging.DEBUG) # still not DEBUG before this call: why? TODO
                LOGGER.warning("DEBUG level activated (%s)", LOGGER)
                utils.set_default_log_level( logging.DEBUG )
            else:
                LOGGER.debug("DEBUG level already set.")

        # execute task:
        args.run(args) # actions multiplexer FIXME

        end_datetime = datetime.now()
        elapsed_time = end_datetime - start_datetime
        LOGGER.info("Elapsed time:  %s", elapsed_time)

    except Exception:
        LOGGER.exception("Failed to complete.")
        raise

# ------------------------------------------------------------------------------
# Entry point:
#
if __name__ == "__main__":
    # parse the command line arguments
    parser = climdex_parser()
    args = parser.parse_args()

    # call execution
    climdex(args)

    #index = 'all' if len(sys.argv) <= 1 else sys.argv[1].split(",")
    #test_case(index)
