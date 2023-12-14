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

def check_for_horizontal_mirror(input_list):

    # which rows are duplicated?
    counter = collections.Counter(input_list)
    counts = counter.most_common() # list of tuples ("element", count)
    repeated_elements = [x[0] for x in counts if x[1] > 1] # element for tuple in counts if occurrences is greater than 1

    # are the repeated elements clustered around a line
    indices = []
    likely_spot = []
    for element in repeated_elements:
        first_occurrence = input_list.index(element)
        second_occurrence = input_list.index(element, first_occurrence+1)
        indices.append(first_occurrence)
        indices.append(second_occurrence)


        likely_spot.append((second_occurrence + first_occurrence)/2)

    if len(indices) > 0:
        if max(indices) == len(data) - 1 or min(indices) == 0:
            counter = collections.Counter(likely_spot)
            counts = counter.most_common()
            return counts[0][0] + 0.5

    # clustering - are the indices sequential?
    if len(indices) > 0:
        if check_if_sequential(indices):
            mirror_line = (max(indices) + min(indices)) / 2 # will be a number and a half
            rows_above_mirror_line = mirror_line + 0.5
        else:
            return 0
    else:
        return 0

    # Are the remaining rows valid?
    # Need to have some rows outside of the reflection area
    # On ONE side only

    remaining_row_indices = [x for x in range(len(input_list)) if x not in indices]
    if check_if_sequential(remaining_row_indices):
        return rows_above_mirror_line
    else:
        return 0
    
def check_for_vertical_mirror(input_list):
    data = transpose_list(input_list)
    return check_for_horizontal_mirror(data)

def summarise_data(data):
    vertical_nummber = check_for_vertical_mirror(data)
    if vertical_nummber == 0:
        horizontal_number = 100 * check_for_horizontal_mirror(data)
    else:
        horizontal_number = 0
    # if vertical_nummber == 0 and horizontal_number == 0:
    #     print("fail")
    # else:
    #     print("success")
    return horizontal_number + vertical_nummber

total = 0
for chunk in data:
    total += int(summarise_data(chunk))

print("Part 1:", total)


### First broke on an input with a row repeated 3 times
