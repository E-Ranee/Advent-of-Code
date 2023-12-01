f = open(f"input.txt", "r")
# f = open(f"example_input.txt", "r")
data = f.readlines()
f.close()

rock_path_commands = []
for line in data:
    rock_path_commands.append(line.strip())

##################################################################

def command_to_coordinates(string):
    string_coords = string.split(" -> ")

    int_coords = []
    for pair in string_coords:
        temp_list = pair.split(",")
        int_coords.append( (int(temp_list[0]), int(temp_list[1])) )

    return int_coords

#################################################################

rock_paths_coordinates = []

def draw_rock_paths(start_coord, end_coord):
    # coordinates come as two tuples
    x1 = start_coord[0]
    y1 = start_coord[1]

    x2 = end_coord[0]
    y2 = end_coord[1]

    list_of_rock_coords = []

    if x1 == x2:
        # path moves vertically, change y coord
        x_range = []
        if y1 < y2:
            x_range = list(range(y1, y2 + 1))
        else:
            x_range = list(range(y2, y1 + 1))

        list_of_rock_coords += ( [(x1, y) for y in x_range] )

    if y1 == y2:
        # path moves horizontally, change x coord
        y_range = []
        if x1 < x2:
            y_range = list(range(x1, x2 + 1))
        else:
            y_range = list(range(x2, x1 + 1))

        list_of_rock_coords += ( [(x, y1) for x in y_range] )

    return list_of_rock_coords

#################################################################

sand_locations = []

def sand_fall(start_coord, rock_list, sand_list, bounds):

    current_coord = start_coord
    x = current_coord[0]
    y = current_coord[1]

    max_y = bounds[3]

    sand_is_falling = True

    while sand_is_falling:
        down_coord = (x, y+1)
        down_left_coord = (x-1, y+1)
        down_right_coord = (x+1, y+1)

        double_list = set(sand_list + rock_list)

        ### Part 1
        # if y <= max_y:
        #     return None

        ### Part 2
        if y == max_y + 1:
            return (x,y)

        # try falling down (note: y INCREASES as it falls)
        elif down_coord not in double_list:
            # didn't crash into anything
            y = down_coord[1]

        # try falling down and left
        elif down_left_coord not in double_list:
            # didn't crash into anything
            x = down_left_coord[0]
            y = down_left_coord[1]

        # try falling down and right
        elif down_right_coord not in double_list:
            # didn't crash into anything
            x = down_right_coord[0]
            y = down_right_coord[1]

        else:
            return (x,y) # this needs to be added to the sand_locations list

######################################################

for line in rock_path_commands:
    individual_coords = command_to_coordinates(line)

    for index in range(len(individual_coords)-1):
        rock_paths_coordinates += draw_rock_paths(individual_coords[index], individual_coords[index + 1])

# Rock paths should be built now

def out_of_bounds(rock_coords, sand_source_coords):
    min_x = sand_source_coords[0]
    max_x = sand_source_coords[0]
    min_y = sand_source_coords[1]
    max_y = sand_source_coords[1]

    for coords in rock_coords:
        if coords[0] < min_x:
            min_x = coords[0]
        elif coords[0] > max_x:
            max_x = coords[0]
        if coords[1] < min_y:
            min_y = coords[1]
        elif coords[1] > max_y:
            max_y = coords[1]

    return [min_x, min_y, max_x, max_y]

sand_source_location = (500,0)
bounds = out_of_bounds(rock_paths_coordinates, sand_source_location)

# sand_is_falling = True
# while sand_is_falling:
#     result = sand_fall(sand_source_location, rock_paths_coordinates, sand_locations, bounds)
#     if result == None:
#         sand_is_falling = False
#     else:
#         sand_locations.append(result)

# print(len(sand_locations))

###############################################

floor_y_coordinate = bounds[3] + 2
# rock_paths_coordinates += [(x, floor_y_coordinate) for x in list(range(bounds[0]-150, bounds[2] + 150))]
# bounds = out_of_bounds(rock_paths_coordinates, sand_source_location)

sand_is_falling = True
counter = 0
while sand_is_falling:
    result = sand_fall(sand_source_location, rock_paths_coordinates, sand_locations, bounds)
    # print(result)
    counter += 1
    if counter % 100 == 0:
        print(counter)

    if result == None:
        sand_is_falling = False
    elif result == sand_source_location:
        sand_is_falling = False
        sand_locations.append(result)
        print("\ndone\n\n")
    else:
        sand_locations.append(result)

print(len(sand_locations))




