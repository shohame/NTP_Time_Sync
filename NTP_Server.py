import socket
import time
from datetime import datetime
from NTP_common import *
from NTP_Parameters import *

def time_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server started at {host}:{port}. Waiting for connections...")
        while True:
            conn, addr = s.accept()
            conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

            with conn:
                print('Connected by', addr)
                send_current_time(conn)
                dt_msec, _ = receive_time_and_calculate_diff(conn)
                sent_dt(conn, dt_msec)

if __name__ == "__main__":

    time_server(host=NTP_SERVER_IP, port=NTP_SERVER_PORT)