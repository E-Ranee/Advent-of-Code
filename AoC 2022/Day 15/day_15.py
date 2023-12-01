import re
from time import time

f = open(f"input.txt", "r")
dimension_x = dimension_y = 4000000 # real_input
# f = open(f"example_input.txt", "r")
# dimension_x = dimension_y = 20 # example input
data = f.readlines()
f.close()

now = time()

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

print(f"It took {time() - now}s")

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
now = time()
part1(instructions, all_coords, 2000000) # real data
print(f"It took {time() - now}s")
#####################################################################################

distances_list = [] # [sensor_x, sensor_y, signal_radius]
for pair in instructions: # [sensor_x, sensor_y, beacon_x, beacon_y]
    distance = manhattan_distance(pair[0], pair[1], pair[2], pair[3])
    distances_list.append( [pair[0], pair[1], distance] )


### New plan based on the following post:
### https://www.reddit.com/r/adventofcode/comments/zmfwg1/2022_day_15_part_2_seekin_for_the_beacon/
### Follow the perimeter of each box

def in_range(x1, y1, triple_entry):
    signal_radius = triple_entry[2]
    local_distance = manhattan_distance(x1, y1, triple_entry[0], triple_entry[1])
    return local_distance <= signal_radius

def check_if_in_signal_area(distances_list, coord):
    # if all return false, that is the solution
    x = coord[0]
    y = coord[1]

    running_result = False
    for sensor in distances_list:
        running_result = in_range(x, y, sensor)
        if running_result == True:
            break

    if running_result == False:
        return((x * 4000000) + y)
        # if no trues, return coords
    else:
        return None

def find_distress_beacon_attempt_2(dimension_x, dimension_y, distances_list):
    for sensor in distances_list:
        sensor_x = sensor[0]
        sensor_y = sensor[1]
        signal_range = sensor[2]
        # find perimeter
        for index, value in enumerate(list(range(sensor_x - signal_range - 1, sensor_x + 1))): # x coords
            # value = x coord
            coord1 = (value, sensor_y + index)
            coord2 = (value, sensor_y - index)

            if coord1[0] <= dimension_x and coord1[1] <= dimension_y and coord1[0] >= 0 and coord1[1] >= 0:
                result = check_if_in_signal_area(distances_list, coord1)
                if result != None:
                    return result
            if coord2[0] <= dimension_x and coord2[1] <= dimension_y and coord2[0] >= 0 and coord2[1] >= 0:
                result = check_if_in_signal_area(distances_list, coord2)
                if result != None:
                    return result


        for index, value in enumerate(list(range(sensor_x + 1, sensor_x  + signal_range + 2))):
            coord1 = (value, sensor_y + signal_range - index)
            coord2 = (value, sensor_y - (signal_range - index))

            if coord1[0] <= dimension_x and coord1[1] <= dimension_y and coord1[0] >= 0 and coord1[1] >= 0:
                result = check_if_in_signal_area(distances_list, coord1)
                if result != None:
                    return result
            if coord2[0] <= dimension_x and coord2[1] <= dimension_y and coord2[0] >= 0 and coord2[1] >= 0:
                result = check_if_in_signal_area(distances_list, coord2)
                if result != None:
                    return result

        print("One sensor done", sensor)

now = time()
print(find_distress_beacon_attempt_2(dimension_x, dimension_y, distances_list))

print("Done!")
print(f"It took {time() - now}s")


