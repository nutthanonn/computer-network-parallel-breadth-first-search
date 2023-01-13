import socket
import threading

HEADER = 64
HOST = 'localhost'
PORT = 3000
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)


def handle_client(conn, addr):
    print(f'New connection: {addr}')

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f'{addr} {msg}')

    conn.close()


def main():
    s.listen()
    print(f'Server is listening on {HOST}:{PORT}')
    while True:
        conn, addr = s.accept()
        print(f'Connected to {addr}')
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f'Active connections: {threading.activeCount() - 1}')


if __name__ == '__main__':
    print('Server started')
    main()
