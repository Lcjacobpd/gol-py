# grid.py
# defines the space in which the individual cells exist

# Cell Rules:
#	1. Cells are either alive or dead
#	2. Cells have 8 neighbors (N,E,S,W and diagonals)
#	3. Neighbors outside the bounds of the grid are assumed dead

# Rules of the Grid:
#	1. Any live cell with fewer than two live white neighbors dies
#	2. Any live cell with 2-3 live neighbors lives on to the next generation
#	3. Any live cell with more than 3 live neighbors dies
#	4. Any dead cell with 3 live neighbors becomes alive

import random
import csv


# World space definition
class Grid:
	 
	#CONTSTRUCTOR
	def __init__(self, width, height):
		self.height = height
		self.width  = width
		self.matrix = []

		#each cell has x, y, status (0 = dead, 1 = alive)
		for x in range(width):
			column = []
			for y in range(height):
				column.append({'x': x, 'y': y, 'status': 0})

			self.matrix.append(column)


	#DISPLAY WORLD MATRIX
	def display(self):
		#print header
		print(u"\u001b[31m  ", end="")
		for x in range(self.height):
			print(f"{x:2d}", end=" ")
		print(u"\u001b[0m")

		#print □ in living cells
		for x in range(self.width):
			print(u"\u001b[36m" + f"{x:2d}", end=u"\u001b[0m")
			for y in range(self.height):

				#print □ in living cels
				if self.matrix[x][y]['status'] == 1:
					print(u"\u001b[33m ■ \u001b[0m", end="")
				else:
					print(" □ ", end="")
			print()


	#RANDOMLY POPULATE CELLS (50-50 chance)
	def populate(self):
		for x in range(self.width):
			for y in range(self.height):
				self.matrix[x][y]['status'] = random.choice([1,0]) 
	

	#READ TEMPLATE FROM FILE
	def template(filename):
		f = open(filename, 'rt')
		rows = csv.reader(f)
		
		#header of file containts grid dimmensions
		header = next(rows)
		print()
		print(f"Reading {filename} with dimensions:", header)
		w = int(header[0])
		h = int(header[1])	
	
		#create new grid to populate
		preset = Grid(w, h)

		xpos = 0 #x position marker
		ypos = 0
		for row in rows:
			xpos = 0
			for char in row[0]:
				preset.matrix[ypos][xpos]['status'] = int(char)
				xpos += 1
			ypos += 1 

		return  preset
	
	
	#DISPLAY SEVERAL GENERATIONS OF THE GRID
	def iterate(self, generations, display_all = True):
		#lifetime statistic variables
		total_died = 0;
		total_born = 0;
		
		#label generation
		if display_all:
			print()
			print("Generation: \t", 0)
			for j in range(self.width):
				print("---", end="")
			print('-')
			
		#display initial grid
		if display_all: self.display()
		print()
		
		for i in range(generations - 1):
			
			
			#create next generation according to the grid rules
			subsequent_matrix = []
			h = self.height - 1
			w = self.width  - 1

			#generation statistics
			alive = self.census()
			born = 0
			died = 0
			survived = 0

			for x in range(self.width):
				sub_column = []
				for y in range(self.height):
					cell = self.matrix[x][y]
					neighbor_count = 0 #living neighbors

					#determin living neighbors
					if x > 0:
						neighbor_count += self.matrix[x-1][y]['status'] #alive = 1
						if y > 0: neighbor_count += self.matrix[x-1][y-1]['status']
						if y < h: neighbor_count += self.matrix[x-1][y+1]['status']
					
					if x < w:
						neighbor_count += self.matrix[x+1][y]['status']
						if y > 0: neighbor_count += self.matrix[x+1][y-1]['status']
						if y < h: neighbor_count += self.matrix[x+1][y+1]['status']

					if y > 0: neighbor_count += self.matrix[x][y-1]['status']
					if y < h: neighbor_count += self.matrix[x][y+1]['status']

					#check grid rules	
					if cell['status'] == 1: #living cell
						if neighbor_count < 2: #rule 1
							sub_column.append({'x':x, 'y':y, 'status':0})
							died += 1
							total_died += 1

						elif neighbor_count < 4: #rule 2
							sub_column.append({'x':x, 'y':y, 'status':1})
							survived += 1

						elif neighbor_count > 3: #rule 3
							sub_column.append({'x':x, 'y':y, 'status':0})
							died += 1
							total_died += 1

					else: #dead cell
						if neighbor_count == 3: #rule 4
							sub_column.append({'x':x, 'y':y, 'status':1})
							born += 1
							total_born += 1

						else: #default = dead
							sub_column.append({'x':x, 'y':y, 'status':0})			
	
				subsequent_matrix.append(sub_column)
			self.matrix = subsequent_matrix #update matrix

			#label generation
			if display_all:
				print()
				print("Generation: \t", i+1)
				for j in range(self.width):
					print("---", end="")
				print('-')

			#display grid (starting with inital)
			if display_all: self.display()
			
			#display generation statistics
			if display_all:
				print(f"Before: {alive:>3}")
				print(f"       +{born:>3d} (born)")
				print(f"       -{died:>3d} (died)")
				print(f"After:  {self.census():3d} ({survived} survivors)")
				print()	
		
		#display total lifetime statistics
		if display_all:
			print("Final statistics:")
			print(f"born:     {total_born:>3d}")
			print(f"died:     {total_died:>3d}")
			print()


	#SKIP FORWARD N GENERATIONS
	def advance(self, n, display=False):
		if n > 1:
			print(f"Skipping to generation {n}...")
		self.iterate(n, display) #iterate showing only last generation
		
	
	
	#GO TO THE NEXT GENERATION
	def next(self):
		self.iterate(2, False)
		self.display()
		

	#COUNT LIVNG CELLS IN GRIDSPACE
	def census(self):
		count = 0
		for x in range(self.width):
			for y in range(self.height):
				count += self.matrix[x][y]['status'] #alive = 1

		return count




#TEST AREA

import argparse
#setup parser
parser = argparse.ArgumentParser(description="get user input")
parser.add_argument("w", type=int)
parser.add_argument("h", type=int)
parser.add_argument("--template")
parser.add_argument("--gen", type=int)
parser.add_argument("--repl")
args = parser.parse_args()


#process user parameters
if args.repl: #manual control
	m = Grid(10,10) #default to be overwritten

	#check for template
	if args.template:
		m = Grid.template(args.template)
	else:
		m = Grid(args.w, args.h)	

	print("Enabling REPL control...")
	m.display()
	
	#runtime loop
	command = "run"
	while command != "stop":
		print()
		print("next  - show next generation")
		print("alter - change cell state")
		print("reset - create new grid")
		print("exit")
		print("----------")

		#get user command
		command = input()

		#get and display next generation
		if command == "next":
			m.next()
		
		#reset/create new grid		
		elif command == "reset":
			print()
			print("\tload   - load template file")
			print("\trandom - randomly populate")
			print("\tclean  - empty grid")
			print("\t----------")
			command = input("\t")
			
			if command == "load":
				filename = input("Enter template file name: ")
				m = Grid.template(filename)
				m.display()
				
			elif command == "random" or command == "clean":
				dimensions = input("\tHeight, Width:").split(',')
				h = int(dimensions[0])
				w = int(dimensions[1])
				m = Grid(h, w) #clean grid
				
				if command == "random":
					#generate random grid
					m.populate()

				m.display()
			
			else:
				print("\tUnknown command: cancelling")
					
		#change cell state
		elif command == "alter":
			#get cell to be modified
			cell_position = input(u"\tCell position (\u001b[36my\u001b[0m" + ',' + u"\u001b[31mx\u001b[0m): ").split(',')
			x = int(cell_position[0])
			y = int(cell_position[1])
			
			#ensure position is valid
			while x < 0 or x >= m.width or y < 0 or y >= m.height: 
				print("\tPosition is out of bounds")
				cell_position = input(u"\tCell position (\u001b[36my\u001b[0m" + ',' + u"\u001b[31mx\u001b[0m): ").split(',')	
				x = int(cell_position[0])
				y = int(cell_position[1])
				
			#get new cell state
			cell_state = input("\t1 = alive, 0 = dead ")
			
			#update cell in grid & display changes
			m.matrix[x][y]['status'] = int(cell_state)
			m.display()
			
		#close program		
		elif command == "exit": 
			print("Exiting...")
			break
		


elif args.template: #if template is specified, disregard dimensions
	m = Grid.template(args.template)
	
	if args.gen: #call iterate if necessary
		print(f"Showing {args.gen} generations...")
		m.iterate(args.gen)
	else:
		m.display()

elif args.w and args.h:
	print("No template specified, assuming random population")
	m = Grid(args.w, args.h)
	m.populate()

	if args.gen:
		print(f"Showing {args.gen} generations...")
		m.iterate(args.gen)
	else:
		m.display()



