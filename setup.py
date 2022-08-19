from distutils.core import setup
import py2exe

import sys
main_script_dir = "challenger\\main.py"
main_folder = main_script_dir.rsplit("\\",1)[0]
sys.path.append(main_folder)

data_files = [("basic_setup", ["c:/Users/gabri/OneDrive/Desktop/Library/challenger_script_v3/challenger/basic_setup.json"])]

setup(
    name='ChallengerScript',
    version='3.0',
    packages=['challenger', 'challenger.gui'],
    author='Gabriel Artemie, Loredana Bujor, Catalina Poenaru',
    description='A tool to help in building OLS models from a database',
    windows= ["challenger//exec.py"],
    options= {"py2exe":{"compressed":2,
                        "optimize":2,
                        "bundle_files":3,
                        "dist_dir":"dist"}
              },
    data_file= data_files

)
