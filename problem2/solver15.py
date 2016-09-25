# 1)	Set of states S: Any arrangement of 15 tiles on a 4x4 board
#	(Note some arrangements are not solvable)
# 2)	Initial State: a 15 puzzle board arrangement as given in a text file
# 3)	Successor Function SUCC: The successor function returns
#	the four possible boards that result from the four possible
#	moves that are available, Left, Right, Down, and Up
# 4)	Goal state: 15 puzzle goal state
# 5)	Cost function: Cost = 1 for each edge traveled between nodes. The number
#	of edges traveled is the total cost. 
#	to reach the goal state is the total cost.
# 6)	Heuristic Function: The heuristic funtion chooses the succesor state
#	with the lowest number of misplaced tiles 

# References:
#
# Learned how to read a .txt file into python from the command line at:
# https://stackoverflow.com/questions/7439145/i-want-to-read-in-a-file-from-the-command-line-in-python
#
# Learned how to create a matrix from a text file at:
# http://stackoverflow.com/questions/31877901/python-string-to-matrix-representation
#
# Learned how to find the index of an item in a list of lists here:
# http://stackoverflow.com/questions/9553638/python-find-the-index-of-an-item-in-a-list-of-lists

import sys
import pprint
from queue import PriorityQueue
import heapq

puzzle_unordered = []
goal_state = [[1, 2, 3, 4],
              [5, 6, 7, 8],
              [9, 10, 11, 12],
              [13, 14, 15, 0]]

# goal_state = [[1, 2, 3],
#               [4, 0, 5],
#               [6, 7, 8]]

puzzle_length = -1

def read_input_file():
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

# Heuristic function (number of misplaced tiles)
def heuristic_misplaced(puzzle_board):
    misplaced = 0
    for i in range(len(puzzle_board)):
        for j in range(len(puzzle_board[0])):
            if puzzle_board[i][j] != goal_state[i][j]:
                misplaced += 1
    return misplaced


# Successor function (returns 4 nodes representing the 4 possible moves)

def generate_successors(state):
    # Find the zero'th position
    zero_position = [(i, state[i].index(0)) for i in range(len(state)) if 0 in state[i]][0]
    # Create new possible posistions for the blank tile, based on the defined moves
    new_positions = [((zero_position[0]+i)%puzzle_length, (zero_position[1]+j)%puzzle_length) for i in (-1, 0, +1) for j in (-1, 0, +1) if abs(i) != abs(j)]
    successors = []
    # generate successors
    for pos in new_positions:
        succ = [row[:] for row in state]
        succ[zero_position[0]][zero_position[1]] = succ[pos[0]][pos[1]]
        succ[pos[0]][pos[1]] = 0
        successors.append(succ)
    return successors

def is_goal_state(board_state):
    if heuristic_misplaced(board_state) == 0:
        return True

def remove_larger_item_in_fringe(fringe, state, new_cost):
    for index, item in enumerate(fringe):
        if item[1][1] == state and item[0] > new_cost:
            fringe[index], fringe[-1] = fringe[-1], fringe[index]
            fringe.pop()
            heapq.heapify(fringe)
            return True
    return False


def solve_puzzle(initial_state):
    fringe = []
    closed = {}
    heap_index = {} # Lets have a dictionary to have the index of a specific board in the heap, to make the search faster
    if is_goal_state(initial_state):
        return initial_state

    heapq.heappush(fringe, (0, (0, initial_state)))

    while fringe:
        # print("Printing fringe:")
        # print('Fringe Length:',len(fringe),'\n')
        # print('\n'.join(' '.join(map(str, row)) for row in fringe))
        (cost, (cost_till_state, board_state)) = heapq.heappop(fringe)
        # print((cost, (cost_till_state, board_state)))
        closed[hash(str(board_state))] = True
        if is_goal_state(board_state):
            print('Fringe Length:',len(fringe),'\n')
            return board_state
        successors = generate_successors(board_state)
        for succ in successors:
            if closed.get(hash(str(succ))):
                continue

            h_misplaced = heuristic_misplaced(succ)
            # print('\n', 'Cost: ', h_misplaced + cost_till_state+1, 'Heuristic:', h_misplaced)
            # print('\n'.join(' '.join(map(str, row)) for row in succ))
            new_cost = h_misplaced + cost_till_state+1

            # BELOW CODE TO CHECK AND ADD BETTER COST TO FRINGE MIGHT NOT BE NEEDED AS ITS VERY EXPENSIVE
            # SO, EVEN IF WE ADD A LOWER COST TO THE FRINGE IT STILL IS GOING TO PROCESS THAT FIRST,
            # INSTEAD OF A HIGHER COST ONE..

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

            heapq.heappush(fringe, (new_cost, (cost_till_state + 1, succ)))


puzzle_unordered = read_input_file()
puzzle_length = len(puzzle_unordered)
goal = solve_puzzle(puzzle_unordered)
pprint.pprint(goal, indent=4)


# FOR TESTING
# successors = generate_successors(puzzle_unordered)
# for succ in successors:
#     print('\n'.join(' '.join(map(str, row)) for row in succ))
