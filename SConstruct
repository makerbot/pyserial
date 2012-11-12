#
# Top-level SConstruct file for pyserial
#

import os

AddOption('--test', action='store_true', dest='test')
run_test = GetOption('test')

env = Environment(ENV = os.environ)

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

#we're not using pyparallel
#env.Command('pyparallel/build', 'pyparallel/setup.py',
#            'cd pyparallel;python setup.py build')

env.CleanAction('pyserial_clean', Action(['rm -r pyserial/build']))
#env.CleanAction('pyparallel_clean', Action(['rm -r pyparallel/build'])

if run_test:
    env.Command('pyserial_test', 'pyserial/test/test.py',
                'cd pyserial/test; python run_all_tests.py')
#   env.Command('pyparallel_test', 'pyparallel/test/test.py',
#               'cd pyparallel/test; python run_all_tests.py')

