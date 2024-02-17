import socket

import subprocess
import time
from datetime import datetime
import ctypes
from ctypes import wintypes
from NTP_common import *
import platform


def ntp_client(server_host, server_port, do_set_time=False):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((server_host, server_port))

        dt_msec, datetime_server = receive_time_and_calculate_diff(s)
        send_current_time(s)
        server_dt_msec = receive_dt(s)

    if do_set_time:
        if 'windows' in platform.system().lower():
            set_system_time_precise(datetime_server)
          #  set_system_time_windows(server_time_str)
        else:
            # set_system_time_linux(server_time)
            pass
    return datetime_server, server_dt_msec


def test_time_diff(server_host, server_port):

    while(True):
        datetime_server, server_dt_msec = NTP_client(server_host, server_port, do_set_time=False)
        time_diff = (datetime.now() - datetime_server)
        sec_diff = time_diff.total_seconds()
        msec_diff = sec_diff * 1000
        print(f"Server time is: {dt_server_time}; the difference is {msec_diff} ms; server diff is {server_dt_msec} ms.")

        time.sleep(1)

if __name__ == "__main__":


 #   NTP_client(server_host=NTP_SERVER_IP, server_port=NTP_SERVER_PORT, do_set_time=True)
    test_time_diff(server_host=NTP_SERVER_IP , server_port=NTP_SERVER_PORT)


