message("configureing pyserial")
project(pyserial)
message("building egg")

add_custom_command(
    OUTPUT 
        ${EGG_OUTPUT_PATH}/pyserial-2.7_mb2.1-py2.7.egg 
    COMMAND ${CMAKE_COMMAND} -P ${CMAKE_SOURCE_DIR}/mw-cmake-tools/addEgg.cmake)

add_custom_target(pyserial ALL DEPENDS ${EGG_OUTPUT_PATH}/pyserial-2.7_mb2.1-py2.7.egg)


