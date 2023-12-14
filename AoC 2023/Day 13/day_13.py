import collections

file = "input.txt"
# file = "test.txt"

f = open(file, "r")
file_data = f.readlines()
f.close()

# format the data from new line separated chunks into a list of lists of strings
current_chunk = []
data = []
for row in file_data:
    if row == "\n":
        data.append(current_chunk)
        current_chunk = []
    else:
        current_chunk.append(row.strip())
data.append(current_chunk)

"""
"." = ash
"# = rocks

find a perfect teflection across either a horizontal line BETWEEN two rows or a vertical line BETWEEN two columns
"""

def transpose_list(input_list):
    """Takes a list of lists and returns a list of strings but with the rows and columns swapped"""
    result = list(map(list, zip(*input_list))) # list of list of strings
    result = ["".join(x) for x in result]
    return result

def check_if_sequential(input_list):
    return set(input_list) == set(range(min(input_list), max(input_list) + 1))

def find_number_bonds(lower_bound, upper_bound):
    # eg 0, 5
    pairs = []
    for i in range(int((upper_bound - lower_bound + 1)/2)): # eg 3
        pairs.append((lower_bound + i, upper_bound - i))
    return pairs

def check_for_horizontal_mirror(input_list):

    # start at index 0 and check rows sequentially to see if it matches
    # then compare intermediary rows
    starting_row = input_list[0]
    for index, row in enumerate(input_list):
        if index == 0: # don't want to match with itself
            continue
        if index % 2 == 0: # skip every other row (mirror line is always between two rows)
            continue
        ### above this is "exit early" checks ###

        if row == starting_row:
            if index == 1: # 0th index of slice of input list
                return 1 # one row above the mirror line
            # check inbetween rows
            # currently index = "3"
            # check index - 1, check start + 1

            success_state = True

            index_pairs = find_number_bonds(0, index)
            for lower, upper in index_pairs[1:]:
                # pair eg (1,4)
                if input_list[lower] != input_list[upper]:
                    success_state = False
                    break

            if success_state:
                return int((index + 1) / 2)
    return 0 

    
def check_for_vertical_mirror(input_list):
    data = transpose_list(input_list)
    check_forwards = check_for_horizontal_mirror(data)
    if check_forwards == 0:
        data.reverse()
        check_backwards = check_for_horizontal_mirror(data)
        if check_backwards == 0:
            return 0
        else:
            check_forwards = len(data) - check_backwards
    return check_forwards

def summarise_data(data):
    horizontal_number = 0
    vertical_number = 0

    horizontal_check_forwards = check_for_horizontal_mirror(data)
    if horizontal_check_forwards == 0:
        reversed_data = data[::-1]
        horizontal_check_backwards = check_for_horizontal_mirror(reversed_data)
        if horizontal_check_backwards == 0:
            vertical_number = check_for_vertical_mirror(data)
        else:
            horizontal_number = len(data) - horizontal_check_backwards
    else:
        horizontal_number = horizontal_check_forwards

    if vertical_number == 0:
        horizontal_number *= 100
    else:
        horizontal_number = 0
    if vertical_number == 0 and horizontal_number == 0:
        print("fail")
    else:
        print("success")
    return horizontal_number + vertical_number

if __name__ == "__main__":
    total = 0
    for chunk in data:
        total += int(summarise_data(chunk))

    print("Part 1:", total)


### First broke on an input with a row repeated 3 times
