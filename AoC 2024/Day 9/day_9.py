from time import perf_counter
from typing import Dict, List

# after import lines
timer_script_start=perf_counter()
timer_parse_start=perf_counter()

file = "input.txt" # 19999 characters long, 94945 total
# file = "time_check.txt"
file = "test_2.txt"

f = open(file, "r")
file_data = f.readlines()
f.close()

data = []
for row in file_data: # just the one row today but this still works
    data += [int(x) for x in row.strip()]

################################ EXPANDING THE INPUT ###########################
individual_blocks = []

# https://www.reddit.com/r/adventofcode/comments/1ha27bo/comment/m15re2h/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
# Needed help optimising and this comment was clear about how to achieve this
file_blocks: Dict[int, List[int]] = {} # digit number: [starting index, length]
space_blocks: Dict[int, List[int]] = {} # length of free space: [list of starting indices with a space of that length]


counter = {}
file_id = 0
is_space = False
number_of_spaces = 0
current_index = 0
for file in data:
    print(f"Current index: {current_index}")
    if is_space:
        # {file} number of blocks with value "."
        individual_blocks += ["."] * file
        if file > 0:
            print(f"{file} spaces")
            if file not in space_blocks: # part 2
                space_blocks[file] = [current_index]
            else:
                space_blocks[file].append(current_index)
        number_of_spaces += file
        current_index += file
        is_space = False
    else:
        # {file} number of blocks with value {file_id}
        print(f"{file} number of blocks with value {file_id}")
        individual_blocks += [file_id] * file
        file_blocks[file_id] = [current_index, file] # part 2. eg 9: [starts on 5th index, continues for 4 indices]
        current_index += file
        counter[file_id] = file
        file_id += 1
        is_space = True

print()
print(file_blocks)
print()

# after processing input and running past functions
timer_parse_end=timer_part1_start=perf_counter()

################################### PART 1 ####################################
reversed_list = [x for x in list(reversed(individual_blocks)) if x != "."] # list in reverse order without spaces
altered_list = [] # build the list from left to right, adding the original digit if it exists or the reversed order digit if it's a space

for block in individual_blocks:
    if len(altered_list) != len(individual_blocks) - number_of_spaces: # end when you would have all the spaces at the end
        if block != ".":
            altered_list.append(block) # add the original index
        else:
            altered_list.append(reversed_list.pop(0)) # add the index from the reversed list, then delete it to push the queue along

part_1_total = 0
for index, block in enumerate(altered_list):
    part_1_total += index * block

# solve part 1
timer_part1_end=timer_part2_start=perf_counter()


################################### PART 2 ####################################
reversed_list = list(range(int(individual_blocks[-1]), 0, -1)) # the indices in reverse order
# Slightly cheating but I checked the input and there is never a space with a length of greater than 9
# print(file_blocks)

for number in reversed_list:
    number_length = file_blocks[number][1]
    print(f"Looking for the first space of {number_length} or higher for the {number}s")
    # find the first space of that size or higher
    potential_spaces = []
    for space_length in range(number_length, 10):
        if space_length in space_blocks:
            if len(space_blocks[space_length]) > 0:
                potential_spaces.append([min(space_blocks[space_length]), space_length]) # appends a list of [index, length] 

    # find the minimum index
    sorted_spaces = sorted(potential_spaces) # sorts by first element in each "tuple" (list)
    if len(sorted_spaces) == 0:
        # no valid spaces found
        pass
    else:
        first_space_index, first_space_length = sorted_spaces[0]
        remaining_space = first_space_length - number_length # the space may be larger than needed
        if first_space_index < file_blocks[number][0]:
            # set the new index of the number to occur where the space currently is
            file_blocks[number] = [first_space_index, number_length]
            # delete the space from the dictionary for its current length
            space_blocks[first_space_length].pop(0)
            # print(file_blocks)
            # if it has a new length, add it to that entry
            if remaining_space > 0:
                if remaining_space not in space_blocks:
                    space_blocks[remaining_space] = [first_space_index + number_length]
                else:
                    space_blocks[remaining_space].append(first_space_index + number_length)

part_2_total = 0
for number, index_length_list in file_blocks.items():
    for i in range(index_length_list[1]):
        part_2_total += number * (index_length_list[0] + i)
        # print(f"{number}: {number} x {index_length_list[0] + i} = {number * (index_length_list[0] + i)}")
    




# solve part 2
timer_part2_end=timer_script_end=perf_counter()

print()
print(part_1_total)
print(part_2_total)

print(f"""
Execution times (sec)
Parse: {timer_parse_end-timer_parse_start:3.3f}
Part1: {timer_part1_end-timer_part1_start:3.3f}
Part2: {timer_part2_end-timer_part2_start:3.3f}
Total: {timer_script_end-timer_script_start:3.3f}""")