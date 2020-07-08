#!/usr/bin/env python3
from grid import Grid
from os import system
import argparse
import time

#DISPLAY UTILITIES
def clear():
    _ = system('clear')

RED    = '\u001b[31m'
CYAN   = '\u001b[36m'
YELLOW = '\u001b[33m'
GRAY   = '\u001b[1;30m'
WHITE  = '\u001b[0m'

ALIVE = 1
DEAD = 0


#ARGEPARSE SETUP
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


def warning(name, minimum, default):
    print('\t\t' + YELLOW + '[!] ' + WHITE, end='')
    print(F'{name} must be greater than {minimum}')
    print(F'\t\tdefaulting to {default}...')
    time.sleep(3)
    print('\n')
    clear()
    m.display()
    return default


def iterateconfig():
    '''
    retrieve desired generation settings from user (none)
    '''
    delay = 1
    generations = 50
    command = ''


    while command != 'begin':
        options = ['', '\t..', F'\tdelay: {delay}', F'\tgenerations: {generations}', '\tbegin']
        for o in options: print(o)
        print('\t' + '-' * 9)
        command = input('\t')

        if command == '..': #cancel
            clear()
            return {'delay':-1, 'generations':-1}

        elif command == 'delay':
            delay = float(input('\t\t(float) set delay: '))
            if not(delay > 0):
                delay = warning('delay', 0, 1)

        elif command == 'generations':
            generations = int(input('\t\t(int) set generations: '))
            if not(generations > 1):
                generations = warning('generations', 1, 2)

        if command == 'begin':
            clear()
            return {'delay':delay, 'generations':generations}


def resetconfig():
    '''
    get specific instructions for resetting gridspace
    '''
    command =''
    options = ['', '\t..', '\tload   - load template file', '\trandom - randomly populate',
        '\tclean  - empty grid'
    ]

    while command != 'stop':
        for o in options: print(o)
        print('\t' + '-' * 9)
        command = input('\t')

        if command == '..': #cancel
            clear()
            return {'type':'none', 'size':(-1, -1)}

        elif command == 'load':
            filename = input('\tname of template file: ')
            return {'type':'load', 'source':filename}

        elif command == 'random' or command == 'clean':
            dimensions = input(CYAN + '\theight' + WHITE + ',' + RED + 'width' + WHITE + ': ')
            dimensions = dimensions.split(',')

            try:
                dimensions[0] = int(dimensions[0])
                dimensions[1] = int(dimensions[1])
            except:
                print('\t\t' + YELLOW + '[!] ' + WHITE, end='')
                print('dimensions must be comma separated integers')
                print('\t\tdefaulting to 10,10...')
                dimensions = [10, 10]
                time.sleep(3)

            if dimensions[0] < 5:
                dimensions[0] = warning('height', 4, 5)
            if dimensions[1] < 5:
                dimensions[1] = warning('width', 4, 5)

            return {'type': command, 'size':dimensions}


def alterconfig(grid):
    '''
    retreive and verify changes to cells in the matrix (grid instance)
    '''
    command = ''
    options = ['', '\t..', RED + '\txpos' + WHITE + ', ' + CYAN + 'ypos' + WHITE + ', status']
    while command != 'stop':
        for o in options: print(o)
        print('\t' + '-' * 9)
        command = input('\t')

        if command == '..':
            clear()
            return
        #else
        try:
            details = command.split(',')
            ypos   = int(details[0])
            xpos   = int(details[1])
            status = int(details[2])
        except:
            print('\t\t' + YELLOW + '[!] ' + WHITE, end='')
            print('x, y position & status must be comma separated integers')
            print('\t\tstatus: 0 = dead, 1 = alive')
            continue

        #check for valid position
        if xpos < 0 or xpos >= grid.width or ypos < 0 or ypos >= grid.height:
            print('\t\t' + YELLOW + '[!] ' + WHITE, end='')
            print('x, y position must be within the gridspace')

        else: #is valid
            status = ALIVE if status > 0 else DEAD
            grid.matrix[xpos][ypos]['status'] = status
            clear()
            print('\n')
            grid.display()


#RUNTIME ENVIRONMENT
def manual_control(m):
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
        for o in options: print(o)
        print('-' * 9)

        command = input()

        if command == 'next':
            m.next()

        elif command == 'run':
            settings = iterateconfig()
            if(settings['delay'] == -1):
                print('\n')
                m.display()
                continue #catch run cancel
            #else
            m.iterate(settings['generations'], True, settings['delay'])

        elif command == 'reset':
            settings = resetconfig()
            if settings['type'] == 'none':
                print('\n')
                m.display()
                continue #catch reset cancel
            elif settings['type'] == 'load':
                m = Grid.load(settings['source'])
            else:
                h = settings['size'][0]
                w = settings['size'][1]
                m = Grid(h, w)

                if settings['type'] == 'random':
                    m.populate()
            clear()
            print('\n')
            m.display()

        elif command == 'alter':
            alterconfig(m)
            clear()
            print('\n')
            m.display()

        elif command == 'save':
            print()
            filename = input('\tEnter output filename: ')
            m.save(filename)

        elif command == 'exit':
            print('exiting...')
            break


#END OF REPL ENVIRONMENT
#-------------------------------------------------------------------


#RENDER SINGLE GRID OR SEVERAL GENERATIONS FROM CONSOLE ARGS
def argparse_render(grid, args):
    if args.gen: #call iterate if necessary
        print(f'Showing {args.gen} generations...')
        grid.iterate(args.gen, True, 1) #generations, display_all, frame_delay
    else:
        grid.display()

#PROCESS USER PARAMETERS
if args.repl: #manual control
    clear()
    m = Grid(20,20) #default to be overwritten

    #check for template
    if args.load: m = Grid.load(args.load)
    else: m = Grid(args.height, args.width) #generate blank with dimensions otherwise
    print('\n')
    m.display()

    #runtime loop
    manual_control(m)

elif args.load: #if load is specified, disregard dimensions
    m = Grid.load(args.load)
    argparse_render(m, args) #render single grid or several generations

elif args.width and args.height:
    clear()
    print('No load template specified, assuming random population')
    m = Grid(args.height, args.width)
    m.populate()
    argparse_render(m, args)


