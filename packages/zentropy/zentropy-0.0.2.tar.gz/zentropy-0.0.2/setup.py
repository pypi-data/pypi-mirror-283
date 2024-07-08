from setuptools import setup, Extension
import numpy

extensions = [
    Extension("zentropy.lib", ["lib/lib.c",],
        include_dirs=[numpy.get_include(),]),
]
setup_args = dict(
    ext_modules = extensions,
    package_data = {"lib":["lib.c"],}
)
setup(**setup_args)