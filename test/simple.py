import socket
import threading

import os
from dotenv import load_dotenv

load_dotenv()

HEADER = 64
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
SERVER_NAME = os.getenv('SERVER_NAME')

FORMAT = 'utf-8'
ADDR = (HOST, PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)


def send(ip, recv=None):
    message = recv.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, 8080))
    client.send(send_length)
    client.send(message)

    recv = client.recv(2048).decode(FORMAT)

    return recv


def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected.')

    if SERVER_NAME == '2':
        conn.send(f'from Conn2'.encode(FORMAT))
    else:
        recv = send('172.20.0.3', 'from Conn1')
        conn.send(f'{recv} Conn1'.encode(FORMAT))
    conn.close()


def main():
    s.listen(5)
    print(f'Server is listening on {HOST}:{PORT}')
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == '__main__':
    print(f'Server {SERVER_NAME} started')
    main()
