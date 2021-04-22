'''
Facilitate user control of the Grid class
'''
# !/usr/bin/env python3
import argparse
from grid import Grid
from util import Util


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
    help='Grid dimensions: width,height'
)
parser.add_argument(
    '-load', type=str,
    help='Filepath to template'
)
parser.add_argument(
    '-gen',
    type=int,
    help='Number of generations to display'
)
args = parser.parse_args()


Util.clear()

# Load from file
if args.load:
    print(f'Loading template: {args.load}...\n')
    grid = Grid.load(args.load)

# Populate dimensions randomly
elif args.dim:
    print('No template specified, populating randomly...\n')
    dim = args.dim.split(',')
    grid = Grid(dim)
    grid.populate()
    grid.display()

# Call iterate if necessary
if args.gen:
    input('\nPress enter to begin...')
    Util.clear()
    grid.iterate(args.gen)
