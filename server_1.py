"""
        _                 ______   ______               ___    _        _______  _______  _______        
       ( (    /||\     /|/ ___  \ / ___  \ |\     /|   /   )  ( (    /|(  __   )(  ___  )(  ___  )       
       |  \  ( || )   ( |\/   )  )\/   )  )| )   ( |  / /) |  |  \  ( || (  )  || (   ) || (   ) |       
       |   \ | || |   | |    /  /     /  / | (___) | / (_) (_ |   \ | || | /   || |   | || |   | |       
       | (\ \) || |   | |   /  /     /  /  |  ___  |(____   _)| (\ \) || (/ /) || |   | || |   | |       
       | | \   || |   | |  /  /     /  /   | (   ) |     ) (  | | \   ||   / | || | /\| || | /\| |       
       | )  \  || (___) | /  /     /  /    | )   ( |     | |  | )  \  ||  (__) || (_\ \ || (_\ \ |       
 _____ |/    )_)(_______) \_/      \_/     |/     \|     (_)  |/    )_)(_______)(____\/_)(____\/_) _____ 
(_____)                                                                                           (_____)

"""


"""
!!!!!! CONFIG !!!!!!

HEADER =
HOST =
PORT =
ADDR =
FORMAT =
DISCONNECT_MESSAGE =
MAX_NODE =
SERVER_NAME =

"""


import socket
import threading
import json
import time
import math
HEADER = 64
HOST = '0.0.0.0'
PORT = 3000
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
MAX_NODE = 3
SERVER_NAME = "1"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)


def send(port, recv=None):
    message = recv.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, port+3000))
    client.send(send_length)
    client.send(message)

    recv = client.recv(2048).decode(FORMAT)

    return recv


def handle_client(conn, addr):

    try:
        print(f'Conn from: {addr}')

        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                msg = json.loads(msg)

                if msg == DISCONNECT_MESSAGE:
                    connected = False

                if SERVER_NAME not in msg['node']:
                    msg['node'].append(SERVER_NAME)
                    msg['weight'] += msg['graph'][msg['node'][-2]][SERVER_NAME]

                col_path = []

                if len(msg['node']) == MAX_NODE:
                    msg['weight'] += msg['graph'][SERVER_NAME][msg['node'][0]]
                    print(
                        f'Visited: {msg["node"]}, Weight: {msg["weight"]}')
                    conn.send(json.dumps(msg).encode(FORMAT))
                    print("="*20)
                else:
                    for visited in range(MAX_NODE):
                        if str(visited+1) not in msg['node']:
                            time.sleep(1)
                            recv = send(visited, json.dumps(msg))

                            if len(msg['node']) == 1:
                                j = json.loads(recv)
                                col_path.append(
                                    [f'Path: {j["node"]}', f"Weight: {j['weight']}"])

                                if len(col_path) == math.factorial(MAX_NODE-1):
                                    temp = [str(x) for x in col_path]
                                    conn.send("\n".join(temp).encode(FORMAT))

                            else:
                                conn.send(recv.encode(FORMAT))

                            print("="*20)

    except Exception as e:
        print(f'Error occured: {e}')
        conn.close()
    print("="*30)


def main():
    s.listen(5)
    print(f'Server is listening on {HOST}:{PORT}')
    while True:
        conn, addr = s.accept()
        # print(f'Connected to {addr}')
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == '__main__':
    print('Server_1 started')
    main()
