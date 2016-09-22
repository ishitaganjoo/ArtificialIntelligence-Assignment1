#1)	Set of states S: Any arrangement of 15 tiles on a 4x4 board 
#	(Note some arrangements are not solvable)
#2)	Initial State: a 15 puzzle board arrangement as given in a text file
#3)	Successor Function SUCC: The successor function returns 
#	the four possible moves that are available, Left, Right, Down, and Up
#4)	Goal state: 15 puzzle goal state
#5)	Cost function: Cost = 1 for each move. The sum of Manhattan distances 
# 	traveled to reach the goal state is the total cost.


import sys

#open text file from the command line and store as a matrix
with open(sys.argv[1], 'r') as f:
    text_puzzle = f.read().splitlines()

puzzle_unordered = []
for tile in text_puzzle:
    sublist = []
    for num in tile.split(' '):
        sublist.append(int(num))
    puzzle_unordered.append(sublist)
	
print puzzle_unordered

#Heuristic function (number of misplaced tiles)
goal_state = ([[1, 2, 3, 4],[5, 6, 7, 8], [9, 10, 11, 12],[13, 14, 15, 0]])
print goal_state

misplaced = 0
for i in range(4):
	for j in range(4):
   		if puzzle_unordered[i][j] != goal_state[i][j]:
   		   	misplaced += 1
print misplaced	
	
#A* search algorithm using hueristic_astar
#def astar():

#use number of misplaced tiles to find best path
#def heuristic_astar():

#Returns a list of all moves
#def moves(): 
#    output = [] 