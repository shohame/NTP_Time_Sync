import socket

import subprocess
import time
from datetime import datetime


def set_system_time_windows(time_str):
    # Convert the time string to datetime object assuming the format '%Y-%m-%d %H:%M:%S'
    new_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    # Setting date
    subprocess.run(['date', new_time.strftime('%m-%d-%Y')], shell=True)
    # Setting time
    subprocess.run(['time', new_time.strftime('%H:%M:%S')], shell=True)


def time_client(server_host='localhost', server_port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_host, server_port))
        server_time = s.recv(1024).decode('utf-8')
        print(f"Server time is: {server_time}")
        # Here, you would adjust the client's system clock based on server_time
        # This step is platform dependent and requires admin rights
        set_system_time_windows(server_time)

def test_time_diff(server_host='localhost', server_port=12345):

    while(True):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_host, server_port))
            server_time = s.recv(1024).decode('utf-8')
            sec_diff = (datetime.now() - datetime.strptime(server_time, '%Y-%m-%d %H:%M:%S')).seconds
            msec_diff = sec_diff * 1000 + (datetime.now() - datetime.strptime(server_time, '%Y-%m-%d %H:%M:%S')).microseconds / 1000

            print(f"Server time is: {server_time} and the difference is {msec_diff} ms.")

        time.sleep(1)

if __name__ == "__main__":

    SERV_IP = "10.0.0.3"
    SERV_PORT = 6000

    time_client(server_host=SERV_IP , server_port=SERV_PORT)
    test_time_diff(server_host=SERV_IP , server_port=SERV_PORT)