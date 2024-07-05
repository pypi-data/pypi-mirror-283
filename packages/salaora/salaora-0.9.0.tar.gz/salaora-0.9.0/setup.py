import os
from importlib.resources import files
import atexit

from setuptools import setup
from setuptools.command.install import install

import re
VERSIONFILE="salaora/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

def install_executables():
    if os.name == "nt":
        base_dir = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        run_file = os.path.join(base_dir, "run_salaora.bat")
        with open(run_file, "w", encoding="utf8") as fout:
            fout.write("python -m salaora")

        upgrade_file = os.path.join(base_dir, "upgrade_salaora.bat")
        with open(upgrade_file, "w", encoding="utf8") as fout:
            fout.write("pip install --upgrade -I salaora")

class new_install(install):
    def __init__(self, *args, **kwargs):
        super(new_install, self).__init__(*args, **kwargs)
        atexit.register(install_executables)

setup(
    cmdclass = {
        "install": new_install
    },
    version = verstr
)
