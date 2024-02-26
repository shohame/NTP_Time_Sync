import subprocess
from datetime import datetime
import ctypes
from ctypes import wintypes
from datetime import timedelta
import platform


STR_TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


def update_computer_current_time_with_a_delta_msec(real_dt_msec):
    datetime_current_time = datetime.now()
    if platform.system() == 'Windows':
        lt_tz = datetime_current_time.astimezone()
        utc_offset_seconds = lt_tz.utcoffset().total_seconds() if lt_tz.utcoffset() else 0    # Getting the UTC offset in seconds
        msec_from_current_time = real_dt_msec + utc_offset_seconds * 1000
    else: # Linux
        msec_from_current_time = real_dt_msec
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

CLOCK_REALTIME = 0
class timespec(ctypes.Structure):
    _fields_ = [("tv_sec", ctypes.c_long), ("tv_nsec", ctypes.c_long)]

def set_system_time_precise(datetime_obj):
    if platform.system() == 'Windows':

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
    else: # Linux:
        timestamp = datetime_obj.timestamp()
        sec = int(timestamp)
        nsec = int((timestamp - sec) * 1e9)  # Convert remainder to nanoseconds

        # Prepare timespec structure
        ts = timespec(sec, nsec)

        # Load the library and set argument types
        librt = ctypes.CDLL('librt.so.1', use_errno=True)
        librt.clock_settime.argtypes = [ctypes.c_int, ctypes.POINTER(timespec)]

        # Set system time (requires root privileges)
        if librt.clock_settime(CLOCK_REALTIME, ctypes.byref(ts)) != 0:
            errno = ctypes.get_errno()
            raise OSError(errno, f"Failed to set system time: {os.strerror(errno)}")

