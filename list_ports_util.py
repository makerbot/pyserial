import serial.tools.list_ports as lp

print list(lp.list_ports_by_vid_pid())