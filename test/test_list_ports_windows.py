import unittest
import serial.tools.list_ports_windows

class TestListPortsWindows(unittest.TestCase):

    def test_parse_port_info_from_sym_name(self):
        sym_name = "horrible_stuff#PID_0000&VID_1111#12345678901234567890"
        expected_sym = {
                "iSerial"   :   '12345678901234567890',
                "PID"       :   int('0000', 16),
                "VID"       :   int('1111', 16),
                }
        got_sym = serial.tools.list_ports_windows.parse_port_info_from_sym_name(sym_name)
        self.assertEqual(got_sym, expected_sym)

    def test_get_path(self):
        vid = '0000'
        pid = '1111'
        expected_path = 'SYSTEM\\CurrentControlSet\\Enum\\USB\\VID_%sPID_%s' %(vid, pid)
        got_path = serial.tools.list_ports_windows.get_path(vid, pid)
        self.assertEqual(expected_path, got_path)


if __name__ == '__main__':
    unittest.main()
