from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy

extensions = [
    Extension("approxe", ["test_cython/approxe.pyx"]),
    Extension("dot_cython", ["test_cython/dot_cython.pyx"],include_dirs=[numpy.get_include()])
    ]

setup(
    name = 'test_cython_zx',
    description='test_cython infrastructure',
    author='test_cython',
    author_email='info@puyuan.tech',
    packages=['test_cython'],
    ext_modules=cythonize(
    extensions, compiler_directives={'language_level' : "3"}),
)