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


y_level = 10 # part 1
y_level = 2000000 # part 2
positions_present = []
for pair in instructions:
    positions_present += calculate_affected_coordinates(y_level, pair[0], pair[1], pair[2], pair[3])

# remove beacons and sensors from the list, ignore duplicates
positions_present = list(set(positions_present) - set(all_coords)) 

print(len(set(positions_present)))

