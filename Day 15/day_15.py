import re

f = open(f"input.txt", "r")
# f = open(f"example_input.txt", "r")
data = f.readlines()
f.close()

instructions = [] # each row takes the form [sensor_x, sensor_y, beacon_x, beacon_y]
all_coords = []

for line in data:
    # remove the new line
    clean_line = line.strip()
    # pull out a list of coordinates eg ["2", "18", "2", "15"]
    temp_list = re.findall("-?[\d]+", line.strip())
    # Turn coords into integers
    int_list = [int(x) for x in temp_list]
    instructions.append(int_list)
    all_coords.append((int_list[0], int_list[1])) # adds sensor coordinates
    all_coords.append((int_list[2], int_list[3])) # adds beacon coordinates

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def calculate_affected_coordinates(y_level, sensor_x, sensor_y, beacon_x, beacon_y):
    signal_radius = manhattan_distance(beacon_x, beacon_y, sensor_x, sensor_y)
    distance_between_sensor_and_y = abs(sensor_y - y_level)

    coordinates_affected = []

    if distance_between_sensor_and_y <= signal_radius:
        # some signal on the y level
        for i in range((signal_radius - distance_between_sensor_and_y) + 1):
            coordinates_affected.append( (sensor_x + i, y_level) )
            coordinates_affected.append( (sensor_x - i, y_level) )

    return coordinates_affected


def part1(instructions, all_coords, y_level):

    positions_present = []
    for pair in instructions:
        positions_present += calculate_affected_coordinates(y_level, pair[0], pair[1], pair[2], pair[3])

    # remove beacons and sensors from the list, ignore duplicates
    positions_present = list(set(positions_present) - set(all_coords)) 

    print(len(set(positions_present)))

# part1(instructions, all_coords, 10) # example data
# part1(instructions, all_coords, 2000000) # real data

#####################################################################################

distances_list = [] # [sensor_x, sensor_y, signal_radius]
for pair in instructions: # [sensor_x, sensor_y, beacon_x, beacon_y]
    distance = manhattan_distance(pair[0], pair[1], pair[2], pair[3])
    distances_list.append( [pair[0], pair[1], distance] )

dimension_x = dimension_y = 20 # example input
dimension_x = dimension_y = 4000000 # real_input

def in_range(x1, y1, triple_entry):
    signal_radius = triple_entry[2]
    local_distance = manhattan_distance(x1, y1, triple_entry[0], triple_entry[1])
    return local_distance <= signal_radius

def find_distress_beacon(dimension_x, dimension_y, distances_list):
    for x in range(dimension_x + 1):
        for y in range(dimension_y + 1):
            print(y)
            # if all return false, that is the solution
            running_result = False
            for sensor in distances_list:
                running_result = in_range(x, y, sensor)
                if running_result == True:
                    break

            if running_result == False:
                return((x * 4000000) + y)
            # if no trues, return coords

print(find_distress_beacon(dimension_x, dimension_y, distances_list))


