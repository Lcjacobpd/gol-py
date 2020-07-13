# grid.py
# defines the space in which the individual cells exist

# Cell Rules:
#    1. Cells are either alive or dead
#    2. Cells have 8 neighbors (N,E,S,W and diagonals)
#    3. Neighbors outside the bounds of the grid are assumed dead

# Rules of the Grid:
#    1. Any live cell with fewer than two live white neighbors dies
#    2. Any live cell with 2-3 live neighbors lives on to the next generation
#    3. Any live cell with more than 3 live neighbors dies
#    4. Any dead cell with 3 live neighbors becomes alive
'''
Worldspace definitions for implimentation of Conway's Game of Life
'''

import random
import csv
import time
import typing
import collections
from os import system

# display utilities
RED = '\u001b[31m'
CYAN = '\u001b[36m'
YELLOW = '\u001b[33m'
GRAY = '\u001b[1;30m'
WHITE = '\u001b[0m'


def clear() -> None:
    '''
    reset terminal screen space
    '''
    _ = system('clear')


ALIVE = 1
DEAD = 0

class Grid:
    '''
    contains the matrix of cells and its dimensions
    '''
    def __init__(self, width: int, height: int) -> None:
        '''
        Constructs an instance of a gridspace (width, height)
        '''
        self.height = height
        self.width = width
        self.matrix = []

        # each cell has x, y, status (0 = dead, 1 = alive)
        for xpos in range(width):
            column = []
            for ypos in range(height):
                column.append({'x': xpos, 'y': ypos, 'status': DEAD})
            self.matrix.append(column)

    def populate(self) -> None:
        '''
        Randomly populates the cells of a grid (none)
        '''
        for xpos in range(self.width):
            for ypos in range(self.height):
                status = random.choice([ALIVE, DEAD])
                self.matrix[xpos][ypos]['status'] = status

    @staticmethod
    def load(filename: str) -> 'Grid':
        '''
        Create datagrid from template file (filename)
        '''
        with open(filename, 'rt') as infile:
            rows = csv.reader(infile)
            header = next(rows)  # header contains grid dimmensions

            print()
            print(f'Reading {filename} with dimensions:', header)
            width = int(header[0])
            height = int(header[1])

            # create new grid to populate
            preset = Grid(width, height)
            xpos = 0
            ypos = 0

            # convert document lines to grid rows
            for row in rows:
                xpos = 0
                for char in row[0]:
                    preset.matrix[ypos][xpos]['status'] = int(char)
                    xpos += 1
                ypos += 1
            return preset

    def save(self, filename: str) -> None:
        '''
        Writes the current grid data to a text file (filename)
        '''
        with open(filename, 'wt') as outfile:
            # place grid dimensions in header
            outfile.write(f'{self.width},{self.height}\n')

            for xpos in range(self.width):
                for ypos in range(self.height):
                    outfile.write(str(self.matrix[xpos][ypos]['status']))
                outfile.write('\n')

    def label(self, iteration: int, generations: int) -> None:
        '''
        Creates a label for the grid display in the terminal (generation)
        '''
        print(F'Generation: \t{iteration}/{generations}')
        print('---' * self.height, end='-\n')

    def display(self) -> None:
        '''
        Displays the current grid configuration (none)
        '''
        # column numbers
        print(RED, end='  ')
        for xpos in range(self.height):
            print(f'{xpos:2d}', end=' ')
        print(WHITE)

        for xpos in range(self.width):
            # row numbers
            print(CYAN + F'{xpos:2d}' + WHITE, end='')

            for ypos in range(self.height):
                if self.matrix[xpos][ypos]['status'] == ALIVE:
                    print(YELLOW + ' ■ ', end=WHITE)
                else:
                    print(GRAY + ' □ ', end=WHITE)
            print()

    def census(self) -> int:
        '''
        Counts the number of currently living cells in the grid (None)
        '''
        count = 0
        for xpos in range(self.width):
            for ypos in range(self.height):
                count += self.matrix[xpos][ypos]['status']  # alive = 1
        return count

    def check_neighbors(self, xpos: int, ypos: int) -> int:
        '''
        Counts the number of living neighbors (x, y positions)
        '''
        neighbor_count = 0
        height = self.height - 1
        width = self.width - 1
        left = xpos - 1
        right = xpos + 1
        down = ypos - 1
        up = ypos + 1

        if xpos > 0:
            neighbor_count += self.matrix[left][ypos]['status']
            if ypos > 0:
                neighbor_count += self.matrix[left][down]['status']
            if ypos < height:
                neighbor_count += self.matrix[left][up]['status']

        if xpos < width:
            neighbor_count += self.matrix[right][ypos]['status']
            if ypos > 0:
                neighbor_count += self.matrix[right][down]['status']
            if ypos < height:
                neighbor_count += self.matrix[right][up]['status']

        if ypos > 0:
            neighbor_count += self.matrix[xpos][down]['status']
        if ypos < height:
            neighbor_count += self.matrix[xpos][up]['status']

        return neighbor_count


    def stats(self, stats: dict) -> None:
        '''
        Prints stats of the current grid (Living, Born, Deaths, Survivors)
        '''
        print(f'Before: {stats["living"]:>3}')
        print(f'       +{stats["born"]:>3d} (born)')
        print(f'       -{stats["died"]:>3d} (died)')
        print(f'After:  {self.census():3d} ({stats["survivors"]} survivors)')
        print()

    def iterate(self, generations: int, display_all: bool = True,
                frame_delay: float = 1.0) -> None:
        '''
        Display several generations of the grid
        '''
        # lifetime statistics variables
        total_died = 0
        total_born = 0

        # display initial grid with label
        if display_all:
            self.label(0, generations)
            self.display()
            print()

        # process grid generations
        for i in range(generations):
            if display_all:
                time.sleep(frame_delay)  # apply delay

            # create next generation according to the grid rules
            subsequent_matrix = []

            # generation statistics
            stats = {
                'living': self.census(),
                'born': 0,
                'died': 0,
                'survivors': 0
            }
            stale = True

            for xpos in range(self.width):
                column = []
                for ypos in range(self.height):
                    cell = self.matrix[xpos][ypos]

                    neighbor_count = self.check_neighbors(xpos, ypos)

                    # check grid rules
                    if cell['status'] == ALIVE:
                        if neighbor_count < 2:  # rule 1
                            column.append({
                                'x': xpos,
                                'y': ypos,
                                'status': DEAD
                            })
                            stats['died'] += 1
                            total_died += 1
                            stale = False

                        elif neighbor_count < 4:  # rule 2
                            column.append({
                                'x': xpos,
                                'y': ypos,
                                'status': ALIVE
                            })
                            stats['survivors'] += 1

                        elif neighbor_count > 3:  # rule 3
                            column.append({
                                'x': xpos,
                                'y': ypos,
                                'status': DEAD
                            })
                            stats['died'] += 1
                            total_died += 1
                            stale = False

                    else:  # dead cell
                        if neighbor_count == 3:  # rule 4
                            column.append({
                                'x': xpos,
                                'y': ypos,
                                'status': ALIVE
                            })
                            stats['born'] += 1
                            total_born += 1
                            stale = False

                        else:  # default = dead
                            column.append({
                                'x': xpos,
                                'y': ypos,
                                'status': DEAD
                            })

                subsequent_matrix.append(column)
            self.matrix = subsequent_matrix  # update matrix

            # label generation & display generation statistics
            if display_all:
                clear()
                self.label(i+1, generations)
                self.display()
                self.stats(stats)

            # if stale stop iterations (not for 'next' command)
            if stale:
                print()
                print('Grid is stagnant; stopping life cycle...')
                return

        # display last generation if none of the rest
        if display_all is False:
            clear()
            print('\n')
            self.display()
            self.stats(stats)

        # display lifetime statistics
        else:
            time.sleep(frame_delay)
            print('Lifetime statistics:')
            print(f'born:     {total_born:>3d}')
            print(f'died:     {total_died:>3d}')
            print()

    def next(self) -> None:
        '''
        Shows the next generation of the grid (None)
        '''
        self.iterate(1, False)  # step size, don't display all
