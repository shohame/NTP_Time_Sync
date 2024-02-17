import subprocess
from datetime import datetime
import ctypes
from ctypes import wintypes

NTP_SERVER_IP = "10.0.0.3"
NTP_SERVER_IP = "10.100.102.24"
NTP_SERVER_PORT = 12349

STR_TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

def str_to_datetime(time_str):
    return datetime.strptime(time_str, STR_TIME_FORMAT)

def datetime_to_str(datetime_obj):
    return datetime_obj.strftime(STR_TIME_FORMAT)

def sent_dt(s, dt_msec):
    s.sendall(str(dt_msec).encode('utf-8'))

def receive_dt(s):
    return s.recv(1024).decode('utf-8')
def receive_time_and_calculate_diff(s):
    server_time_str = s.recv(1024).decode('utf-8')
    datetime_other = str_to_datetime(server_time_str)
    time_diff = (datetime.now() - datetime_other)
    sec_diff = time_diff.total_seconds()
    dt_msec = sec_diff * 1000
    return dt_msec, datetime_other

def send_current_time(s):
    current_time_str = datetime.now().strftime(STR_TIME_FORMAT)
    s.sendall(current_time_str.encode('utf-8'))



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

