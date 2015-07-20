
cmake_minimum_required(VERSION 3.1)

project(pyserial NONE)

find_package(MBCMakeTools REQUIRED NO_POLICY_SCOPE)

find_package(PythonInterp)

check_for_setuptools()

set(setup_py ${PROJECT_SOURCE_DIR}/setup.py)

execute_process(
    COMMAND ${PYTHON_EXECUTABLE} ${setup_py} --fullname
    OUTPUT_VARIABLE egg_basename
    OUTPUT_STRIP_TRAILING_WHITESPACE)

set(dist_dir ${PROJECT_BINARY_DIR}/dist)
set(egg_name ${egg_basename}-py2.7.egg)
set(egg ${dist_dir}/${egg_name})

add_custom_command(
    OUTPUT
        ${egg}
    COMMAND
        ${PYTHON_EXECUTABLE}
        ${setup_py}
        bdist_egg
        --bdist-dir ${PROJECT_BINARY_DIR}/bdist-tmp
        --dist-dir ${dist_dir}
    WORKING_DIRECTORY
        ${PROJECT_SOURCE_DIR}
    VERBATIM
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

add_custom_target(pyserial ALL DEPENDS ${egg})

install(
    FILES ${egg}
    DESTINATION ${EGG_INSTALL_DIR})

generate_and_install_config(
    NAME Pyserial
    ADDITIONAL_PATHS
        pyserial ${EGG_INSTALL_DIR}/${egg_name})

enable_testing()

set(tests
    test_readline
    test_iolib
    test_list_ports_windows
    test_lockage
    test_list_ports_vid_pid_osx_posix
    test
    handlers/protocol_test
    handlers/__init__
    test_url
    test_high_load
    test_advanced)
foreach(t ${tests})
    add_test(NAME ${t}
        WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}/test"
        COMMAND sudo ${PYTHON_EXECUTABLE}
        "${PROJECT_SOURCE_DIR}/test/run_all_tests.py"
            "/dev/ttyACM0"
            "${t}" -v)
endforeach()
add_subdirectory(documentation)
