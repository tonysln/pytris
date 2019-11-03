import configparser as cp
import tkinter as tk
import pygame as pg
import random

# Load customizable data and set up variables
cfg = cp.ConfigParser()
cfg.read('config.ini')

BLOCK_SIZE = cfg.getint('Options', 'blocksize')
BOARD_H = cfg.getint('Options', 'boardheight')
BOARD_H += 4 # 4 extra spaces for spawning in the shapes
BOARD_W = cfg.getint('Options', 'boardwidth')
FPS = cfg.getint('Options', 'fpscap')
START_DIFFICULTY = cfg.getint('Options', 'startdifficulty')

SIDE_PANEL_W = BLOCK_SIZE * 6 # next shape panel is 4x4 plus padding on each side
TOP_PANEL_H = BLOCK_SIZE * 4 # the same 4 extra spaces but in blocks
NEXT_SHAPE_PANEL_SIZE = BLOCK_SIZE * 4
SCREEN_H = BLOCK_SIZE * BOARD_H
SCREEN_W = BLOCK_SIZE * BOARD_W + SIDE_PANEL_W

def start_gui():
    # GUI/Menu function for customizing game and running it

    run_game()


def run_game():
    # The main game runtime function

    def spawn_shape():
        # Choose a new random shape from the SHAPES dict
        new_shape_name = random.choice(list(SHAPES))
        new_shape = SHAPES[str(new_shape_name)]
        # Reset coordinates and speed
        x = 0
        # Spawn shape one block above the visible board (on the last rows of the 4 extra spaces)
        y = 0 + get_size(new_shape)['h'] 
        spd_modifier = 1
        return new_shape, new_shape_name, x, y, spd_modifier

    def update_grid(shape, current_x, current_y):
        rows_empty = 0
        cols_empty = 0

        # Remove old shape position each frame in case it has updated
        for y in range(len(GRID)): 
            for x in range(len(GRID[y])):
                if GRID[y][x] == '*':
                    GRID[y][x] = '0'
        # Count empty rows/cols of the shape from ONE side, to keep 
        # the coordinates correct (more on this in documentation)
        for row in shape: 
            if '1' not in row:
                rows_empty += 1
            else:
                break
        for row in rotate_shape(shape):
            if '1' not in row:
                cols_empty += 1
            else:
                break
        # Append new shape to the grid, accounting for its' position and empty rows/cols
        for y in range(len(shape)): 
            for x in range(len(shape[y])): 
                if shape[y][x] == '1':
                    GRID[y + current_y - rows_empty][x + current_x - cols_empty] = '*' 

    def draw_grid(shape, name):
        # Each frame refersh the screen by filling it with black at first
        scr.fill((0,0,0))
        # Scan through the GRID for any saved or active blocks and draw them
        # Color is defined by the saved shape's letter or current shape's name
        for y in range(len(GRID)): 
            for x in range(len(GRID[y])):
                if GRID[y][x] in COLORS:
                    pg.draw.rect(scr, COLORS[GRID[y][x]], [(x * BLOCK_SIZE), (y * BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE])
                if GRID[y][x] == '*':
                    pg.draw.rect(scr, COLORS[name], [(x * BLOCK_SIZE), (y * BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE])
        
    def draw_panel():
        pass

    def rotate_shape(shape):
        # First create a temp matrix
        t = list()
        for row in range(len(shape)):
            t.append(list())
            for col in range(len(shape[0])):
                t[row].append(' ')
        # Then transpose the original and save into temp
        for y in range(len(shape)):
            for x in range(len(shape[0])):
                t[x][y] = shape[y][x]
        # Then reverse the order of items on each row
        shape = list([row[::-1] for row in t])
        return shape

    def get_size(shape):
        w = len(shape[0])
        h = len(shape)
        # Remove from height if row empty
        for row in shape:
            if '1' not in row:
                h -= 1
        # Remove from width if column empty
        for row in rotate_shape(shape):
            if '1' not in row:
                w -= 1
        return {'w':w, 'h':h}

    def save_shape():
        pass

    def check_rows():
        for y in range(len(GRID)):
            # If there are no active blocks or empty blocks in a row, shift down every row above it
            if not ('0' in GRID[y] or '*' in GRID[y]):
                for row in range(y, 0, -1):
                    for x in range(len(GRID[row])):
                        GRID[row][x] = GRID[row-1][x]

    def shape_below():
        for y in range(len(GRID)):
            for x in range(len(GRID[y])):
                # For every active block, check the block below and return true if it's colored (aka saved)
                if GRID[y][x] == '*' and GRID[y+1][x] in COLORS:
                    return True
        return False

    def shape_left():
        for y in range(len(GRID)):
            for x in range(len(GRID[y])):
                # Check if the left block is saved
                if GRID[y][x] == '*' and GRID[y][x-1] in COLORS:
                    return True
        return False

    def shape_right():
        for y in range(len(GRID)):
            for x in range(len(GRID[y])):
                # Check if the right block is saved
                if GRID[y][x] == '*' and GRID[y][x+1] in COLORS:
                    return True
        return False

    # Decode shape data into matrix form and save shapes into dict
    SHAPES = dict()
    for item in cfg.items('Shapes'):
        SHAPES[item[0].upper()] = list()
        for row in item[1].split(','):
            SHAPES[item[0].upper()].append(list(row))  

    # Create a dict of color codes (as lists) for the default shapes 
    COLORS = dict()
    for item in cfg.items('Colors'):
        COLORS[item[0].upper()] = list()
        for row in item[1].split(','):
            COLORS[item[0].upper()].append(int(row))

    # Later with custom shapes - assign random letter combo such as 'C1' and assign random color from a range

    # Create an empty matrix - playing board
    GRID = list()
    for y in range(BOARD_H):
        GRID.append(list())
        for x in range(BOARD_W):
            GRID[y].append('0')

    # Pygame initialization
    pg.init()
    scr = pg.display.set_mode((SCREEN_W, SCREEN_H))
    pg.display.set_caption("PYTRIS")
    clock = pg.time.Clock()

    # Get time in milliseconds from the last tick (to make movement even on all CPU speeds)
    dt = clock.tick(FPS) 
    d_counter = 0 # Counter for controlling down movement 
    lr_counter = 0 # Counter for controlling left/right movement
    
    # Spawn in the first two shapes, set up their position and speed
    new_shape, new_shape_name, x, y, spd_modifier = spawn_shape()
    next_shape, next_shape_name, x, y, spd_modifier = spawn_shape()
    
    difficulty = START_DIFFICULTY # Difficulty will be changing, first assign it from config
    rows_counter = 0 
    
    left_pressed = False
    right_pressed = False
    
    game_paused = False
    
    # Music and sound effects init will be here


    # Main game loop
    is_running = True
    while is_running:
        # Input/controls 
        event = pg.event.poll()
        if event.type == pg.QUIT:
            is_running = False
        if event.type == pg.KEYDOWN:
            # Key Q for exit
            if event.key == pg.K_q:
                is_running = False
            # Key P for pause and unpause
            if event.key == pg.K_p or event.key == pg.K_ESCAPE:
                game_paused = not game_paused
        
        # This way pause has control over everything on the screen, so no need to save any other states
        if not game_paused:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP or event.key == pg.K_x:
                    pass # rotate
                if event.key == pg.K_DOWN:
                    pass # hard/soft drop
                if event.key == pg.K_LEFT:
                    pass # move left
                if event.key == pg.K_RIGHT:
                    pass # move right
                if event.key == pg.K_SPACE:
                    pass # hard drop
                if event.key == pg.K_r:
                    pass # restart game, for debugging
                if event.key == pg.K_n:
                    pass # new shape, for debugging
            
            check_rows()
            update_grid(new_shape, x, y)
            draw_grid(new_shape, new_shape_name)
            draw_panel()
            
            # Update display, run next frame
            pg.display.flip()
            dt = clock.tick(FPS)

    pg.quit()


start_gui()