import unittest
import serial.tools.list_ports_windows as lp_win

class TestListPortsWindows(unittest.TestCase):

    def test_parse_port_info_from_sym_name(self):
        sym_name = "horrible_stuff#PID_0000&VID_1111#12345678901234567890"
        portBlob = {'a':1,'b':2}
        expected_sym = {
                "iSerial"   :   '12345678901234567890'
                ,"PID"       :   '0000'
                ,"VID"       :   '1111'
		,'Port'	     :   portBlob
                }
        portdict = lp_win.portdict_from_sym_name(sym_name,portBlob)
        self.assertEqual(portdict, expected_sym)

    def test_get_path(self):
        vid = '0000'
        pid = '1111'
        expected_path = 'SYSTEM\\CurrentControlSet\\Enum\\USB\\VID_%s&PID_%s' %(vid, pid)
        got_path = lp_win.get_path(vid, pid)
        self.assertEqual(expected_path, got_path)


if __name__ == '__main__':
    unittest.main()
