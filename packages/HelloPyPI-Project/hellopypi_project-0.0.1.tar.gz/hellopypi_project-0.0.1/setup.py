from setuptools import setup, find_packages
import os

VERSION = '0.0.1'
DESCRIPTION = 'First Python Package in PyPI'
LONG_DESCRIPTION = 'This is an Example project that demonstrates how to publish our own Python Package in PyPI'
# Setting up
setup(
    name="HelloPyPI_Project",
    version=VERSION,
    author="Baburam Chaudhary",
    author_email="<baburam.ch208@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['setuptools'],
    keywords=['python', 'python package'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ])
