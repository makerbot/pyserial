import os

env = Environment(
    ENV=os.environ,
    tools=['default', 'mb_install'],
    toolpath=['#/../mw-scons-tools', '#/Install/mw-scons-tools'])

source = env.MBMagicPythonGlob('serial')

build = env.Command('pyserial/build', 'setup.py', 'python setup.py build')
env.Clean(build, '#/build')

pyserial_wheel = env.MBDistWheel('dist/pyserial-2.7_mb2.1', source)
env.MBInstallEgg(pyserial_wheel)
env.Clean(pyserial_wheel, '#/dist')
# env.Clean(pyserial_wheel, '#/pyserial.egg-info')

env.MBCreateInstallTarget()
