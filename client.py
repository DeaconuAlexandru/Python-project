# client.py

import socket

host = '127.0.0.1'
port = 8889

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((host, port))

message = input('Introduceti mesajul (litere mici): ')
clientSocket.send(message.encode())

while True:
    response = clientSocket.recv(1024).decode()
    print(response)

    if response.startswith("OK"):
        direction = input('Introduceti directia (U, D, L, R): ')
        clientSocket.send(direction.encode())
    elif response.startswith("Ai reusit!") or response.startswith("Ai picat"):
        choice = input('Introduceti "START" pentru un nou joc sau "STOP" pentru a iesi: ')
        clientSocket.send(choice.encode())
        if choice == "STOP":
            break

clientSocket.close()
