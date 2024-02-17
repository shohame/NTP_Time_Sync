import socket

import time
from datetime import timedelta, datetime
from NTP_common import *
import platform


def ntp_client(server_host, server_port):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((server_host, server_port))

        dt_msec, datetime_server = receive_time_and_calculate_diff(s)
        send_current_time(s)
        server_dt_msec = receive_dt(s)

    return datetime_server, server_dt_msec


def test_time_diff(server_host, server_port):
    datetime_server, server_dt_msec = ntp_client(server_host, server_port)
    time_diff = (datetime.now() - datetime_server)
    sec_diff = time_diff.total_seconds()
    msec_diff = sec_diff * 1000
#    print(f"Server time is: {datetime_server}; the difference is {msec_diff} ms; server diff is {server_dt_msec} ms.")
    real_dt_msec = (msec_diff - server_dt_msec) / 2
    datetime_current_time = datetime.now()

    lt_tz = datetime_current_time.astimezone()

    # Getting the UTC offset in seconds
    utc_offset_seconds = lt_tz.utcoffset().total_seconds() if lt_tz.utcoffset() else 0

    # substitute real_dt_msec from datetime_current_time:
    datetime_to_set = datetime_current_time - timedelta(milliseconds=real_dt_msec+utc_offset_seconds*1000)
    set_system_time_precise(datetime_to_set)

    while(True):
        datetime_server, server_dt_msec = ntp_client(server_host, server_port)
        time_diff = (datetime.now() - datetime_server)
        sec_diff = time_diff.total_seconds()
        msec_diff = sec_diff * 1000
        print(f"Server time is: {datetime_server}; the difference is {msec_diff} ms; server diff is {server_dt_msec} ms.")

        time.sleep(1)

if __name__ == "__main__":


 #   NTP_client(server_host=NTP_SERVER_IP, server_port=NTP_SERVER_PORT, do_set_time=True)
    test_time_diff(server_host=NTP_SERVER_IP , server_port=NTP_SERVER_PORT)


