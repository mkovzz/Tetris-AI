import pygame
import random
import copy

pygame.init()

#Constants
#Tetris Constants
GRID_WIDTH = 10     #number of columns
GRID_HEIGHT = 20    #number of rows
CELL_SIZE = 30      #size of a cell (in pixels)
GRID_X_OFFSET = 50  #Offset from topleft of window
GRID_Y_OFFSET = 50  #Offset from topleft of window 

#Pygame Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

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
         ".....",
         "####.",
         ".....",
         "....."],
        [".....",
         "..#..",
         "..#..",
         "..#..",
         "..#.."]],
    "L": [
        [".....",
         "...#.",
         ".###.",
         ".....",
         "....."],
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
         "....."]],
    "J": [
        [".....",
         ".#...",
         ".###.",
         ".....",
         "....."],
        [".....",
         "..#..",
         "..#..",
         ".##..",
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
         "..#..",
         ".###.",
         ".....",
         "....."],
        [".....",
         ".....",
         ".###.",
         "..#..",
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
         "....."]],
}

shapes = ['I', 'L', 'J', 'Z', 'S', 'O', 'T']
shape_colours = [CYAN, ORANGE, BLUE, GREEN, RED, YELLOW, PURPLE]

#Pygame Display Initialization
pygame.display.set_caption("Tetris")
screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.RESIZABLE)
game_ui_font = pygame.font.SysFont('Arial', 30)

#Pygame Display Functions
#Pass in game by reference
def draw(game_state): 
    game = game_state #Passing in the Tetris game class
    #Setting up the game UI
    screen.fill(BLACK)
    
    #Drawing the grid for the game
    grid_rect = pygame.Rect(
        GRID_X_OFFSET,
        GRID_Y_OFFSET,
        GRID_WIDTH * CELL_SIZE,
        GRID_HEIGHT * CELL_SIZE
    )
    pygame.draw.rect(screen, WHITE, grid_rect, width=2)

    #Drawing filled cells
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            if game.grid[j][i] != 0:
                filled_cell = pygame.Rect(
                    GRID_X_OFFSET + i * CELL_SIZE,
                    GRID_Y_OFFSET + j * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
                pygame.draw.rect(screen, game.grid[j][i], filled_cell)

    #Drawing falling piece
    piece_cells = get_piece_cells(game.current_piece)
    for (x, y) in piece_cells:
        if y >= 0:
            falling_piece = pygame.Rect(
                GRID_X_OFFSET + x * CELL_SIZE,
                GRID_Y_OFFSET + y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(screen, game.current_piece.color, falling_piece)
            pygame.draw.rect(screen, WHITE, falling_piece, width=1) #Border of the piece 
            
    #Displaying UI elements
    score_text = game_ui_font.render(f"Score: {game.score}", True, WHITE)
    level_text = game_ui_font.render(f"Level: {game.level}", True, WHITE)
    lines_text = game_ui_font.render(f"Lines Cleared: {game.lines_cleared}", True, WHITE)
    screen.blit(score_text, (600, 100))
    screen.blit(level_text, (600, 150))
    screen.blit(lines_text, (600, 200))

def run(game_state):
    running = True
    while running:
        draw(game_state)
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        
        pygame.display.flip()
    
    pygame.quit()

#Checks for line clears, game overs (piece is place above the grid), updates falling piece
def update_game_state(game_state, delta):
    game = game_state
    game.fall_time += delta

    if game.fall_time >= game.fall_speed:
        pass #TO BE COMPLETED


#Tetris Classes
#Information about current game
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

#Information about pieces
class Tetromino:
    def __init__(self):
        self.shape = get_new_piece() #Selecting a random tetromino
        self.rotation = 0
        self.x = 0
        self.y = 0
        self.color = shape_colours[shapes.index(self.shape)] #gets the color that maps to the specific shape

#Tetris Functions
#Selection of a random piece
def get_new_piece() -> str:
    index = random.randint(0, 6)
    return shapes[index]

#Converts piece from 2D array of characters to cells on the grid
def get_piece_cells(piece) -> list:
    shape_data = TETROMINOES.get(piece.shape)[piece.rotation]
    cell_positions = []
    for i in range(5):
        for j in range(5):
            if shape_data[i][j] == "#":
                cell_positions.append((i + piece.x, j + piece.y)) #Adding current tetromino position in the game to the position
    
    return cell_positions

#Function for moving pieces
def move_piece(game_state, piece, delta_x, delta_y, rotation_change):
    game = game_state
    updated_piece = copy.deepcopy(piece)
    updated_piece.x += delta_x
    updated_piece.y += delta_y

    if rotation_change != 0:
        possible_rotations = TETROMINOES.get(updated_piece.shape)
        updated_piece.rotation = (updated_piece.rotation + rotation_change) % len(possible_rotations)

    if is_valid_position(updated_piece):
        game.current_piece = updated_piece
        return True

    return False

#Verifiying if the piece is in a valid position
def is_valid_position(game_state, piece):
    game = game_state
    #TO BE COMPLETED

def main():
    starting_piece = Tetromino()
    next_starting_piece = Tetromino()
    game = TetrisGame(current_tetromino=starting_piece, next_tetromino=next_starting_piece)
    run(game)
    print(starting_piece.colour, next_starting_piece.colour)

if __name__ == "__main__":
    main()