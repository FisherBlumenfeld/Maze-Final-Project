import pygame
import random
import time

x_offset = 10
y_offset = 10

class MazeBlock:
    def __init__(self):
        self.visited = False
        self.possibleMoves = [] #when a square is visited, append -1 * step to get there, when it visits, append step taken
    def __str__(self):
        return str(self.visited)
    def visit(self):
        self.visited = True
    def addPosMove(self,move):
        self.possibleMoves.append(move)
    def posMoves(self):
        return(self.possibleMoves)

        
class MazeBoard:
    def __init__ (self, width, height):
        self.board = []
        self.height = height
        self.width = width
        for i in range(0,height):
            self.board.append([])
            for j in range(0,width):
                self.board[i].append(MazeBlock())
        
        #pygame stuff
        pygame.init()
        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Maze")
        for y in range(0,self.height):
            for x in range(0,self.width):
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(x_offset+20*x + 2,y_offset+20*y + 2, 16, 16)) #makes white squares on all blocks

        pygame.display.flip()

    def __str__(self):
        for i in range(0,self.height):
            for j in range(0,self.width):
                print(self.board[i][j], end = " ")
            print()
        return ""
    def availableNeighbors(self,x,y):
        neighbors = []
        if (x > 0) and not (self.board[y][x-1].visited):
            neighbors.append((-1,0))
        if (x < self.width - 1) and not (self.board[y][x+1].visited):
            neighbors.append((1,0))
        if (y > 0) and not (self.board[y-1][x].visited):
            neighbors.append((0,-1))
        if (y < self.height-1) and not (self.board[y+1][x].visited):
            neighbors.append((0,1))
        return neighbors
    def recursiveGen(self,x,y,delay):
        self.board[y][x].visit()
        while (self.availableNeighbors(x,y) != []):
            step = random.choice(self.availableNeighbors(x,y)) #picks random available neighbor to step to
            self.board[step[1] + y][step[0] + x].visit() #marks stepped to block as visited
            self.board[y][x].addPosMove(step) #adds next step to possible steps
            self.board[y+step[1]][x+step[0]].addPosMove((step[0]*-1, step[1]*-1)) #adds backwards step to possible moves of next square
            
            pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(x_offset+20*x + 2,y_offset+20*y + 2, 16, 16)) #draws red square on current location
            pygame.display.flip()

            time.sleep(delay) #waits for delay to allow user to see drawn red square

            pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(x_offset+20*x + 2,y_offset+20*y + 2, 16, 16)) #returns to white box

            
            if -1 not in step: #connects stepped to box 
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(x_offset+20*x + 2,y_offset+20*y + 2, 16+4*step[0], 16+4*step[1])) 
            elif step == (-1,0):
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(x_offset+20*x - 2,y_offset+20*y + 2, 4, 16))
            else:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(x_offset+20*x + 2,y_offset+20*y - 2, 16, 4))
            
            pygame.display.flip()

            self.recursiveGen(step[0] + x,step[1] + y,delay) #repeats for stepped to neighbor
            
class player: #class for the player object
    def __init__(self, b): #sets player
        self.xCoord = 0
        self.yCoord = 0
        self.maze = b
        pygame.draw.rect(self.maze.screen, (255, 0, 0), pygame.Rect(x_offset+20*self.xCoord + 2, y_offset+20*self.yCoord + 2, 16, 16))

    def move(self, direction): #moves player
        tempX = self.xCoord #temp coords used for screen update
        tempY = self.yCoord
        move = False
        if (direction == pygame.K_w) and ((0,-1) in self.maze.board[tempY][tempX].posMoves()): #when 'w' key pressed move up
            self.yCoord += -1
            move = True
        elif (direction == pygame.K_a) and ((-1, 0) in self.maze.board[tempY][tempX].posMoves()): #when 'a' key pressed move left
            self.xCoord += -1
            move = True
        elif (direction == pygame.K_s) and ((0, 1) in self.maze.board[tempY][tempX].posMoves()): #when 's' key pressed move down
            self.yCoord += 1
            move = True
        elif (direction == pygame.K_d) and ((1, 0) in self.maze.board[tempY][tempX].posMoves()): #when 'd' key pressed move right
            self.xCoord += 1
            move = True
        else:
            move = False

        if move: #checks if a move was possible and completed and update rectangle location
            pygame.draw.rect(self.maze.screen, (255, 255, 255), pygame.Rect(x_offset+20*tempX + 2, y_offset+20*tempY + 2, 16, 16))
            pygame.draw.rect(self.maze.screen, (255, 0, 0), pygame.Rect(x_offset+20*self.xCoord + 2, y_offset+20*self.yCoord + 2, 16, 16))

game = True
height = 27
width = 36
delay = 0.01
while game: #while loop for infinite games to be played
    maze = MazeBoard(width,height)
    time.sleep(1)
    maze.recursiveGen(random.randint(0, width), random.randint(0, height),delay) #starts maze generation
    pygame.draw.rect(maze.screen,(0,255,0),pygame.Rect(x_offset+20*(width-1) + 2,y_offset+20*(height-1) + 2, 16, 16))
    player1 = player(maze)
    run = True     
    while run: #while loop for events in each individual maze
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #shutdown the game when window is closed
                run = False
                game = False
        
            if event.type == pygame.KEYDOWN: #register keystroke
                player1.move(event.key)
        
        if player1.xCoord == 35 and player1.yCoord == 26: #check for player reaching end of the maze
            run = False
        pygame.display.update()

pygame.quit()
