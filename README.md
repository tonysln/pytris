# PYTRIS

A customized version of Tetris with the ability to design shapes and set the board size.

Project by Anton Slavin and Elen Liivapuu.

Python modules used: pygame, tkinter.

### Set the board size
Use the sliders to set a size for the playing board. Press "Update Size" for the changes to take effect!

### Add/Remove shapes

To add a shape, press on the "Add Shape" button and give a name to your shape. A good idea is to use single letters or 2-3 letter words. After that, you have the enter the shape's representation.

Imagine a 3x3 or 4x4 grid and your shape placed into it, just like the shapes below (**sizes below 2x2 and over 4x4 are highly not recommended, as the game may become unstable**):

![](https://static.packt-cdn.com/products/9781849690904/graphics/0904_06_03.jpg)

*[Source](https://subscription.packtpub.com/book/game_development/9781849690904/5/ch05lvl1sec77/creating-the-tetrominoes)*

Every block that the shape occupies is a `1` and every empty block is a `0`. Blocks in a row do not have spaces between them and every row has a comma `,` as the seperator. For example, the first shape in the image can be represented as `0000,1111,0000,0000`. The third "T" shape: `0000,1110,0100,0000`.

Now, write down the representation of your shape with 1s and 0s, rows seperated by commas (and no comma at the end).

You should now see the name of your shape appear in the active shapes list. After starting the game, it will automatically include and use your newly created shape(s).

To remove a shape, press on the "Remove Shape" button and input its name.


### Shortcuts
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

### Completed alpha and beta goals
* Board grid implemented
* Classic shapes (Tetrominos) implemented
* Working game clock
* Working keyboard controls
* Shapes respond to controls
* Shapes can detect surroundings in the grid
* Shapes get randomly generated
* Shapes settle into place correctly
* The grid acknowledges a filled row and removes it, shifting everything down
* Ability to play with custom shapes
* Ability to set custom board size
* Hard and soft drop implemented
* Upcoming shape displayed
* The game ends when the grid gets filled to the top
* A complete menu GUI with settings
* GUI for creating and deleting custom shapes
* Finished row counter

### Additional goals
* 7-bag randomizer
* Ghost piece functionality
* Game and shape statistics
* Multiple upcoming shapes display
* Save high score