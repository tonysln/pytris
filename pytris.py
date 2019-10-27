import configparser as cp
import tkinter as tk
import pygame as pg
import random

# Load customizable data and set up variables
cfg = cp.ConfigParser()
cfg.read('config.ini')

BLOCK_SIZE = cfg.getint('Options', 'blocksize')
BOARD_H = cfg.getint('Options', 'boardheight')
BOARD_W = cfg.getint('Options', 'boardwidth')
FPS = cfg.getint('Options', 'fpscap')
SLOWDOWN = cfg.getint('Options', 'slowdown')

SCREEN_H = BLOCK_SIZE * BOARD_H
SCREEN_W = BLOCK_SIZE * BOARD_W

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

    def get_size():
        pass

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
    # Set up a counter 
    t_counter = 0
    # Spawn in the first shape and set up some variables
    new_shape, new_shape_name, x, y, spd_modifier = spawn_shape()

    is_running = True
    while is_running:
        # Input/controls 
        event = pg.event.poll()
        if event.type == pg.QUIT:
            is_running = False

        check_rows()
        update_grid()
        draw_grid()
        
        # Update display, run next frame
        pg.display.flip()
        dt = clock.tick(FPS)

    pg.quit()


start_gui()