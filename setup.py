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
    url = ["http://pyserial.sourceforge.net/", "http://github.com/makerbot/pyserial"],
    packages = ['serial', 'serial.tools', 'serial.urlhandler'],
    license = "Python",
    long_description = "Python Serial Port Extension for Win32, Linux, BSD, Jython, IronPython",
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Python Software Foundation License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        #~ 'Operating System :: Microsoft :: Windows :: Windows CE', # could work due to new ctypes impl. someone needs to confirm that
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.3',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Topic :: Communications',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Terminals :: Serial',
    ],
    platforms = 'any',
    cmdclass = {'build_py': build_py, 'build_scripts': build_scripts},

    scripts = ['serial/tools/miniterm.py'],
)
