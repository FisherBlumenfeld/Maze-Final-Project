import pygame
import random
import time

x_offset = 10
y_offset = 10

class MazeBlock:
    def __init__(self):
        self.visited = False
        self.possibleMoves = [] #stores tuples of potential (x,y) changes out of this square. ie: left = (-1,0)
    def __str__(self): #string func, used for debugging
        return str(self.visited)
    def visit(self): #sets visit = True for use in generation algo
        self.visited = True
    def addPosMove(self,move): #stores valid moves out of this square
        self.possibleMoves.append(move)
    def posMoves(self): 
        return(self.possibleMoves)

        
class MazeBoard:
    def __init__ (self, width, height, wH, wW):
        self.board = []
        self.height = height
        self.width = width
        for i in range(0,height):
            self.board.append([])
            for j in range(0,width):
                self.board[i].append(MazeBlock()) #fills board with lists of MazeBlocks according to height and width
        
        #pygame stuff
        pygame.init()
        self.screen = pygame.display.set_mode((wW,wH)) #initializes pygame screen
        pygame.display.set_caption("Maze")
        for y in range(0,self.height):
            for x in range(0,self.width):
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(x_offset+20*x + 2,y_offset+20*y + 2, 16, 16)) #makes white squares on all blocks

        pygame.display.flip()

    def __str__(self): #string function, used for debugging
        for i in range(0,self.height):
            for j in range(0,self.width):
                print(self.board[i][j], end = " ") 
            print()
        return ""
    def availableNeighbors(self,x,y): #adds tuples of potential moves to neighbors list
        neighbors = []
        if (x > 0) and not (self.board[y][x-1].visited): #leftward
            neighbors.append((-1,0))
        if (x < self.width - 1) and not (self.board[y][x+1].visited): #rightward
            neighbors.append((1,0))
        if (y > 0) and not (self.board[y-1][x].visited): #upward
            neighbors.append((0,-1))
        if (y < self.height-1) and not (self.board[y+1][x].visited): #downward
            neighbors.append((0,1)) 
        return neighbors
    def recursiveGen(self,x,y,delay): #generates maze and updates connections in posMoves all blocks as well as updating graphics of screen to demonstrate algo
        self.board[y][x].visit() #sets to visited to remove from possible neighbors
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
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(x_offset+20*x + 2,y_offset+20*y + 2, 16+4*step[0], 16+4*step[1])) #draws connections to rightward and downward blocks
            elif step == (-1,0):
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(x_offset+20*x - 2,y_offset+20*y + 2, 4, 16)) #draws connection to leftward block
            else:
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(x_offset+20*x + 2,y_offset+20*y - 2, 16, 4)) #draws connection to upward block
            
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
height = 0
width = 0
windowHeight = 0
windowWidth = 0
delay = 0.01

difficulty = input("Choose a difficulty (demo, E, M, or H): ")
while difficulty not in ["E", "M", "H","demo"]: #setting difficulty with user input
    difficulty = input("Choose a difficulty (demo, E, M, or H): ")
if difficulty == "E":
    height = 9
    width = 12
elif difficulty == "M":
    height = 18
    width = 24
elif difficulty == "H":
    height = 27
    width = 36
elif difficulty == "demo":
    height = 18
    width = 24
    delay = 0.1 #slows down generation algorithm for easier viewing

windowHeight = 2*y_offset + 20*height
windowWidth = 2*x_offset + 20*width #sets window dimensions based on maze dimensions

while game: #while loop for infinite games to be played
    maze = MazeBoard(width,height,windowHeight,windowWidth) #initializes maze
    time.sleep(1)
    maze.recursiveGen(random.randint(0, width-1), random.randint(0, height-1),delay) #starts maze generation
    pygame.draw.rect(maze.screen,(0,255,0),pygame.Rect(x_offset+20*(width-1) + 2,y_offset+20*(height-1) + 2, 16, 16)) #draws goal in botton right of maze
    player1 = player(maze) #initializes player
    run = True     
    while run: #while loop for events in each individual maze
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #end game after window closed
                run = False
                game = False
        
            if event.type == pygame.KEYDOWN: #register keystroke
                player1.move(event.key) 
        
        if player1.xCoord == width-1 and player1.yCoord == height-1: #check for player reaching end of the maze
            run = False
        pygame.display.update() #updates screen to reflect movements

pygame.quit()
