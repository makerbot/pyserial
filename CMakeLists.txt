message("configureing pyserial")
project(pyserial)
message("building egg")

add_custom_command(
    OUTPUT
        ${EGG_OUTPUT_PATH}/pyserial-2.7_mb2.1-py2.7.egg
    COMMAND ${PYTHON_EXECUTABLE}
        ${CMAKE_SOURCE_DIR}/makeegg.py bdist_egg
    COMMAND ${CMAKE_COMMAND} -E copy
        ${CMAKE_SOURCE_DIR}/dist/pyserial-2.7_mb2.1-py2.7.egg
        ${EGG_OUTPUT_PATH}/pyserial-2.7_mb2.1-py2.7.egg)

add_custom_target(pyserial ALL DEPENDS
    ${EGG_OUTPUT_PATH}/pyserial-2.7_mb2.1-py2.7.egg)
