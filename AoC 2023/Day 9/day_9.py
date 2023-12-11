file = "input.txt"
# file = "test.txt"

f = open(file, "r")
data = f.readlines()
f.close()

rows = []
for row in data:
    rows.append([int(x) for x in row.strip().split()])

def predict_next_values(list_of_ints):
    """Recursively generates lists showing the current pattern until a row of all 0s is found, then returns the list of lists found"""

    full_list = [list_of_ints]

    differences = []
    for i in range(len(list_of_ints) - 1):
        differences.append(list_of_ints[i + 1] - list_of_ints[i]) # difference between adjacent numbers

    if set(differences) == {0}:
        full_list.append(differences)

    if set(differences) != {0}:
        full_list += (predict_next_values(differences))

    return full_list

def extrapolate_pattern(list_of_lists, reversed=False):

    temp_list = list_of_lists
    temp_list.reverse()

    # can ignore the 0s list

    for index in range(len(temp_list)):
        if index == 0:
            pass
        else:
            if reversed:
                temp_list[index].insert(0, temp_list[index][0] - temp_list[index-1][0]) # calculates the number that should go on the left
            else:
                temp_list[index] += [temp_list[index-1][-1] + temp_list[index][-1]] # calculates the number to go on the right

    return temp_list[-1][-1] if reversed == False else temp_list[-1][0] # index -1 because we reversed the input and want to get the first element of the list of lists

def solve_puzzle(input=rows, part2=False):
    
    running_total = 0

    for sequence in input:
        list_of_new_sequences = predict_next_values(sequence)
        extrapolated_data = extrapolate_pattern(list_of_new_sequences, reversed=part2)
        running_total += extrapolated_data

    return running_total

print("Part 1:", solve_puzzle())
print("Part 2:", solve_puzzle(part2=True))
