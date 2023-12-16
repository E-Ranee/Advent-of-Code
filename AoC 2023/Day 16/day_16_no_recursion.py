
from enum import Enum
from pprint import pprint

file = "input.txt"
# file = "test.txt"
# file = "test2.txt"

f = open(file, "r")
file_data = f.readlines()
f.close()

data = []
for row in file_data:
    data.append([x for x in row.strip()]) # list of characters

"""
The beam enters in the top-left corner from the left and heading to the right. Then, its behavior depends on what it encounters as it moves:

If the beam encounters empty space (.), 
    it continues in the same direction.
If the beam encounters a mirror (/ or \), 
    the beam is reflected 90 degrees depending on the angle of the mirror. 
    For instance, a rightward-moving beam that encounters a / mirror would continue upward in the mirror's column, while a rightward-moving beam that encounters a \ mirror would continue downward from the mirror's column.
If the beam encounters the pointy end of a splitter (| or -),
    the beam passes through the splitter as if the splitter were empty space. 
    For instance, a rightward-moving beam that encounters a - splitter would continue in the same direction.
If the beam encounters the flat side of a splitter (| or -), 
    the beam is split into two beams going in each of the two directions the splitter's pointy ends are pointing. 
    For instance, a rightward-moving beam that encounters a | splitter would split into two beams: one that continues upward from the splitter's column and one that continues downward from the splitter's column.
"""

class CardinalDirection(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)

# mirror /
mirror_forwardslash = {
    CardinalDirection.NORTH : CardinalDirection.EAST,
    CardinalDirection.EAST : CardinalDirection.NORTH,
    CardinalDirection.SOUTH : CardinalDirection.WEST,
    CardinalDirection.WEST : CardinalDirection.SOUTH
}

mirror_backslash = {
    CardinalDirection.NORTH : CardinalDirection.WEST,
    CardinalDirection.EAST : CardinalDirection.SOUTH,
    CardinalDirection.SOUTH : CardinalDirection.EAST,
    CardinalDirection.WEST : CardinalDirection.NORTH
}

def next_tile_coordinates(direction_beam_is_moving: CardinalDirection, current_coords):
    difference_tuple = direction_beam_is_moving.value
    return (current_coords[0] + difference_tuple[0], current_coords[1] + difference_tuple[1])

energised_tiles = {} # we will add duplicates in case part 2 needs it

def move_beam(direction_beam_is_moving: CardinalDirection, current_position_of_beam):
    # eg CardinalDirection, (0,0)
    current_row = current_position_of_beam[0]
    current_col = current_position_of_beam[1]

    if current_row < 0 or current_row >= len(data):
        return []
    if current_col < 0 or current_col >= len(data[0]):
        return []
    
    current_tile = data[current_row][current_col]

    # check if current_position is energised in that direction
    # set current position to energised
    if current_position_of_beam in energised_tiles:
        if direction_beam_is_moving in energised_tiles[current_position_of_beam]:
            return []
        else:
            energised_tiles[current_position_of_beam].append(direction_beam_is_moving)
    else: 
        energised_tiles[current_position_of_beam] = [direction_beam_is_moving]

    # if it has encountered a splitter
    if current_tile == "|":
        if direction_beam_is_moving == CardinalDirection.EAST or direction_beam_is_moving == CardinalDirection.WEST:
            # splits into two
            return [
                (CardinalDirection.NORTH, (current_row - 1, current_col)),
                (CardinalDirection.SOUTH, (current_row + 1, current_col))
            ]
    elif current_tile == "-":
        if direction_beam_is_moving == CardinalDirection.NORTH or direction_beam_is_moving == CardinalDirection.SOUTH:
            # splits into two

            return [
                (CardinalDirection.EAST, (current_row, current_col + 1)),
                (CardinalDirection.WEST, (current_row, current_col - 1))
            ]

    # if empty space
    if current_tile == "." or current_tile == "|" or current_tile == "-":
        return [(direction_beam_is_moving, next_tile_coordinates(direction_beam_is_moving, current_position_of_beam))]

    # if it encounters a mirror
    elif current_tile == "/":
        # change direction using mirror_forwardslash dict
        changed_direction = mirror_forwardslash[direction_beam_is_moving]
        return [(changed_direction, next_tile_coordinates(changed_direction, current_position_of_beam))]
    elif current_tile == "\\":
        # change direction using mirror_backslash dict
        changed_direction = mirror_backslash[direction_beam_is_moving]
        return [(changed_direction, next_tile_coordinates(changed_direction, current_position_of_beam))]
    else:
        raise Exception("An unexpected case occurred!")


def get_energised_count(starting_tuple):
    global energised_tiles
    live_beams = [starting_tuple]
    while len(live_beams) > 0:
        temp_beams = []
        for beam in live_beams:
            temp_beams += move_beam(beam[0], beam[1])
        live_beams = temp_beams

    number_of_tiles = len(energised_tiles)
    energised_tiles = {}

    return number_of_tiles

entry_points = []
for row_num in range(len(data)):
    entry_points.append((CardinalDirection.EAST, (row_num, 0)))
    entry_points.append((CardinalDirection.WEST, (row_num, len(data[0])-1)))
for col_num in range(len(data[0])):
    entry_points.append((CardinalDirection.SOUTH, (0, col_num)))
    entry_points.append((CardinalDirection.NORTH, (len(data)-1, col_num)))

max_energised_number = 0
for point in entry_points:
    energised_total = get_energised_count(point)
    max_energised_number = max(max_energised_number, energised_total)

print("Part 1:", get_energised_count((CardinalDirection.EAST, (0,0))))
print("Part 2:", max_energised_number)