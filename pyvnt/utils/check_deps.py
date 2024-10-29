import subprocess, re
from pyvnt.Reference.error_classes import VersionError
'''
This function checks for the existence of an external software package. 
'''

def check_package(name, version): 

    pkg_cmd = ""
    if name == "OpenFOAM":
        pkg_cmd = "blockMesh"

        try:   
            res = subprocess.check_output([pkg_cmd, "-help"], text=True, shell=True)
            
            match = re.search(r"OpenFOAM-(\d+)", res)

            v = match.group(1)

            if v != version:
                raise VersionError(v)
        except Exception as e:
            print(e)
            print("OpenFOAM might not be installed or its environment might not be active")