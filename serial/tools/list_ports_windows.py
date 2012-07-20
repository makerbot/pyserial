import ctypes
import _winreg as winreg
import itertools
import sets
import re

def ValidHandle(value, func, arguments):
    if value == 0:
        raise ctypes.WinError()
    return value

import serial
from serial.win32 import ULONG_PTR, is_64bit
from ctypes.wintypes import HANDLE
from ctypes.wintypes import BOOL
from ctypes.wintypes import HWND
from ctypes.wintypes import DWORD
from ctypes.wintypes import WORD
from ctypes.wintypes import LONG
from ctypes.wintypes import ULONG
from ctypes.wintypes import LPCSTR
from ctypes.wintypes import HKEY
from ctypes.wintypes import BYTE

NULL = 0
HDEVINFO = ctypes.c_void_p
PCTSTR = ctypes.c_char_p
CHAR = ctypes.c_char
LPDWORD = PDWORD = ctypes.POINTER(DWORD)
#~ LPBYTE = PBYTE = ctypes.POINTER(BYTE)
LPBYTE = PBYTE = ctypes.c_void_p        # XXX avoids error about types
PHKEY = ctypes.POINTER(HKEY)

ACCESS_MASK = DWORD
REGSAM = ACCESS_MASK

def byte_buffer(length):
    """Get a buffer for a string"""
    return (BYTE*length)()

def string(buffer):
    s = []
    for c in buffer:
        if c == 0: break
        s.append(chr(c & 0xff)) # "& 0xff": hack to convert signed to unsigned
    return ''.join(s)


class GUID(ctypes.Structure):
    _fields_ = [
        ('Data1', DWORD),
        ('Data2', WORD),
        ('Data3', WORD),
        ('Data4', BYTE*8),
    ]
    def __str__(self):
        return "{%08x-%04x-%04x-%s-%s}" % (
            self.Data1,
            self.Data2,
            self.Data3,
            ''.join(["%02x" % d for d in self.Data4[:2]]),
            ''.join(["%02x" % d for d in self.Data4[2:]]),
        )

class SP_DEVINFO_DATA(ctypes.Structure):
    _fields_ = [
        ('cbSize', DWORD),
        ('ClassGuid', GUID),
        ('DevInst', DWORD),
        ('Reserved', ULONG_PTR),
    ]
    def __str__(self):
        return "ClassGuid:%s DevInst:%s" % (self.ClassGuid, self.DevInst)
PSP_DEVINFO_DATA = ctypes.POINTER(SP_DEVINFO_DATA)

class SP_DEVICE_INTERFACE_DATA(ctypes.Structure):
    _fields_ = [
        ('cbSize', DWORD),
        ('InterfaceClassGuid', GUID),
        ('Flags', DWORD),
        ('Reserved', ULONG_PTR),
    ]
    def __str__(self):
        return "InterfaceClassGuid:%s Flags:%s" % (self.InterfaceClassGuid, self.Flags)
PSP_DEVICE_INTERFACE_DATA = ctypes.POINTER(SP_DEVICE_INTERFACE_DATA)

PSP_DEVICE_INTERFACE_DETAIL_DATA = ctypes.c_void_p

setupapi = ctypes.windll.LoadLibrary("setupapi")
SetupDiDestroyDeviceInfoList = setupapi.SetupDiDestroyDeviceInfoList
SetupDiDestroyDeviceInfoList.argtypes = [HDEVINFO]
SetupDiDestroyDeviceInfoList.restype = BOOL

SetupDiGetClassDevs = setupapi.SetupDiGetClassDevsA
SetupDiGetClassDevs.argtypes = [ctypes.POINTER(GUID), PCTSTR, HWND, DWORD]
SetupDiGetClassDevs.restype = HDEVINFO
SetupDiGetClassDevs.errcheck = ValidHandle

SetupDiEnumDeviceInterfaces = setupapi.SetupDiEnumDeviceInterfaces
SetupDiEnumDeviceInterfaces.argtypes = [HDEVINFO, PSP_DEVINFO_DATA, ctypes.POINTER(GUID), DWORD, PSP_DEVICE_INTERFACE_DATA]
SetupDiEnumDeviceInterfaces.restype = BOOL

SetupDiGetDeviceInterfaceDetail = setupapi.SetupDiGetDeviceInterfaceDetailA
SetupDiGetDeviceInterfaceDetail.argtypes = [HDEVINFO, PSP_DEVICE_INTERFACE_DATA, PSP_DEVICE_INTERFACE_DETAIL_DATA, DWORD, PDWORD, PSP_DEVINFO_DATA]
SetupDiGetDeviceInterfaceDetail.restype = BOOL

SetupDiGetDeviceRegistryProperty = setupapi.SetupDiGetDeviceRegistryPropertyA
SetupDiGetDeviceRegistryProperty.argtypes = [HDEVINFO, PSP_DEVINFO_DATA, DWORD, PDWORD, PBYTE, DWORD, PDWORD]
SetupDiGetDeviceRegistryProperty.restype = BOOL

SetupDiOpenDevRegKey = setupapi.SetupDiOpenDevRegKey
SetupDiOpenDevRegKey.argtypes = [HDEVINFO, PSP_DEVINFO_DATA, DWORD, DWORD, DWORD, REGSAM]
SetupDiOpenDevRegKey.restype = HKEY

advapi32 = ctypes.windll.LoadLibrary("Advapi32")
RegCloseKey = advapi32.RegCloseKey
RegCloseKey.argtypes = [HKEY]
RegCloseKey.restype = LONG

RegQueryValueEx = advapi32.RegQueryValueExA
RegQueryValueEx.argtypes = [HKEY, LPCSTR, LPDWORD, LPDWORD, LPBYTE, LPDWORD]
RegQueryValueEx.restype = LONG


GUID_CLASS_COMPORT = GUID(0x86e0d1e0L, 0x8089, 0x11d0,
    (BYTE*8)(0x9c, 0xe4, 0x08, 0x00, 0x3e, 0x30, 0x1f, 0x73))

DIGCF_PRESENT = 2
DIGCF_DEVICEINTERFACE = 16
INVALID_HANDLE_VALUE = 0
ERROR_INSUFFICIENT_BUFFER = 122
SPDRP_HARDWAREID = 1
SPDRP_FRIENDLYNAME = 12
ERROR_NO_MORE_ITEMS = 259
DICS_FLAG_GLOBAL = 1
DIREG_DEV = 0x00000001
KEY_READ = 0x20019
REG_SZ = 1

# workaround for compatibility between Python 2.x and 3.x
PortName = serial.to_bytes([80, 111, 114, 116, 78, 97, 109, 101]) # "PortName"

def comports():
    """This generator scans the device registry for com ports and yields port, desc, hwid"""
    g_hdi = SetupDiGetClassDevs(ctypes.byref(GUID_CLASS_COMPORT), None, NULL, DIGCF_PRESENT|DIGCF_DEVICEINTERFACE);
    #~ for i in range(256):
    for dwIndex in range(256):
        did = SP_DEVICE_INTERFACE_DATA()
        did.cbSize = ctypes.sizeof(did)

        if not SetupDiEnumDeviceInterfaces(g_hdi, None, ctypes.byref(GUID_CLASS_COMPORT), dwIndex, ctypes.byref(did)):
            if ctypes.GetLastError() != ERROR_NO_MORE_ITEMS:
                raise ctypes.WinError()
            break

        dwNeeded = DWORD()
        # get the size
        if not SetupDiGetDeviceInterfaceDetail(g_hdi, ctypes.byref(did), None, 0, ctypes.byref(dwNeeded), None):
            # Ignore ERROR_INSUFFICIENT_BUFFER
            if ctypes.GetLastError() != ERROR_INSUFFICIENT_BUFFER:
                raise ctypes.WinError()
        # allocate buffer
        class SP_DEVICE_INTERFACE_DETAIL_DATA_A(ctypes.Structure):
            _fields_ = [
                ('cbSize', DWORD),
                ('DevicePath', CHAR*(dwNeeded.value - ctypes.sizeof(DWORD))),
            ]
            def __str__(self):
                return "DevicePath:%s" % (self.DevicePath,)
        idd = SP_DEVICE_INTERFACE_DETAIL_DATA_A()
        if is_64bit():
            idd.cbSize = 8
        else:
            idd.cbSize = 5
        devinfo = SP_DEVINFO_DATA()
        devinfo.cbSize = ctypes.sizeof(devinfo)
        if not SetupDiGetDeviceInterfaceDetail(g_hdi, ctypes.byref(did), ctypes.byref(idd), dwNeeded, None, ctypes.byref(devinfo)):
            raise ctypes.WinError()

        # hardware ID
        szHardwareID = byte_buffer(250)
        if not SetupDiGetDeviceRegistryProperty(g_hdi, ctypes.byref(devinfo), SPDRP_HARDWAREID, None, ctypes.byref(szHardwareID), ctypes.sizeof(szHardwareID) - 1, None):
            # Ignore ERROR_INSUFFICIENT_BUFFER
            if GetLastError() != ERROR_INSUFFICIENT_BUFFER:
                raise ctypes.WinError()

        # friendly name
        szFriendlyName = byte_buffer(250)
        if not SetupDiGetDeviceRegistryProperty(g_hdi, ctypes.byref(devinfo), SPDRP_FRIENDLYNAME, None, ctypes.byref(szFriendlyName), ctypes.sizeof(szFriendlyName) - 1, None):
            # Ignore ERROR_INSUFFICIENT_BUFFER
            if ctypes.GetLastError() != ERROR_INSUFFICIENT_BUFFER:
                #~ raise IOError("failed to get details for %s (%s)" % (devinfo, szHardwareID.value))
                port_name = None
        else:
            # the real com port name has to read differently...
            hkey = SetupDiOpenDevRegKey(g_hdi, ctypes.byref(devinfo), DICS_FLAG_GLOBAL, 0, DIREG_DEV, KEY_READ)
            port_name_buffer = byte_buffer(250)
            port_name_length = ULONG(ctypes.sizeof(port_name_buffer))
            RegQueryValueEx(hkey, PortName, None, None, ctypes.byref(port_name_buffer), ctypes.byref(port_name_length))
            RegCloseKey(hkey)
            yield string(port_name_buffer), string(szFriendlyName), string(szHardwareID)

    SetupDiDestroyDeviceInfoList(g_hdi)


class VIDPIDAccessError(Exception):
    """a VIDPIDAccessError is indicative of the specific VID/PID
    registry key missing.  This happens if a windows machine has never
    seen a Replicator before.
    """
    def __init__(self):
        pass

class COMPORTAccessError(Exception):
    """A COMPORTAccessError is indicative of the SERIALCOMM key
    missing.  This actually happens every time (I think) windows
    resets.  Its expected the layer on top of this one
    will catch this error and report accordingly.
    """
    def __init__(self):
        pass

def enumerate_recorded_ports_by_vid_pid(vid, pid):
    """Given a port name, checks the dynamically
    linked registries to find the VID/PID values
    associated with this port.
    """
    #Convert pid/hex to upper case hex numbers
    vid = hex(vid).replace('0x', '').upper()
    pid = hex(pid).replace('0x', '').upper()
    path = get_path(vid, pid)
    try:
        #The key is the VID PID address for all possible Rep connections
       key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
    except WindowsError as e:
       raise VIDPIDAccessError
    #For each subkey of key
    for i in itertools.count():
       try:
           #we grab the keys name
           child_name = winreg.EnumKey(key, i) #EnumKey gets the NAME of a subkey
           #Open a new key which is pointing at the node with the info we need
           new_path = "%s\\%s\\Device Parameters" %(path, child_name)
           child_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, new_path)
           #child_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path+'\\'+child_name+'\\Device Parameters')
           comport_info = {}
           #For each bit of information in this new key
           for j in itertools.count():
               try:
                   #Grab the values for a certain index
                   child_values = winreg.EnumValue(child_key, j)
                   comport_info[child_values[0]] = child_values[1]
               #We've reached the end of the tree
               except EnvironmentError:
                  yield comport_info
                  break
       #We've reached the end of the tree
       except EnvironmentError:
           break
  
def get_path(vid, pid):
    """
    The registry path is dependent on the PID values
    we are looking for.

    @param str pid: The PID value in base 16
    @param str vid: The VID value in base 16
    @return str The path we are looking for
    """
    path = "SYSTEM\\CurrentControlSet\\Enum\\USB\\"
    target = "VID_%s&PID_%s" %(vid, pid)
    return path+target

def enumerate_active_serial_ports():
    """ Uses the Win32 registry to return an
    iterator of serial (COM) ports
    existing on this computer.

    NB: When windows resets, it removes the SERIALCOMM key.
    This means that if we try to scan before anything has been
    plugged in, we will raise COMPORTAccessErrors.  Its expected
    that the layer on top of this one will catch those errors
    and report back accordingly.
    """
    path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
    except WindowsError:
        raise COMPORTAccessError

    for i in itertools.count():
        try:
            val = winreg.EnumValue(key, i)
            yield val
        except EnvironmentError:
            break

def parse_port_info_from_sym_name(sym_name):
    """
    Windows stores the VID, PID, iSerial (along with other bits of info)
    in a single string separated by a # sign.  We parse that information out 
    and export it.

    @param str sym_name: The uber-string windows uses as an identifier
    @return list: All the bits of information we need to id a port by its VIP/PID
    """
    return_dict = {}
    sym_list = sym_name.split('#')
    return_dict['iSerial'] = sym_list[2]
    v_p = sym_list[1]
    v_p = v_p.replace('_', '')
    v_p = v_p.split('&')
    v_p.sort() #Windows labels their VID/PIDs, so we sort so we know which is which
    pid = v_p[0]
    pid = pid.replace('PID', '')
    vid = v_p[1]
    vid = vid.replace('VID', '')
    return_dict['PID'] = int(pid, 16)
    return_dict['VID'] = int(vid, 16)
    return return_dict
    

def get_ports_by_vid_pid(vid, pid):
    """
    Given VID and PID values, searched windows' registry keys for all COMPORTS
    that have the same VID PID values, and returns the intersection of those ports
    with the current ports that are being accessed.

    @param str vid: The vendor id # for a usb device
    @param str vid: The product id # for a usb device
    @return iterator: Ports that are currently active with these VID/PID values
    """
    recorded_ports = list(enumerate_recorded_ports_by_vid_pid(vid, pid))
    current_ports = list(enumerate_active_serial_ports())
    for c_port in current_ports:
        for r_port in recorded_ports:
            #If the COM ports are the same
            if c_port[1] == r_port['PortName']:
                #We put, in this order: COM#, ADDRESS, VIP, PID, iSerial
                active_replicator = dict({"PORT":c_port[1], "ADDRESS":c_port[0]}.items() + parse_port_info_from_sym_name(r_port['SymbolicName']).items())
                yield active_replicator

if __name__ == '__main__':
    ports = get_ports_by_vid_pid(int('23C1', 16), int('D314', 16))
    for port in ports:
        print port
