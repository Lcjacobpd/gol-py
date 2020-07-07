#!/usr/bin/env python3
from grid import Grid
from os import system

#DISPLAY UTILITIES
def clear():
    _ = system('clear')
    
RED    = "\u001b[31m"
CYAN   = "\u001b[36m"
YELLOW = "\u001b[33m"
GRAY   = "\u001b[1;30m"
WHITE  = "\u001b[0m"


#setup parser
import argparse
parser = argparse.ArgumentParser(
	description="Create, view and manage grids in Conway's Game of lifes"
)
parser.add_argument(
    "--width", 
    type=int,
    default=20,
)
parser.add_argument(
    "--height", 
    type=int,
    default=20,
)
parser.add_argument("--load")
parser.add_argument("--gen", type=int)
parser.add_argument(
    "--repl",
    action='store_true'
)
args = parser.parse_args()


#RUNTIME ENVIRONMENT
def manual_control(m):
    command = "run"
    while command != "stop":
        print()
        print("next  - show next generation")
        print("run   - iterate generations")
        print("alter - change cell state")
        print("reset - create new grid")
        print("save  - create template file")
        print("exit")
        print("-" * 9)

        command = input()

        if command == "next":
            m.next()

                        
        #produce grid generations
        if command == "run":
            #variables
            frame_delay = 1
            generations = 50
        
            #grid iteration control loop
            while command != "begin":
                print()
                print("\tenter variable name to modify")
                print(f"\t[frame_delay: {frame_delay}]")
                print(f"\t[generations: {generations}]")
                print()
                print("\tbegin")
                print("\t----------")
                command = input("\t")
                
                #modify frame delay
                if command == "frame_delay":
                    frame_delay = float(input("\t\t(float)frame_delay: "))
                    if frame_delay < 0:
                        print("\t\tDelay must be greater than 0, defaulting to 1")
                        frame_delay = 1
                
                #modify the number of generations to calculate
                elif command == "generations":
                    generations = int(input("\t\t(int)generations: "))
                    if generations < 1:
                        print("\t\tMinimum count is 1")
                        generations = 1
                
                #begin calculating generations
                elif command == "begin":
                    continue
                    
                else:
                    print("\tUnknown command: cancelling")
                    break
            #catch unknown command break
            if command != "begin": 
                command == "stop"
                continue
            
            #user chose "begin"
            clear()
            m.iterate(generations, True, frame_delay)
            
        #reset/create new grid
        elif command == "reset":
            print()
            print("\tload   - load template file")
            print("\trandom - randomly populate")
            print("\tclean  - empty grid")
            print("\t----------")
            command = input("\t")
            
            #load template file
            if command == "load":
                filename = input("\tEnter template file name: ")
                m = Grid.load(filename)
                clear()
                print("\n")
                m.display()
            
            #populate randomly or clean grid
            elif command == "random" or command == "clean":
                dimensions = input("\tHeight, Width: ").split(',')
                h = int(dimensions[0])
                w = int(dimensions[1])
                m = Grid(h, w) #clean grid
                
                if command == "random":
                    #generate random grid
                    m.populate()

                clear()
                print("\n")
                m.display()
            
            else:
                print("\tUnknown command: cancelling")
                
        #change cell state
        elif command == "alter":
            #get cell to be modified
            cell_position = input(F"\tCell position ({CYAN}y{WHITE},{RED}x{WHITE}): ").split(',')
            x = int(cell_position[0])
            y = int(cell_position[1])
            
            #ensure position is valid
            while x < 0 or x >= m.width or y < 0 or y >= m.height: 
                print("\tPosition is out of bounds")
                cell_position = input(F"\tCell position ({CYAN}y{WHITE},{RED}x{WHITE}").split(',')
                x = int(cell_position[0])
                y = int(cell_position[1])
                
            #get new cell state
            cell_state = input("\t1 = alive, 0 = dead ")
            
            #update cell in grid & display changes
            m.matrix[x][y]['status'] = int(cell_state)
            
            clear()
            m.display()
            
        #output grid to file
        elif command == "save":
            print()
            filename = input("\tEnter output filename: ")
            m.save(filename)
        
        #close program
        elif command == "exit":
            print("Exiting...")
            break


#END OF REPL ENVIRONMENT
#-------------------------------------------------------------------


#RENDER SINGLE GRID OR SEVERAL GENERATIONS FROM CONSOLE ARGS
def argparse_render(grid, args):
    if args.gen: #call iterate if necessary
        print(f"Showing {args.gen} generations...")
        grid.iterate(args.gen, True, 1) #generations, display_all, frame_delay
    else:
        grid.display()

#PROCESS USER PARAMETERS
if args.repl: #manual control
    clear()
    m = Grid(20,20) #default to be overwritten

    #check forload
    if args.load: m = Grid.load(args.load)
    else: m = Grid(args.height, args.width) #generate blank with dimensions otherwise
    print("\n")
    m.display()
    
    #runtime loop
    manual_control(m)
        
elif args.load: #if load is specified, disregard dimensions
    m = Grid.load(args.load)
    argparse_render(m, args) #render single grid or several generations

elif args.width and args.height:
    clear()
    print("No load template specified, assuming random population")
    m = Grid(args.height, args.width)
    m.populate()
    argparse_render(m, args)



