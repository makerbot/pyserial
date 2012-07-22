import unittest

import sys

#assuming this is run from ../, this imports the base directory at start of python path,
#so the ../serial folder is imported as 'import serial' rather than the system serial

sys.path.insert(0,'.') 
import serial.tools.list_ports_vid_pid_osx_posix as lp_vidpid

class TestListPortsOsx(unittest.TestCase):

    def test_blank_string(self):
        dummyport = ('','')
        self.assertEquals(
		lp_vidpid.portdict_from_port(dummyport)
		,{'Port':dummyport} )

    def test_not_usb_device(self):
	dummyport=('','abcdefg')
        self.assertEquals(lp_vidpid.portdict_from_port(dummyport)
			  ,{'Port':dummyport})

    def test_good_params_upper_case(self):
        dummyport = ('', 'USB VID:PID=12AB:34CD SNR=56Ef')
        expected_info = {
          'VID' : '12AB'
          ,'PID' : '34CD'
          ,'iSerial' : '56Ef'
          ,'Port' : dummyport
          }

        self.assertEquals(
            lp_vidpid.portdict_from_port(dummyport),
            expected_info
          )


if __name__ == '__main__':
    unittest.main()
