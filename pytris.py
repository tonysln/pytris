import configparser as cp
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
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

    def startup():
        root.destroy()
        run_game()
        
    def updatesize():
        cfg.set("Options", "boardheight", str(hscale.get()))
        cfg.set("Options", "boardwidth", str(wscale.get()))
        with open("config.ini", "w") as cfgfile:
            cfg.write(cfgfile)
        tk.messagebox.showinfo("PYTRIS Launcher", "Size settings updated")
        
    def helpwindow():
        help_content = """
        Repository: 
        https://github.com/toshkeen/pytris

        Controls:
        Q - Quit
        ESC / P - Pause
        R - Restart
        M - Mute
        N - New shape (difficulty will increase faster by using this!)
        X / UP - Rotate shape
        DOWN - Soft drop
        SPACE - Hard drop
        LEFT - Move left
        RIGHT - Move right
        """
        tk.messagebox.showinfo("PYTRIS Launcher", help_content) 
        
    def updateshapelist():
        new_text = ""
        for item in cfg.items("Shapes"):
            new_text += str(item[0]).upper() + " "
            shapes_loaded.set(new_text)
            
    def addshape():
        ns_name = simpledialog.askstring("PYTRIS Launcher", "New shape name:", parent = frame)
        ns_shape = simpledialog.askstring("PYTRIS Launcher", "New shape:", parent = frame)
        if ns_name and ns_shape:
            cfg.set("Shapes", str(ns_name), str(ns_shape))
            random_color = str(random.randint(0,255)) + "," + str(random.randint(0,255)) + "," + str(random.randint(0,255))
            cfg.set("Colors", str(ns_name), random_color)
            with open("config.ini", "w") as cfgfile:
                cfg.write(cfgfile)
            updateshapelist()
    
    def removeshape():
        rs_name = simpledialog.askstring("PYTRIS Launcher", "Name of shape to remove:", parent = frame)
        if rs_name:
            cfg.remove_option("Shapes", str(rs_name))
            cfg.remove_option("Colors", str(rs_name))
            with open("config.ini", "w") as cfgfile:
                cfg.write(cfgfile)
            updateshapelist()
        

    root = tk.Tk()
    root.title('PYTRIS Launcher')
    root.resizable(False, False)
    frame = tk.Frame(root)
    frame.pack()

    boardhlbl = tk.Label(frame, text="Board height:").grid(row=0, column=0, sticky='W', padx=48, pady=(24,10))
    hscale = tk.Scale(frame, from_=10, to=36, orient="horizontal")
    hscale.set(BOARD_H - 4)
    hscale.grid(row=1, column=0, sticky="w", padx=48, pady=1)
    
    boardwlbl = tk.Label(frame, text="Board width:").grid(row=2, column=0, sticky='W', padx=48, pady=10)
    wscale = tk.Scale(frame, from_=8, to=28, orient="horizontal")
    wscale.set(BOARD_W)
    wscale.grid(row=3, column=0, sticky="w", padx=48, pady=1)
    
    upbtn = tk.Button(frame,text="Update Size", command=updatesize).grid(row=4, column=0, sticky='W', padx=48, pady=(10,30))
    runbtn = tk.Button(frame,text="Run Game", command=startup, height=2, width=10).grid(row=0, column=2, sticky='W', padx=48, pady=(24,10))
    helpbtn = tk.Button(frame,text="Help", command=helpwindow).grid(row=1, column=2, sticky='W', padx=48, pady=10)
    exitbtn = tk.Button(frame, text="Exit", command=quit).grid(row=2, column=2, sticky='W', padx=48, pady=10)

    shapeslbl = tk.Label(frame, text="Current shapes:").grid(row=2, column=1, sticky='W', padx=48, pady=10)
    shapes_loaded = tk.StringVar()
    shapes_loaded_text = ""
    for item in cfg.items("Shapes"):
        shapes_loaded_text += str(item[0]).upper() + " "
    shapes_loaded.set(shapes_loaded_text)
    
    shapescontentlbl = tk.Label(frame, textvariable=shapes_loaded)
    shapescontentlbl.grid(row=3, column=1, sticky='W', padx=48, pady=10)

    addshapebtn = tk.Button(frame, text="Add Shape", command=addshape).grid(row=0, column=1, sticky='W', padx=48, pady=(24,10))
    removeshapebtn = tk.Button(frame, text="Remove Shape", command=removeshape).grid(row=1, column=1, sticky='W', padx=48, pady=10)

    root.mainloop()

    # run_game()


def run_game():
    # The main game runtime function

    def spawn_shape():
        # Choose a new random shape from the SHAPES dict
        new_shape_name = random.choice(list(SHAPES))
        new_shape = SHAPES[str(new_shape_name)]
        # Reset coordinates and speed
        x = 0 + (BOARD_W - get_size(new_shape)['w']) // 2
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
        
        # Drawing the grid lines every block for all blocks on the screen
        for i in range(1,BOARD_W + 1):
            pg.draw.line(scr, (60,60,60), [i*BLOCK_SIZE, 0], [i*BLOCK_SIZE, SCREEN_H], 1)
        for i in range(1,BOARD_H):
            pg.draw.line(scr, (60,60,60), [0, i*BLOCK_SIZE], [SCREEN_W - SIDE_PANEL_W, i*BLOCK_SIZE], 1)

        # Hide top bocks
        pg.draw.rect(scr, (0,0,0), [0, 0, SCREEN_W, TOP_PANEL_H])
        
    def draw_panel(next_shape, next_shape_name):
        # Draw next shape
        for y in range(len(next_shape)): 
            for x in range(len(next_shape[y])): 
                if next_shape[y][x] == '1':
                    pg.draw.rect(scr, COLORS[next_shape_name], [(x * BLOCK_SIZE + (BOARD_W * BLOCK_SIZE + BLOCK_SIZE)), (y * BLOCK_SIZE + (TOP_PANEL_H + BLOCK_SIZE)), BLOCK_SIZE, BLOCK_SIZE]) 

        # Draw grid for next shape window
        for i in range(5):
            pg.draw.line(scr, (60,60,60), [(BOARD_W * BLOCK_SIZE + BLOCK_SIZE) + BLOCK_SIZE * i, TOP_PANEL_H + BLOCK_SIZE], [(BOARD_W * BLOCK_SIZE + BLOCK_SIZE) + BLOCK_SIZE * i, BLOCK_SIZE * 4 + TOP_PANEL_H + BLOCK_SIZE], 1)
            pg.draw.line(scr, (60,60,60), [(BOARD_W * BLOCK_SIZE + BLOCK_SIZE), (TOP_PANEL_H + BLOCK_SIZE) + BLOCK_SIZE * i], [(BOARD_W * BLOCK_SIZE + BLOCK_SIZE) + NEXT_SHAPE_PANEL_SIZE ,(TOP_PANEL_H + BLOCK_SIZE) + BLOCK_SIZE * i], 1)

        # Draw text
        next_shape_f = pg.font.SysFont('Consolas', 20)
        next_shape_text = next_shape_f.render(('NEXT SHAPE'), False, (250, 250, 250))
        scr.blit(next_shape_text, (BOARD_W * BLOCK_SIZE + BLOCK_SIZE, TOP_PANEL_H))

        title_f = pg.font.SysFont('Consolas', 36)
        title_text = title_f.render(('PYTRIS'), False, (250, 250, 250))
        scr.blit(title_text, (SCREEN_W//2 - title_text.get_width()//2, TOP_PANEL_H//3))

        rows_f = pg.font.SysFont('Consolas', 20)
        rows_text = rows_f.render(('ROWS: {}'.format(rows_counter)), False, (250, 250, 250))
        scr.blit(rows_text, (BOARD_W * BLOCK_SIZE + BLOCK_SIZE, TOP_PANEL_H + NEXT_SHAPE_PANEL_SIZE + 2 * BLOCK_SIZE))
        

    def rotate_shape(shape):
        # First create a temp matrix
        t = list()
        for row in range(len(shape[0])):
            t.append(list())
            for col in range(len(shape)):
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

    def save_shape(name):
        for y in range(len(GRID)):
            for x in range(len(GRID[y])):
                # Save shape and color to the grid, using the name of the current shape
                if GRID[y][x] == '*':
                    GRID[y][x] = str(name)

    def check_rows(rows_counter, difficulty):
        rows_full = False
        for y in range(len(GRID)):
            # If there are no active blocks or empty blocks in a row, shift down every row above it
            if not ('0' in GRID[y] or '*' in GRID[y]):
                rows_full = True
                rows_counter += 1
                for row in range(y, 0, -1):
                    for x in range(len(GRID[row])):
                        GRID[row][x] = GRID[row-1][x]
        if rows_full:
            beep.play()
            if difficulty > 2:
                difficulty -= 1
        return rows_counter, difficulty
        
    def check_lose():
        for x in GRID[4]:
            if x in COLORS:
                return True
        return False

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
      
    def clean_board():
        for y in range(len(GRID)):
            for x in range(len(GRID[y])):
                # Remove everything
                GRID[y][x] = '0'
    
    # Read config again in case of changes from the menu
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
    

    # Decode shape data into matrix form and save shapes into dict
    SHAPES = dict()
    for item in cfg.items('Shapes'):
        SHAPES[item[0].upper()] = list()
        for row in item[1].split(','):
            if '1' in row:
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
    icon = pg.image.load('pt_icon.png')
    pg.display.set_icon(icon)
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
    down_pressed = False
    
    game_paused = False
    
    # Music and sound effects init
    pg.mixer.pre_init(44100, -16, 2, 2048)
    pg.init()
    pg.mixer.init()
    pg.mixer.music.set_volume(0.1)
    pg.mixer.music.load('korobeiniki.mp3')
    pg.mixer.music.play(-1) #-1 means loop!

    beep = pg.mixer.Sound('beep.wav')
    beep.set_volume(0.1)

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
            if (not check_lose()) and (event.key == pg.K_p or event.key == pg.K_ESCAPE):
                game_paused = not game_paused
                if game_paused:
                    pg.mixer.music.pause()
                if not game_paused:
                    pg.mixer.music.unpause()
        
        if game_paused and not check_lose():
            pg.draw.rect(scr, (0,0,0), [0, 0, SCREEN_W, SCREEN_H])
            pause_f = pg.font.SysFont('Consolas', 20)
            pause_text = pause_f.render(('PYTRIS Paused'), False, (250, 250, 250))
            scr.blit(pause_text, (SCREEN_W//2 - pause_text.get_width()//2, TOP_PANEL_H))
                
            pg.display.flip()
            dt = clock.tick(FPS)
            
        if check_lose() and not game_paused:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    # restart game, for debugging
                    clean_board()
                    difficulty = START_DIFFICULTY
                    rows_counter = 0
                    # Use the next generated shape instead of the current one
                    new_shape = next_shape
                    new_shape_name = next_shape_name
                    next_shape, next_shape_name, x, y, spd_modifier = spawn_shape()
                    pg.mixer.music.stop()
                    pg.mixer.music.play(-1) 
                    
            pg.draw.rect(scr, (0,0,0), [0, 0, SCREEN_W, SCREEN_H])
            pause_f = pg.font.SysFont('Consolas', 20)
            pause_text = pause_f.render(('Game Lost! Press R to restart'), False, (250, 250, 250))
            scr.blit(pause_text, (SCREEN_W//2 - pause_text.get_width()//2, TOP_PANEL_H))
            rows_f = pg.font.SysFont('Consolas', 20)
            rows_text = rows_f.render((f'Rows cleared: {rows_counter}'), False, (250, 250, 250))
            scr.blit(rows_text, (SCREEN_W//2 - rows_text.get_width()//2, TOP_PANEL_H + 2*pause_text.get_height()))
            
            pg.mixer.music.stop()
            pg.display.flip()
            dt = clock.tick(FPS)
        
        
        # This way pause has control over everything on the screen, so no need to save any other states
        if not game_paused and not check_lose():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP or event.key == pg.K_x:
                    # Rotation - warning, very buggy at this point
                    if y >= 4 and (x >= 0 or x + get_size(new_shape)['w'] < BOARD_W):
                        try:
                            update_grid(rotate_shape(new_shape), x, y)
                            new_shape = rotate_shape(new_shape)
                        except:
                            x -= 1 # Fixing things with tape for now
                            try:
                                update_grid(rotate_shape(new_shape), x, y)
                                new_shape = rotate_shape(new_shape)
                            except:
                                pass

                if event.key == pg.K_DOWN:
                    down_pressed = True
                if event.key == pg.K_SPACE:
                    # Simulates a hard drop - increases FPS drastically
                    spd_modifier = 50
                if event.key == pg.K_LEFT:
                    left_pressed = True
                    # Move left if there isn't a shape or end of the board there
                    if x > 0 and not shape_left():
                        x -= 1
                if event.key == pg.K_RIGHT:
                    right_pressed = True
                    # Move right if there isn't a shape or end of the board there
                    if (x + get_size(new_shape)['w'] < BOARD_W) and not shape_right():
                        x += 1
                if event.key == pg.K_r:
                    # restart game, for debugging
                    clean_board()
                    difficulty = START_DIFFICULTY
                    rows_counter = 0
                    # Use the next generated shape instead of the current one
                    new_shape = next_shape
                    new_shape_name = next_shape_name
                    next_shape, next_shape_name, x, y, spd_modifier = spawn_shape()
                    pg.mixer.music.stop()
                    pg.mixer.music.play(-1) 
                if event.key == pg.K_n:
                    # new shape, for debugging
                    # if we decide to leave it in, increase game speed as a penalty
                    if difficulty > 3:
                        difficulty -= 2
                    new_shape = next_shape
                    new_shape_name = next_shape_name
                    next_shape, next_shape_name, x, y, spd_modifier = spawn_shape()
                if event.key == pg.K_m:
                    if pg.mixer.music.get_volume() == 0 and beep.get_volume() == 0:
                        pg.mixer.music.set_volume(0.1)
                        beep.set_volume(0.1)
                    else:
                        pg.mixer.music.set_volume(0)
                        beep.set_volume(0)

            # Reset the key presses when the keys are physically released
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    left_pressed = False
                    lr_counter = 1
                if event.key == pg.K_RIGHT:
                    right_pressed = False
                    lr_counter = 1
                if event.key == pg.K_DOWN:
                    down_pressed = False
                    spd_modifier = 1

            # Start up a counter to move the shape for as long as the key is pressed
            # Values 0.1, 18 and 1.4 were chosen after lots of experimentation
            # Goal - smooth movement, not too fast yet fast enough to be effective
            if left_pressed:
                lr_counter *= (0.1 * dt)
                if lr_counter > 18 * dt:
                    if x > 0 and not shape_left():
                        x -= 1
                    lr_counter = 1.4 * dt

            if right_pressed:
                lr_counter *= (0.1 * dt)
                if lr_counter > 18 * dt:
                    if x + get_size(new_shape)['w'] < BOARD_W and not shape_right():
                        x += 1
                    lr_counter = 1.4 * dt

            if down_pressed:
                spd_modifier = 20
            
            d_counter += (FPS * dt) / ((difficulty*10) / spd_modifier)

            if d_counter >= BLOCK_SIZE:
                # Save shape if it's on the last row of the grid or there's a shape below
                if y == (BOARD_H - get_size(new_shape)['h']) or shape_below():
                    save_shape(new_shape_name)
                    # Spawn a new shape but choose the last generated one as the active shape
                    new_shape = next_shape
                    new_shape_name = next_shape_name
                    next_shape, next_shape_name, x, y, spd_modifier = spawn_shape()
                    # Reset any pressed buttons here
                    left_pressed, right_pressed, down_pressed = False, False, False
                y += 1
                d_counter = 0
            
            rows_counter, difficulty = check_rows(rows_counter, difficulty)
            update_grid(new_shape, x, y)
            draw_grid(new_shape, new_shape_name)
            draw_panel(next_shape, next_shape_name)
            
            # Update display, run next frame
            pg.display.flip()
            dt = clock.tick(FPS)

    pg.quit()
    start_gui()

start_gui()