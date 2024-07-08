#!/usr/bin/env python

"""
Blueprint (Abstract Base Class) for worker types.
A worker is a slave-object that runs an atomic task
that can be parallelized by the master controller.
"""

from abc import ABC, abstractmethod

# ------------------------------------------------------------------------------
# Worker blueprint.
#
class IWorker(ABC):

    """Identifier of the worker type (it shall coincide with prefix of params in indices.ini)"""
    ID : str

    """List of indices' names managed by this worker (names shall coincide with section names in indices.ini)"""
    INDICES : list

    def __setup__(self):
        # report stats
        self.tasks_ok = 0
        self.tasks_error = 0

    @classmethod
    @abstractmethod
    def compute(self, index, inputs, *args, **kwargs):
        """
        Computes a climate index for the specific scenario/model case.

        Parameters
        ----------
        index : str
            Identifier of the index (it shall be tracked in the supported indices in INDICES).
        inputs
            The inputs that are necessary for the calculation of the index
            These can be passed on whatever the type is required by the worker
            (file names, dictionaries, lists, etc).

        Returns
        -------
        The path to the output index file.
        """
        ...


    @classmethod
    @abstractmethod
    def compute_all(self, index, index_conf, pool, idir, odir, **kwargs) -> int:
        """
        Execute the task, based on the input arguments.
        This method is meant to iteratively call the {compute} method based
        on all possible combinations of the inputs.

        Parameters
        ----------
        index : str
            Identifier of the index (it shall be tracked in the supported indices in INDICES).
        scenario : str
            The scenario of the climate forecasts IDIR/var/scenario data structure is assumed).
        index_conf :_dict
            Properties/configuration of the given index.
        pool : Pool
            The process/threads pool where to spawn atomic
            sub-tasks (set to None for sequential execution).
        idir : str or Path
            The directory containing the input datasets.
        odir : str or Path
            The root directory where to store the output files.
        **kwargs:
            Worker-specific dictionary of arguments.

        Returns
        -------
        The number of atomic sub-tasks that were processed.
        """
        ...

    @classmethod
    def can_handle(self, index):
        return index in self.INDICES


# ------------------------------------------------------------------------------
# Workers' factory.
#
class IWorkerFactory(ABC):

    @classmethod
    @abstractmethod
    def get_worker(self) -> IWorker:
        """Creates a worker instance."""
        ...

