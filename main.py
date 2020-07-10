'''
Facilitate user control of the Grid class
'''
# !/usr/bin/env python3
import argparse
import time
import typing
import collections
from os import system
from grid import Grid


# DISPLAY UTILITIES
def clear() -> None:
    '''
    reset terminal screen space
    '''
    _ = system('clear')


RED = '\u001b[31m'
CYAN = '\u001b[36m'
YELLOW = '\u001b[33m'
GRAY = '\u001b[1;30m'
WHITE = '\u001b[0m'

ALIVE = 1
DEAD = 0


# ARGEPARSE SETUP
parser = argparse.ArgumentParser(
    description='Create, view and manage grids in Conways game of life'
)
parser.add_argument(
    '--width',
    type=int,
    default=20,
)
parser.add_argument(
    '--height',
    type=int,
    default=20,
)
parser.add_argument('--load')
parser.add_argument('--gen', type=int)
parser.add_argument(
    '--repl',
    action='store_true'
)
args = parser.parse_args()


def warning(name: str, minimum: int, default: int) -> int:
    '''
    Create generic warning
    '''
    print('\t\t' + YELLOW + '[!] ' + WHITE, end='')
    print(F'{name} must be greater than {minimum}')
    print(F'\t\tdefaulting to {default}...')
    time.sleep(3)
    print('\n')
    clear()
    grid.display()
    return default


iConfig = collections.namedtuple('iConfig', [
    'delay',
    'generations'
])

def iterateconfig() -> 'iConfig':
    '''
    retrieve desired generation settings from user (none)
    '''
    delay = 1.0
    generations = 50
    command = ''

    while command != 'begin':
        options = [
            '', '\t..', F'\tdelay: {delay}',
            F'\tgenerations: {generations}', '\tbegin'
        ]
        for item in options:
            print(item)
        print('\t' + '-' * 9)
        command = input('\t')

        if command == '..':  # cancel
            clear()
            return iConfig(-1, -1)

        if command == 'delay':
            delay = float(input('\t\t(float) set delay: '))
            if delay <= 0:
                delay = float(warning('delay', 0, 1))

        elif command == 'generations':
            generations = int(input('\t\t(int) set generations: '))
            if generations <= 1:
                generations = warning('generations', 1, 2)

        if command == 'begin':
            clear()
            return iConfig(float(delay), generations)
    return iConfig(float(delay), generations)


rConfig = collections.namedtuple('rConfig', [
    'type',
    'source',
    'height',
    'width'
])

def resetconfig() -> 'rConfig':
    '''
    get specific instructions for resetting gridspace
    '''
    command = ''
    options = [
        '', '\t..', '\tload   - load template file',
        '\trandom - randomly populate', '\tclean  - empty grid'
    ]

    while command != 'stop':
        for item in options:
            print(item)
        print('\t' + '-' * 9)
        command = input('\t')

        if command == '..':  # cancel
            clear()
            return rConfig('none', 'none', -1, -1)

        if command == 'load':
            filename = input('\tname of template file: ')
            return rConfig('load', filename, -1, -1)

        if command in ('random', 'clean'):
            size = input(CYAN + '\theight' + WHITE + ',' +
                               RED + 'width' + WHITE + ': ')
            dimensions = size.split(',')

            try:
                height = int(dimensions[0])
                width = int(dimensions[1])
            except Exception:
                print('\t\t' + YELLOW + '[!] ' + WHITE, end='')
                print('dimensions must be comma separated integers')
                print('\t\tdefaulting to 10,10...')
                height = 10
                width = 10
                time.sleep(3)

            if height < 5:
                height = warning('height', 4, 5)
            if width < 5:
                width = warning('width', 4, 5)

            return rConfig(command, 'none', height, width)
    return rConfig('none', 'none', -1, -1)  # error catch


def alterconfig(grid: Grid) -> None:
    '''
    retreive and verify changes to cells in the matrix (grid instance)
    '''
    command = ''
    options = [
        '', '\t..', RED + '\txpos' + WHITE + ', ' +
        CYAN + 'ypos' + WHITE + ', status']
    while command != 'stop':
        for item in options:
            print(item)
        print('\t' + '-' * 9)
        command = input('\t')

        if command == '..':
            clear()
            return
        # else
        try:
            details = command.split(',')
            ypos = int(details[0])
            xpos = int(details[1])
            status = int(details[2])
        except Exception:
            print('\t\t' + YELLOW + '[!] ' + WHITE, end='')
            print('x, y position & status must be comma separated integers')
            print('\t\tstatus: 0 = dead, 1 = alive')
            continue

        # check for valid position
        if xpos < 0 or xpos >= grid.width or ypos < 0 or ypos >= grid.height:
            print('\t\t' + YELLOW + '[!] ' + WHITE, end='')
            print('x, y position must be within the gridspace')

        else:  # is valid
            status = ALIVE if status > 0 else DEAD
            grid.matrix[xpos][ypos]['status'] = status
            clear()
            print('\n')
            grid.display()


# RUNTIME ENVIRONMENT
def manual_control(grid: Grid) -> None:
    '''
    REPL control of the current gridspace (grid instance)
    '''
    command = ''
    options = [
        '', 'next  - show next generation', 'run   - iterate generations',
        'alter - change cell state', 'reset - create new grid',
        'save  - create template file', 'exit'
    ]

    while command != 'stop':
        for item in options:
            print(item)
        print('-' * 9)

        command = input()

        if command == 'next':
            grid.next()

        elif command == 'run':
            iSettings = iterateconfig()
            if iSettings[0] == -1:
                print('\n')
                grid.display()
                continue  # catch run cancel
            # else
            grid.iterate(iSettings[1], True, iSettings[0])

        elif command == 'reset':
            rSettings = resetconfig()
            if rSettings[0] == 'none':
                print('\n')
                grid.display()
                continue  # catch reset cancel
            if rSettings[0] == 'load':
                grid = Grid.load(rSettings[1])
            else:
                height = rSettings[2]
                width = rSettings[3]
                grid = Grid(height, width)

                if rSettings[0] == 'random':
                    grid.populate()
            clear()
            print('\n')
            grid.display()

        elif command == 'alter':
            alterconfig(grid)
            clear()
            print('\n')
            grid.display()

        elif command == 'save':
            print()
            filename = input('\tEnter output filename: ')
            grid.save(filename)

        elif command == 'exit':
            print('exiting...')
            break


# END OF REPL ENVIRONMENT
# -------------------------------------------------------------------


# RENDER SINGLE GRID OR SEVERAL GENERATIONS FROM CONSOLE ARGS
def argparse_render(grid: Grid, args: argparse.Namespace) -> None:
    '''
    render one or more generations from argparse
    '''
    if args.gen:  # call iterate if necessary
        print(f'Showing {args.gen} generations...')
        # generations, display_all, frame_delay
        grid.iterate(args.gen, True, 1)
    else:
        grid.display()


# PROCESS USER PARAMETERS
if args.repl:  # manual control
    clear()
    grid = Grid(20, 20)  # default to be overwritten

    # check for template
    if args.load:
        grid = Grid.load(args.load)
    else:
        # generate blank with dimensions otherwise
        grid = Grid(args.height, args.width)
    print('\n')
    grid.display()

    # runtime loop
    manual_control(grid)

elif args.load:  # if load is specified, disregard dimensions
    grid = Grid.load(args.load)
    argparse_render(grid, args)  # render single grid or several generations

elif args.width and args.height:
    clear()
    print('No load template specified, ' +
          'assuming random population')
    grid = Grid(args.height, args.width)
    grid.populate()
    argparse_render(grid, args)
