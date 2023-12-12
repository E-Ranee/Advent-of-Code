import itertools

file = "input.txt"
# file = "test.txt"

f = open(file, "r")
data = f.readlines()
f.close()

def expand_universe(data):

    rows = []
    for row in data:
        x = row.strip()
        if x == len(x)*".": # if it's an empty row, duplicate it
            rows.append(x)
        rows.append(x)

    transposed_matrix = list(map(list, zip(*rows)))
    expanded_transposed_matrix = []
    for col in transposed_matrix:
        if "".join(col) == len(col)*".": # if it's an empty column, duplicate it
            expanded_transposed_matrix.append(col)
        expanded_transposed_matrix.append(col)

    final_matrix = list(map(list, zip(*expanded_transposed_matrix)))

    return final_matrix

def find_galaxies(matrix):

    list_of_galaxies = []

    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if matrix[row][col] == "#":
                list_of_galaxies.append((row, col))

    return list_of_galaxies

def find_manhattan_distance(coords_1, coords_2): # format (row, col)
    r1, c1 = coords_1
    r2, c2 = coords_2

    row_difference = abs(r2 - r1)
    col_difference = abs(c2 - c1)

    return row_difference + col_difference

def find_combinations(list_of_galaxies):
    # order does NOT matter
    combinations = list(itertools.combinations(list_of_galaxies, r=2))
    return combinations

matrix = expand_universe(data)
list_of_galaxies = find_galaxies(matrix)
combinations = find_combinations(list_of_galaxies)

total_distance = 0
for pair in combinations: # ((0, 4), (1, 9))
    total_distance += find_manhattan_distance(pair[0], pair[1])

print(total_distance)
