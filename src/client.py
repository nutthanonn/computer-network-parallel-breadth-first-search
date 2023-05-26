import json
import socket

HEADER = 64
HOST = '192.168.1.105'
PORT = 8080
# ADDR = (HOST, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(ADDR)



def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    # print(client.recv(2048).decode(FORMAT))


graph = {
    'node': ["1"],
    'weight': 0,
    'graph': {
        "1": {"2": 1, "3": 3, "4": 1},
        "2": {"1": 1, "3": 2, "4": 2},
        "3": {"1": 3, "2": 2, "4": 1},
        "4": {"1": 1, "2": 2, "3": 1}
    }
}

# graph = {
#     'node': ["1"],
#     'weight': 0,
#     'graph': {
#         "1": {"2": 1, "3": 3},
#         "2": {"1": 1, "3": 2},
#         "3": {"1": 3, "2": 2},
#     }
# }

# graph = {
#     'node': ["1"],
#     'weight': 0,
#     'graph': {
#         "1": {"2": 2},
#         "2": {"1": 2},
#     }
# }

for i in range(4):
    client.connect((HOST,PORT+i))
    graph["node"]=[str(i+1)]
    send(json.dumps(graph))
    client.close()
