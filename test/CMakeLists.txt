
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

construct_env_path(
    VALUES ${egg}
    PREPEND_ENV_VAL PYTHONPATH
    PREPEND_ASSIGNMENT
    OUTPUT_VARIABLE pythonpath)

foreach(t ${tests})
    add_test(
        NAME ${t}
        COMMAND
            ${CMAKE_COMMAND} -E env "${pythonpath}"
            ${PYTHON_EXECUTABLE} ${PROJECT_SOURCE_DIR}/test/run_all_tests.py
            /dev/ttyACM0
            ${PROJECT_SOURCE_DIR}/test/${t}
            -v)
endforeach()
