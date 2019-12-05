from setuptools import setup, find_packages
VERSION = '1.0'
DESCRIPTION = 'Service Sechedule Excel Loader'
AUTHOR = 'Paul Daekyu, pdkship, mamma'
AUTHOR_EMAIL = 'mamma1234@gmail.com'
URL = 'https://github.com/mamma1234'
SRC_DIR = 'src'
setup(name='scheduleloader', 
    version=VERSION, 
    package_dir={'': SRC_DIR},
    description = DESCRIPTION,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,    
    packages=find_packages(SRC_DIR))
