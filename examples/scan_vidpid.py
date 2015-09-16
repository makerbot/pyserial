#! /usr/bin/env python
"""\
Scan for serial ports. Linux specific variant that also includes USB/Serial
adapters.

Part of pySerial (http://pyserial.sf.net)
(C) 2009 <cliechti@gmx.net>
"""

import sys

sys.path.insert(0,'.')

import serial
try:
    import serial.tools.list_ports as lp
except ImportError as e:  
    print("not using serial containing list_ports tools")
    print(e)
    exit(-1)
except ImportError as e:  
    print("not using serial containing list_ports tools")
    print(e)
    exit(-1)
if __name__=='__main__':

    print("Usage: python scan_vidpid.py VendorId ProductId")
    print("Found ports:")
    
    pid = None
    vid = None
    if len(sys.argv) > 1:
      vid = int(sys.argv[1],16)
    if len(sys.argv) > 2:
      pid = int(sys.argv[2],16)
    print("searcing for vid: " + str(vid) + " pid: " + str(pid))
    for portDict in lp.list_ports_by_vid_pid(vid,pid):
      print(portDict)
	
