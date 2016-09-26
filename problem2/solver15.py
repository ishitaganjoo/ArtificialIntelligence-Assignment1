'''
Created on Sep 18, 2016
@author: Subhash Bylaiah, Brian Trippi
'''
# 1)	Set of states S: Any arrangement of 15 tiles on a 4x4 board
#	(Note some arrangements are not solvable)
# 2)	Initial State: a 15 puzzle board arrangement as given in a text file
# 3)	Successor Function SUCC: The successor function returns
#	the four possible boards that result from the four possible
#	moves that are available, Left, Right, Down, and Up
# 4)	Goal state: 15 puzzle goal state
# 5)	Cost function: Cost = 1 for each edge traveled between nodes. The number
#	of edges traveled is the total cost. 
# 6)	Heuristic Function: The heuristic funtion chooses the succesor state
#	with the lowest number of misplaced tiles 


# SOLUTION DISCUSSION:
#   Implemented the Heuristic cost estimation using
#       1) Misplaced Tiles Heuristic
#       2) Manhattan Distance Heuristic
#   As expected, the Manhattan Distance Heuristic works better as the heuristic is more accurate and informative
#   than the Misplaced Tile Heuristic
#   For the given example input board:
#       Using Manhattan Distance Heuristic, finds solution with below characteristics
#           ('Fringe Length:', 5812, 'Num Nodes Expanded:', 2823, 'Cost till state:', 24)
#             TIME TAKEN:: 0.4 seconds
#
#       Using MISPLACED TILE Heuristic, finds solution with below characteristics
#           ('Fringe Length:', 1367490, 'Num Nodes Expanded:', 646486, 'Cost till state:', 24)
#             TIME TAKEN:: 89 seconds
#

# References:
#

######################################################################################################################
#       USES PYTHON VERSION 3
######################################################################################################################



#!/usr/local/bin/python3


import sys
import pprint
import heapq
import math
import time

if sys.version_info.major==2:
	print("warning! use python3")


# This is the GOAL STATE for the 15 Puzzle
goal_state = [[1, 2, 3, 4],
              [5, 6, 7, 8],
              [9, 10, 11, 12],
              [13, 14, 15, 0]]

# goal_state = [[1, 2, 3],
#               [4, 5, 6],
#               [7, 8, 0]]


# MANHATTAN OR MISPLACED
H_FUNCTION = 'MANHATTAN'


# Define a dictionary to represent the Directional moves based on the add/subtraction of row/col
# Ex: if ROW is subtracted (and nothing done to Col), it represents the move DOWN
moves_dict = {
        (-1,0): 'D',
        (0,-1): 'R',
        (0,1): 'L',
        (1,0): 'U'
    }

def read_input_file():
    """
    Read from the input file specified on the command prompt and create the initial board configuration
    :return: Returns the initial board config
    """
    input_puzzle = []
    # open text file from the command line and store as a matrix
    with open(sys.argv[1], 'r') as f:
        text_puzzle = f.read().splitlines()

    for line in text_puzzle:
        sublist = []
        for tile in line.split(' '):
            sublist.append(int(tile))
        input_puzzle.append(sublist)
    return input_puzzle

def heuristic_misplaced(puzzle_board):
    """
    Function to compute the cost estimate using misplaced tiles heuristic
    :param puzzle_board:
    :return: Heuristic cost estimate
    """
    misplaced = 0
    for i in range(len(puzzle_board)):
        for j in range(len(puzzle_board[0])):
            if puzzle_board[i][j] != goal_state[i][j]:
                misplaced += 1
    return misplaced


def get_goal_row_col(tile_number):
    """
    Function to compute the Goal state Row Col for any given tile number
    :param tile_number:
    :return: Row/Col of the goal state for the Tile
    """
    return (math.floor((tile_number-1)/puzzle_length), (tile_number-1)%4)


def get_manhattan_dist_to_goal(board_state):
    """
    Compute Manhattan distance for the given board
    For any Tile it is computed as the absolute Vertical distance (along the row) and Horizontal Distance(along the column)
    to reach the goal state for the tile.
    The total distance is the sum of all the distances for all tiles in the given board config
    :param board_state:
    :return: Cost for the Heuristic estimate
    """
    dist = 0
    for row in range(puzzle_length):
        for col in range(puzzle_length):
            if board_state[row][col] != 0:
                goal_row, goal_col = get_goal_row_col(board_state[row][col])
                dist = dist + abs(row - goal_row) + abs( col - goal_col)
    return dist


def generate_successors(state):
    """
    Successor function (returns 4 nodes representing the 4 possible moves)
    :param state:
    :return: List of Tuples of the form (successorstate, movedirection)
    """
    # Find the zero'th position
    zero_position = [(i, state[i].index(0)) for i in range(len(state)) if 0 in state[i]][0]
    # Create new possible posistions for the blank tile, based on the defined moves
    new_positions = [(((zero_position[0]+i)%puzzle_length, (zero_position[1]+j)%puzzle_length), (i,j)) for i in (-1, 0, +1) for j in (-1, 0, +1) if abs(i) != abs(j)]
    successors = []
    # generate successors
    for (pos, move) in new_positions:
        succ = [row[:] for row in state]
        succ[zero_position[0]][zero_position[1]] = succ[pos[0]][pos[1]]
        succ[pos[0]][pos[1]] = 0
        successors.append((succ, moves_dict[move]))
    return successors

def is_goal_state(board_state):
    if heuristic_misplaced(board_state) == 0:
        return True

def get_H_cost(succ):
    """
    Function to compute the Heuristic cost, for a given board state
         Heuristic Function to be used is defined by the H_FUNCTION constant
    :param succ: Board State
    :return: Will return heuristic cost
    """
    if H_FUNCTION == 'MANHATTAN':
        return get_manhattan_dist_to_goal(succ)
    elif H_FUNCTION == 'MISPLACED':
        return heuristic_misplaced(succ)


def solve_puzzle(initial_state):
    """
    Solution function to solve the initial Board using A* Algorithm
        Heuristic function to be used is based on the constant H_FUNCTION
    The fringe is managed as a Heap datastructure using the heapq module
    The fringe is a list of tuples of the form: (Evaluated_cost, (Cost_from_Initial, Board_state, Path_From_Initial_State))
    :param initial_state:
    :return: Board_State, Path for the Goal state
    """

    fringe = []
    closed = {}
    # heap_index = {} # Lets have a dictionary to have the index of a specific board in the heap, to make the search faster
    if is_goal_state(initial_state):
        return initial_state, []

    heapq.heappush(fringe, (0, (0, initial_state, [])))

    while fringe:
        # print("Printing fringe:")
        # print('Fringe Length:',len(fringe),'\n')
        # print('\n'.join(' '.join(map(str, row)) for row in fringe))
        (cost, (cost_till_state, board_state, path)) = heapq.heappop(fringe)
        # print((cost, (cost_till_state, board_state)))
        closed[hash(str(board_state))] = True
        if is_goal_state(board_state):
            print('Fringe Length:',len(fringe), 'Num Nodes Expanded:', len(closed), '\n', 'Cost till state:', cost_till_state)
            return board_state, path
        successors = generate_successors(board_state)
        for succ, move in successors:
            if closed.get(hash(str(succ))):
                continue

            h_cost = get_H_cost(succ)
            # print('\n', 'Cost: ', h_misplaced + cost_till_state+1, 'Heuristic:', h_misplaced)
            # print('\n'.join(' '.join(map(str, row)) for row in succ))
            new_cost = h_cost + cost_till_state+1

            # BELOW CODE TO CHECK AND ADD BETTER COST TO FRINGE MIGHT NOT BE NEEDED AS ITS VERY EXPENSIVE
            # SO, EVEN IF WE ADD A LOWER COST TO THE FRINGE IT STILL IS GOING TO PROCESS THAT FIRST,
            # INSTEAD OF A HIGHER COST ONE..
            # THE OTHER OPTION TO TRY OUT IS TO INCLUDE A DICTIONARY BASED APPROACH AND REMOVING A
            # NODE AS SUGGESTED ON https://docs.python.org/3/library/heapq.html
            # BUT IN OUR CASE EVEN THAT IS NOT NEEDED AS WE ARE ONLY GOING TO PICK AN ITEM
            # THAT IS LOWER COST

            ############################################################################################################
            # item_present = False
            # for index, item in enumerate(fringe):
            #     if item[1][1] == succ:
            #         item_present = True
            #         if item[0] > new_cost:
            #             fringe[index], fringe[-1] = fringe[-1], fringe[index]
            #             fringe.pop()
            #             heapq.heapify(fringe)
            #             heapq.heappush(fringe, (new_cost, (cost_till_state+1, succ)))
            #
            # if not item_present:
            #     heapq.heappush(fringe, (new_cost, (cost_till_state + 1, succ)))
            #     heap_index[succ] = len(fringe)
            ############################################################################################################
            heapq.heappush(fringe, (new_cost, (cost_till_state + 1, succ, path[:] + [move])))


initial_board = read_input_file()
puzzle_length = len(initial_board)

start_time = time.time()
goal, path = solve_puzzle(initial_board)
end_time = time.time()

print('\nGoal State:')
pprint.pprint(goal, indent=4)

print("Time taken to Solve", end_time - start_time, " seconds")

print("Path to goal:")
# print('['+'] ['.join(path) + ']')
print(' '.join(path))

# FOR TESTING
# successors = generate_successors(puzzle_unordered)
# for succ in successors:
#     print('\n'.join(' '.join(map(str, row)) for row in succ))
