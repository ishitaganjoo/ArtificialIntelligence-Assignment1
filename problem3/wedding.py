# wedding,py : The problem here is to arrange

# Spate Space:
#       This is the space of all possible seating arrangement of M people,
#       in an (MxN) matrix space
#           where M represents the minimum number of tables (rows) needed
#           and N represents the seats accomodated in a table
#
#
# Successor Function:
#       The successor function generates the next state,
#           by adding one more person to the matrix (M_min x N),
#           such that the person added to a table does not know anyone seated on that table
#               where min(M) represents the minimum number of rows added to the meet the
#           The successor function adds a row to the matrix if a new person being added cannot be accomodated in the
#           existing tables

#
# Goal State:
#       The final arrangement of all M people in M_min tables, such that no two people know each other


