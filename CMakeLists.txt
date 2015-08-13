
cmake_minimum_required(VERSION 3.1)

project(pyserial NONE)

find_package(MBCMakeTools REQUIRED NO_POLICY_SCOPE)

set(pyserial_sources
    serial/serialposix.py
    serial/urlhandler/protocol_socket.py
    serial/urlhandler/protocol_loop.py
    serial/urlhandler/protocol_hwgrep.py
    serial/urlhandler/protocol_rfc2217.py
    serial/urlhandler/__init__.py
    serial/rfc2217.py
    serial/serialwin32.py
    serial/serialjava.py
    serial/tools/list_ports_posix.py
    serial/tools/list_ports.py
    serial/tools/miniterm.py
    serial/tools/list_ports_windows.py
    serial/tools/__init__.py
    serial/tools/list_ports_osx.py
    serial/tools/list_ports_vid_pid_osx_posix.py
    serial/win32.py
    serial/__init__.py
    serial/sermsdos.py
    serial/serialutil.py
    serial/serialcli.py)

# Build a python2.7 egg for conveyor
build_egg(
    pyserial
    SETUP_PY ${PROJECT_SOURCE_DIR}/setup.py
    SOURCES ${pyserial_sources}
    EGG_NAME egg_name
    EGG egg)

install(
    FILES ${egg}
    DESTINATION ${EGG_INSTALL_DIR})

# Bulid a python3.4 wheel for usb-microdaemon
build_wheel(
    pyserial34
    SETUP_PY ${PROJECT_SOURCE_DIR}/setup.py
    SOURCES ${pyserial_sources}
    WHEEL_NAME wheel_name
    WHEEL wheel)

pip_install(${wheel} pip_target)
add_dependencies(pip_target pyserial34)

# For now we only export the path to the egg in our config,
# since I don't know if we actually need to export the wheel
generate_and_install_config(
    NAME Pyserial
    ADDITIONAL_PATHS
        pyserial ${EGG_INSTALL_DIR}/${egg_name})

enable_testing()
add_subdirectory(test)
add_subdirectory(documentation)
