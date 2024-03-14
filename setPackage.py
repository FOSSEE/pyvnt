
# Code to update the package in the testenv

import os
import shutil

source = r"pyvnt"
destination = r"../env/lib/python3.11/site-packages/pyvnt"
target = r"../env/lib/python3.11/site-packages/pyvnt/"

try:
    shutil.rmtree(target)
except:
    pass

shutil.copytree(source, destination)