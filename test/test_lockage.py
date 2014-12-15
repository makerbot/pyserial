#!/usr/bin/env python

""" Tests for locking files on posix and windows
"""

import os
import sys

sys.path.insert(0,"../") #for testing only, make sure we load our serial first

try :
    import unittest2 as unittest
except ImportError:
    import unittest

import serial
import serial.serialposix
import mock

class TestLocking(unittest.TestCase):
	
    def test_lockHappens(self):
        port = input("specify an actual com port >")
        x = serial.Serial(port)
        #check that HSF Lockfile exists
        base, file = os.path.split(port)
        lockfilename = serial.serialposix.getLockfilePath(file)
        self.assertTrue(os.path.isfile(lockfilename), "Lock file expected" )
 
        #check a 2nd open attempt will assert
        with self.assertRaises(serial.SerialException):
            y = serial.Serial(port)

        # check that 'close' works
        x.close()       
        self.assertFalse(x.isOpen(), "post close, isOpen should be false")  
        self.assertFalse(os.path.isfile(lockfilename), "post close Lock file unExpected" )
        
        # check that 'open' works
        x.open()       
        self.assertTrue(x.isOpen(), "post reopen we need isOpen true")  
        self.assertTrue(os.path.isfile(lockfilename), "post open Lock file Expected" )

        #post reopen, check a 2nd open attempt will assert
        with self.assertRaises(serial.SerialException):
            y = serial.Serial(port)

        

if __name__ == '__main__':
	unittest.main()
