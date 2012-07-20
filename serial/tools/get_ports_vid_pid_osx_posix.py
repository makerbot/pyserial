import re

def get_info_from_serial_identifier(identifier_string):
    data = {}
    try:
        vid, pid, serial_number = re.search('VID:PID=([0-9A-Fa-f]*):([0-9A-Fa-f]*) SNR=(\w*)', identifier_string).groups()
        data['VID'] = int(vid, 16)
        data['PID'] = int(pid, 16)
        data['iSerial'] = serial_number
    except AttributeError:
        pass
    return data   

def check_if_port_is_replicator(vid, pid, data):
    val = False
    try:
        if data['VID'] == vid and data['PID'] == pid:
            val = True
    except KeyError:
        pass
    return val

def get_ports_by_vid_pid(vid, pid):
    """Given a VID and PID value, return ports 
    that have those values.

    @param str vid: The VID value for a port
    @param str pid: The PID value for a port
    @return iterator: Ports that are currently active with these VID/PID values
    """
    ports = comports()
    for port in ports:
        data = get_info_from_serial_identifier(port[-1])
        if check_if_port_is_replicator(vid, pid, data):
            data['PORT'] = port[0]
            yield data
