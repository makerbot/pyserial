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
        vid = 0
        pid = 1
        expected_path = 'SYSTEM\\CurrentControlSet\\Enum\\USB\\VID_%s&PID_%s' %(lp_win.convert_to_16_bit_hex(vid), convert_to_16_bit_hex(pid))
        got_path = lp_win.get_path(vid, pid)
        self.assertEqual(expected_path, got_path)

class TestConvertTo16BitHex(unittest.TestCase):

    def test_convert_to_16_bit_hex_bad_values(self):
        cases =[
            -1,   #Negative numbers = Bad
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
            self.assertEqual(case[1], lp_win.convert_to_16_bit_hex(case[0]))

if __name__ == '__main__':
    unittest.main()
