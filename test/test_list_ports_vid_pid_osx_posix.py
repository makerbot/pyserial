import unittest

import sys

#assuming this is run from ../, this imports the base directory at start of python path,
#so the ../serial folder is imported as 'import serial' rather than the system serial

sys.path.insert(0,'.') 
import serial.tools.list_ports_vid_pid_osx_posix as lp_vidpid

class TestListPortsOsx(unittest.TestCase):
  

    def test_filter_ports(self):
      input_ports = [
        ['/dev/cu.usbmodemfd121', 'The Replicator', 'USB VID:PID=23c1:d314 SNR=64935343133351107190'],
        ['/dev/cu.Bluetooth-PDA-Sync', '', ''],
        ['/dev/cu.Bluetooth-Modem', '', '']
        ]
      gen = lp_vidpid.filter_ports_by_vid_pid(input_ports) 
      self.assertEquals(len(list(gen)), len(input_ports))
 
      gen = lp_vidpid.filter_ports_by_vid_pid(input_ports,vid=0x23C1) 
      self.assertEquals(len(list(gen)), 1)

      gen = lp_vidpid.filter_ports_by_vid_pid(input_ports,pid=0x1111) 
      self.assertEquals(len(list(gen)), 0)

      gen = lp_vidpid.filter_ports_by_vid_pid(input_ports,pid=0xd314) 
      self.assertEquals(len(list(gen)), 1)
      
      gen = lp_vidpid.filter_ports_by_vid_pid(input_ports,pid=0xD315, vid=0x23C1) 



    def test_blank_string(self):
        dummyport = ('a','b')
        self.assertEquals(
		        lp_vidpid.portdict_from_port(dummyport)
		        ,{'blob':dummyport, 'port':dummyport[0]} )

    def test_not_usb_device(self):
        dummyport=('','abcdefg')
        self.assertEquals(lp_vidpid.portdict_from_port(dummyport)
			      ,{'blob':dummyport, 'port':dummyport[0]})

    def test_good_params_upper_case(self):
        dummyport = ('', 'USB VID:PID=12AB:34CD SNR=00254ba7e5d0')
        expected_info = {
          'VID' : 0x12AB
          ,'PID' : 0x34CD
	  # vvv last 12 or first 8 + last 12 of uuid == iSerial vvv
	  ,'uuid': UUID('87654321-d34d-4360-ba18-00254ba7e5d0')
          ,'iSerial' : '00254ba7e5d0'
          ,'blob' : dummyport
          ,'port' : dummyport[0]
          }
        import pdb
	pdb.set_trace()
	result = lp_vidpid.portdict_from_port(dummyport),
        self.assertEquals( expected_info, result  )



if __name__ == '__main__':
    unittest.main()
