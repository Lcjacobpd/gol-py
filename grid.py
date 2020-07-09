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

import random
import csv
import time
from os import system

# display utilities
RED = '\u001b[31m'
CYAN = '\u001b[36m'
YELLOW = '\u001b[33m'
GRAY = '\u001b[1;30m'
WHITE = '\u001b[0m'


def clear():
    _ = system('clear')


ALIVE = 1
DEAD = 0


class Grid:
    def __init__(self, width, height):
        '''
        Constructs an instance of a gridspace (width, height)
        '''
        self.height = height
        self.width = width
        self.matrix = []

        # each cell has x, y, status (0 = dead, 1 = alive)
        for x in range(width):
            column = []
            for y in range(height):
                column.append({'x': x, 'y': y, 'status': DEAD})
            self.matrix.append(column)

    def populate(self):
        '''
        Randomly populates the cells of a grid (none)
        '''
        for x in range(self.width):
            for y in range(self.height):
                self.matrix[x][y]['status'] = random.choice([ALIVE, DEAD])

    def load(filename):
        '''
        Create datagrid from template file (filename)
        '''
        with open(filename, 'rt') as f:
            rows = csv.reader(f)
            header = next(rows)  # header contains grid dimmensions

            print()
            print(f'Reading {filename} with dimensions:', header)
            w = int(header[0])
            h = int(header[1])

            # create new grid to populate
            preset = Grid(w, h)
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

    def save(self, filename):
        '''
        Writes the current grid data to a text file (filename)
        '''
        with open(filename, 'wt') as f:
            # place grid dimensions in header
            f.write(f'{self.width},{self.height}\n')

            for x in range(self.width):
                for y in range(self.height):
                    f.write(str(self.matrix[x][y]['status']))
                f.write('\n')

    def label(self, i, generations):
        '''
        Creates a label for the grid display in the terminal (generation)
        '''
        print(F'Generation: \t{i}/{generations}')
        print('---' * self.height, end='-\n')

    def display(self):
        '''
        Displays the current grid configuration (none)
        '''
        # column numbers
        print(RED, end='  ')
        for x in range(self.height):
            print(f'{x:2d}', end=' ')
        print(WHITE)

        for x in range(self.width):
            # row numbers
            print(CYAN + F'{x:2d}' + WHITE, end='')

            for y in range(self.height):
                if self.matrix[x][y]['status'] == ALIVE:
                    print(YELLOW + ' ■ ', end=WHITE)
                else:
                    print(GRAY + ' □ ', end=WHITE)
            print()

    def census(self):
        '''
        Counts the number of currently living cells in the grid (None)
        '''
        count = 0
        for x in range(self.width):
            for y in range(self.height):
                count += self.matrix[x][y]['status']  # alive = 1
        return count

    def check_neighbors(self, x, y):
        '''
        Counts the number of living neighbors (x, y positions)
        '''
        neighbor_count = 0
        h = self.height - 1
        w = self.width - 1

        if x > 0:
            neighbor_count += self.matrix[x-1][y]['status']  # alive = 1
            if y > 0:
                neighbor_count += self.matrix[x-1][y-1]['status']
            if y < h:
                neighbor_count += self.matrix[x-1][y+1]['status']

        if x < w:
            neighbor_count += self.matrix[x+1][y]['status']
            if y > 0:
                neighbor_count += self.matrix[x+1][y-1]['status']
            if y < h:
                neighbor_count += self.matrix[x+1][y+1]['status']

        if y > 0:
            neighbor_count += self.matrix[x][y-1]['status']
        if y < h:
            neighbor_count += self.matrix[x][y+1]['status']

        return neighbor_count

    def stats(self, living, births, deaths, survivors):
        '''
        Prints stats of the current grid (Living, Born, Deaths, Survivors)
        '''
        print(f'Before: {living:>3}')
        print(f'       +{births:>3d} (born)')
        print(f'       -{deaths:>3d} (died)')
        print(f'After:  {self.census():3d} ({survivors} survivors)')
        print()

    def iterate(self, generations, display_all=True, frame_delay=1):
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
            living = self.census()
            births = 0
            deaths = 0
            survivors = 0
            stale = True

            for x in range(self.width):
                column = []
                for y in range(self.height):
                    cell = self.matrix[x][y]

                    neighbor_count = self.check_neighbors(x, y)

                    # check grid rules
                    if cell['status'] == ALIVE:
                        if neighbor_count < 2:  # rule 1
                            column.append({'x': x,  'y': y, 'status': DEAD})
                            deaths += 1
                            total_died += 1
                            stale = False

                        elif neighbor_count < 4:  # rule 2
                            column.append({'x': x,  'y': y, 'status': ALIVE})
                            survivors += 1

                        elif neighbor_count > 3:  # rule 3
                            column.append({'x': x,  'y': y, 'status': DEAD})
                            deaths += 1
                            total_died += 1
                            stale = False

                    else:  # dead cell
                        if neighbor_count == 3:  # rule 4
                            column.append({'x': x,  'y': y, 'status': ALIVE})
                            births += 1
                            total_born += 1
                            stale = False

                        else:  # default = dead
                            column.append({'x': x,  'y': y, 'status': DEAD})

                subsequent_matrix.append(column)
            self.matrix = subsequent_matrix  # update matrix

            # label generation & display generation statistics
            if display_all:
                clear()
                self.label(i+1, generations)
                self.display()
                self.stats(living, births, deaths, survivors)

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
            self.stats(living, births, deaths, survivors)

        # display lifetime statistics
        else:
            time.sleep(frame_delay)
            print('Lifetime statistics:')
            print(f'born:     {total_born:>3d}')
            print(f'died:     {total_died:>3d}')
            print()

    def next(self):
        '''
        Shows the next generation of the grid (None)
        '''
        self.iterate(1, False)  # step size, don't display all
