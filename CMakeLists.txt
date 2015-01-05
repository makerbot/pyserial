message("configureing pyserial")
cmake_minimum_required(VERSION 2.8.3)
project(pyserial)
set(utils ${CMAKE_SOURCE_DIR}/../../mw-cmake-tools/utils.cmake)
if(EXISTS "${utils}")
    include("../../mw-cmake-tools/utils.cmake")
    set(TR_BUILD true)
else()
    include("build/mw-cmake-tools/utils.cmake")
endif()
setup_environment()
message("building egg")

add_custom_command(
    OUTPUT
        ${EGG_OUTPUT_PATH}/pyserial-2.7_mb2.1-py2.7.egg
    COMMAND ${PYTHON_EXECUTABLE}
        ${PROJECT_SOURCE_DIR}/makeegg.py bdist_egg
    COMMAND ${CMAKE_COMMAND} -E copy
        ${PROJECT_SOURCE_DIR}/dist/pyserial-2.7_mb2.1-py2.7.egg
        ${EGG_OUTPUT_PATH}/pyserial-2.7_mb2.1-py2.7.egg)

add_custom_target(pyserial ALL DEPENDS
    ${EGG_OUTPUT_PATH}/pyserial-2.7_mb2.1-py2.7.egg)
