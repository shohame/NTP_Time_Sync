import subprocess
from datetime import datetime
import ctypes
from ctypes import wintypes
import time
from datetime import timedelta
from NTP_Parameters import *


STR_TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


def update_computer_current_time_with_a_delta_msec(real_dt_msec):
    datetime_current_time = datetime.now()
    lt_tz = datetime_current_time.astimezone()
    utc_offset_seconds = lt_tz.utcoffset().total_seconds() if lt_tz.utcoffset() else 0    # Getting the UTC offset in seconds
    msec_from_current_time = real_dt_msec + utc_offset_seconds*1000
    datetime_to_set = datetime_current_time - timedelta(milliseconds=msec_from_current_time)
    set_system_time_precise(datetime_to_set)

def str_to_datetime(time_str):
    return datetime.strptime(time_str, STR_TIME_FORMAT)

def datetime_to_str(datetime_obj):
    return datetime_obj.strftime(STR_TIME_FORMAT)

def sent_dt(s, dt_msec):
    s.sendall(str(dt_msec).encode('utf-8'))

def receive_dt(s):
    return float(s.recv(1024).decode('utf-8'))

def receive_time_and_calculate_diff(s):
    other_time_str = s.recv(1024).decode('utf-8')
    other_datetime = str_to_datetime(other_time_str)
    time_diff = (datetime.now() - other_datetime)
    sec_diff = time_diff.total_seconds()
    dt_msec = sec_diff * 1000
    return dt_msec, other_datetime

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

