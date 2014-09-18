import sys
import os
import subprocess 
#os.environ['PYTHONPATH'] = os.path.dirname(os.path.realpath(__file__)) + "/../build/eggs/pyserial-2.7_mb2.1-py2.7.egg"
import setuptools
if (sys.argv > 1):
    print sys.argv[1]
    subprocess.call('python setup.py ' + sys.argv[1], shell=True)
