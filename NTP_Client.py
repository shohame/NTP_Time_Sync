import socket

import time
from datetime import timedelta, datetime
from NTP_common import *
import platform
from NTP_Parameters import *

def ntp_client(server_host, server_port):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((server_host, server_port))

        client_dt_msec, datetime_server = receive_time_and_calculate_diff(s)
        send_current_time(s)
        server_dt_msec = receive_dt(s)

    real_dt_msec = (client_dt_msec - server_dt_msec) / 2
    return datetime_server, server_dt_msec, client_dt_msec, real_dt_msec


def sync_time_with_server(server_host, server_port):
    print ('-------------------Syncing time with server...------------------')
    server_datetime, server_dt_msec, client_dt_msec, real_dt_msec = ntp_client(server_host, server_port)
    update_computer_current_time_with_a_delta_msec(real_dt_msec)
    server_datetime, server_dt_msec, client_dt_msec, real_dt_msec = ntp_client(server_host, server_port)
    update_computer_current_time_with_a_delta_msec(real_dt_msec)
    server_datetime, server_dt_msec, client_dt_msec, real_dt_msec = ntp_client(server_host, server_port)
    update_computer_duration_msec = real_dt_msec
    for i in range(5):
        server_datetime, server_dt_msec, client_dt_msec, real_dt_msec = ntp_client(server_host, server_port)
        update_computer_current_time_with_a_delta_msec(real_dt_msec + update_computer_duration_msec)
        update_computer_duration_msec += real_dt_msec



def test_time_diff(server_host, server_port):

    sync_time_with_server(server_host, server_port)
    time_gap_count = 0
    delay = 1
    while(True):

        server_datetime, server_dt_msec, client_dt_msec, real_dt_msec = ntp_client(server_host, server_port)
        print(f"Server time is: {server_datetime}; real_dt = {real_dt_msec:2.3}mSec | m from s = {client_dt_msec:2.3}mSec | s from m = {server_dt_msec:2.3}mSec.")
        if abs(real_dt_msec) > SYNC_THRESHOLD_MSEC:
            time_gap_count += 1
            delay = 1
        else:
            time_gap_count = 0
            delay = DELAY_BETWEEN_SYNC_TESTING

        if time_gap_count > 2:
            sync_time_with_server(server_host, server_port)
            time_gap_count = 3

        time.sleep(delay)

if __name__ == "__main__":


 #   NTP_client(server_host=NTP_SERVER_IP, server_port=NTP_SERVER_PORT, do_set_time=True)
    test_time_diff(server_host=NTP_SERVER_IP , server_port=NTP_SERVER_PORT)


