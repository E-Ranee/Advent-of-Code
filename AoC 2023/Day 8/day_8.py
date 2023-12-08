import re

file = "input.txt"
# file = "test.txt"
# file = "test2.txt"
# file = "part_2_test.txt"

f = open(file, "r")
data = f.readlines()
f.close()

rows = []
for row in data:
    rows.append(row.strip())

instructions = rows[0] # format eg "RL"

node_dict = {}
nodes_A_list = []
for row in rows[2:]: # format "AAA = (BBB, CCC)"
    node, left, right = re.findall("[A-Z]+", row)
    node_dict[node] = (left, right)

    # part 2
    if node[2] == "A":
        nodes_A_list.append(node)

def find_next_node(current_node, instruction, node_dict=node_dict):
    next_node = node_dict[current_node][0 if instruction == "L" else 1]
    return next_node

searching_for_solution = True
current_node = "AAA"
steps = 0

while searching_for_solution:
    if file == "part_2_test.txt": # breaks because there is no "ZZZ"
        searching_for_solution = False
        break
    for letter in instructions:
        current_node = find_next_node(current_node, letter)
        steps += 1

        if current_node == "ZZZ":
            searching_for_solution = False
            break

print("Part 1:", steps)

###### CANNOT BRUTE FORCE IT - SOLUTION IS 14 DIGITS LONG
###### NEED TO FIND LOOP LENGTHS AND THE LOWEST COMMON DENOMINATOR

# searching_for_solution = True
# steps = 0
# current_nodes = nodes_A_list
# while searching_for_solution:
#     for letter in instructions:
#         next_nodes = []
#         found_solution = True # disproven by a single non Z destination
#         for node in current_nodes:
#             new_node = find_next_node(node, letter)
#             next_nodes.append(new_node)
#             if new_node[-1] != "Z":
#                 found_solution = False

#         steps += 1
#         current_nodes = next_nodes
#         searching_for_solution = not found_solution

# print("Part 2:", steps)
