from time import perf_counter
from collections import Counter

# after import lines
timer_script_start=perf_counter()
timer_parse_start=perf_counter()

file = "input.txt" # 19999 characters long, 94945 total
# file = "test.txt"

f = open(file, "r")
file_data = f.readlines()
f.close()

data = []
for row in file_data: # just the one row today but this still works
    data += [int(x) for x in row.strip()]

################################ EXPANDING THE INPUT ###########################
individual_blocks = []
file_blocks = []
file_id = 0
is_space = False
number_of_spaces = 0
for file in data:
    if is_space:
        # {file} number of blocks with value "."
        individual_blocks += ["."] * file
        if file > 0:
            file_blocks += ["." * file]
        number_of_spaces += file
        is_space = False
    else:
        # {file} number of blocks with value {file_id}
        individual_blocks += [file_id] * file
        file_blocks += [str(file_id)*file]
        file_id += 1
        is_space = True

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
print(part_1_total)

################################### PART 2 ####################################
reversed_list = list(range(int(individual_blocks[-1]), 0, -1)) # the indices in reverse order
counter = Counter([x for x in individual_blocks if x != "."]) # counts how many times each element shows up 

while len(reversed_list) != 0:
    print(max(reversed_list), len(file_blocks))
    found = False
    if found == False:
        for index in range(len(file_blocks)):
            try: 
                file = file_blocks[index]
                chunk_length = counter[reversed_list[0]] # eg 8 occurs 4 times
                prev_index = file_blocks.index(str(reversed_list[0])*chunk_length)

                if len(file) == 0:
                    pass
                elif file[0] == "." and found == False and index < prev_index:
                    # found a space
                    # check rightmost chunk to see if it'll fit
                    if len(file) >= counter[reversed_list[0]]: # it fits
                        found = True
                        remainder = len(file) - chunk_length # any spare spaces

                        
                        # Remove the existing chunk and CONCATONATE THE SPACES
                        file_blocks[prev_index] = "." * chunk_length # set old chunk to be spaces
                        # if next block is a space, concatonate (if not end of row)
                        if prev_index == len(file_blocks) - 1:
                            pass
                        elif file_blocks[prev_index + 1][0] == ".":
                            file_blocks[prev_index] += file_blocks.pop(prev_index + 1)
                        # if previous block is a space, concatonate
                        if file_blocks[prev_index - 1][0] == ".":
                            file_blocks[prev_index - 1] += file_blocks.pop(prev_index)

                        file_blocks[index] = str(reversed_list.pop(0)) * chunk_length # replace space with new chunk
                        if remainder > 0: # add a chunk if there's any space remaining
                            file_blocks.insert(index + 1, "."*remainder)

            except IndexError: # the list to compare to gets smaller during the loop
                pass

    if found == False:
        reversed_list.pop(0)

individual_blocks = "".join(file_blocks)
part_2_total = 0
for index, block in enumerate(individual_blocks):
    if block != ".":
        part_2_total += index * int(block)

# solve part 2
timer_part2_end=timer_script_end=perf_counter()
print(part_2_total)

print(f"""Execution times (sec)
Parse: {timer_parse_end-timer_parse_start:3.3f}
Part1: {timer_part1_end-timer_part1_start:3.3f}
Part2: {timer_part2_end-timer_part2_start:3.3f}
Total: {timer_script_end-timer_script_start:3.3f}""")