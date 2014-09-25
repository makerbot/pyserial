message("configureing pyserial")
project(pyserial)
message("building egg")
#installFilesRecursive(${PROJECT_SOURCE_DIR}/serial "*.py")

add_custom_command(
    OUTPUT 
        ${EGG_OUTPUT_PATH}/pyserial-2.7_mb2.1-py2.7.egg 
    COMMAND ${CMAKE_COMMAND} -P ${CMAKE_SOURCE_DIR}/mw-cmake-tools/addEgg.cmake)
    #COMMAND cp ${PROJECT_SOURCE_DIR}/dist/pyserial-2.7_mb2.1-py2.7.egg ${EGG_OUTPUT_PATH}/)
add_custom_target(pyserial ALL DEPENDS ${EGG_OUTPUT_PATH}/pyserial-2.7_mb2.1-py2.7.egg)


