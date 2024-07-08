from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import shutil
import os
import platform

class CustomBuildExtCommand(build_ext):
    """Custom build_ext command to include the pre-built shared library."""
    def run(self):
        # Define the shared library name based on the platform
        shared_library_name = 'libchilkat.so'
        if platform.system() == 'Windows':
            shared_library_name = '_chilkat.pyd'
        elif platform.system() == 'Darwin':
            shared_library_name = 'libchilkat.dylib'
        
        # Copy the shared library to the build directory
        build_lib = self.build_lib
        os.makedirs(build_lib, exist_ok=True)
        shutil.copy(shared_library_name, build_lib)
        
        # Run the standard build_ext command
        super().run()

setup(
    name="chilkat",
    version="1.0.4",
    author="Chilkat Software",
    author_email="info@chilkatsoft.com",
    description="Chilkat Python Module (CkPython)",
    py_modules=['chilkat'],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    data_files=[
        ('', ['libchilkat.so' if platform.system() == 'Linux' else
              '_chilkat.pyd' if platform.system() == 'Windows' else
              'libchilkat.dylib'])
    ],
    cmdclass={
        'build_ext': CustomBuildExtCommand,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
    ],
    python_requires='>=3.6',
)
