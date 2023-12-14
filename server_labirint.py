
import socket
import random

class JocLabirint:
    def __init__(self):
        self.maze_models = [
            "# # # # # # # # # #",
            "#         # M    # #",
            "#         #        #",
            "#   #  #  #        #",
            "#   #          # # #",
            "#   #     #    #   #",
            "# J          #   # #",
            "# #   #      # #   #",
            "#   # # #    #     #",
            "# # # # #    # # # #"
            # Define other maze models here...
        ]
        self.player_pos = None
        self.monster_pos = None
        self.exit_pos = None
        self.moves = 0

    def start_game(self):
        self.moves = 0
        self.choose_maze()
        self.place_objects()
        return self.display_maze()

    def choose_maze(self):
        self.current_maze = random.choice(self.maze_models)

    def place_objects(self):
        self.player_pos = self.find_empty_position()
        self.monster_pos = self.find_empty_position(distance_from_player=3)
        self.exit_pos = self.find_empty_position(min_distance_from_player=3)
        self.current_maze = self.update_maze()

    def find_empty_position(self, distance_from_player=0, min_distance_from_player=0):
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)

            if self.current_maze[y][x] == ' ' and \
               (self.player_pos is None or abs(x - self.player_pos[0]) + abs(y - self.player_pos[1]) >= distance_from_player) and \
               (min_distance_from_player == 0 or abs(x - self.player_pos[0]) + abs(y - self.player_pos[1]) >= min_distance_from_player):
                return x, y

    def update_maze(self):
        updated_maze = [list(row) for row in self.current_maze]
        x, y = self.player_pos
        updated_maze[y][x] = 'J'
        x, y = self.monster_pos
        updated_maze[y][x] = 'M'
        x, y = self.exit_pos
        updated_maze[y][x] = 'E'
        return ["".join(row) for row in updated_maze]

    def display_maze(self):
        return "\n".join(self.current_maze)

    def move_player(self, direction):
        if self.player_pos is None:
            return "Jocul nu a început. Trimiteți comanda 'START' pentru a începe jocul."

        x, y = self.player_pos

        if direction == 'U' and y > 0 and self.current_maze[y-1][x] != '#':
            y -= 1
        elif direction == 'D' and y < 9 and self.current_maze[y+1][x] != '#':
            y += 1
        elif direction == 'L' and x > 0 and self.current_maze[y][x-1] != '#':
            x -= 1
        elif direction == 'R' and x < 9 and self.current_maze[y][x+1] != '#':
            x += 1

        self.player_pos = (x, y)
        self.moves += 1

        if self.player_pos == self.exit_pos:
            return f'Ai reușit! Ai ieșit din labirint în {self.moves} mișcări'
        elif self.player_pos == self.monster_pos:
            return f'Ai picat pradă monstrului din labirint... ai pierdut jocul. Încearcă din nou!'
        else:
            return self.display_maze()

class ServerTCP:
    def __init__(self, host='127.0.0.1', port=8888):
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


server = ServerTCP()
server.start()
