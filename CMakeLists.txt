
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

# So, we've been trying pretty hard to maintain that under cmake
# all build files are strictly under the build dir. Unfortunately
# setuptools-distutils is a mass of spaghetti, and the bdist_egg
# "Command" doesn't expose the arguments to the other Commands it
# calls, so there's no way to change the location of the build
# directory. Instead, I'm setting this up to copy the files into
# a folder and running setup.py in there.
set(sandbox ${PROJECT_BINARY_DIR}/setuptools_sandbox)
set(dist_dir ${sandbox}/dist)
set(egg_name ${egg_basename}-py2.7.egg)
set(egg ${dist_dir}/${egg_name})

set(source_files

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

set(copied_files)
foreach(f ${source_files})
    set(source_file ${PROJECT_SOURCE_DIR}/${f})
    set(dest_file ${sandbox}/${f})
    list(APPEND copied_files ${dest_file})
    add_custom_command(
        OUTPUT ${dest_file}
        COMMAND
            ${CMAKE_COMMAND} -E copy_if_different
            ${source_file}
            ${dest_file})
endforeach()

add_custom_command(
    OUTPUT
        ${egg}
    COMMAND
        ${PYTHON_EXECUTABLE} ${setup_py}
        bdist_egg
        --bdist-dir ${sandbox}/bdist-tmp
        --dist-dir ${dist_dir}
    WORKING_DIRECTORY
        ${sandbox}
    VERBATIM
    DEPENDS
        ${copied_files})

add_custom_target(pyserial ALL DEPENDS ${egg})

install(
    FILES ${egg}
    DESTINATION ${EGG_INSTALL_DIR})

generate_and_install_config(
    NAME Pyserial
    ADDITIONAL_PATHS
        pyserial ${EGG_INSTALL_DIR}/${egg_name})

enable_testing()
add_subdirectory(test)
add_subdirectory(documentation)
