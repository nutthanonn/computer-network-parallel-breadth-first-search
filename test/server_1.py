import time
import json
import threading
import socket
import math


from dotenv import load_dotenv
import os
load_dotenv()


HEADER = 64
HOST = os.getenv('HOST')
PORT = 8080
MAX_NODE = int(os.getenv('MAX_NODE'))
SERVER_NAME = '1'
PORT_COLLECTION = ['192.168.1.105', '192.168.1.105', '192.168.1.105', '192.168.1.105']

ADDR = (HOST, PORT)
FORMAT = 'utf-8'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)
path_collection = []


def send(ip, port, recv=None):
    message = recv.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    client.send(send_length)
    client.send(message)


def handle_client(conn, addr):
    connected = True

    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                msg = json.loads(msg)

                if SERVER_NAME not in msg['node']:
                    msg['node'].append(SERVER_NAME)
                    msg['weight'] += msg['graph'][msg['node'][-2]][SERVER_NAME]

                if len(msg['node']) == MAX_NODE:
                    if msg['node'][0] != SERVER_NAME:
                        print(
                            f"Send to {msg['node'][0]}, Node Path: {msg['node']}, Weight: {msg['weight']}")
                        send(
                            PORT_COLLECTION[int(msg['node'][0])-1], 8080, json.dumps(msg))  # send to server 1 (port 8080)
                    else:
                        path_collection.append(
                            f"Node{SERVER_NAME} Path: {msg['node']}, Weight: {msg['weight']}")
                        if len(path_collection) == math.factorial(MAX_NODE-1):
                            print(path_collection)
                else:
                    for node, val in enumerate(PORT_COLLECTION):
                        if str(node+1) not in msg['node']:
                            print(f"send to {val}{node}")
                            time.sleep(1)

                            send(val, node+8080, json.dumps(msg))
        except Exception as e:
            print(e)
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