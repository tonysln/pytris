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
        # Reset coordinates and speed
        x = 0
        y = 0
        spd_modifier = 1
        # Choose a new random shape from the SHAPES dict
        new_shape_name = random.choice(list(SHAPES))
        new_shape = SHAPES[str(new_shape_name)]
        # Rotate the shape randomly by 0-360 degrees
        for i in range(random.randint(0,4)):
            new_shape = rotate_shape(new_shape)
        return new_shape, new_shape_name, x, y, spd_modifier

    def update_grid():
        pass

    def draw_grid():
        pass
        
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
        return (w,h)

    def save_shape():
        pass

    def check_rows():
        pass

    def shape_below():
        pass

    def shape_left():
        pass

    def shape_right():
        pass

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
    new_shape_next, new_shape_next_name, x, y, spd_modifier = spawn_shape()
    
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
            update_grid()
            draw_grid()
            draw_panel()
            
            # Update display, run next frame
            pg.display.flip()
            dt = clock.tick(FPS)

    pg.quit()


start_gui()