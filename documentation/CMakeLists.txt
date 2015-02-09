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
install_docs(
    FILES "${documents}"
    PREFIX pyserial)
