import string

# f = open(f"input.txt", "r")
f = open(f"example_input.txt", "r")
data = f.readlines()
f.close()

alphabet = list(string.ascii_letters) # produces a list of a-z, A-Z
map = []

for line in data:
    temp_list = []
    for char in line.strip():   
        if char != "E":
            temp_list.append(alphabet.index(char))
        else: 
            temp_list.append(27)
    map.append(temp_list)

# now the map is a list of lists

valid_moves_dict = {} # dict of coordinates to valid directions

def check_cardinal_directions(row, col):
    coord_value = map[row][col]

    if row - 1 < 0:
        north = False
    elif map[row - 1][col] <= coord_value + 1:
        north = (-1, 0)
    else: north = False

    if col - 1 < 0:
        west = False
    elif map[row][col - 1] <= coord_value + 1:
        west = (0, -1)
    else:
        west = False

    if row + 1 > len(map) - 1:
        south = False
    elif map[row + 1][col] <= coord_value + 1:
        south = (1, 0)
    else:
        south = False

    if col + 1 > len(map[0]) - 1:
        east = False
    elif map[row][col + 1] <= coord_value + 1:
        east = (0, 1)
    else:
        east = False

    valid_moves_dict[(row, col)] = [north, east, south, west]

for i in range(len(map)): #row
    for j in range(len(map[0])): #col
        check_cardinal_directions(i,j)

current_shortest_path_length = len(map) * len(map[0])
current_shortest_path = []
current_path = []
banned_coordinates = []

def try_out_path(starting_row, starting_col):
    global current_shortest_path_length
    starting_valid_moves = valid_moves_dict[(starting_row, starting_col)]
    current_value = map[starting_row][starting_col]

    for move in starting_valid_moves:
        if move != False:
            new_coordinate = (starting_row + move[0], starting_col + move[1])
            if new_coordinate not in current_path and new_coordinate not in banned_coordinates:
                current_path.append(new_coordinate)
                try_out_path(new_coordinate[0], new_coordinate[1])
    
    # no more moves
    if map[starting_row][starting_col] == 27:
        print("winning route found")
        if len(current_path) < current_shortest_path_length:
            current_shortest_path_length = len(current_path)
            print(current_path, current_shortest_path_length)

    else:
        if len(banned_coordinates) < 39:
            banned_coordinates.append(current_path.pop(-1)) 
            print((current_path[-1][0], current_path[-1][1]), len(banned_coordinates))
            try_out_path(current_path[-1][0], current_path[-1][1])
        else:
            return
        # if no moves give up/remove last element, add to banned

### follow similar algorithm to the folder puzzle 
# (if you can't progress, remove the last item and try a different path)
### change the Trues to coordinate moves? north = (-1, 0)
### add a check so you can't go back to previously visited coordinates

try_out_path(0,0)

print(current_shortest_path_length)
print(current_shortest_path)