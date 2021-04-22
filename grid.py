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
import time
from util import Util


ALIVE = 1
DEAD = 0


class Grid:
    '''
    contains the matrix of cells and its dimensions
    '''
    def __init__(self, dim: list) -> None:
        '''
        Constructs an instance of a gridspace (width, height)
        '''
        self.width = int(dim[0])
        self.height = int(dim[1])
        self.matrix = []

        # each cell has status (0 = dead, 1 = alive)
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                row.append({'status': DEAD})
            self.matrix.append(row)

    def populate(self) -> None:
        '''
        Randomly populates the cells of a grid (none)
        '''
        for ypos in range(self.height):
            for xpos in range(self.width):
                status = random.choice([ALIVE, DEAD])
                self.matrix[ypos][xpos]['status'] = status

    @staticmethod
    def load(filename: str) -> 'Grid':
        '''
        Create datagrid from template file (filename)
        '''
        with open(filename, 'rt') as infile:
            lines = infile.readlines()
            width = len(lines[0]) -1
            height = len(lines) -1
            dim = [width, height]

            # create new grid to populate
            preset = Grid(dim)
            preset.display()

            # convert document lines to grid rows
            for ypos in range(height):
                for xpos in range(width):
                    val = int(lines[ypos][xpos])
                    preset.matrix[ypos][xpos]['status'] = val

            return preset

    def save(self, filename: str) -> None:
        '''
        Writes the current grid data to a text file (filename)
        '''
        with open(filename, 'wt') as outfile:
            # place grid dimensions in header
            outfile.write(f'{self.width},{self.height}\n')

            for ypos in range(self.height):
                for xpos in range(self.width):
                    outfile.write(str(self.matrix[ypos][xpos]['status']))
                outfile.write('\n')

    def label(self, iteration: int, generations: int) -> None:
        '''
        Creates a label for the grid display in the terminal (generation)
        '''
        print('Gen:' + f'{iteration}/{generations}'.rjust(self.width*2-2, ' '))
        print('▀▀' * self.width, end='▀▀\n')

    def display(self) -> None:
        '''
        Displays the current grid configuration (none)
        '''
        # columns
        Util.red()
        print('', end='  ')
        for xpos in range(self.width):
            print('░░' if xpos % 2 == 0 else '  ', end='')
        print()

        for ypos in range(self.height):
            # rows
            Util.cyan()
            print('░░' if ypos % 2 == 0 else '  ', end='')
            Util.white()

            for xpos in range(self.width):

                if self.matrix[ypos][xpos]['status'] == ALIVE:
                    print('██', end='')
                else:
                    print('  ', end='')
            print()

    def census(self) -> int:
        '''
        Counts the number of currently living cells in the grid (None)
        '''
        count = 0
        for xpos in range(self.width):
            for ypos in range(self.height):
                count += self.matrix[ypos][xpos]['status']  # alive = 1
        return count

    def check_neighbors(self, ypos: int, xpos: int) -> int:
        '''
        Counts the number of living neighbors (x, y positions)
        '''
        neighbor_count = 0
        height = self.height - 1
        width = self.width - 1
        left = xpos - 1
        right = xpos + 1
        down = ypos - 1
        upper = ypos + 1

        if xpos > 0:
            neighbor_count += self.matrix[ypos][left]['status']
            if ypos > 0:
                neighbor_count += self.matrix[down][left]['status']
            if ypos < height:
                neighbor_count += self.matrix[upper][left]['status']

        if xpos < width:
            neighbor_count += self.matrix[ypos][right]['status']
            if ypos > 0:
                neighbor_count += self.matrix[down][right]['status']
            if ypos < height:
                neighbor_count += self.matrix[upper][right]['status']

        if ypos > 0:
            neighbor_count += self.matrix[down][xpos]['status']
        if ypos < height:
            neighbor_count += self.matrix[upper][xpos]['status']

        return neighbor_count

    def stats(self, stats: dict) -> None:
        '''
        Prints stats of the current grid (Living, Born, Deaths, Survivors)
        '''
        print()
        print(f'Before: {stats["living"]:>3}')
        print(f'       +{stats["born"]:>3d} (born)')
        print(f'       -{stats["died"]:>3d} (died)')
        print(f'After:  {self.census():3d} ({stats["survivors"]} survivors)')
        print()

    def iterate(self, generations: int) -> None:
        '''
        Display several generations of the grid
        '''
        # lifetime statistics variables
        total_died = 0
        total_born = 0

        self.label(0, generations)
        self.display()
        print()

        # process grid generations
        for i in range(generations):
            time.sleep(0.5)  # apply delay

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

            for ypos in range(self.height):
                row = []
                for xpos in range(self.width):
                    cell = self.matrix[ypos][xpos]

                    neighbor_count = self.check_neighbors(ypos, xpos)

                    # check grid rules
                    if cell['status'] == ALIVE:
                        if neighbor_count < 2:  # rule 1
                            row.append({
                                'status': DEAD
                            })
                            stats['died'] += 1
                            total_died += 1
                            stale = False

                        elif neighbor_count < 4:  # rule 2
                            row.append({
                                'status': ALIVE
                            })
                            stats['survivors'] += 1

                        elif neighbor_count > 3:  # rule 3
                            row.append({
                                'status': DEAD
                            })
                            stats['died'] += 1
                            total_died += 1
                            stale = False

                    else:  # dead cell
                        if neighbor_count == 3:  # rule 4
                            row.append({
                                'status': ALIVE
                            })
                            stats['born'] += 1
                            total_born += 1
                            stale = False

                        else:  # default = dead
                            row.append({
                                'status': DEAD
                            })

                subsequent_matrix.append(row)
            self.matrix = subsequent_matrix  # update matrix

            # label generation & display generation statistics

            Util.clear()
            self.label(i+1, generations)
            self.display()
            self.stats(stats)

            # if stale stop iterations (not for 'next' command)
            if stale:
                print()
                print('Grid is stagnant; stopping life cycle...')
                return

        time.sleep(1)
        print('Lifetime statistics:')
        print(f'born:     {total_born:>3d}')
        print(f'died:     {total_died:>3d}')
        print()

    def next(self) -> None:
        '''
        Shows the next generation of the grid (None)
        '''
        self.iterate(1)  # step size, don't display all
