import time
import json
import threading
import socket
import math
import logging

from dotenv import load_dotenv
import os
load_dotenv()

HEADER = 64
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
MAX_NODE = int(os.getenv('MAX_NODE'))
SERVER_NAME = os.getenv('SERVER_NAME')
PORT_COLLECTION = ['172.20.0.2', '172.20.0.3', '172.20.0.4', '172.20.0.5']

GRAPH = {
    'node': ["1"],
    'weight': 0,
    'graph': {
        "1": {"2": 1, "3": 3, "4": 1},
        "2": {"1": 1, "3": 2, "4": 2},
        "3": {"1": 3, "2": 2, "4": 1},
        "4": {"1": 1, "2": 2, "3": 1}
    }
}

FORMAT = 'utf-8'
ADDR = (HOST, PORT)
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
                            PORT_COLLECTION[int(msg['node'][0])-1], 8080, json.dumps(msg))
                    else:
                        path_collection.append(
                            f"Node Path: {msg['node']}, Weight: {msg['weight']}")
                        if len(path_collection) == math.factorial(MAX_NODE-1):
                            logging.warning(path_collection)
                else:
                    for node, val in enumerate(PORT_COLLECTION):
                        if str(node+1) not in msg['node']:
                            time.sleep(1)
                            print(f"send to {val}")

                            send(val, 8080, json.dumps(msg))
        except Exception as e:
            logging.warning(e)
    conn.close()


def client_send():
    time.sleep(5)

    GRAPH["node"] = [SERVER_NAME]
    send(HOST, 8080, json.dumps(GRAPH))


def main():
    s.listen(5)

    client_send()
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == '__main__':
    print(f'Server {SERVER_NAME} started')
    main()
