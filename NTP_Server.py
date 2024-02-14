import socket
import time
from datetime import datetime

def time_server(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server started at {host}:{port}. Waiting for connections...")
        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                conn.sendall(current_time.encode('utf-8'))

if __name__ == "__main__":
    time_server()