import pygame
import random

pygame.init()

#Constants
#Tetris Constants
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
GRID_X_OFFSET = 50
GRID_Y_OFFSET = 50

#Pygame Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#Piece Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

TETROMINOES = {
    "I": [
        [".....",
         "..#..",
         "..#..",
         "..#..",
         "..#.."],
        [".....",
         ".....",
         "####.",
         ".....",
         "....."]],
    "L": [
        [".....",
         "..#..",
         "..#..",
         "..##.",
         "....."],
        [".....",
         ".....",
         ".###.",
         ".#...",
         "....."],
        [".....",
         ".##..",
         "..#..",
         "..#..",
         "....."],
        [".....",
         "...#.",
         ".###.",
         ".....",
         "....."]],
    "J": [
        [".....",
         "..#..",
         "..#..",
         ".##..",
         "....."],
        [".....",
         ".#...",
         ".###.",
         ".....",
         "....."],
        [".....",
         "..##.",
         "..#..",
         "..#..",
         "....."],
        [".....",
         ".....",
         ".###.",
         "...#.",
         "....."]],
    "Z": [
        [".....",
         ".....",
         ".##..",
         "..##.",
         "....."],
        [".....",
         "..#..",
         ".##..",
         ".#...",
         "....."]],
    "S": [
        [".....",
         ".....",
         "..##.",
         ".##..",
         "....."],
        [".....",
         "..#..",
         "..##.",
         "...#.",
         "....."]],
    "O": [
        [".....",
         ".....",
         ".##..",
         ".##..",
         "....."]],
    "T": [
        [".....",
         ".....",
         ".###.",
         "..#..",
         "....."],
        [".....",
         "..#..",
         ".###.",
         ".....",
         "....."],
        [".....",
         "..#..",
         "..##.",
         "..#..",
         "....."],
        [".....",
         "..#..",
         ".##..",
         "..#..",
         ".....",]],
}

shapes = ['I', 'L', 'J', 'Z', 'S', 'O', 'T']
shape_colours = [CYAN, ORANGE, BLUE, GREEN, RED, YELLOW, PURPLE]

#Pygame Display Initialization
pygame.display.set_caption("Tetris")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font()

#Pygame Display Functions
#Pass in game by reference
def draw(game_state): 
    game = game_state #Passing in the Tetris game class
    #Setting up the game UI
    screen.fill(BLACK)

    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            current_piece = pygame.Rect(GRID_X_OFFSET + game.current_piece.x * CELL_SIZE,
                                         GRID_Y_OFFSET + game.current_piece.y * CELL_SIZE,
                                         CELL_SIZE, CELL_SIZE)
            if game.grid[j][i] != 0:
                pygame.draw.rect(screen, game.grid[j][i], current_piece)
            pygame.draw.rect(screen, WHITE, current_piece, 1)

def run(game_state):
    running = True
    while running:
        draw(game_state)
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        
        pygame.display.update()
    
    pygame.quit()

#Tetris Classes
class TetrisGame:
    def __init__(self, current_tetromino, next_tetromino):
        self.grid = [[0 for i in range(GRID_WIDTH)] for j in range(GRID_HEIGHT)]
        self.current_piece = current_tetromino
        self.next_piece = next_tetromino
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = 0
        self.fall_speed = 500 #in ms

class Tetromino:
    def __init__(self):
        self.shape = get_new_piece() #Selecting a random tetromino
        self.rotation = 0
        self.x = GRID_WIDTH/2
        self.y = 0
        self.colour = shape_colours[shapes.index(self.shape)] #gets the color that maps to the specific shape

#Tetris Functions
#selection of a random piece
def get_new_piece():
    index = random.randint(0, 6)
    shape = shapes[index]
    return shape



#grid initalization
def create_grid():
    pass




def main():
    starting_piece = Tetromino()
    next_starting_piece = Tetromino()
    game = TetrisGame(current_tetromino=starting_piece, next_tetromino=next_starting_piece)
    run(game)
    print(starting_piece.colour, next_starting_piece.colour)

if __name__ == "__main__":
    main()