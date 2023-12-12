file = "input.txt"
# file = "test2.txt"
# file = "test.txt"

f = open(file, "r")
data = f.readlines()
f.close()

rows = []
for row in data:
    rows.append(row.strip())

"""| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has."""

pipe_description_dict = {
    "|" : ["north", "south"],
    "-" : ["east", "west"],
    "L" : ["north", "east"],
    "J" : ["north", "west"],
    "7" : ["south", "west"],
    "F" : ["south", "east"],
    "." : []
}

directions_dict = {
    "north": [-1, 0],
    "east": [0, 1],
    "south": [1, 0],
    "west": [0, -1] 
}

reverse_directions_dict = {
    "south": "north",
    "west": "east",
    "north": "south",
    "east": "west"
}

# find starting coordinates
s_coords = []
for index, row in enumerate(rows):
    if "S" in row:
        s_coords.append(index)
        for col_index, col in enumerate(row):
            if col == "S":
                s_coords.append(col_index)

# need to look at the 4 adjacent directions
# note which direction you came from and validate if a direction is possible
# if no more valid directions, go up a level and try again
# keep going until back at S
# keep track of number of VALID steps and halve to find furthest point

def check_starting_pipe(direction, data=rows):
    """Looks in the 4 directions from the starting point to identify which paths can connect"""
    start_row = s_coords[0]
    start_col = s_coords[1]

    change_in_coords = directions_dict[direction]

    new_row = start_row + change_in_coords[0]
    new_col = start_col + change_in_coords[1]

    # make sure the new tile is in range (eg starting point might be at the edge of the data)
    if new_row not in range(len(data)) or new_col not in range(len(data[0])):
        return

    new_pipe = data[new_row][new_col]
    possible_directions = pipe_description_dict[new_pipe]

    reversed_direction = reverse_directions_dict[direction]

    if reversed_direction in possible_directions:
        return [new_pipe, [new_row, new_col], direction] # returns the name and the coordinates of the new pipe as well as which direction you're travelling in
    
def follow_pipe(pipe_name, starting_coordinates, direction): # eg east into a 7
    """Takes a starting direction and a pipe and returns what it found at the other end of the pipe, its coordinates and what direction was travelled in"""
    start_row = starting_coordinates[0]
    start_col = starting_coordinates[1]

    origin_direction = reverse_directions_dict[direction] # eg came from west
    potential_directions = pipe_description_dict[pipe_name].copy()
    potential_directions.remove(origin_direction)
    destination_direction = potential_directions[0] # eg going south

    change_in_coords = directions_dict[destination_direction] # eg row below current coords

    new_row = start_row + change_in_coords[0]
    new_col = start_col + change_in_coords[1]

    new_pipe = data[new_row][new_col]

    # fail state: out of bounds or not a valid pipe
    if new_row not in range(len(data)) or new_col not in range(len(data[0])):
        return "failed"
    if new_pipe == ".": # NOTE: this worked to find the solution but does not account for finding a pipe that doesn't fit the path. Eg | into -
        return "failed"

    return new_pipe, [new_row, new_col], destination_direction


cardinal_directions = ["north", "east", "south", "west"]
options = []
for path in cardinal_directions:
    options.append(check_starting_pipe(path)) # returns [new_pipe, [new_row, new_col], direction] 
while None in options:
    options.remove(None)

for option in options:
    looking_for_S = True
    pipe, coords, direction = option
    counter = 1
    while looking_for_S:
        results = follow_pipe(pipe, coords, direction)
        if results == "failed":
            looking_for_S = False
            # print("\n", "trying again", "\n")
            break
        pipe, coords, direction = follow_pipe(pipe, coords, direction)
        counter += 1
        # print(pipe, coords, direction)
        if pipe == "S":
            looking_for_S = False

print(int(counter / 2))