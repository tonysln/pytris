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