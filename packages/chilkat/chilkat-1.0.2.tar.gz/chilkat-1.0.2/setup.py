from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension
import os

class BuildExtCommand(build_ext):
    """Custom build_ext command to handle building the shared library."""
    def run(self):
        # You can add commands here to build your shared library if necessary
        # For example, you could call make or another build system
        build_ext.run(self)

setup(
    name="chilkat",
    version="1.0.2",
    author="Chilkat Software",
    author_email="info@chilkatsoft.com",
    description="Chilkat Python Module (CkPython)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'chilkat': ['_chilkat.pyd']  # or .dll, .dylib
    },
    cmdclass={
        'build_ext': BuildExtCommand,
    },
    ext_modules=[Extension('_chilkat', sources=[])],  # No source files for the extension itself
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6',
)
