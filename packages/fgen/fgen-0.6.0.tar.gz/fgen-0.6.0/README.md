# Fortran-Python wrapper

<!---
Can use start-after and end-before directives in docs, see
https://myst-parser.readthedocs.io/en/latest/syntax/organising_content.html#inserting-other-documents-directly-into-the-current-document
-->

<!--- sec-begin-description -->

Automatically generate wrappers to integrate Fortran and Python


This project consists of a few different components:

* fgen
* fgen_runtime
* libfgen

<!--- sec-end-description -->

Full documentation can be found at:
[fgen.readthedocs.io](https://fgen.readthedocs.io/en/latest/).
We recommend reading the docs there because the internal documentation links
don't render correctly on GitLab's viewer.

## Installation

<!--- sec-begin-installation -->

fgen can be installed with pip:

```bash
pip install fgen
```

## Usage

TODO

### libfgen

If you wish to use the fortran functionality in a downstream library, the fortran library must be compiled and
linked against. A CMake module for finding or fetching the `fgen` library is available as part of this
repository (from the repository root, see `cmake/Findfgen.cmake`). This module will try and find fgen
according a few different methods:

* cmake: Use a cmake config file (uses the cmake command `find_package(fgen CONFIG)`)
* subproject: Use a relative directory (relative to the CMake file) that points to a cloned `fgen` repository
* fetch: Download the project from GitLab and build locally

The order that the methods tried can be set using the CMake define : `FGEN_FIND_METHOD`
(default order: `["cmake" "subproject" "fetch"]`). The `Findfgen.cmake` CMake module must be accessible
from the target repository. The current recommendation is to copy `Findfgen.cmake` into the repository. This
allows the target repository to pin the specific git hash of `fgen` to use.

The library can then be integrated into a CMake project by adding the snippet below:

```cmake
if(
  NOT
  TARGET
  "fgen::fgen"
)
  # Find the fgen package, fetch it from gitlab if it isn't available locally
  find_package(
    "fgen"
    REQUIRED
  )
endif()
```

Some examples of using fgen are provided in `tests/test-data`.


<!--- sec-end-installation -->

### For developers

<!--- sec-begin-installation-dev -->

For development, we rely on [poetry](https://python-poetry.org) for all our
dependency management. To get started, you will need to make sure that poetry
is installed
([instructions here](https://python-poetry.org/docs/#installing-with-the-official-installer),
we found that pipx and pip worked better to install on a Mac).

For all of work, we use our `Makefile`.
You can read the instructions out and run the commands by hand if you wish,
but we generally discourage this because it can be error prone.
In order to create your environment, run `make virtual-environment`.

Once the virtual environment has been created, `libfgen` can be built
using `make build`. This library contains the common Fortran code used by
all wrappers and uses [CMake](https://cmake.org/) to build and requires
a working Fortran compiler.

If there are any issues, the messages from the `Makefile` should guide you
through. If not, please raise an issue in the
[issue tracker](https://gitlab.com/magicc/fgen/issues).

For the rest of our developer docs, please see [](development-reference).

<!--- sec-end-installation-dev -->
