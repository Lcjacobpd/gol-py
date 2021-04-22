# gof-py

<br/>

## Introduction:

An implimentation of Conway's "Game of Life" grid algorithm
in python displayed in the terminal.

### Cell Rules:
Conway's algorithm establishes life as a series of cells with
specific properties. 

1. Cells are either alive or dead
2. Cells have 8 neighbors (N,E,S,W and diagonals)
3. Neighbors outside the bounds of the grid are assumed dead

### Rules of the Grid:
The rules of the grid can be simplified to four cases,
Underpopulation, Continuation, Overpopulation, Colonization
or, more explicitly defined.

1. Any live cell with fewer than two live neighbors dies
2. Any live cell with 2-3 live neighbors survives
3. Any live cell with more than 3 live neighbors dies
4. Any dead cell with 3 live neighbors becomes alive

With these rules, and worldspace we can begin to view "life"
as a series of generations on the grid. During which we can
see patterns emerge out of random distributions or view
tried-and-true templates others have discovered.

-----

<br/>

## Code Usage:

```Shell
$ python3 main.py
```

### Flags:
There are several flags to be aware of when using this code.
All of which can be viewed with the -h flag. I'll review them
breifly here as well. 

#### -dim
Accepts two integers separated by a comma, with a default
value of "20,20". Specifies the width, height of the grid.

#### -load
Accepts a string, or more accurately, a path to a template
file. Two examples can be found in ```saves/```.

#### -gen
Accepts a positive integer, typically larger than 1 as the
first generation of a grid is displayed by default.
Determines the number of generations to iterate through.

