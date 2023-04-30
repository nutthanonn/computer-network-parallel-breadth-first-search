import socket

HEADER = 64
HOST = '0.0.0.0'
PORT = 3002
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


# send('{"node":["1"], "weight": 0, "neighbors": {"2": 1, "3": 2} }')
send('{"node":["3"], "weight": 0, "graph": {"1":{"2": 1, "3": 3}, "2":{"1": 1, "3": 2}, "3": {"1": 3, "2": 2} } }')
