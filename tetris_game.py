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
         ".##..",
         "..#..",
         "..#..",
         "....."],
         [".....",
         ".....",
         ".###.",
         ".#...",
         "....."],
         [".....",
         "..#..",
         "..#..",
         "..##.",
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
         ".....",
         ".###.",
         "...#.",
         "....."],
         [".....",
         "..##.",
         "..#..",
         "..#..",
         "....."],
         [".....",
         ".#...",
         ".###.",
         ".....",
         "....."]],
    "Z": [
        [".....",
         "..#..",
         ".##..",
         ".#...",
         "....."],
         [".....",
         ".....",
         ".##..",
         "..##.",
         "....."]],
    "S": [
        [".....",
         "..#..",
         "..##.",
         "...#.",
         "....."],
         [".....",
         ".....",
         "..##.",
         ".##..",
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
         ".##..",
         "..#..",
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
         ".###.",
         ".....",
         "....."]],
}

shapes = ['I', 'L', 'J', 'Z', 'S', 'O', 'T']
shape_colors = [CYAN, ORANGE, BLUE, GREEN, RED, YELLOW, PURPLE]

#Pygame Display Initialization
pygame.display.set_caption("Tetris")
screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.RESIZABLE)
game_ui_font = pygame.font.SysFont('Arial', 30)

#Pygame Display Functions
#Pass in game by reference
def draw(game_state): 
    game = game_state #Passing in the Tetris game class
    #Setting up the game UI
    screen.fill((128, 128, 128))
    
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

    #Drawing the shadow of the falling piece
    ghost_piece_cells = get_piece_cells(game.ghost_piece)

    #Need to create another surface to support the changing opacity of the ghost pieces
    ghost_surface = pygame.Surface(
        (GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE),
        pygame.SRCALPHA
    )

    for (x, y) in ghost_piece_cells:
        if y >= 0:
            piece_outline = pygame.Rect(
                x * CELL_SIZE,
                y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            #Casting the tuple to a pygame color object so that the transparency can be changed
            translucent_color = (*game.ghost_piece.color, 80)
            pygame.draw.rect(ghost_surface, translucent_color, piece_outline)
            
    #drawing this surface onto the main surface onto the offset (top left of the grid)
    screen.blit(ghost_surface, (GRID_X_OFFSET, GRID_Y_OFFSET))

    #Displaying UI elements
    score_text = game_ui_font.render(f"Score: {game.score}", True, WHITE)
    level_text = game_ui_font.render(f"Level: {game.level}", True, WHITE)
    lines_text = game_ui_font.render(f"Lines Cleared: {game.lines_cleared}", True, WHITE)
    screen.blit(score_text, (600, 100))
    screen.blit(level_text, (600, 150))
    screen.blit(lines_text, (600, 200))
    pygame.display.flip()

def run(game_state):
    game = game_state
    clock = pygame.time.Clock()
    running = True
    
    while running:
        tick_time = clock.tick(30)

        if handle_inputs(game) == False:
            break

        if update_game_state(game, tick=tick_time) == False:
            print("Game Over!")
            running = False
        
        draw(game)

    pygame.quit()

def handle_inputs(game_state) -> bool:
    game = game_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_piece(piece=game.current_piece, game_state=game, delta_x=0, delta_y=0, rotation_change=1)
            elif event.key == pygame.K_SPACE:
                hard_drop(game)

    #Out of the loop to allow for holding the keys down since it checks each frame
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        move_piece(piece=game.current_piece, game_state=game, delta_x=-1, delta_y=0, rotation_change=0)
    elif keys[pygame.K_RIGHT]:
        move_piece(piece=game.current_piece, game_state=game, delta_x=1, delta_y=0, rotation_change=0)
    elif keys[pygame.K_DOWN]:
        if move_piece(piece=game.current_piece, game_state=game, delta_x=0, delta_y=1, rotation_change=0):
            game.score += 1
    
    return True

#Checks for line clears, game overs (piece is place above the grid), updates falling piece
def update_game_state(game_state, tick) -> bool:
    game = game_state
    game.fall_time += tick #delta is number of ticks before the game will update (ticks are in ms in pygame)

    update_ghost_piece(game)

    if game.fall_time >= game.fall_speed:
        #Checking if the piece will hit the bottom when it moves down
        if move_piece(piece=game.current_piece, game_state=game, delta_x=0, delta_y=1, rotation_change=0) == False:

            #Placing a piece and clearing its lines
            place_piece(game, game.current_piece)
            clear_lines(game)

            #get a new random piece
            game.current_piece = game.next_piece
            game.ghost_piece = copy.deepcopy(game.current_piece)
            game.next_piece = Tetromino()

            #Checking if the new piece will fit on the board, game over if not
            if is_valid_position(game, game.current_piece) == False:
                return False

        #Reset once the piece drops one row
        game.fall_time = 0
 
    return True

#Tetris Classes
#Information about current game
class TetrisGame:
    def __init__(self, current_tetromino, next_tetromino):
        self.grid = [[0 for i in range(GRID_WIDTH)] for j in range(GRID_HEIGHT)]
        self.current_piece = current_tetromino
        self.ghost_piece = copy.deepcopy(current_tetromino)
        self.next_piece = next_tetromino
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = 0
        self.fall_speed = 500 #in ms

#Information about pieces
class Tetromino:
    def __init__(self):
        self.shape = select_random_piece() #Selecting a random tetromino
        self.rotation = 0
        self.x = 2
        self.y = -2
        self.color = shape_colors[shapes.index(self.shape)] #gets the color that maps to the specific shape

#Tetris Functions
#Gets a random index in the piece and color array
def select_random_piece() -> str:
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
def move_piece(piece, game_state, delta_x, delta_y, rotation_change) -> bool:
    game = game_state
    
    #Deep copy the piece to cleanly handle position updates and rotations
    updated_piece = copy.deepcopy(piece)
    updated_piece.x += delta_x
    updated_piece.y += delta_y

    if rotation_change != 0:
        possible_rotations = TETROMINOES.get(updated_piece.shape)
        updated_piece.rotation = (updated_piece.rotation + rotation_change) % len(possible_rotations)

    if is_valid_position(game, updated_piece):
        game.current_piece = updated_piece
        return True

    return False

#for updating ghost piece efficiently
def update_ghost_piece(game_state) -> None:
    game = game_state
    ghost = copy.deepcopy(game.current_piece)
    while 1:
        ghost.y += 1
        if is_valid_position(game, ghost) == False:
            ghost.y -= 1
            break
    game.ghost_piece = ghost

#Automatically place the piece at the bottom
def hard_drop(game_state) -> None:
    game = game_state
    
    #Cells for score calculations
    cells_before_drop = get_piece_cells(game.current_piece)
    while move_piece(piece=game.current_piece, game_state=game, delta_x=0, delta_y=1, rotation_change=0):
        pass #give 2 points per each cell
    cells_after_drop = get_piece_cells(game.current_piece)

    #Fixing piece in place then clearing
    place_piece(game, game.current_piece)
    clear_lines(game)

    game.current_piece = game.next_piece
    game.ghost_piece = copy.deepcopy(game.current_piece)
    game.next_piece = Tetromino()

    if is_valid_position(game, game.current_piece) == False:
        print("Game Over!")
        pygame.quit()
    
    #Updating the score (2 per cell if hard drop)
    #Get the highest cell of the piece before and after the drop; difference is score
    min_before = min(cells_before_drop, key=lambda x: x[1])[1]
    min_after = min(cells_after_drop, key=lambda x: x[1])[1]
    game.score += 2 * (min_after - min_before)

#Verifying if the piece is in a valid position
def is_valid_position(game_state, piece) -> bool:
    game = game_state
    piece_cells = get_piece_cells(piece)

    for (x, y) in piece_cells:
        if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
            return False
        if y >= 0 and game.grid[y][x] != 0:
            return False
        
    return True

#keeps piece in place when it reaches a surface
def place_piece(game_state, piece) -> None:
    game = game_state
    piece_cells = get_piece_cells(piece)

    for (x, y) in piece_cells:
        if y >= 0:
            game.grid[y][x] = piece.color

#clears a line if it exists
def clear_lines(game_state) -> None:
    game = game_state
    rows_cleared = 0
    for y in range(GRID_HEIGHT):
        cells_filled = 0
        for x in range(GRID_WIDTH):
            if game.grid[y][x] != 0:
                cells_filled += 1
        
        if cells_filled == 10:
            rows_cleared += 1
            game.grid.pop(y)
            game.grid.insert(0, ([0] * 10))
            
    if rows_cleared == 1:
        game.score += 100 * game.level
    elif rows_cleared == 2:
        game.score += 300 * game.level
    elif rows_cleared == 3:
        game.score += 500 * game.level
    elif rows_cleared == 4:
        game.score += 800 * game.level #multiplied by 1.5 if back-to-back difficult clears
        
def main():
    starting_piece = Tetromino()
    next_starting_piece = Tetromino()
    game = TetrisGame(current_tetromino=starting_piece, next_tetromino=next_starting_piece)
    run(game)

if __name__ == "__main__":
    main()