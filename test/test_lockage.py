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
import 
class TestLocking(unittest.TestCase):
	
    def test_lockHappens(self):
        port = raw_input("specify an actual com port >")
        x = serial.Serial(port)
        
        #check that HSF Lockfile exists
        base, file = os.path.split(port)
        lockfilename = os.path.join('/var/lock/LCK..', str(base))
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
        self.assertFalse(os.path.isfile(lockfilename), "post open Lock file Expected" )

        #post reopen, check a 2nd open attempt will assert
        with self.assertRaises(serial.SerialException):
            y = serial.Serial(port)

        

if __name__ == '__main__':
	unittest.main()
