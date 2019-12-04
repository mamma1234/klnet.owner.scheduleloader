from setuptools import setup, find_packages
SRC_DIR = 'src'
setup(name='scheduleloader', 
    version='1.0', 
    package_dir={'': SRC_DIR},
    packages=find_packages(SRC_DIR))