import re
import uuid
from serial.tools.list_ports import comports

""" 
Contains tools for taking a serial object from the standard serial module,
and intellegently parse out and use PID/VID and iSerial values from it
"""   

def portdict_from_port(port):
    """
    Given a port object from serial.comport() create a vid/pid/iSerial/port dict if possible

    @param str identifier_string: String retrieved from a serial port
    @return dict: A dictionary VID/PID/iSerial/Port.  On parse error dict contails only 'Port':port'
    """
    identifier_string = port[-1]
    data = {'blob':port}
    data['port'] = port[0]
    try:
        fields= ['0x87654321', '0xd34d', '0x4360', '0xba', '0x18', '0x00254ba7e5d0']
	mgroup = re.search('VID:PID=([0-9A-Fa-f]{4}):([0-9A-Fa-f]{4}) SNR=([0-9A-Fa-f]{12})', identifier_string).groups()
        vid, pid, serial_number= mgroup[0],mgroup[1],mgroup[2]
        data['VID'] = int(vid,16)
        data['PID'] = int(pid,16)
        data['iSerial'] = serial_number
        if len(serial_number) >= 12:
        	fields[5] = '0x' + serial_number[-12:]
	if len(serial_number) >= 20:
                fields[0] = '0x' + serial_number[:8]
        dFields = [int(i,16) for i in fields]
        data['uuid'] = uuid.UUID(fields=dFields)

    except AttributeError:
        pass
    return data   



def list_ports_by_vid_pid(vid=None, pid=None):
    """ Given a VID and PID value, scans for available port, and
	if matches are found, returns a dict of 'VID/PID/iSerial/Port'
	that have those values.

    @param int vid: The VID value for a port
    @param int pid: The PID value for a port
    @return iterator: Ports that are currently active with these VID/PID values
    """
    #Get a list of all ports
    ports = comports()
    return filter_ports_by_vid_pid(ports, vid, pid)

def filter_ports_by_vid_pid(ports,vid=None,pid=None):
    """ Given a VID and PID value, scans for available port, and
	f matches are found, returns a dict of 'VID/PID/iSerial/Port'
	that have those values.

    @param list ports: Ports object of valid ports
    @param int vid: The VID value for a port
    @param int pid: The PID value for a port
    @return iterator: Ports that are currently active with these VID/PID values
    """
    for port in ports:
        #Parse some info out of the identifier string
        try: 
            data = portdict_from_port(port)
            if vid == None or data.get('VID',None) == vid:
                if  pid == None or data.get('PID',None) == pid:
            	    yield data
        except Exception as e:
            pass
