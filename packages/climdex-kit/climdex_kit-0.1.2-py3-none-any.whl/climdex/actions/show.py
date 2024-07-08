#!/usr/bin/env python

"""
Handler of the {show,sh} action.
"""

import argparse

from climdex import indices, utils



# ------------------------------------------------------------------------------
#
def validate_args(args) -> bool:
    """
    Arguments validation for the {show,sh} action.
    """

    indices.load_indices( force_reload=False )

    index = args.index
    idxs  = indices.list_indices()

    if index not in idxs:
        raise ValueError("'{0}' not available. See {{list,ls}} sub-command for a full list of available indices."
                .format(index))

# ------------------------------------------------------------------------------
#
def run(args) -> bool:
    """
    Executes the configured {show,sh} action.
    """

    LOGGER = utils.get_logger(__name__)
    LOGGER.debug("{show,sh} action called.")

    indices.load_indices( force_reload=False )

    index = args.index
    idxs  = indices.list_indices()
    conf  = indices.indices_conf

    # header
    header = "========== {0} ====================".format(index)
    print(header)

    # body
    keys = [key for key in conf[index]]
    keys.sort()

    for key in keys:
        print(" {0:<20} : {1}".format(key, conf[index][key].replace('\n', ' ')))

    print('=' * len(header))

