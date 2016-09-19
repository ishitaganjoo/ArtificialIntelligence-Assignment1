import sys

#open text file from the command line and store as a list of lists
with open(sys.argv[1], 'r') as f:
    puzzle = f.read().splitlines()

print puzzle