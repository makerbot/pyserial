import re

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
    data = {'Port':port}
    try:
        vid, pid, serial_number = re.search('VID:PID=([0-9A-Fa-f]*):([0-9A-Fa-f]*) SNR=(\w*)', identifier_string).groups()
        data['VID'] = vid 
        data['PID'] = pid
        data['iSerial'] = serial_number
    except AttributeError:
        pass
    return data   


def list_ports_by_vid_pid(vid, pid):
    """ Given a VID and PID value, scans for available port, and
	if matches are found, returns a dict of 'VID/PID/iSerial/Port'
	that have those values.

    @param str vid: The VID value for a port
    @param str pid: The PID value for a port
    @return iterator: Ports that are currently active with these VID/PID values
    """
    #Get a list of all ports
    ports = comports()
    for port in ports:
        #Parse some info out of the identifier string
        data = portdict_from_port(port[-1])
        try: 
            if data['VID'] == vid and data['PID'] == pid:
            	yield data
	except:
		pass
