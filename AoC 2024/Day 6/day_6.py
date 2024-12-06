file = "input.txt"
# file = "test.txt"

f = open(file, "r")
file_data = f.readlines()
f.close()

data = []
for row in file_data:
    data.append([x for x in row.strip()]) # makes a 2d array of characters

# STEP 1: find the starting position of the guard
starting_coords = []
for row_index in range(len(data)):
    if "^" in data[row_index]:
        # found the row, now find the col
        col_index = data[row_index].index("^")
        starting_coords = [row_index, col_index]

# STEP 2: move the guard around the grid
def move_guard(starting_coords, direction, spaces_visited, data=data):
    # direction = [-1,0] north, [0,1] east, [1,0] south, [0,-1] west
    # apply direction
    new_coords = [starting_coords[0] + direction[0], starting_coords[1] + direction[1]]

    # check if next space is the edge of the map, if so: end
    row_within_bounds = new_coords[0] > -1 and new_coords[0] < len(data)
    col_within_bounds = new_coords[1] > -1 and new_coords[1] < len(data[0])

    if row_within_bounds and col_within_bounds:
        # still within bounds. Check if next space is empty. If so: progress and add to list of spaces passed through
        if data[new_coords[0]][new_coords[1]] == "." or data[new_coords[0]][new_coords[1]] == "^":
            # next space is empty. Call this function again with the new coordinates and same direction
            if new_coords not in spaces_visited:
                spaces_visited.append(new_coords)
            return move_guard(new_coords, direction, spaces_visited)
        elif data[new_coords[0]][new_coords[1]] == "#":
            # hit a block. Turn right and try again
            direction_dict = {
                (-1,0):[0,1],
                (0,1):[1,0],
                (1,0):[0,-1],
                (0,-1):[-1,0]
            }

            new_direction = direction_dict[(direction[0], direction[1])]
            return move_guard(starting_coords, new_direction, spaces_visited)

    else:
        # returns? 
        # I want the list of places visited
        return spaces_visited



unique_spaces = move_guard(starting_coords, [-1,0], [starting_coords])
print(len(unique_spaces))