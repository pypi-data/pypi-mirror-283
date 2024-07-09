from setuptools import setup, find_packages
import os 

VERSION = os.environ["PACKAGE_VERSION"] = "0.0.4"
DESCRIPTION = 'Zero-TOTP Database Model'
LONG_DESCRIPTION = 'The database shared model used accross the zero-totp project.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="zero_totp_db_model", 
        version=VERSION,
        author="Seaweedbrain",
        author_email="developer@zero-totp.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        
        keywords=['Zero-TOTP', 'database'],
)