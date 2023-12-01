import re
from itertools import permutations
from time import time
from math import factorial

f = open(f"input.txt", "r")
f = open(f"example_input.txt", "r")
data = f.readlines()
f.close()

class Valve:
    def __init__(self, name="", flow_rate=0, tunnels=[]):
        self.name = name
        self.open_state = False
        self.flow_rate = flow_rate
        self.tunnels = tunnels # this is a list eg ["DD", "II", "BB"]

dict_of_valves = {}
list_of_valves = []

for line in data:
    clean_line = line.strip()
    valves_results = re.findall("[A-Z]{2}", clean_line)
    starting_valve = valves_results[0]
    joining_tunnels = valves_results[1:]
    flow_rate = int(re.findall("[\d]+", clean_line)[0]) # extract numbers and turn to ints

    valve_object = Valve(starting_valve, flow_rate, joining_tunnels)
    dict_of_valves[starting_valve] = valve_object
    list_of_valves.append(starting_valve)

# Starts at list_of_valves[0]


############################################################################
### Got stuck looking for an algorithm so started following this comment ###
### https://www.reddit.com/r/adventofcode/comments/zn6k1l/comment/j0frm88/?utm_source=share&utm_medium=web2x&context=3 ###
############################################################################

# The relevant search space can be formulated as "which is the next valve to turn off"
# precalculate the distances between all nodes with non-zero flow rate


def breadth_first_search(dict_of_valves, root_node):
    queue = []
    queue.append(root_node)
    distance_dict = {}
    distance_dict[(root_node, root_node)] = 0


    # root_node has been visited
    visited_nodes = []
    visited_nodes.append(root_node)

    while len(queue) > 0:
        current_node = queue.pop(0)

        # for all neighbours of current node
        for index, node in enumerate(dict_of_valves[current_node].tunnels):
            if node not in visited_nodes:
                queue.append(node)
                visited_nodes.append(node)
                # Adds the distance between the root node and the current node
                # (adds one to the distance from the parent node)
                # print(distance_dict[(root_node, current_node)])
                distance_dict[(root_node, dict_of_valves[current_node].tunnels[index])] = distance_dict[(root_node, current_node)] + 1

    return distance_dict


list_of_non_0_flow_valves = []
for valve_name, valve_object in dict_of_valves.items():
    if valve_object.flow_rate != 0:
        list_of_non_0_flow_valves.append(valve_name)

distances_dict = {}
distances_dict.update(breadth_first_search(dict_of_valves, list_of_valves[0]))
for valve in list_of_non_0_flow_valves:
    distances_dict.update(breadth_first_search(dict_of_valves, valve))
# note that sets are unhashable so the dictionary keys are duplicated
# eg AA --> BB and BB --> AA

#########################################################################################

# Want to make a graph with node = flow, edge = distance
def make_new_interconnected_graph(node1, node2, distances_dict, dict_of_valves):
    distance = distances_dict[(node1, node2)]
    node_2_flow = dict_of_valves[node2].flow_rate

    return (node1, node2), node_2_flow, distance # coordinates, node, edge

relevant_valves = [list_of_valves[0]] + list_of_non_0_flow_valves
new_graph = {}

for node1 in relevant_valves:
    for node2 in relevant_valves:
        result = make_new_interconnected_graph(node1, node2, distances_dict, dict_of_valves)
        # ( (node1, node2), node_flow, edge_distance )
        new_graph.update({result[0] : (result[1], result[2])})

for key, value in new_graph.items():
    print(key, value)

def find_path_cost(new_graph, list_of_nodes):
    """Returns the total shortest distance between two nodes"""
    distance = 0
    for index in range(len(list_of_nodes) - 1):
        node1 = list_of_nodes[index]
        node2 = list_of_nodes[index + 1]
        distance += new_graph[(node1, node2)][1]
    return distance

print(find_path_cost(new_graph, ["AA", "EE", "BB", "HH"]))


# iterate recursively. Ditch if sum(distances) > 30. Must be unique nodes

