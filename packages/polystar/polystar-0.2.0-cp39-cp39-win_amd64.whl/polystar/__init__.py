# Copyright © 2023 Greg Tucker <greggory.tucker@gmail.com>
#
# This file is part of polystar.
#
# polystar is free software: you can redistribute it and/or modify it under the
# terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# polystar is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with polystar. If not, see <https://www.gnu.org/licenses/>.

"""Python module :py:mod:`polystar`
=================================

This module provides access to the C++ polystar library which can be used to
interact with polyhedron and polygon routines.

.. currentmodule:: polystar

.. autosummary::
    :toctree: _generate
"""


# start delvewheel patch
def _delvewheel_patch_1_7_1():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'polystar.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-polystar-0.2.0')
        if os.path.isfile(load_order_filepath):
            with open(os.path.join(libs_dir, '.load-order-polystar-0.2.0')) as file:
                load_order = file.read().split()
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(ctypes.c_wchar_p(lib_path), None, 0x00000008):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_7_1()
del _delvewheel_patch_1_7_1
# end delvewheel patch

from .bound import (
    __version__,
    version,
    ApproxConfig,
    Polyhedron,
    Polygon,
    CoordinatePolygon,
    BitmapI,
    BitmapF,
    BitmapD,
    Network,
    CoordinateNetwork,
    SVG,
    animated_svg,
    __polygon_types__,
    __polyhedron_types__,
    __bitmap_types__,
    __network_types__,
)