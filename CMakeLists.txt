message("configureing pyserial")
project(pyserial)
file(GLOB_RECURSE source serial "*.py")
message("building egg")
#installFilesRecursive(${PROJECT_SOURCE_DIR}/serial "*.py")

add_custom_command(
    OUTPUT 
        ${PROJECT_SOURCE_DIR}/dist/pyserial-2.7_mb2.1-py2.7.egg 
    COMMAND ${CMAKE_COMMAND} -P ${CMAKE_SOURCE_DIR}/mw-cmake-tools/addEgg.cmake)
add_custom_target(pyserial ALL DEPENDS ${PROJECT_SOURCE_DIR}/dist/pyserial-2.7_mb2.1-py2.7.egg)


