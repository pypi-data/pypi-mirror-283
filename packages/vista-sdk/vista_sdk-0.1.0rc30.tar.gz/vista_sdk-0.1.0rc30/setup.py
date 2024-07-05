import os
import sys
from setuptools import setup, find_packages

# Default version number


version = "0.1.0-preview-"

if len(sys.argv) > 1:
    for arg in sys.argv:
        if arg.startswith("--version="):
            version += arg.split("=")[1]
            sys.argv.remove(arg)

resource_directory = os.path.join(os.path.dirname(__file__), '..', '..', 'resources')

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            # Add relative path to the files
            paths.append(os.path.relpath(os.path.join(path, filename), os.path.dirname(__file__)))
    return paths


resource_files = package_files(resource_directory)

setup(
    name="vista-sdk",
    version=version,
    author="Anders Fredriksen",
    author_email="anders.fredriksen@dnv.com",
    description="SDKs and tools relating to DNVs Vessel Information Structure (VIS), ISO 19847, ISO 19848 standards",
    url="https://github.com/dnv-opensource/vista-sdk",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    package_data={'resources': resource_files},
    install_requires=['cachetools>=5.3.3','parameterized>=0.9.0','pydantic>=2.7.1'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
