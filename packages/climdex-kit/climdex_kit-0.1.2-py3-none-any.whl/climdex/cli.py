#!/usr/bin/env python
"""
Command line arguments parsers.
"""

import argparse
import logging

from pathlib import Path

from climdex._version import version
from climdex.constants import (
        PARALLELISM_KWDS, INDICES_ALL,
        DEFAULT_INDEXCONF_PATH, LOGGING_CONF)
from climdex.actions import compute, list as ls, show
from climdex.nc import NETCDF_RGX
from climdex.utils import MODULE_PATH
from climdex import indices, utils
# ------------------------------------------------------------------------------
#
def climdex_parser():
    """Main parser for the climdex tool."""

    parser = argparse.ArgumentParser(
        prog="climdex",
        description="Compute one or more climate indices on time-series of temperature and precipitation forecasts.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    #
    # action-independent args
    #
    # --list turned to {list,ls} sub-command
    #parser.add_argument('-l', '--list', help="List all indices",
    #    action='store_true',
    #    required=False)

    parser.add_argument('-d', help="Enable debug mode (append multiple 'd' for more verbose debugging)",
         action='store_true',
         dest='debug',
         required=False) # SET LOGGING LEVEL/HANDLER [+cdo.debug=True]

    parser.add_argument('--version', help="Get the version number of the program",
        action='version',
        version=f'%(prog)s {version}')

    # TODO (and mind the -d debug mode option)
    #parser.add_argument('-v', '--verbose',
    #    action='store_true',
    #    required=False)

    # alternative indices.ini file
    parser.add_argument('-c', '--idx-conf',
        help="Alternative indices configuration file (.ini)",
        type=str,
        dest='idx_conf',
        default=indices.settings_path,
        required=False)

    # alternative indices.ini file
    parser.add_argument('-L', '--log-conf',
        help="Alternative loggging configuration file (.yaml)",
        type=str,
        dest='log_conf',
        default=Path(MODULE_PATH, LOGGING_CONF),
        required=False)

    # TODO
    # alternative logging.yaml file

    # TODO
    # colored output switch

    #
    # sub-parsers
    #
    actions_subparsers = parser.add_subparsers(
            title='actions',
            description='valid actions to execute',
            dest='action_name')
            #parser_class=CustomArgumentParser)

    #
    # sub-commands
    #
    co_parser = add_climdex_co_subparser( actions_subparsers )
    ls_parser = add_climdex_ls_subparser( actions_subparsers )
    sh_parser = add_climdex_sh_subparser( actions_subparsers )

    return parser

# ------------------------------------------------------------------------------
#
def add_climdex_co_subparser(subparsers_group):
    """Adds the sub-parser of the {compute,co} action to the given group of sub-parsers."""

    compute_parser = subparsers_group.add_parser('compute', aliases=['co'])
    compute_parser.set_defaults(
            validate=compute.validate_args,
            run=compute.run)

    compute_parser.add_argument('-i', '--index', help="Indices to compute (comma-separated list, see {list,ls} for a full listing)",
        #choices = [ INDICES_ALL ] + indices.list_indices(), clutter the help: do manually
        action=IndicesListAction, #"extend",
        nargs="?", # should be +, but to have compat help, I'll manually -> required
        default='',
        type=str)

    compute_parser.add_argument('--multiprocessing',
        help="CPU parallelism: set either a keyword among {} or the desired number of CPU/cores."
            .format(PARALLELISM_KWDS),
        type=str, #choices=PARALLELISM_KWDS,
        default='1', # no parallelism by default
        required=False)

    # input dir
    compute_parser.add_argument('--idir',
        help="Root folder where to look for input files (expected structure: $input_dir/variable/scenario/*.nc).",
        required=True)

    # output dir
    compute_parser.add_argument('-o', '--odir',
        help="Root folder where to store indices files tree.",
        required=True)

    # scenario
    compute_parser.add_argument('-s', '--scenario',
        help="White-space separated list of scenarios (it shall coincide with input sub-folder name)",
        action='extend',
        type=str,
        nargs='+')

    # filter
    compute_parser.add_argument('-x', '--regex',
        help="Filter input files with regex expression (NOTE: regex will be used as-is: no '*' signs will be prepended/appended).",
        default=NETCDF_RGX,
        type=str,
        required=False)

    # metadata_only
    compute_parser.add_argument('-m', '--metadata-only',
        help="Only re-set the output attributes (metadata) on existing indices files.",
        action='store_true',
        dest='metadata_only',
        required=False)

    # dry_run
    compute_parser.add_argument('-n', '--dry-run',
        help="Dry-run: only print jobs to output without doing anything.",
        action='store_true',
        dest='dry_run',
        required=False)

    # force
    compute_parser.add_argument('-f', '--force',
        help="Force overwrite of existing output indices files and tmp folders (otherwise execution is stopped).",
        action='store_true',
        required=False)

    return compute_parser

# ------------------------------------------------------------------------------
#
def add_climdex_ls_subparser(subparsers_group):
    """Adds the sub-parser of the {list,ls} action to the given group of sub-parsers."""

    compute_parser = subparsers_group.add_parser('list', aliases=['ls'])
    compute_parser.set_defaults(
            validate=ls.validate_args,
            run=ls.run)

    # TODO any filtering option for instance?

# ------------------------------------------------------------------------------
#
def add_climdex_sh_subparser(subparsers_group):
    """Adds the sub-parser of the {show,sh} action to the given group of sub-parsers."""

    compute_parser = subparsers_group.add_parser('show', aliases=['sh'])
    compute_parser.set_defaults(
            validate=show.validate_args,
            run=show.run)

    compute_parser.add_argument('index',
        help="The index to be shown (see {list,ls} for a full listing)",
        action='store')

# ------------------------------------------------------------------------------
#
def validate_climdex_args(args) -> bool:
    """
    Validate CLI arguments.
    """

    # index conf file exists
    idx_conf = Path(args.idx_conf)
    if not idx_conf.exists():
        raise ValueError(f"Indices configuration file could not be found: '{args.idx_conf}'.")

    # logging conf file exists
    if args.log_conf is not None:
        log_conf = Path(args.log_conf)
        if not log_conf.exists():
            raise ValueError(f"Logging configuration file could not be found: '{args.log_conf}'.")

    # action-specific checks
    args.validate(args)

    return True


# ------------------------------------------------------------------------------
#
class IndicesListAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        #print('I give up')
        setattr(namespace, self.dest, values)

