#!/usr/bin/env python

"""
Registry of indices computation worker types.
"""

from threading import Lock

from climdex import utils


#
# thread safety
#
lock = Lock()

#
# registry of workers: {index}->{worker_class}
#
__workers = {}


# ------------------------------------------------------------------------------
#
def register_worker(worker_factory, indices, force=False) -> bool:
    """
    Register the given worker type as handler of the 1+ indices provided.

    Parameters
    ----------
    worker_factory: IWorkerFactory
        A factory of workers (None is not allowed)
    indices : list
        List of the names of indices that are handled by these workers.
    force : bool
        Force replacement of indices for already registered worker type.

    Returns
    -------
    True if the given worker type was not known yet; False if the worker type
    was already registered (use force to replace existing indices), or if
    it did not comply with registration requirements (eg. indices list is not empty).
    Exception is raised if the 1+ of the given indices are already handled
    by some other existing worker type.
    """

    LOGGER = utils.get_logger(__name__)

    # - - - - - - - - - -
    if worker_factory is None:
        raise ValueError("None cannot be used as worker factory.")

    if len(indices) == 0:
        LOGGER.debug("0-length indices for %s: skipping.", worker_factory)
        return False
    # - - - - - - - - - -

    ret = True

    with lock:

        all_indices      = [ idx for idxs in __workers.values() for idx in idxs]
        existing_indices = [ idx for idx in indices if idx in all_indices]

        if len(existing_indices) > 0:
            raise ValueError("%s are already handled.", existing_indices)

        if worker_factory in __workers.keys() and not force:
            ret = False
        else:
            __workers[worker_factory] = indices
            LOGGER.debug("New worker registered: %s -> %s", worker_factory, indices)

    return ret



#------------------------------------------------------------------------------
#
def unregister_worker(worker_factory) -> bool:
    """
    Unregisters the given worker type from the catalogue.

    Parameters
    ----------
    worker_factory: IWorkerFactory
        The type of workers to be unregistered.

    Returns
    -------
    True on successfully unregistration of the worker,
    False if the worker type was not previously registered.
    """

    ret = False

    with lock:
        if worker_factory in __workers.keys():
            __workers.pop(factory)
            ret = True

    return ret


# ------------------------------------------------------------------------------
#
def get_handled_indices(worker_factory):
    """Returns the list of indices handled by the given worker type (empty list on unregistered worker)."""
    return __workers.get(worker_factory)

# ------------------------------------------------------------------------------
#
def get_worker_factory(index:str):
    """Returns the factory of workers that handles the given index (None if index is not handled)."""
    factory = [w for w in __workers.keys() if index in __workers[w]]
    if len(factory) == 0:
        return None
    elif len(factory) > 1:
        raise RuntimeError("Incoherent workers registry: %s", __workers)
    else:
        return factory[0]


