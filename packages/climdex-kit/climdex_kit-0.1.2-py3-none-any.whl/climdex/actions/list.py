#!/usr/bin/env python

"""
Handler of the {list,ls} action.
"""

import argparse

from climdex import indices, utils


# ------------------------------------------------------------------------------
#
def validate_args(args) -> bool:
    """
    Arguments validation for the {list,ls} action.
    """

    return True

# ------------------------------------------------------------------------------
#
def run(args) -> bool:
    """
    Executes the configured {list,ls} action.
    """

    LOGGER = utils.get_logger(__name__)
    LOGGER.debug("{list,ls} action called.")

    indices.load_indices( force_reload=False )

    # header
    print("---------------------------------------------------------")
    print("     index     |             description                  ")
    print("---------------------------------------------------------")

    # body
    conf = indices.indices_conf
    idxs = indices.list_indices()
    idxs.sort()

    for index in idxs:
        print(" {0:<13} | {1}".format(index, conf[index]['nc.long_name']))

    print("---------------------------------------------------------")
