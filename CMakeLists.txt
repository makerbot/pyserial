
cmake_minimum_required(VERSION 3.1)

project(pyserial NONE)

find_package(MBCMakeTools REQUIRED NO_POLICY_SCOPE)

build_wheel(
    pyserial
    SETUP_PY ${PROJECT_SOURCE_DIR}/setup.py
    SOURCES
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
        serial/serialcli.py
    WHEEL_NAME wheel_name
    WHEEL wheel)

# Also create a .pth file so that we can import the egg without
# manually adding it to the path (see the docs for site.py).
# TODO(chris):  Resolve python3 issues and use mustache here
set(pyserial_pth "${PROJECT_BINARY_DIR}/pyserial.pth")
configure_file("${PROJECT_SOURCE_DIR}/pyserial.pth.in" "${pyserial_pth}")

install(
    FILES ${wheel} ${pyserial_pth}
    DESTINATION ${PY34_MODULE_DIR})

generate_and_install_config(
    NAME Pyserial
    ADDITIONAL_PATHS
        pyserial ${PY34_MODULE_DIR}/${wheel_name})

enable_testing()
add_subdirectory(test)
add_subdirectory(documentation)
