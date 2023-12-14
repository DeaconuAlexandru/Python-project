# server.py

import socket

from server_labirint import JocLabirint


class ServerTCP:
    def __init__(self, host='127.0.0.1', port=8889):
        self.host = host
        self.port = port
        self.game = JocLabirint()

    def start(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((self.host, self.port))
        serverSocket.listen(2)
        print('Serverul TCP asculta pe adresa: ', serverSocket.getsockname())

        while True:
            connectionSocket, clientAddress = serverSocket.accept()
            print('Accesat de catre:', clientAddress)

            message = connectionSocket.recv(1024).decode()

            if message == 'START':
                response = self.game.start_game()
            else:
                response = self.game.move_player(message)

            connectionSocket.send(response.encode())
            connectionSocket.close()

if __name__ == "__main__":
    server = ServerTCP()
    server.start()
