import os

env = Environment(ENV = os.environ, tools=['default', 'mb_install'])

serial_src = []
src_str = '#/serial'

for curpath, dirnames, filenames in os.walk(str(Dir(src_str))):
    serial_src.append(filter(lambda f:
                                 (os.path.exists(str(f)) and
                                  not os.path.isdir(str(f))),
                             env.Glob(os.path.join(curpath, '*.py'))))

build = env.Command('pyserial/build', 'setup.py', 'python setup.py build')

pyserial_egg = env.Command('dist/pyserial-2.7_mb2.1-py2.7.egg',
                           serial_src,
               'python -c "import setuptools; execfile(\'setup.py\')" bdist_egg')
env.MBInstallEgg(pyserial_egg)

if env.MBIsMac():
    pyserial_egg26 = env.Command('dist/pyserial-2.7_mb2.1-py2.6.egg',
                               serial_src,
           'python2.6 -c "import setuptools; execfile(\'setup.py\')" bdist_egg')
    env.MBInstallEgg(pyserial_egg26)

env.MBCreateInstallTarget()

env.Clean('.', build)

if env.MBRunTests():
    env.Command('pyserial_test', 'pyserial/test/test.py',
                'cd pyserial/test; python run_all_tests.py')
