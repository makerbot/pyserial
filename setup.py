import sys
from setuptools import setup
from serial import __version__ as version
from distutils.command.build_py import build_py
from distutils.command.build_scripts import build_scripts

setup(
    name = "pyserial",
    description = "Python Serial Port Extension Extended by Makerbot Industries",
    version = version,
    author = ["Chris Liechti", "Matt Mets", "David Sayles"],
    author_email = ["cliechti@gmx.net", "david.sayles@makerbot.com"],
    packages = ['serial', 'serial.tools', 'serial.urlhandler'],
    long_description = "Python Serial Port Extension for Win32, Linux, BSD, Jython, IronPython",
)
