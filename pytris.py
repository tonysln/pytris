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

def start_gui():
    # GUI/Menu function for customizing game and running it

    run_game()


def run_game():
    # The main game runtime function

    # Decode shape data into matrix form and save shapes into dict
    SHAPES = dict()
    for item in cfg.items('Shapes'):
        SHAPES[item[0].upper()] = list()
        for row in item[1].split(','):
            SHAPES[item[0].upper()].append(row)    

    # Create an empty matrix - playing board
    GRID = list()
    for y in range(BOARD_H):
        GRID.append(list())
        for x in range(BOARD_W):
            GRID[y].append(0)

    # Set up local variables
    SCREEN_H = BLOCK_SIZE * BOARD_H
    SCREEN_W = BLOCK_SIZE * BOARD_W

    # Pygame initialization
    pg.init()
    scr = pg.display.set_mode((SCREEN_W, SCREEN_H))
    pg.display.set_caption("PYTRIS")
    clock = pg.time.Clock()
    is_running = True

    while is_running:
        # Input/controls 
        event = pg.event.poll()
        if event.type == pg.QUIT:
            is_running = False
        
        # Update display, run next frame
        pg.display.flip()
        clock.tick(FPS)

    pg.quit()


start_gui()