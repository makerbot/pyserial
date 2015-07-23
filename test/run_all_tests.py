#! /usr/bin/env python

"""\
UnitTest runner. This one searches for all files named test_*.py and collects
all test cases from these files. Finally it runs all tests and prints a
summary.
"""

import argparse
import os
import sys
import unittest


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-p',
        '--port',
        default='loop://',
        help="The port on which tests should be performed")

    parser.add_argument(
        '-v',
        '--verbose',
        dest='verbosity',
        action='store_const',
        default=1,
        const=2,
        help='increase output')

    parser.add_argument(
        '-t',
        '--tests',
        action='append',
        help='one or more tests to run')

    parser.add_argument(
        '--no-path-mangling',
        action='store_true',
        help='If you want to set up the path yourself.')

    return parser.parse_args()


def main(port, tests, verbosity):
    if not tests:
        tests = os.listdir(os.path.dirname(__file__))
        tests = [os.path.splitext(t)[0] for t in tests]

    # find files and the tests in them
    mainsuite = unittest.TestSuite()
    for modulename in tests:
        try:
            module = __import__(modulename)
        except ImportError:
            print("skipping %s" % modulename)
        else:
            module.PORT = port
            testsuite = unittest.findTestCases(module)
            print(
                "found %s tests in %r" %
                (testsuite.countTestCases(), modulename))
            mainsuite.addTest(testsuite)

    # run the collected tests
    testRunner = unittest.TextTestRunner(verbosity=verbosity)
    result = testRunner.run(mainsuite)

    # set exit code according to test results
    return (0 if result.wasSuccessful() else 1)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])

    if not args.no_path_mangling:
        # inject local copy to avoid testing the installed
        # version instead of the working copy
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))

        import serial
        print(
            "Patching sys.path to test local version. Testing Version: %s" %
            serial.VERSION)

    sys.exit(main(args.port, args.tests, args.verbosity))
