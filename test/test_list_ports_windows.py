import unittest
import serial.tools.list_ports_windows as lp_win

class TestListPortsWindows(unittest.TestCase):

    def test_parse_port_info_from_sym_name(self):
        vid = '0000'
        pid = '1111'
        sym_name = "horrible_stuff#VID_%s&PID_%s#12345678901234567890", %(pid, vid)
        portBlob = 'com13'
        expected_sym = {
                "iSerial"   :   '12345678901234567890'
                ,"PID"       :   int(pid, 16),
                ,"VID"       :   int(vid, 16),
                ,'Port'	     :   portBlob
                }
        portdict = lp_win.portdict_from_sym_name(sym_name,portBlob)
        self.assertEqual(portdict, expected_sym)

    def test_get_path(self):
        vid = lp_win.convert_to_16_bit_hex(0)
        pid = lp_win.convert_to_16_bit_hex(1)
        expected_path = 'SYSTEM\\CurrentControlSet\\Enum\\USB\\VID_%s&PID_%s' %(vid, pid)
        got_path = lp_win.get_path(vid, pid)
        self.assertEqual(expected_path, got_path)

class TestConvertTo16BitHex(unittest.TestCase):

    def test_convert_to_16_bit_hex_bad_values(self):
        cases =[
            -1,   #Too Small!!
            65536,#Too Big!!
            ]
        for case in cases:
            self.assertRaises(ValueError, lp_win.convert_to_16_bit_hex, case)

    def test_convert_to_16_bit_hex(self):
        cases = [
        ['0000', 0],
        ['0001', 1],
        ['FFFF', 65535],
        ['F0F0', 61680],
        ]
        for case in cases:
            self.assertEqual(case[0], lp_win.convert_to_16_bit_hex(case[1]))

if __name__ == '__main__':
    unittest.main()
