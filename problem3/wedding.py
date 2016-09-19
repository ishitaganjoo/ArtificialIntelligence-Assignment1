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

# Data Structures used:
#     Tables matrix: dictionary of tables, with key as table number and value as list of people seated on it


import pprint

#   This function reads from the input file and creates
#       a friends_dict, which creates a mapping for a friend that knows other friends
#       a friends_list, with list of all people, and we will pop out from the list as we go about adding them on to the
#           tables, seating arrangement


MAX_SEATS_AT_TABLE = 4

def read_friends_from_file(filename):

    with open(filename) as f:
        for line in f:
            friends = line.split()
            friends_dict[friends[0]] = friends[1:]
            list(friends_list.append(friend) for friend in friends if friend not in friends_list)

def has_friend_at_table(friend, people_at_table):
    has_friend = False
    for person in people_at_table:
        if (friend in friends_dict.get(person, []) or person in friends_dict.get(friend, [])):
            has_friend = True
    return has_friend

def solve_friends_seating(table_size):
    while friends_list:
        friend = friends_list.pop(0)
        added = False
        for table in tables.keys():
            people_at_table = list(tables.get(table))
            if (len(people_at_table) == table_size or has_friend_at_table(friend, people_at_table)):
                continue
            else:
                people_at_table.append(friend)
                tables[table] = people_at_table
                added = True
        if not added:
            table_num = len(tables.keys()) + 1
            tables[table_num] = [friend]


friends_dict = {}
friends_list = []
tables = {}

read_friends_from_file('myfriends.txt')
print('\n')
pprint.pprint(friends_dict, indent=4)
print('\n')
pprint.pprint(friends_list, indent=4)
print('\n')

solve_friends_seating(4)

pprint.pprint(tables, indent=4)
