"""
pyshtools
=========

pyshtools a scientific package that can be used to perform spherical harmonic
transforms and reconstructions, rotations of data expressed in spherical
harmonics, and multitaper spectral analyses on the sphere.

This module imports the following classes and subpackages into the
main namespace:

    SHCoeffs          : Class for spherical harmonic coefficients.
    SHGrid            : Class for global grids.
    SHWindow          : Class for localized spectral analyses.
    Slepian           : Class for Slepian functions.
    SHGravCoeffs      : Class for gravitational potential spherical harmonic
                        coefficients.
    SHMagCoeffs       : Class for magnetic potential spherical harmonic
                        coefficients.

    shclasses         : All pyshtools classes and subclasses.
    shtools           : All Python-wrapped Fortran 95 routines.
    constants         : pyshtools constants.
    legendre          : Legendre functions.
    expand            : Spherical harmonic expansion routines.
    shio              : Spherical harmonic I/O, storage, and conversion
                        routines.
    spectralanalysis  : Global and localized spectral analysis routines.
    rotate            : Spherical harmonic rotation routines.
    gravmag           : Gravity and magnetics routines.
    utils             : pyshtools utilities.
    backends          : Routines for selecting the spherical harmonic
                        transform backend.

For further information, consult the web documentation at

   https://shtools.github.io/SHTOOLS/

and the GitHub project page at

   https://github.com/SHTOOLS/SHTOOLS
"""


# start delvewheel patch
def _delvewheel_patch_1_7_1():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pyshtools.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-pyshtools-4.13.1')
        if os.path.isfile(load_order_filepath):
            with open(os.path.join(libs_dir, '.load-order-pyshtools-4.13.1')) as file:
                load_order = file.read().split()
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(ctypes.c_wchar_p(lib_path), None, 0x00000008):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_7_1()
del _delvewheel_patch_1_7_1
# end delvewheel patch

from importlib.metadata import version, PackageNotFoundError

# ---- Import shtools subpackages ----
from . import backends
from . import constants
from . import shclasses
from . import datasets
from . import legendre
from . import expand
from . import shio
from . import spectralanalysis
from . import rotate
from . import gravmag
from . import utils

# ---- Import principal classes into pyshtools namespace
from .shclasses import SHCoeffs
from .shclasses import SHGrid
from .shclasses import SHWindow
from .shclasses import Slepian
from .shclasses import SHGravCoeffs
from .shclasses import SHMagCoeffs

try:
    __version__ = version('pyshtools')
except PackageNotFoundError:
    # package is not installed
    pass

__author__ = 'SHTOOLS developers'

# ---- Define __all__ for use with: from pyshtools import * ----
__all__ = ['constants', 'shclasses', 'legendre', 'expand', 'shio', 'shtools',
           'spectralanalysis', 'rotate', 'gravmag', 'utils', 'backends',
           'SHCoeffs', 'SHGrid', 'SHWindow', 'Slepian', 'SHGravCoeffs',
           'SHMagCoeffs', 'datasets']