
enable_testing()

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

foreach(t ${tests})
    add_test(
        NAME ${t}
        COMMAND ${PYTHON_EXECUTABLE} run_all_tests.py /dev/ttyACM0 ${t} -v)
endforeach()
