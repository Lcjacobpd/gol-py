'''
Facilitate user control of the Grid class
'''
# !/usr/bin/env python3
import argparse

import typing
import collections
from os import system
from grid import Grid
from Util import Util


ALIVE = 1
DEAD = 0


# ARGEPARSE SETUP
parser = argparse.ArgumentParser(
    description='Create, view and manage grids in Conways game of life'
)
parser.add_argument(
    '-dim',
    type=str,
    default='20,20',
)
parser.add_argument('--load')
parser.add_argument('--gen', type=int)
args = parser.parse_args()


if args.load:  # if load is specified, disregard dimensions
    grid = Grid.load(args.load)

elif args.dim:
    Util.clear()
    print('No template specified, populating randomly...\n')
    dim = args.dim.split(',')
    grid = Grid(dim)
    grid.populate()
    grid.display()
    
    # call iterate if necessary
    if args.gen:
        input('\nPress enter to begin...')
        Util.clear()
        grid.iterate(args.gen)
        
