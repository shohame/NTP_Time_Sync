import socket

import subprocess
import time
from datetime import datetime
import ctypes
from ctypes import wintypes
from NTP_common import *
import platform

# Define the SYSTEMTIME structure
class SYSTEMTIME(ctypes.Structure):
    _fields_ = [
        ("wYear", wintypes.WORD),
        ("wMonth", wintypes.WORD),
        ("wDayOfWeek", wintypes.WORD),
        ("wDay", wintypes.WORD),
        ("wHour", wintypes.WORD),
        ("wMinute", wintypes.WORD),
        ("wSecond", wintypes.WORD),
        ("wMilliseconds", wintypes.WORD),
    ]

def set_system_time_precise(datetime_obj):
    st = SYSTEMTIME()
    st.wYear = datetime_obj.year
    st.wMonth = datetime_obj.month
    st.wDay = datetime_obj.day
    # wDayOfWeek is automatically recalculated by Windows, so it's set to 0
    st.wHour = datetime_obj.hour
    st.wMinute = datetime_obj.minute
    st.wSecond = datetime_obj.second
    st.wMilliseconds = int(datetime_obj.microsecond / 1000)  # Convert microseconds to milliseconds

    # Load the kernel32 library
    kernel32 = ctypes.windll.kernel32
    kernel32.SetSystemTime.argtypes = [ctypes.POINTER(SYSTEMTIME)]

    # Set system time (requires administrative privileges)
    if not kernel32.SetSystemTime(ctypes.byref(st)):
        raise ctypes.WinError()

def set_system_time_windows(time_str):
    # Convert the time string to datetime object assuming the format '%Y-%m-%d %H:%M:%S'
    new_time = datetime.strptime(time_str, STR_TIME_FORMAT)
    # Setting date
    subprocess.run(['date', new_time.strftime('%m-%d-%Y')], shell=True)
    # Setting time
    subprocess.run(['time', new_time.strftime('%H:%M:%S')], shell=True)


# Example usage
# set_system_time_precise(2024, 2, 14, 12, 34, 56, 123)
def time_client(server_host, server_port, do_set_time=False):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_host, server_port))
        server_time_str = s.recv(1024).decode('utf-8')
    print(f"Server time is: {server_time_str}")

    dt_server = datetime.strptime(server_time_str, STR_TIME_FORMAT)

    if do_set_time:
        if 'windows' in platform.system().lower():
            set_system_time_precise(dt_server)
          #  set_system_time_windows(server_time_str)
        else:
            # set_system_time_linux(server_time)
            pass
    return dt_server


def test_time_diff(server_host, server_port):

    while(True):
        dt_server_time = time_client(server_host, server_port, do_set_time=False)
        time_diff = (datetime.now() - dt_server_time)
        sec_diff = time_diff.total_seconds()
        msec_diff = sec_diff * 1000
        print(f"Server time is: {dt_server_time} and the difference is {msec_diff} ms.")

        time.sleep(1)

if __name__ == "__main__":

    SERV_IP = "10.0.0.3"
    SERV_PORT = 6000

    time_client(server_host=NTP_SERVER_IP , server_port=NTP_SERVER_PORT, do_set_time=True)
    test_time_diff(server_host=NTP_SERVER_IP , server_port=NTP_SERVER_PORT)


