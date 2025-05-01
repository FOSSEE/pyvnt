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
    # packages_dir={"": "pyvnt"},
    # data_files=[('Shared_Objects', [
    #     './pyvnt/Converter/cpp_src/dictionaryFile/lib/dictionaryFile.so', 
    #     './pyvnt/Converter/cpp_src/dictionaryFileIterator/lib/dictionaryFileIterator.so'
    # ])],
    packages=find_packages(include=['pyvnt', 'pyvnt.*']),
    # py_modules=['pyvnt'],
    include_package_data=True,
    # package_data={'': ['./pyvnt/Converter/cpp_src/dictionaryFile/lib/dictionaryFile.so', './pyvnt/Converter/cpp_src/dictionaryFileIterator/lib/dictionaryFileIterator.so']},
    install_requires=['anytree', 'dataclasses','ply','pyyaml'],
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

