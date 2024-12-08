from time import perf_counter
from math import gcd                    # greatest common divisor
from itertools import combinations

############################################# PARSING DATA #################################
timer_script_start=perf_counter()

file = "input.txt"
# file = "test.txt"

timer_parse_start=perf_counter()

f = open(file, "r")
file_data = f.readlines()
f.close()

data = []
for row in file_data:
    data.append([x for x in row.strip()])

timer_parse_end=timer_part1_start=perf_counter()

########################################### PARTS 1 AND 2 ###########################################

# make a dictionary of antenna locations
antenna_locations = {}

total_rows = len(data)
total_cols = len(data[0])

for row_index in range(total_rows):
    for col_index in range(total_cols):
        antenna_type = data[row_index][col_index]
        if antenna_type != ".": # antenna found
            # add it to the dictionary entry if one exists, if not, create one
            if antenna_type in antenna_locations.keys():
                antenna_locations[antenna_type].append((row_index, col_index))
            else:
                antenna_locations[antenna_type] = [(row_index, col_index)]

def get_antinode_locations(antenna_1, antenna_2):
    """Calculates the distance between two antennas, finds coordinates of two antinodes, returns coordinates if within bounds.
    Returns a list of valid tuples eg [(row, col), (row, col)]"""
    row_difference = antenna_2[0] - antenna_1[0] # y change
    col_difference = antenna_2[1] - antenna_1[1] # x change
    antinode_1 = (antenna_1[0] - row_difference, antenna_1[1] - col_difference) # first direction
    antinode_2 = (antenna_2[0] + row_difference, antenna_2[1] + col_difference) # second direction
    antinodes_within_bounds = []
    if antinode_1[0] >= 0 and antinode_1[0] < total_rows and antinode_1[1] >= 0 and antinode_1[1] < total_cols:
        antinodes_within_bounds.append(antinode_1)
    if antinode_2[0] >= 0 and antinode_2[0] < total_rows and antinode_2[1] >= 0 and antinode_2[1] < total_cols:
        antinodes_within_bounds.append(antinode_2)
    return antinodes_within_bounds

def part2_get_antinode_locations(antenna_1, antenna_2):
    """Calculates smallest repeating distance between two nodes, finds all nodes along the line, returns coordinates if within bounds."""
    row_difference = antenna_2[0] - antenna_1[0]
    col_difference = antenna_2[1] - antenna_1[1]
    greatest_common_divisor = gcd(row_difference, col_difference)
    smallest_row_difference = row_difference / greatest_common_divisor
    smallest_col_difference = col_difference / greatest_common_divisor

    antinodes_within_bounds = [antenna_1] # start at antenna 1, work backwards until out of range, then work forwards until out of range

    loop_direction_1 = True
    next_antinode = (antenna_1[0] - smallest_row_difference, antenna_1[1] - smallest_col_difference) # set it to the starting node
    while loop_direction_1:
        # go from latest antinode in the given direction
        next_antinode = (antinodes_within_bounds[-1][0] - smallest_row_difference, antinodes_within_bounds[-1][1] - smallest_col_difference)
        # is it within bounds?
        if next_antinode[0] >= 0 and next_antinode[0] < total_rows and next_antinode[1] >= 0 and next_antinode[1] < total_cols: 
            antinodes_within_bounds.append(next_antinode)
        else:
            loop_direction_1 = False

    loop_direction_2 = True
    next_antinode = (antenna_1[0] + smallest_row_difference, antenna_1[1] + smallest_col_difference) # reset it to the starting node
    while loop_direction_2:
        next_antinode = (antinodes_within_bounds[-1][0] + smallest_row_difference, antinodes_within_bounds[-1][1] + smallest_col_difference)
        if next_antinode[0] >= 0 and next_antinode[0] < total_rows and next_antinode[1] >= 0 and next_antinode[1] < total_cols:
            antinodes_within_bounds.append(next_antinode)
        else:
            loop_direction_2 = False

    return antinodes_within_bounds

list_of_antinode_locations = []
part2_list_of_antinode_locations = []

for list_of_locations in antenna_locations.values(): # format '#': [[1, 3], [2, 0], [6, 2]]
    # we have the list of locations, now to compare each item in the list to the other items in the list
    list_of_pairs = list(combinations(list_of_locations, 2))
    for pair in list_of_pairs:
        list_of_antinode_locations += get_antinode_locations(pair[0], pair[1]) # may include duplicates
        part2_list_of_antinode_locations += part2_get_antinode_locations(pair[0], pair[1]) # may include duplicates
# remove duplicate values
unique = list(dict.fromkeys(list_of_antinode_locations))
part2_unique = list(dict.fromkeys(part2_list_of_antinode_locations))


# solve part 1
print(f"Part 1: {len(unique)}") # This was 0.001 seconds
# solve part 2
print(f"Part 1: {len(part2_unique)}")

timer_script_end=perf_counter()

print(f"""Execution times (sec)
Parse: {timer_parse_end-timer_parse_start:3.3f}
Total: {timer_script_end-timer_script_start:3.3f}""")