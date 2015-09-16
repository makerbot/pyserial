
# TODO(chris): Fix these tests to use PYTHONHOME, but still run
#              against the local egg.

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

# We test the built egg, not the source
construct_env_path(
    VALUES ${wheel}
    PREPEND_ENV_VAL PYTHONPATH
    PREPEND_ASSIGNMENT
    OUTPUT_VARIABLE pythonpath)

foreach(t ${tests})
    add_test(
        NAME ${t}
        COMMAND
            ${CMAKE_COMMAND} -E env "${pythonpath}"
            ${PYTHON_EXECUTABLE} ${PROJECT_SOURCE_DIR}/test/run_all_tests.py
            --port /dev/ttyACM0
            --tests ${PROJECT_SOURCE_DIR}/test/${t}
            -v
            --no-path-mangling)
endforeach()
