from distutils.core import setup, Extension
from Cython.Build import cythonize
from version import __version__
import numpy

extensions = [
    Extension("test_cython.approxe", ["test_cython/approxe.pyx"]),
    Extension("test_cython.dot_cython", ["test_cython/dot_cython.pyx"], include_dirs=[numpy.get_include()]),
    Extension("test_cython.account", ["test_cython/account.pyx", "test_cython/account.cpp"], language="c++")
]

setup(
    name = 'test_cython_zx',
    version=__version__,
    description='test_cython infrastructure',
    author='test_cythonv',
    author_email='info@puyuan.tech',
    packages=['test_cython'],
    ext_modules=cythonize(
    extensions, compiler_directives={'language_level' : "3"}),
)

