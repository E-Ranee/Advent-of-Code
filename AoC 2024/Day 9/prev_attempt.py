from time import perf_counter


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
counter = {}
file_id = 0
is_space = False
number_of_spaces = 0
for file in data:
    if is_space:
        # {file} number of blocks with value "."
        individual_blocks += ["."] * file
        if file > 0:
            file_blocks.append([".", file]) # part 2
        number_of_spaces += file
        is_space = False
    else:
        # {file} number of blocks with value {file_id}
        individual_blocks += [file_id] * file
        file_blocks.append([file_id, file]) # part 2
        counter[file_id] = file
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
import copy
reversed_list = list(range(int(individual_blocks[-1]), 0, -1)) # the indices in reverse order
altered_list = [] # generates from left to right

while len(reversed_list) != 0:
    if max(reversed_list) % 100 == 0:
        print(max(reversed_list), len(file_blocks))
    found = False
    first_space_found = False
    for index in range(len(file_blocks)):
        if found == False:
            try:
                file = file_blocks[index]
                if first_space_found == False and file[0] != ".":
                    altered_list.append(file)
                    file_blocks.pop(0)
                    found = True
                elif first_space_found == False and file[0] == ".":
                    first_space_found = True
                if first_space_found == True:
            
                    chunk_length = counter[reversed_list[0]]
                    prev_index = file_blocks.index([reversed_list[0], chunk_length])
                    if file[0] == "." and found == False and index < prev_index:
                        # found any space
                        # check to see if the rightmost chunk will fit
                        if file[1] >= chunk_length:
                            found = True # it fits
                            remainder = file[1] - chunk_length # any spare spaces
                            # remove the existing chunk
                            file_blocks[prev_index] = [".", chunk_length]
                            file_blocks[index] = (reversed_list.pop(0), chunk_length) # replace the space with the new chunk
                            if remainder > 0: # add an extra chunk if there's any space remaining
                                file_blocks.insert(index + 1, [".", remainder])

            except IndexError: # the list to compare to gets smaller during the loop
                pass
            except ValueError: # Ran out of items
                found = True
                reversed_list = []

    if found == False:
        reversed_list.pop(0)
final_list = altered_list + file_blocks
individual_blocks = "".join([str(x[0])*x[1] for x in final_list])
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