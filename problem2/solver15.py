#1)	Set of states S: Any arrangement of 15 tiles on a 4x4 board 
#	(Note some arrangements are not solvable)
#2)	Initial State: a 15 puzzle board arrangement as given in a text file
#3)	Successor Function SUCC: The successor function returns 
#	the four possible boards that result from the four possible
#	moves that are available, Left, Right, Down, and Up
#4)	Goal state: 15 puzzle goal state
#5)	Cost function: Cost = 1 for each edge traveled between nodes. The number 
#	of edges traveled is the total cost. 
#	to reach the goal state is the total cost.
#6)	Heuristic Function: The heuristic funtion chooses the succesor state
#	with the lowest number of misplaced tiles 

#References:
#
#Learned how to read a .txt file into python from the command line at:
#https://stackoverflow.com/questions/7439145/i-want-to-read-in-a-file-from-the-command-line-in-python
#
#Learned how to create a matrix from a text file at:
#http://stackoverflow.com/questions/31877901/python-string-to-matrix-representation
#
#Learned how to find the index of an item in a list of lists here:
#http://stackoverflow.com/questions/9553638/python-find-the-index-of-an-item-in-a-list-of-lists

import sys

#open text file from the command line and store as a matrix
with open(sys.argv[1], 'r') as f:
    text_puzzle = f.read().splitlines()

puzzle_unordered = []
for line in text_puzzle:
    sublist = []
    for tile in line.split(' '):
        sublist.append(int(tile))
    puzzle_unordered.append(sublist)
	
print puzzle_unordered

#Heuristic function (number of misplaced tiles)
def heuristic_misplaced():
	goal_state = ([[1, 2, 3, 4],[5, 6, 7, 8], [9, 10, 11, 12],[13, 14, 15, 0]])
	misplaced = 0
	for i in range(4):
		for j in range(4):
   			if puzzle_unordered[i][j] != goal_state[i][j]:
   		   		misplaced += 1
	return misplaced

# move zero tile up, save move as 'D'
#def move_up(): 

#move zero tile down, save move as 'U'
#def move_down():

#move zero tile right, save move as 'L'
#def move_right():

#move zero tile left, save move as 'R'
#def move_left():


#Successor function (returns 4 nodes representing the 4 possible moves)

possible_moves = []

#find the location of zero
for i,list in enumerate(puzzle_unordered):
   	for j,tile in enumerate(list):
       		if tile == 0:
       			zero_position = i, j
			print zero_position

			#Top side
			#top left corner
			if zero_position[0] == 0:
				if zero_position[1] == 0:
					print "in top left corner"
			#bottom left corner
				else:
					if zero_position[1] == 3:
						print "in top right corner"
			#top row middle		
					else:
						print "in top row middle"
								
			#Bottom side
			#bottom left corner
			if zero_position[0] == 3:
				if zero_position[1] == 0:
					print "in bottom left corner"
			#bottom right corner
				else:
					if zero_position[1] == 3:
						print "in bottom right corner"
			#bottom row middle		
					else: 
						print "in bottom row middle"


			#left side middle
			if zero_position[1] == 0:
				if zero_position[0] == 1 or zero_position == 2:
					print "on left side middle"
			#right side middle
			if zero_position[1] == 3:
				if zero_position[0] == 1 or zero_position == 2:
					print "on right side middle"

			#center tiles
			if zero_position[0] == 1 or zero_position[0] == 2:
				if zero_position[1] == 1 or zero_position[1] == 2:
					print "middle tile"


			
#A* search algorithm
#def astar():

#Returns a list of all moves
#def moves(): 
#    output = [] 