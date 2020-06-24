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


# World space definition
class Grid:
	 
	#constructor
	def __init__(self, height, width):
		self.height = height
		self.width  = width
		self.matrix = []

		#each cell has x, y, status (0 = dead, 1 = alive)
		for x in range(width):
			column = []
			for y in range(height):
				column.append({'x': x, 'y': y, 'status': 0})

			self.matrix.append(column)


	#display world matrix
	def display(self):
		#print header
		print("  ", end="")
		for x in range(self.width):
			print(f"{x:2d}", end=" ")
		print()

		#print □ in living cells
		for x in range(self.width):
			print(f"{x:2d}", end="")
			for y in range(self.height):

				#print □ in living cels
				if self.matrix[x][y]['status'] == 1:
					print(" ■ ", end="")
				else:
					print(" □ ", end="")
			print()


	#randomly populate world cells (50-50 chance)
	def populate(self):
		for x in range(self.width):
			for y in range(self.height):
				self.matrix[x][y]['status'] = random.choice([1,0]) 
	

	#display several generations of the grid
	def iterate(self, generations):
		#lifetime statistic variables
		total_died = 0;
		total_born = 0;

		for i in range(generations):
			#label generation
			print()
			print("Generation: \t", i)
			for j in range(self.width):
				print("---", end="")
			print('-')

			#display grid (starting with inital)
			self.display()
			
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
			print(f"Before: {alive:>3}")
			print(f"       +{born:>3d} (born)")
			print(f"       -{died:>3d} (died)")
			print(f"After:  {self.census():3d} ({survived} survivors)")
			print()	

		#display total lifetime statistics
		print("Final statistics:")
		print(f"born:     {total_born:>3d}")
		print(f"died:     {total_died:>3d}")
		print()

	#count the number of living cells in the grid					
	def census(self):
		count = 0
		for x in range(self.width):
			for y in range(self.height):
				count += self.matrix[x][y]['status'] #alive = 1

		return count

m = Grid(25, 25)
m.display()
m.populate()
m.iterate(5)



