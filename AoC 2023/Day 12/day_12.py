import itertools

file = "input.txt"
# file = "test.txt"

f = open(file, "r")
file_data = f.readlines()
f.close()

data = []
for row in file_data:
    string, pattern = row.strip().split() # format "#.#.###" "1,1,3"
    pattern = [int(x) for x in pattern.split(",")] # format [1, 1, 3]
    data.append((string, pattern)) # format ('???.###', [1, 1, 3])

"""
. = operational
# = damaged
? = unknown
"""

test_example = data[0]

def string_to_pattern(string_of_springs):
    """takes a string with a format like "#....######..#####." and produces a list of integers showing the groupings of damaged springs"""
    damaged_spring_groups = string_of_springs.split(".")
    damaged_spring_groups = list(filter(None, damaged_spring_groups))
    number_of_damaged_springs = [len(x) for x in damaged_spring_groups]
    return number_of_damaged_springs

def try_every_possibility(string_pattern_tuple):
    string = string_pattern_tuple[0]
    pattern = string_pattern_tuple[1]

    # how many ?s in string
    number_of_unknowns = string.count("?")
    # All the different ways those unknowns could manifest
    options = list(itertools.product([".", "#"], repeat=number_of_unknowns))
    
    # Replace unknowns with the options and test if they're valid
    valid_options = 0
    for option in options:
        list_of_options = list(option)
        string_to_test = ""
        # replace ?s with each character sequentially
        for character in string:
            if character == "?":
                string_to_test += list_of_options.pop(0) # essentially moves along the replacement list without needing indices
            else:
                string_to_test += character

        result = string_to_pattern(string_to_test)
        if result == pattern:
            valid_options += 1

    return valid_options

total_arrangements = 0
for row in data:
    total_arrangements += try_every_possibility(row)

print(total_arrangements)

