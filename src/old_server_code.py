import socket
import threading
import json
import time


HEADER = 64
HOST = '0.0.0.0'
PORT = 3003
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
MAX_NODE = 4
SERVER_NAME = "4"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)


def send(port, recv=None):
    message = recv.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, port))
    client.send(send_length)
    client.send(message)

    recv = client.recv(2048).decode(FORMAT)

    return recv


def handle_client(conn, addr):
    connected = True

    isPass = False

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

                for node in range(MAX_NODE):
                    if str(node+1) not in msg['node']:
                        time.sleep(1)
                        recv = send(node + 3000, json.dumps(msg))

                        recv = json.loads(recv)

                        if len(recv['node']) == MAX_NODE:
                            if recv['node'][0] != SERVER_NAME:
                                conn.send(json.dumps(recv).encode(FORMAT))
                            else:
                                print(f"finish path {node+1}")
                        isPass = True

                # last node
                if not isPass:
                    if len(msg['node']) == MAX_NODE and msg['node'][0] != SERVER_NAME:
                        conn.send(json.dumps(msg).encode(FORMAT))
                    print(f'Path: {msg["node"]}')
        except:
            pass
    conn.close()


def main():
    s.listen(5)
    print(f'Server is listening on {HOST}:{PORT}')
    while True:
        conn, addr = s.accept()
        # print(f'Connected to {addr}')
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == '__main__':
    print(f'Server {SERVER_NAME} started')
    main()
