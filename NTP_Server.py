import socket
import time
from datetime import datetime
from NTP_common import *


def time_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server started at {host}:{port}. Waiting for connections...")
        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                current_time_str = datetime.now().strftime(STR_TIME_FORMAT)
                print(f"Sending current time: {current_time_str}")
                conn.sendall(current_time_str.encode('utf-8'))


if __name__ == "__main__":

    time_server(host=NTP_SERVER_IP, port=NTP_SERVER_PORT)