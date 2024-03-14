from setuptools import setup, find_packages

# this script for setting up the package for testing and using

VERSION = '0.0.0'
DESCRIPTION = 'Tree Data Structure for openFoam'

# Setting up
setup(
    name="pyvnt",
    version=VERSION,
    author="",
    author_email="<abs@gmail.com>",
    description=DESCRIPTION,
    packages_dir={"": "pyvnt"},
    packages=find_packages(exclude=['test']),
    install_requires=['anytree', 'dataclasses'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

# Command to run: python setup.py sdist bdist_wheel
# this part is entirely optional, uncomment only if needed

# import setPackage

