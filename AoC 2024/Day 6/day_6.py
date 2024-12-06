import copy

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
            if (new_coords, direction) not in spaces_visited:
                spaces_visited.append((new_coords, direction)) # PART 2: turned spaces visited into coord/direction tuple
            return new_coords, direction, spaces_visited, True
        elif data[new_coords[0]][new_coords[1]] == "#":
            # hit a block. Turn right and try again
            direction_dict = {
                (-1,0):[0,1],
                (0,1):[1,0],
                (1,0):[0,-1],
                (0,-1):[-1,0]
            }

            new_direction = direction_dict[(direction[0], direction[1])]
            return starting_coords, new_direction, spaces_visited, True

    else:
        # returns? 
        # I want the list of places visited
        return starting_coords, direction, spaces_visited, False

current_coords = starting_coords
current_direction = [-1,0]
spaces_visited = [(starting_coords, current_direction)]
guard_in_bounds = True

while guard_in_bounds:
    current_coords, current_direction, spaces_visited, guard_in_bounds = move_guard(current_coords, current_direction, spaces_visited)

unique_spaces = []
for space in spaces_visited:
    if space[0] not in unique_spaces:
        unique_spaces.append(space[0])
print("Part 1:", len(unique_spaces))

### PART 2 ### NOTE: currently takes ~25 minutes to calculate the solution. Do not recommend!

# Repeat simulation with an obstacle in every unique space except the starting one
# if you repeat a (coord, direction), you have reached an infinite loop. Increment counter
potential_obstructions = []
for space in spaces_visited[1:]:
    row = space[0][0]
    col = space[0][1]
    copy_of_data = copy.deepcopy(data)
    copy_of_data[row][col] = "#" # added the obstruction somewhere along the path the guard naturally takes

    current_coords = starting_coords
    current_direction = [-1,0]
    spaces_visited = [(starting_coords, current_direction)]
    unique_spaces = [(starting_coords, current_direction)]
    keep_looping = True

    while keep_looping:
        current_coords, current_direction, spaces_visited, keep_looping = move_guard(current_coords, current_direction, spaces_visited, data=copy_of_data)
        if keep_looping == False:
            continue
        elif (current_coords, current_direction) not in unique_spaces:
            unique_spaces.append((current_coords, current_direction))
        else:
            potential_obstructions.append(space[0])
            keep_looping = False

unique_obstructions = []
for obstruction in potential_obstructions:
    if obstruction not in unique_obstructions:
        unique_obstructions.append(obstruction)

print("Part 2:", len(unique_obstructions))








