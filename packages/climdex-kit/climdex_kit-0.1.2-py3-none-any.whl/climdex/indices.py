#!/usr/bin/env python

"""
Climate indices' configuration.
"""

import os

from configparser import ConfigParser
from pathlib import Path

from climdex import utils
from climdex.constants import INDICES_ALL


# the configurations of all indices
indices_conf = dict()

# indices.ini file
settings_path = None

# ------------------------------------------------------------------------------
# list all indices by their abbreviation

def list_indices() -> list:
    load_indices()
    global indices_conf
    return [ key for key in indices_conf.keys() if key != 'DEFAULT' ]

# ------------------------------------------------------------------------------
# set the indices.ini file

def set_settings_path(indices_ini):
    indices_ini = Path(indices_ini)
    if not indices_ini.exists():
        raise ValueError(f"Cannot find indices configuration file: {indices_ini}")

    global settings_path
    settings_path = indices_ini

# ------------------------------------------------------------------------------
# load indices.ini configuration

def load_indices(force_reload=False):
    """Loads the indices from the "indices.ini" file."""
    global indices_conf
    if force_reload or len(indices_conf) == 0:
        indices_conf = __load_indices(settings_path) # TODO --settings param
    if INDICES_ALL in indices_conf:
        raise ValueError(f"Forbidden [{INDICES_ALL}] section in configuration file: {settings_path}")

def __load_indices(settings_path) -> ConfigParser:
    # - - - - - - - - - -
    if settings_path is None:
        raise ValueError("Missing settings path.")

    if not os.path.isabs(settings_path):
        settings_path = os.path.join(os.getcwd(), settings_path)
            #os.path.dirname(os.path.abspath(__file__)),
            #settings_path)

    if not os.path.exists(settings_path):
        raise ValueError(f"Provided indices settings file does not exist: {settings_path}.")
    # - - - - - - - - - -

    config = ConfigParser()
    config.read(settings_path)

    return config
