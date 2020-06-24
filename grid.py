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
import argparse


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
		print(u"\u001b[36m  ", end="")
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

		for i in range(generations):
			#label generation
			if display_all:
				print()
				print("Generation: \t", i)
				for j in range(self.width):
					print("---", end="")
				print('-')

			#display grid (starting with inital)
			if display_all: self.display()
			
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
	def advance(self, n):
		print(f"Skipping to generation {n}...")
		self.iterate(n, False) #iterate without showing each generation
		self.display()
	
	
	#GO TO THE NEXT GENERATION
	def next(self, display = False):
		self.advance(1, False)
		self.display()
		

	#COUNT LIVNG CELLS IN GRIDSPACE
	def census(self):
		count = 0
		for x in range(self.width):
			for y in range(self.height):
				count += self.matrix[x][y]['status'] #alive = 1

		return count


#MAIN PROGRAM

#setup parser
parser = argparse.ArgumentParser(description="get user input")
parser.add_argument("w", type=int)
parser.add_argument("h", type=int)
parser.add_argument("--template")
args = parser.parse_args()

#process user parameters
if args.template: #if template is specified, disregard dimensions
	m = Grid.template(args.template)
	m.display()

elif args.w and args.h:
	m = Grid(args.w, args.h)
	m.display()



