#!/usr/bin/env python

"""
Wrapper of CDO's [1] related operators.

[1] https://code.mpimet.mpg.de/projects/cdo
"""

import logging
import signal

from cdo import Cdo
from enum import Enum
from multiprocessing import Lock
from pathlib import Path, PosixPath

import time # DEBUG
import glob #

from climdex import utils

OVERWRT_OPT = ''# '-O' [!] CDO binding automatically prepends each call with this
DRY_RUN_OPT = '-A'
NO_HIST_OPT = '--no_history'
TIMSTAT_OPT = '--timestat_date first' # first, middle, midhigh or last

# pickleable instances (top-level module)
# indexed by serial number and **not** by class instance (self)
# When forking a new process "self" hashcode changes!
#
__lock__   = Lock()
__serial__ = 0
__cdos__   = {}


# ------------------------------------------------------------------------------
#
class CDOWrapper:
    """
    Wrapper of the Climate Data Operators (CDO) toolset.
    """
    def __init__(self, uid, *args, **kwargs):
        self.LOGGER = utils.get_logger(__name__)
        self.env = None
        self.uid = uid

        # Cdo __init__: sets its own interrupt handlers ! see Cdo.__catch__()
        self.__store_sig_handlers__()

        #self.LOGGER.debug(f"({self}::{hash(self)}) ARGS:{args} KWARGS={kwargs}")
        __lock__.acquire()
        self.cdo = Cdo(*args, **kwargs)
        __lock__.release() # jic

        #self.LOGGER.debug(f"[{self}] Cur-CDO SIGINT handler: {signal.getsignal(signal.SIGINT)}")
        self.__restore_sig_handlers__()

        #__cdos__[hash(self)] = cdo
        #self.LOGGER.debug(f"{__cdos__}")

        self.env = self.cdo.env


    def __store_sig_handlers__(self):
        self.sig_handlers = {}
        for sign in (signal.SIGINT, signal.SIGTERM, signal.SIGSEGV):
            self.sig_handlers[sign] = signal.getsignal(sign)

    def __restore_sig_handlers__(self):
        for sign, handler in self.sig_handlers.items():
            signal.signal(sign, handler)

    def __enter__(self):
        #assert hash(self) in __cdos__.keys()
        return self

    #
    # FIXME this is not called with async calls to CDO wrapper (--multiprocessing != 1)

    def __exit__(self, exc_type, exc_value, traceback):
        __lock__.acquire()
        self.LOGGER.debug(f"[{self}] EXIT")
        self.LOGGER.debug(f"[{self}] clean tmp dir")
        cdo = self.__cdo__()
        self.LOGGER.debug("tmp files: %s", str(glob.glob(cdo.tempStore.dir + "/*")))
        #cdo.tempStore.__del__()
        cdo.cleanTempDir() # check the TMP folder
        __lock__.release()

    def __catch__(self, signum, frame):
        self.LOGGER.debug(f"[{self}] CAUGHT SIGINT")
        cdo = self.__cdo__()
        cdo.__catch__(signum, frame) # cleans tmp store
        self.LOGGER.debug(str(glob.glob(cdo.tempStore.dir + "/*")))

    def supports(self, op:str) -> bool:
        """
        Tells whether the given op (operator) is supported by the
        underlying CDO toolset.
        """
        cdo = self.__cdo__()
        return op in _do.operators

    def get_years(self, ifile):
        """
        Returns the years of the input file.

        See Also
        --------
        $ cdo --help showyear
        """
        # - - - - - - - - - -
        ifile = str(ifile)
        # - - - - - - - - - -

        years = []

        if ifile is not None:
            #self.LOGGER.debug("[CDO] cdo showyear %s", ifile)
            cdo = self.__cdo__()
            res = cdo.showyear(input=ifile)
            years = res[0].split(' ')
            years = [int(y) for y in years]

        return years

    def mergetime(self, ifiles, ofile, dry_run=False, history=False):
        """
        Merges all input files sorted by date and time onto a single output file.
        """
        # - - - - - - - - - -
        if type(ifiles) in [str, PosixPath]:
            ifiles = [ifiles]
        # - - - - - - - - - -
        ifiles =[str(f) for f in ifiles]
        ofile  = str(ofile)
        # - - - - - - - - - -

        res = None

        if len(ifiles) > 0:
            opts = []
            if dry_run:     opts.append(DRY_RUN_OPT)
            if not history: opts.append(NO_HIST_OPT)
            if True:        opts.append(OVERWRT_OPT)
            if True:        opts.append(TIMSTAT_OPT)
            opts = ' '.join(opts)
            #self.LOGGER.debug("[CDO] cdo mergetime %s %s %s", opts, ifiles, ofile)
            cdo = self.__cdo__()
            res = cdo.mergetime(input=ifiles, output=ofile, options=opts)

        return res


    def compute(self, op:str, op_args:str=None, ifile:str=None, iexpr:str=None, ofile=None, var=None, dry_run=False, history=False):
        """
        Computes a climate operator on an input file.

        Parameters
        ----------
        op : str
            The name of the cdo climate operator to compute (see `$ cdo --operators` for a full list)
        op_args : str
            The operator's arguments
        ifile : str or Path
            The input file (leave empty in case of operator's chaining).
            This argument is mutually exclusive with iexpr.
        iexpr : str
            The string defining the chaining of CDO operators that provide
            the input(s) to this CDO call.
            This argument is mutually exclusive with ifile
        ofile : str or Path
            The output file (if required by the operator).
            Leave to None also if you want to store the output to a temporary
            file to be automatically managed by CDO (you can get its
            path as the returned value of this call).
        var : TODO
            The metadata of the new variable to be set in the output file
        dry_run : only show processed cdo call without running it
        history : let CDO fill in the global `history' NetCDF attribute

        Returns
        -------
        The output of the CDO's operator (see `$ cdo -h OPERATOR` for more details).
        """
        # - - - - - - - - - -
        if ifile is not None and iexpr is not None:
            raise ValueError(f"ifile and iexpr args are mutually exclusive: {ifile} -- {iexpr}")

        if ifile is None and iexpr is None:
            raise ValueError("Specify one among ifile and iexpr.")

        if ifile is not None:
            ifile = Path(ifile) if type(ifile) is str else ifile
            if not ifile.exists():
                raise ValueError(f"Invalid input file: {ifile}")

        #self.LOGGER.debug("%s in %s", self, __cdos__)
        cdo = self.__cdo__()

        try:
            method = getattr(cdo, op)
            # [!] restore original signal handler (getattr apparently re-__init__s a Cdo instance)
            self.__restore_sig_handlers__()
        except AttributeError:
            raise NotImplementedError(f"Unsupported {op} operator.")
        # - - - - - - - - - -
        op_args = '' if op_args is None else op_args
        iexpr   = iexpr if ifile is None else str(ifile)
        ofile   = str(ofile) if ofile is not None else None
        opts = []
        if dry_run:     opts.append(DRY_RUN_OPT)
        if not history: opts.append(NO_HIST_OPT)
        if True:        opts.append(OVERWRT_OPT)
        if True:        opts.append(TIMSTAT_OPT)
        opts = ' '.join(opts)
        # - - - - - - - - - -

        __lock__.acquire()
        self.LOGGER.debug("[%s] cdo %s %s,%s %s %s", self, opts, op, op_args, iexpr, ofile)
        __lock__.release()

        try:
            output = method(op_args, input=f'{iexpr}', output=ofile, options=opts)
        except Exception as ex:
            __lock__.acquire()
            self.LOGGER.error("Error executing {0}".format(op))
            __lock__.release()
            raise ex from None

        __lock__.acquire()
        self.LOGGER.debug("OUTPUT: \"{0}\"".format(output))
        __lock__.release()

        return output

    def __cdo__(self):
        return self.cdo #__cdos__[hash(self)]

    def __repr__(self):
        return f'CDOWrapper({self.uid},env={self.env})'

    def __str__(self):
        return f"CDO:{self.uid}"

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.cdo == other.cdo
            #self.__cdo__() == other.__cdo__()
        )

    def __ne__(self, other):
        return (
            self.__class__ != other.__class__ or
            self.cdo != other.cdo
            #self.__cdo__() != other.__cdo__()
        )

    def __hash__(self):
        return hash(self.uid)

