
[[_TOC_]]

# How to contribute

**Thank you** for landing to this page and willing to contribute to the project by either
fixing existing [bugs](https://gitlab.inf.unibz.it/earth_observation_public/cdr/climdex-kit/-/issues),
adding new features, or implementing new indices.

This project contains a single Python package called `climdex`,
whose sources can be found under the `src/` directory.
Tests shall kept outside of the source folder, under `tests/` ([Why?](https://docs.python-guide.org/writing/structure/))

Other important folders include:

- `etc/` : logging and indices configuration files
- `notebooks/` : containing Jupyter notebooks
- `docs/` : containing documentation files and diagrams

Of particular importance is the `indices.ini` file: each index gives the name
to a section, and its implementation and metadata are configured
within the section.
Dotted notation is used to classify types of index attributes, for instance `nc.*`
attributes refer to NetCDF-related fields. etc.

## Setup the environment

Take these steps in order to setup your development environment.

In the first place, you need to install the following dependencies:

* [`conda`](https://docs.conda.io/en/latest/miniconda.html) for managing the virtual environments
* [`pip`](https://pip.pypa.io/en/stable/installation/) for the installation on your local machine
* GNU [`make`](https://www.gnu.org/software/make/manual/make.html) utility for running the `Makefile` rules

After that you can run:

```sh
$ make develop
```

This will create the virtual environment in the local `./venv` folder, and
install the package in your system in development/editable mode, meaning
that local changes to the source code will be immediately effective
(although clearly when running the Python REPL, you will need to either
restart the console or [reload](https://docs.python.org/3/library/importlib.html)
the package)

Finally, to make sure the package has been successfully installed, run:

```sh
$ conda activate venv/
(venv) $ python -m climdex --help
```

## Quickstart

In this section you can fine some recommendations for the most relevant tasks
you might need to undertake as a developer for the package.

Also, refer to the available UML diagrams inside the `docs/uml/` folder to get
an overview of the structure and flow of the program.

### Define a new index

Defining a new index consists of two steps:

1. add a new section in the `etc/indices.ini` configuration file.
1. add the name of the new index (the section name in the configuration file)
   to the list of supported indices in the appropriate *worker* class.

The list of supported indices lies in the `INDICES` list field of the worker class.

All available workers can be found in the `climdex.workers` module:
they adhere to the `IWorker` blueprint interface (`iworker` module) and
can be fetched from a registry of workers -- see `climdex.workers.registry`.

For a proper configuration of the new index, keep in mind that:

- **$**-signed keywords can be used to refer to a metadata field of the specific index file.
   Such keywords can be either a cross-reference to an other index configuration entry
   (eg. `$nc.long_name`), or any of the information encoded in the name of the input climate
   projections files, that is:
  - `$varname` : the name(s) of the input climate variable(s)
  - `$model`   : the name of the model in the ensemble (eg. CNRM-CERFACS-CNRM-CM5_CLMcom-CCLM4-8-17_r1i1p1_v1)
  - `$scenario`: the name of the scenario set for the index (eg. rcp85)
  - `$timeres` : the time resolution of the input file
  - `$yearstart`/`$yearend` : the time range of the input time-series
- If you wish to change a generic attribute -- i.e. defined in the `DEFAULT` section --
   you can be overwrite it by re-setting it in your new index section, but do **not** change
   the default value in order not to cascade the change to all other indices
- NetCDF metadata attributes are identified with the `nc.` prefix (at the moment you
   can set only those that you already see in the `indices.ini` file)
- index type specific options are prepended with the prefix of the correspondent
   worker type defined in its ID field (eg. CDO-specific options are those with the `cdo.`
   prefix, being "cdo" the value of the `ID` field of the `climdex.workers.CDOWorker` class)


### Define a new index type

If you need to create a new *type* of indices, than you first have to
setup a new so-called *worker*.

Define a new worker class, which will adhere to the `IWorker`
Abstract Base Class (ABC) contract and an accompanying factor (`IWorkerFactory` ABC),
then set:

- the `ID` field to identify the index type, while also be used as prefix for worker-specific
configurations (e.g. `cdo.input` for the `CDOWorker` type, whose `ID` is set to `cdo`).
- the `INDICES` field list to declare the indices that this worker can handle
(the names of which will correspond to the section names in the `indices.ini` file)
- the `compute`/`compute_all` methods where the behaviour of the worker is defined

Finally, register your new worker in the `climdex.workers.registry` module with
the `register_worker()` function.


### Define a new sub-command

If you want to define a new CLI sub-command, these are the steps
to be taken:

1. inside the `climdex.actions` model, create a new module
   -- possibly named after the sub-command -- and define
   the function to be executed when called (and also in case a function
   for the validation of the input arguments):
```py
# ./src/climdex/actions/new_thing.py
def validate_args(args) -> bool:
    ...
def run(args) -> bool:
    ...
```
2. define the CLI sub-parser in `cli.py` and add it to the `actions_subparsers`
   sub-parsers group
```py
my_new_subparser = subparsers_group.add_parser('newthing', aliases=['nt'])
...
```
3. link the functions in (1) to the `run` and `validate` options of your sub-parsers:
```py
my_new_subparser.set_defaults(
        validate = new_thing.validate_args,
        run      = new_thing.run)
```

In the `run()` function you will then put the business logic for the correct
execution of your new sub-command.


## Troubleshooting

### The install method you used for conda is not compatible with using conda as an application

If you get this error when trying to run a `Makefile` rule, then you probably have installed
`conda` via `pip install conda` or `easy_install conda`. In order use the fully fledged `conda`
you need to install via binary installer at https://conda.io/miniconda.html.


## External resources

* [FAct-CLIMAX](https://www.eurac.edu/en/institutes-centers/institute-for-earth-observation/projects/fact-climax):
  internal funding project at EURAC
* [climax](https://gitlab.inf.unibz.it/REMSEN/climax): FAct-CLIMAX machine-learning development repository

