import unittest
import serial.tools.get_ports_vid_pid_osx_posix

class TestListPortsOsx(unittest.TestCase):

    def test_blank_string(self):
        self.assertEquals(serial.tools.get_ports_vid_pid_osx_posix.get_info_from_serial_identifier(''), {})

    def test_not_usb_device(self):
        self.assertEquals(serial.tools.get_ports_vid_pid_osx_posix.get_info_from_serial_identifier('abcdefg'), {})

    def test_good_params_upper_case(self):
        identifier_string = 'USB VID:PID=12AB:34CD SNR=56Ef'
        expected_info = {
          'VID' : 4779,
          'PID' : 13517,
          'iSerial' : '56Ef'
          }

        self.assertEquals(
            serial.tools.get_ports_vid_pid_osx_posix.get_info_from_serial_identifier(identifier_string),
            expected_info
          )

    def test_check_if_port_is_replicator_empty_data(self):
        data = {}
        val = serial.tools.get_ports_vid_pid_osx_posix.check_if_port_is_replicator(4779, 13517, data)
        self.assertFalse(val)

    def test_check_if_port_is_replicator_mismatched_vid(self):
        vid = 4779
        pid = 13517
        data = {
            'VID'   :   vid+1,
            'PID'   :   pid,
            'iSerial'   :   '56ef'
            }
        val = serial.tools.get_ports_vid_pid_osx_posix.check_if_port_is_replicator(vid, pid, data)
        self.assertFalse(val)

    def test_check_if_port_is_replicator_mismatched_pid(self):
        vid = 4779
        pid = 13517
        data = {
            'VID'   :   vid,
            'PID'   :   pid+1,
            'iSerial'   :   '56ef',
            }
        val = serial.tools.get_ports_vid_pid_osx_posix.check_if_port_is_replicator(vid, pid, data)
        self.assertFalse(val)

    def test_check_if_port_is_replicator_good_values(self):
        vid = 4779
        pid = 13517
        data = {
            'VID'   :   vid,
            'PID'   :   pid,
            'iSerial'   :   '56ef',
            }
        val = serial.tools.get_ports_vid_pid_osx_posix.check_if_port_is_replicator(vid, pid, data)
        self.assertTrue(val)


if __name__ == '__main__':
    unittest.main()
