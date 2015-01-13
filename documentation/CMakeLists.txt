set(documents
    ${PROJECT_SOURCE_DIR}/documentation/conf.py
    ${PROJECT_SOURCE_DIR}/documentation/pyserial_api.rst
    ${PROJECT_SOURCE_DIR}/documentation/pyparallel.rst
    ${PROJECT_SOURCE_DIR}/documentation/shortintro.rst
    ${PROJECT_SOURCE_DIR}/documentation/CMakeLists.txt
    ${PROJECT_SOURCE_DIR}/documentation/Makefile
    ${PROJECT_SOURCE_DIR}/documentation/examples.rst
    ${PROJECT_SOURCE_DIR}/documentation/appendix.rst
    ${PROJECT_SOURCE_DIR}/documentation/pyserial.rst
    ${PROJECT_SOURCE_DIR}/documentation/index.rst
    ${PROJECT_SOURCE_DIR}/documentation/pyserial.png)
set(DOCUMENT_OUTPUT_PATH
    ${PROJECT_SOURCE_DIR}/testDocs)
add_custom_target(docs)
foreach(doc ${documents})
    add_custom_command(
        TARGET docs
        COMMAND ${CMAKE_COMMAND} -E
            copy ${doc} ${DOCUMENT_OUTPUT_PATH})
endforeach()

set_target_properties(docs PROPERTIES EXCLUDE_FROM_ALL 1 EXCLUDE_FROM_DEFAULT_BUILD 1)

