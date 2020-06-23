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
		print(" ", end="")
		for x in range(self.width):
			print(x, end="")
		print()

		#print □ in living cells
		for x in range(self.width):
			print(x, end="")
			for y in range(self.height):

				#print □ in living cels
				if self.matrix[x][y]['status'] == 1:
					print("□", end="")
				else:
					print("_", end="")

			print()

m = Grid(5, 5)
m.display()
