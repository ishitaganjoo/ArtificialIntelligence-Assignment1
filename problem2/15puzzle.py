import sys

#open text file from the command line and store as a list of lists
with open(sys.argv[1], 'r') as f:
    puzzle = f.read().splitlines()

print puzzle

#A* search algorithm using hueristic_astar
def astar():

#use manhattan distance to limit depth of search
def heuristic_astar():

#Returns a list of all moves
def moves(): 
    output = [] 