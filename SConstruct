#
# Top-level SConstruct file for pyserial
#

import os

AddOption('--test', action='store_true', dest='test')
run_test = GetOption('test')

#not used, added for consistency
AddOption('--debug_build', action='store_true', dest='debug_build')
debug = GetOption('debug_build')

env = Environment(ENV = os.environ)
env.Tool('mb_install', toolpath=[Dir('submodule/mw-scons-tools')])

serial_src = []
src_str = '#/serial'

for curpath, dirnames, filenames in os.walk(str(Dir(src_str))):
    serial_src.append(filter(lambda f:
                                 (os.path.exists(str(f)) and
                                  not os.path.isdir(str(f))),
                             env.Glob(os.path.join(curpath, '*.py'))))


def TestClean(env, targets):
    if not env.GetOption('clean'):
        return False
    else:
        return True

def CleanActionFunc(env, targets, action):
    if TestClean(env, targets):
        env.Execute(action)

env.AddMethod(CleanActionFunc, 'CleanAction')

env.Command('pyserial/build', 'setup.py',
            'python setup.py build')

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

#we're not using pyparallel
#env.Command('pyparallel/build', 'pyparallel/setup.py',
#            'cd pyparallel;python setup.py build')

env.Clean('build', 'build')

if run_test:
    env.Command('pyserial_test', 'pyserial/test/test.py',
                'cd pyserial/test; python run_all_tests.py')
#   env.Command('pyparallel_test', 'pyparallel/test/test.py',
#               'cd pyparallel/test; python run_all_tests.py')

