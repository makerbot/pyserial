message("configureing pyserial")
cmake_minimum_required(VERSION 2.8.3)
project(pyserial)

find_package(
    MBCMakeTools
    REQUIRED)

set_python()

add_custom_command(
    OUTPUT
        ${PROJECT_SOURCE_DIR}/dist/pyserial-2.7_mb2.1-py2.7.egg
    COMMAND ${PYTHON_EXECUTABLE}
        ${PROJECT_SOURCE_DIR}/makeegg.py bdist_egg
    DEPENDS
        ${PROJECT_SOURCE_DIR}/serial/serialposix.py
        ${PROJECT_SOURCE_DIR}/serial/urlhandler/protocol_socket.py
        ${PROJECT_SOURCE_DIR}/serial/urlhandler/protocol_loop.py
        ${PROJECT_SOURCE_DIR}/serial/urlhandler/protocol_hwgrep.py
        ${PROJECT_SOURCE_DIR}/serial/urlhandler/protocol_rfc2217.py
        ${PROJECT_SOURCE_DIR}/serial/urlhandler/__init__.py
        ${PROJECT_SOURCE_DIR}/serial/rfc2217.py
        ${PROJECT_SOURCE_DIR}/serial/serialwin32.py
        ${PROJECT_SOURCE_DIR}/serial/serialjava.py
        ${PROJECT_SOURCE_DIR}/serial/tools/list_ports_posix.py
        ${PROJECT_SOURCE_DIR}/serial/tools/list_ports.py
        ${PROJECT_SOURCE_DIR}/serial/tools/miniterm.py
        ${PROJECT_SOURCE_DIR}/serial/tools/list_ports_windows.py
        ${PROJECT_SOURCE_DIR}/serial/tools/__init__.py
        ${PROJECT_SOURCE_DIR}/serial/tools/list_ports_osx.py
        ${PROJECT_SOURCE_DIR}/serial/tools/list_ports_vid_pid_osx_posix.py
        ${PROJECT_SOURCE_DIR}/serial/win32.py
        ${PROJECT_SOURCE_DIR}/serial/__init__.py
        ${PROJECT_SOURCE_DIR}/serial/sermsdos.py
        ${PROJECT_SOURCE_DIR}/serial/serialutil.py
        ${PROJECT_SOURCE_DIR}/serial/serialcli.py)

add_custom_target(pyserial ALL DEPENDS
    ${PROJECT_SOURCE_DIR}/dist/pyserial-2.7_mb2.1-py2.7.egg)

install(FILES
    ${PROJECT_SOURCE_DIR}/dist/pyserial-2.7_mb2.1-py2.7.egg
     DESTINATION
    ${EGG_OUTPUT_PATH})

enable_testing()

add_test(NAME pyserialTests
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
    COMMAND ${PYTHON_EXECUTABLE}
    ${PROJECT_SOURCE_DIR}/test/run_all_tests.py)

add_subdirectory(documentation)
