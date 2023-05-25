
from setuptools import Extension, setup
from Cython.Build import cythonize

from pysmx import SM3

"""

Libraries have been installed in:
   /usr/local/lib

If you ever happen to want to link against installed libraries
in a given directory, LIBDIR, you must either use libtool, and
specify the full pathname of the library, or use the `-LLIBDIR'
flag during linking and do at least one of the following:
   - add LIBDIR to the `LD_LIBRARY_PATH' environment variable
     during execution
   - add LIBDIR to the `LD_RUN_PATH' environment variable
     during linking
   - use the `-Wl,-rpath -Wl,LIBDIR' linker flag
   - have your system administrator add LIBDIR to `/etc/ld.so.conf'

See any operating system documentation about shared libraries for
more information, such as the ld(1) and ld.so(8) manual pages.

"""


py_x_sources =  [
    "pygcrypt.pyx"
]

py_x_sources =  [
    "/opt/webdak/webapps/modules/pygcrypt/pygcrypt.pyx"
]

include_dirs = ["/opt/python/include/site/python3.11/gcrypt"]
c_libraries = ["gcrypt"]
library_dirs =["/opt/python/lib/libgcrypt"]

exts = [Extension("pygcrypt", py_x_sources, include_dirs=include_dirs, libraries=c_libraries, library_dirs=library_dirs)]

setup(
    ext_modules=cythonize(exts)
)