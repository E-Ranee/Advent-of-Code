import re

file = "input.txt"
# file = "test.txt"

f = open(file, "r")
data = f.readlines()
f.close()

rows = []
for row in data:
    rows.append(row.strip())


# rows[0].split() is in the format ['seeds:', '79', '14', '55', '13']
seeds = [int(numeral) for numeral in rows[0].split()[1:]] # removes "seeds:" and converts to integers

# format the instructions
current_map = ""
current_list_of_rules = []
all_maps_and_rules = []
for row in rows[2:]: # skip the seeds row
    if re.search("((\w+)-to-(\w+))", row):
        current_map = row
    elif row == "":
        all_maps_and_rules.append((current_map, current_list_of_rules))
        current_map = ""
        current_list_of_rules = []
    else:
        current_list_of_rules.append([int(numeral) for numeral in row.split()])
all_maps_and_rules.append((current_map, current_list_of_rules)) # for the last line with no new line after it

def converter(starting_value, list_of_rules):
    """Applies the map to a given starting value to determine if it stays the same or changes"""
    # map is in format [50, 98, 2]
    # map is in format [destination start, source start, range length] 98 --> 50, 99 --> 51

    for rule in list_of_rules:
        if starting_value >= rule[1] and starting_value < rule[1] + rule[2]:    # if in the source range
            return starting_value + (rule[0] - rule[1])                         # shift to the destination range
    return starting_value                                                       # else keep it the same

seed_matrix = [("seeds:", seeds)]

previous_stage = seeds # format [79, 14, 55, 13]
current_stage = []
for transformation in all_maps_and_rules:
    # transformation in format ('seed-to-soil map:', [[50, 98, 2], [52, 50, 48]])
    for seed in previous_stage:
        current_stage.append(converter(seed, transformation[1])) # convert each seed to the new value and add it to the list for eg humidity

    seed_matrix.append((transformation[0], current_stage)) # Add eg ("temp to humidity", new values) to the matrix
    previous_stage = current_stage # progress to the next stage
    current_stage = []

print("Part 1:", min(seed_matrix[-1][1])) # the lowest location






# DO NOT calculate every single value in the almanac. There are tens of millions and it'll take forever
# TODO: going to make a dictionary in case part 2 wants to access any of the other attributes
