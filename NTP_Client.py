import socket

import subprocess
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

if __name__ == "__main__":
    time_client()