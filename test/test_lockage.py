#!/usr/bin/env python

""" Tests for locking files on posix and windows
"""

import os
import sys

try :
    import unittest2 as unittestA
except ImportError:
    import unittest

import serial

class TestLocking(unittest.TestCase):
		
	def test_lockHappens(self):
		port = raw_input("specify an actual com port >")
		x = serial.Serial(port)
		with self.assertRaises(serial.SerialException):
			y = serial.Serial(port)


if __name__ == '__main__':
	unittest.main()
